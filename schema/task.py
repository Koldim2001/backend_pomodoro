from pydantic import BaseModel

class Task(BaseModel):
    name: str
    pomodoro_count: int
    category_id: int