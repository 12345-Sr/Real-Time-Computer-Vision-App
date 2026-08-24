from dataclasses import dataclass
from pathlib import Path


@dataclass
class ModelConfig:
    name: str
    weights: str | None = None
    device: str = "auto"


class ModelManager:
    """Model abstraction used to switch detector variants."""

    def __init__(self, model_name: str = "yolov8n.pt", model_path: str | None = None, device: str = "auto"):
        self.model_name = model_name
        self.model_path = model_path
        self.device = device
        self._registry = {
            "yolov8n.pt": ModelConfig("yolov8n.pt", weights="yolov8n.pt", device=device),
            "yolov8s.pt": ModelConfig("yolov8s.pt", weights="yolov8s.pt", device=device),
            "yolov8m.pt": ModelConfig("yolov8m.pt", weights="yolov8m.pt", device=device),
        }

    def get_model_config(self) -> ModelConfig:
        if self.model_path:
            return ModelConfig(self.model_name, weights=self.model_path, device=self.device)
        return self._registry.get(self.model_name, self._registry["yolov8n.pt"])

    def resolve_model_path(self) -> str:
        config = self.get_model_config()
        return config.weights or self.model_name

    def list_available(self) -> list[str]:
        return list(self._registry)
