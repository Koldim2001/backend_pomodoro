# Бэкенд приложение (обработчик тасок) - версия для локального поднятия (без докера)
FastAPI Pomofocus-like backend

Запуск FastAPI:
```
uvicorn main:app --host 0.0.0.0 --port 8000 --reload --env-file .env
```

http://127.0.0.1:8000 - сайт

http://127.0.0.1:8000/docs - OpenAPI документация (swagger)

![image](https://github.com/user-attachments/assets/c96d44e8-c32f-4f67-9735-0439e4b2f27e)

Запуск celery в отдельном терминале (реализует сервис отправки email отчетов):
```
celery -A celery_workers.email:celery worker --loglevel=INFO --pool=solo
```
