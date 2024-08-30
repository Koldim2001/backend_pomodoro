from pydantic import BaseModel

class Task(BaseModel):
    id: int
    name: str
    pomodoro_count: int
    category_id: int