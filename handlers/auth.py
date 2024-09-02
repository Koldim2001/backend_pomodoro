from fastapi import APIRouter
from settings import Settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get(
    path="/auth",
    summary="Регистрация пользователей",
    description="Осуществляет создание нового пользователя",
)
async def ping_db():
    return {"message": "ok"}
