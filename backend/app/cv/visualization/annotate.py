import cv2
import numpy as np


def draw_annotations(frame: np.ndarray, detections: list[dict]) -> np.ndarray:
    annotated = frame.copy()
    for detection in detections:
        x1, y1, x2, y2 = [int(v) for v in detection["bbox"]]
        label = f"{detection['label']} #{detection['id']} - {detection['confidence']:.2f}"
        cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(annotated, label, (x1, max(25, y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    return annotated
