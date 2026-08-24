import numpy as np

from app.cv.analytics.event_generator import EventGenerator
from app.cv.preprocessing.resize import preprocess_frame
from app.cv.tracker.basetracker import BaseTracker
from app.cv.visualization.annotate import draw_annotations


def test_preprocess_frame_resizes():
    frame = np.zeros((100, 200, 3), dtype=np.uint8)
    resized = preprocess_frame(frame, width=100, height=50)
    assert resized.shape[:2] == (50, 100)


def test_tracker_assigns_ids():
    tracker = BaseTracker(max_age=5, min_hits=1)
    detections = [{"bbox": (0, 0, 10, 10), "label": "person", "confidence": 0.9}]
    tracks = tracker.update(detections)
    assert len(tracks) == 1
    assert tracks[0]["id"] == 1


def test_event_generator_records_message():
    generator = EventGenerator()
    event = generator.add("entry", "Person #1 entered", object_id=1)
    assert event.type == "entry"
    assert generator.recent(1)[0]["message"] == "Person #1 entered"


def test_annotations_drawn():
    frame = np.zeros((64, 64, 3), dtype=np.uint8)
    detections = [{"id": 1, "bbox": (10, 10, 30, 30), "label": "person", "confidence": 0.95}]
    annotated = draw_annotations(frame, detections)
    assert annotated.shape == frame.shape
