from fastapi import APIRouter
from settings import Settings

router = APIRouter(prefix="/ping", tags=["ping"])
settings = Settings()


@router.get(
    path="/db",
    summary="Получение токена",
    description="Выводит хэш токена GOOGLE авторизации",
)
async def ping_db():
    return {"message": "ok", "token": settings.GOOGLE_TOKEN_ID}
