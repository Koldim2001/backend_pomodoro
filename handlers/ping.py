from fastapi import APIRouter
from settings import Settings

router = APIRouter(prefix="/ping", tags=["ping"])
settings = Settings()

@router.get("/db")
async def ping_db():
    return {"message": "ok", "token": settings.GOOGLE_TOKEN_ID}
