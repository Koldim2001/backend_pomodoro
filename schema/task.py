from pydantic import BaseModel

class TaskSchema(BaseModel):
    id: int | None = None
    name: str | None = None
    pomodoro_count: int = 1
    category_id: int
    user_id: int
