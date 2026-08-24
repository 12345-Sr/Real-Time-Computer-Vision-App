import threading
import time
from collections import Counter

import cv2

from app.core.config import get_settings
from app.cv.detector.model_manager import ModelManager
from app.cv.visualization.annotate import draw_annotations


class CameraService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.capture: cv2.VideoCapture | None = None
        self.thread: threading.Thread | None = None
        self.lock = threading.Lock()
        self.running = False
        self.source = self.settings.CAMERA_SOURCE
        self.latest_frame: bytes | None = None
        self.latest_detections: list[dict] = []
        self.metrics = {"fps": 0.0, "latency_ms": 0.0}
        self.error: str | None = None

    def start(self, source: str = "0") -> dict:
        if self.running:
            return self.status()
        camera_source: int | str = int(source) if str(source).isdigit() else source
        capture = cv2.VideoCapture(camera_source)
        if not capture.isOpened():
            capture.release()
            raise ValueError(f"Unable to open camera source: {source}")
        self.capture = capture
        self.source = str(source)
        self.running = True
        self.error = None
        self.thread = threading.Thread(target=self._process, daemon=True)
        self.thread.start()
        return self.status()

    def stop(self) -> None:
        self.running = False
        if self.capture:
            self.capture.release()
            self.capture = None

    def status(self) -> dict:
        return {
            "running": self.running,
            "status": "running" if self.running else "stopped",
            "source": self.source,
            "error": self.error,
        }

    def snapshot(self) -> tuple[bytes | None, list[dict], dict]:
        with self.lock:
            return self.latest_frame, list(self.latest_detections), dict(self.metrics)

    def _process(self) -> None:
        model = None
        try:
            from ultralytics import YOLO

            manager = ModelManager(self.settings.MODEL_NAME, self.settings.MODEL_PATH, self.settings.DEVICE)
            model = YOLO(manager.resolve_model_path())
        except Exception as exc:
            self.error = f"Model loading failed: {exc}"

        frame_count = 0
        started_at = time.perf_counter()
        while self.running and self.capture:
            ok, frame = self.capture.read()
            if not ok:
                self.error = "Camera disconnected or frame read failed"
                break
            frame_count += 1
            begin = time.perf_counter()
            detections: list[dict] = []
            if model and frame_count % max(1, self.settings.FRAME_SKIP) == 0:
                result = model.predict(
                    frame,
                    conf=self.settings.CONFIDENCE_THRESHOLD,
                    iou=self.settings.IOU_THRESHOLD,
                    device=None if self.settings.DEVICE == "auto" else self.settings.DEVICE,
                    verbose=False,
                )[0]
                names = result.names
                for box in result.boxes:
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    confidence = float(box.conf[0])
                    class_id = int(box.cls[0])
                    detections.append({
                        "id": len(detections) + 1,
                        "label": names[class_id],
                        "bbox": (x1, y1, x2, y2),
                        "confidence": confidence,
                    })
            annotated = draw_annotations(frame, detections)
            encoded, buffer = cv2.imencode(".jpg", annotated)
            if encoded:
                with self.lock:
                    self.latest_frame = buffer.tobytes()
                    self.latest_detections = detections
                    self.metrics["latency_ms"] = (time.perf_counter() - begin) * 1000
                    elapsed = time.perf_counter() - started_at
                    self.metrics["fps"] = frame_count / elapsed if elapsed else 0.0
        self.running = False


camera_service = CameraService()