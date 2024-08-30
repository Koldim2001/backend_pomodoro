from fastapi import APIRouter, Form, HTTPException
from schema.task import TaskSchema
from database.queries import SQLQueriesTasks
from database.cache import TaskCache

router = APIRouter(prefix="/task", tags=["task"])

# Инитциализация постграс и редис
sql_queries_tasks = SQLQueriesTasks(table_name="tasks")
task_cache = TaskCache(ttl=5)  # Создаем экземпляр TaskCache с ttl=5 секунд


@router.get(
    path="/",
    response_model=list[TaskSchema],
    summary="Получение списка всех задач",
    description="Выдает по запросу список всех имеющихся задач (берет из БД либо из кэша)",
)
async def get_tasks():
    # Проверяем наличие данных в кэше
    cache_tasks = task_cache.get_tasks()
    if cache_tasks:
        print("Данные взяты из кэша")
        return cache_tasks
    
    # Если данных в кэше нет, выполняем SQL-запрос
    rows = sql_queries_tasks.select_all_rows()
    tasks = [
        TaskSchema(id=row[0], name=row[1], pomodoro_count=row[2], category_id=row[3])
        for row in rows
    ]

    # Сохраняем данные в кэш
    if len(tasks) > 0:
        task_cache.set_tasks(tasks)
    
    return tasks


@router.post(
    "/",
    response_model=TaskSchema,
    summary="Создание новой задачи",
    description="Позволяет создавать новую задачу и сохраняет ее в БД",
)
async def create_task(
    name: str | None = Form(None, description="Name of the task"),
    pomodoro_count: int = Form(1, description="Number of pomodoros for the task"),
    category_id: int = Form(description="Identifier for the category"),
):
    id = sql_queries_tasks.create_new_row(name, pomodoro_count, category_id)
    task = TaskSchema(id=id, name=name, pomodoro_count=pomodoro_count, category_id=category_id)
    return task


@router.post(
    path="/{task_id}",
    response_model=TaskSchema,
    summary="Изменение имени задачи",
    description="Позволяет изменить имя имеющейся задачи по ее id",
)
async def rename_task(task_id: int, name: str):
    rows = sql_queries_tasks.update_task_name(task_id, name)
    if len(rows) > 0:
        row = rows[0]
        task = TaskSchema(id=row[0], name=row[1], pomodoro_count=row[2], category_id=row[3])
        return task
    else:
        raise HTTPException(status_code=400, detail="Invalid request: Task not found")


@router.delete(
    path="/{task_id}",
    summary="Удаление задачи",
    description="Позволяет удалять задачу из БД по ее id",
)
async def delete_task(task_id: int):
    deleted = sql_queries_tasks.delete_row_by_id(task_id)
    if deleted:
        return {"message": "task deleted"}
    else:
        raise HTTPException(status_code=404, detail="Task not found")
