import smtplib
from email.message import EmailMessage
from schema import TaskSchema
from database import sql_queries_tasks
from dotenv import load_dotenv
import os

from celery import Celery

# Загружаем переменные окружения из .env файла
load_dotenv()

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASSWORD = os.getenv('EMAIL_PASSWORD')

celery = Celery("tasks_email", broker="redis://localhost:6379")


def format_tasks_as_yaml(tasks):
    yaml_tasks = []
    for task in tasks:
        yaml_tasks.append(f"name: {task.name}")
        yaml_tasks.append(f"pomodoro_count: {task.pomodoro_count}")
        yaml_tasks.append(f"category_id: {task.category_id}")
        yaml_tasks.append("")  # Добавляем пустую строку для разделения задач
    return "\n".join(yaml_tasks)


def get_tasks_to_send(user_id: int) -> str:
    # выполняем SQL-запрос
    rows = sql_queries_tasks.select_all_rows(user_id=user_id)

    tasks = [
        TaskSchema(
            id=row[0], name=row[1], pomodoro_count=row[2], category_id=row[3], user_id=row[4]
        )
        for row in rows
    ]

    return format_tasks_as_yaml(tasks)


def get_email_template(username: str, recipient_email: str, task_text: str):
    email = EmailMessage()
    email["Subject"] = "Статус тасок в pomodoro"
    email["From"] = SMTP_USER
    email["To"] = recipient_email

    email.set_content(
        "<div>"
        f'<h3 style="color: red;">Здравствуйте, {username}, а вот и ваш отчет по таскам:</h3>'
        f'<pre>{task_text}</pre>'  # Используем <pre> для сохранения форматирования
        "</div>",
        subtype="html",
    )
    return email


@celery.task
def send_email_report_tasks(recipient_email: str, user_id: int):
    task_text = get_tasks_to_send(user_id)
    email = get_email_template(
        username=user_id, recipient_email=recipient_email, task_text=task_text
    )
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)