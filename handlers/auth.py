from fastapi import APIRouter, HTTPException
from schema import UserLoginSchema, UserCreateSchema
from database import sql_queries_users

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    path="/",
    summary="Регистрация пользователей",
    description="Осуществляет создание нового пользователя",
)
async def ping_db(body: UserCreateSchema) -> UserLoginSchema:
    result = sql_queries_users.create_new_user(body.username, body.password)
    
    if isinstance(result, str):
        # Если результат - строка, значит, произошла ошибка
        raise HTTPException(status_code=400, detail=result)
    else:
        # Если результат - кортеж, значит, пользователь успешно создан
        user_id, access_token = result
        return UserLoginSchema(user_id=user_id, access_token=access_token)