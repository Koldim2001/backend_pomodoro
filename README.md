# backend_pomodoro
FastAPI Pomofocus-like backend


```
uvicorn main:app --host 0.0.0.0 --port 8000 --reload --env-file .env
```

http://127.0.0.1:8000 - сайт

http://127.0.0.1:8000/docs - OpenAPI документация (swagger)


![image](https://github.com/user-attachments/assets/775c5031-f6df-489f-8161-43c53f61bc62)


Запуск celery в отдельном терминале:
```
celery -A utils.email:celery worker --loglevel=INFO --pool=solo
```