from pydantic import BaseModel

class Task(BaseModel):
    id: int
    name: str | None = None
    pomodoro_count: int = 1
    category_id: int
