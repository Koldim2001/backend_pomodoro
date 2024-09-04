# backend_pomodoro
FastAPI Pomofocus-like backend


```
uvicorn main:app --host 0.0.0.0 --port 8000 --reload --env-file .env
```

http://127.0.0.1:8000 - сайт

http://127.0.0.1:8000/docs - OpenAPI документация (swagger)

![image](https://github.com/user-attachments/assets/2848e1f9-8959-417c-bfa6-82efa5160495)

Запуск celery в отдельном терминале (реализует сервис отправки email отчетов):
```
celery -A celery_workers.email:celery worker --loglevel=INFO --pool=solo
```
