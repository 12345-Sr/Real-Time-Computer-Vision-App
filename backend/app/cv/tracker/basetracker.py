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
        matched_ids: set[int] = set()
        for detection in detections:
            x1, y1, x2, y2 = detection["bbox"]
            cx = (x1 + x2) / 2.0
            cy = (y1 + y2) / 2.0
            best_id = None
            best_iou = 0.0
            for track_id, existing in self.tracks.items():
                if track_id in matched_ids or existing.label != detection["label"]:
                    continue
                overlap = self._iou(existing.bbox, detection["bbox"])
                if overlap > best_iou:
                    best_id = track_id
                    best_iou = overlap
            track_id = best_id if best_id is not None and best_iou >= 0.1 else self.next_id
            if track_id == self.next_id:
                self.next_id += 1
            track = Track(
                id=track_id,
                label=detection["label"],
                bbox=(x1, y1, x2, y2),
                confidence=detection["confidence"],
                centroid=(cx, cy),
            )
            self.tracks[track.id] = track
            matched_ids.add(track.id)
            results.append({
                "id": track.id,
                "label": track.label,
                "bbox": track.bbox,
                "confidence": track.confidence,
                "centroid": track.centroid,
            })
        return results

    @staticmethod
    def _iou(first: tuple[float, float, float, float], second: tuple[float, float, float, float]) -> float:
        left = max(first[0], second[0])
        top = max(first[1], second[1])
        right = min(first[2], second[2])
        bottom = min(first[3], second[3])
        intersection = max(0.0, right - left) * max(0.0, bottom - top)
        first_area = max(0.0, first[2] - first[0]) * max(0.0, first[3] - first[1])
        second_area = max(0.0, second[2] - second[0]) * max(0.0, second[3] - second[1])
        union = first_area + second_area - intersection
        return intersection / union if union else 0.0
