from fastapi import APIRouter, Form, HTTPException
from schema.task import TaskSchema
from fastapi import status
from database.queries import SQLQueriesTasks

router = APIRouter(prefix="/task", tags=["task"])

sql_queries_tasks = SQLQueriesTasks(table_name="tasks")

@router.get(path="/", response_model=list[TaskSchema])
async def get_tasks():
    rows = sql_queries_tasks.select_all_rows()
    tasks = [TaskSchema(id=row[0], name=row[1], pomodoro_count=row[2], category_id=row[3]) for row in rows]
    return tasks


@router.post(
    "/",
    response_model=TaskSchema,
    summary="Create a new task",
    description="This endpoint allows you to create a new task by providing the task details.",
)
async def create_task(
    name: str | None = Form(None, description="Name of the task"),
    pomodoro_count: int = Form(1, description="Number of pomodoros for the task"),
    category_id: int = Form(description="Identifier for the category"),
):
    id = sql_queries_tasks.create_new_row(name, pomodoro_count, category_id)
    task = TaskSchema(id=id, name=name, pomodoro_count=pomodoro_count, category_id=category_id)
    return task


@router.post(path="/{task_id}", response_model=TaskSchema)
async def rename_task(task_id: int, name: str):
    rows = sql_queries_tasks.update_task_name(task_id, name)
    if len(rows) > 0:
        row = rows[0]
        task = TaskSchema(id=row[0], name=row[1], pomodoro_count=row[2], category_id=row[3])
        return task
    else:
        raise HTTPException(status_code=400, detail="Invalid request: Task not found")


@router.delete(path="/{task_id}")
async def delete_task(task_id: int):
    deleted = sql_queries_tasks.delete_row_by_id(task_id)
    if deleted:
        return {"message": "task deleted"}
    else:
        raise HTTPException(status_code=404, detail="Task not found")


def delete_row_by_id(self, task_id):
        query = "DELETE FROM {table_name} WHERE id = %s"
        self.cursor.execute(query.format(table_name=self.table_name), (task_id,))
        self.connection.commit()