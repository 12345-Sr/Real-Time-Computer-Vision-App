import cv2
import numpy as np


def preprocess_frame(frame: np.ndarray, width: int | None = None, height: int | None = None) -> np.ndarray:
    if width is None and height is None:
        return frame
    if width is None:
        width = int(frame.shape[1] * (height / frame.shape[0]))
    if height is None:
        height = int(frame.shape[0] * (width / frame.shape[1]))
    return cv2.resize(frame, (width, height), interpolation=cv2.INTER_LINEAR)
