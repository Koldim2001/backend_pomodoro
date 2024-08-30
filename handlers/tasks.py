from fastapi import APIRouter
from fixtures import tasks as fixtures_tasks
from schema.task import Task
from fastapi import status


router = APIRouter(prefix="/task", tags=["task"])

@router.delete(path="/{task-id}", stattus_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int):
    for index, task in enumerate(fixtures_tasks):
        if task["id"] == task_id:
            del fixtures_tasks[index]
            return {"message": "task deleted"}
    return {"message": "task not found"}