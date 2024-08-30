from fastapi import APIRouter, Form
from fixtures import tasks as fixtures_tasks
from schema.task import Task
from fastapi import status


router = APIRouter(prefix="/task", tags=["task"])

@router.get(path="/", response_model=list[Task])
async def get_tasks():
    return fixtures_tasks

# @router.post(path="/", response_model=Task)
# async def create_task(task: Task):
#     fixtures_tasks.append(task)
#     return task


@router.post(
    "/",
    response_model=Task,
    summary="Create a new task",
    description="This endpoint allows you to create a new task by providing the task details.",
)
async def create_task(
    id: int = Form(description="Unique identifier for the task"),
    name: str | None = Form(None, description="Name of the task"),
    pomodoro_count: int = Form(1, description="Number of pomodoros for the task"),
    category_id: int = Form(description="Identifier for the category"),
):
    task = Task(id=id, name=name, pomodoro_count=pomodoro_count, category_id=category_id)
    fixtures_tasks.append(task)
    return task


@router.post(path="/{task_id}", response_model=Task)
async def rename_task(task_id: int, name: str):
    for task in fixtures_tasks:
        if task["id"] == task_id:
            task["name"] = name
            return task

@router.delete(path="/{task_id}")
async def delete_task(task_id: int):
    for index, task in enumerate(fixtures_tasks):
        if task["id"] == task_id:
            del fixtures_tasks[index]
            return {"message": "task deleted"} 
    return {"message": "task not found"}
