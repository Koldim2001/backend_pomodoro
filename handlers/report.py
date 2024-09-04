from fastapi import APIRouter, Depends
from celery_workers.email import send_email_report_tasks
from utils.jwt import get_request_user_id

router = APIRouter(prefix="/report", tags=["report"])


@router.post(path="/all_tasks",summary="Отправление на почту списка всех задач",
    description="Отправляет на почту список всех имеющихся задач пользователя",
)
def get_dashboard_report(recipient_email: str, user_id: int = Depends(get_request_user_id)):
    send_email_report_tasks.delay(recipient_email, user_id)
    return {
        "status": 200,
        "data": "Письмо отправлено",
        "recipient_email": recipient_email
    }