from fastapi import FastAPI
from backend.core.config import settings
from backend.api.v1.auth import auth_router
from backend.api.v1.user import router as user_router
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


@app.get("/")
async def root():
    return {
        "message": "borrex-backend-system",
        "status": "online",
    }


@app.get("/health")
async def health_check():
    return {"status": "ok"}

app.include_router(auth_router)
app.include_router(user_router)