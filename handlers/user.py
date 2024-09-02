from fastapi import APIRouter
from schema import UserLoginSchema, UserCreateSchema
from database import sql_queries_users

router = APIRouter(prefix="/user", tags=["user"])


@router.post("", response_model=UserLoginSchema)
async def create_user(body: UserCreateSchema):
    print(body)
    return "hi"
