from fastapi import APIRouter, HTTPException
from schema import UserLoginSchema, UserCreateSchema
from database import sql_queries_users

router = APIRouter(prefix="/user", tags=["user"])


@router.post(path="",
    summary="Авторизация пользователей",
    description="Осуществляет проверку доступа (вход в приложение)",
)
async def create_user(body: UserCreateSchema) -> UserLoginSchema:
    result = sql_queries_users.check_user(body.username, body.password)
    
    if isinstance(result, str):
        # Если результат - строка, значит, произошла ошибка
        raise HTTPException(status_code=400, detail=result)
    else:
        # Если результат - кортеж, значит, проверка пройдена успешно
        user_id, access_token = result
        return UserLoginSchema(user_id=user_id, access_token=access_token)
