from fastapi import APIRouter

router = APIRouter(prefix="/ping", tags=["ping"])

@router.get("/db")
async def ping_db():
    return {"message": "ok"}
