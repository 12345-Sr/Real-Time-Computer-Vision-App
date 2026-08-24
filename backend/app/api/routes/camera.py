import asyncio

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.services.camera_service import camera_service

router = APIRouter()

@router.post("/start")
async def start_camera(payload: dict | None = None) -> dict:
    source = (payload or {}).get("source", "0")
    try:
        return camera_service.start(str(source))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/stop")
async def stop_camera() -> dict:
    camera_service.stop()
    return {"status": "stopped"}


@router.get("/status")
async def camera_status() -> dict:
    return camera_service.status()


@router.get("/detections")
async def camera_detections() -> dict:
    _, detections, metrics = camera_service.snapshot()
    return {"detections": detections, "count": len(detections), "metrics": metrics}


async def frame_stream():
    while True:
        frame, _, _ = camera_service.snapshot()
        if frame:
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
        if not camera_service.running:
            break
        await asyncio.sleep(0.03)


@router.get("/stream")
async def camera_stream() -> StreamingResponse:
    return StreamingResponse(frame_stream(), media_type="multipart/x-mixed-replace; boundary=frame")
