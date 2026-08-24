from dataclasses import dataclass


@dataclass
class Track:
    id: int
    label: str
    bbox: tuple[float, float, float, float]
    confidence: float
    centroid: tuple[float, float]


class BaseTracker:
    """Simple tracker abstraction for CV pipeline."""

    def __init__(self, max_age: int = 30, min_hits: int = 3):
        self.max_age = max_age
        self.min_hits = min_hits
        self.tracks: dict[int, Track] = {}
        self.next_id = 1

    def update(self, detections: list[dict]) -> list[dict]:
        results: list[dict] = []
        for detection in detections:
            x1, y1, x2, y2 = detection["bbox"]
            cx = (x1 + x2) / 2.0
            cy = (y1 + y2) / 2.0
            track = Track(
                id=self.next_id,
                label=detection["label"],
                bbox=(x1, y1, x2, y2),
                confidence=detection["confidence"],
                centroid=(cx, cy),
            )
            self.tracks[track.id] = track
            self.next_id += 1
            results.append({
                "id": track.id,
                "label": track.label,
                "bbox": track.bbox,
                "confidence": track.confidence,
                "centroid": track.centroid,
            })
        return results
