from fastapi import APIRouter, HTTPException

router = APIRouter()

CAMERA_STATE = {
    "running": False,
    "source": "0",
    "status": "stopped",
}


@router.post("/start")
async def start_camera(payload: dict | None = None) -> dict:
    source = (payload or {}).get("source", "0")
    CAMERA_STATE["running"] = True
    CAMERA_STATE["source"] = str(source)
    CAMERA_STATE["status"] = "running"
    return {"status": "started", "source": source}


@router.post("/stop")
async def stop_camera() -> dict:
    CAMERA_STATE["running"] = False
    CAMERA_STATE["status"] = "stopped"
    return {"status": "stopped"}


@router.get("/status")
async def camera_status() -> dict:
    return CAMERA_STATE
