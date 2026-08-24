from fastapi import APIRouter

from app.services.camera_service import camera_service

router = APIRouter()


@router.get("/detections")
async def get_detections():
    _, detections, metrics = camera_service.snapshot()
    return {"detections": detections, "count": len(detections), "metrics": metrics}


@router.get("/tracks")
async def get_tracks():
    _, detections, _ = camera_service.snapshot()
    return {"tracks": detections, "count": len(detections)}


@router.get("/analytics")
async def get_analytics():
    return {
        "objects_per_minute": 0,
        "peak_occupancy": 0,
        "average_occupancy": 0,
        "entries": 0,
        "exits": 0,
        "object_distribution": {},
    }


@router.get("/events")
async def get_events():
    return {"events": []}


@router.get("/metrics")
async def get_metrics():
    _, _, metrics = camera_service.snapshot()
    return {
        "fps": metrics["fps"],
        "latency_ms": metrics["latency_ms"],
        "cpu_usage": 0.0,
        "gpu_usage": 0.0,
        "memory_usage": 0.0,
    }
