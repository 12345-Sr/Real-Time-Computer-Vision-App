from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import camera, analytics, health, settings

app = FastAPI(title="Real-Time CV Analytics", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(camera.router, prefix="/camera", tags=["camera"])
app.include_router(analytics.router, prefix="", tags=["analytics"])
app.include_router(health.router, prefix="", tags=["health"])
app.include_router(settings.router, prefix="/settings", tags=["settings"])


@app.get("/")
async def root() -> dict:
    return {"message": "Real-Time CV Analytics API"}
