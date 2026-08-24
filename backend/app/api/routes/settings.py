from fastapi import APIRouter

router = APIRouter()


@router.post("")
async def save_settings(payload: dict) -> dict:
    return {"status": "updated", "settings": payload}
