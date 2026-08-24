from fastapi import APIRouter

router = APIRouter()


@router.get("/detections")
async def get_detections():
    return {"detections": [], "count": 0}


@router.get("/tracks")
async def get_tracks():
    return {"tracks": [], "count": 0}


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
    return {
        "fps": 0.0,
        "latency_ms": 0.0,
        "cpu_usage": 0.0,
        "gpu_usage": 0.0,
        "memory_usage": 0.0,
    }
