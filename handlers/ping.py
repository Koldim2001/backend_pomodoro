from fastapi import APIRouter

router = APIRouter(prefix="/ping", tags=["ping"])

@router.qet("/db")
async def ping_db():
    return {"message": "ok"}
