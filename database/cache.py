import json
from schema.task import TaskSchema
import redis
from settings import Settings


def get_redis_connection() -> redis.Redis:
    settings = Settings()
    return redis.Redis(host=settings.CACHE_HOST, port=settings.CACHE_PORT, db=settings.CACHE_DB)


class TaskCache:
    def __init__(self, ttl: int = 5):
        self.redis = get_redis_connection()
        self.ttl = ttl  # длительность хранения кэша в секундах

    def get_tasks(self, user_id) -> list[TaskSchema]:
        with self.redis as redis:
            tasks_json = redis.lrange(f"tasks_{user_id}", 0, -1)
            return [TaskSchema.model_validate(json.loads(task)) for task in tasks_json]

    def set_tasks(self, tasks: list[TaskSchema], user_id):
        tasks_json = [task.json() for task in tasks]
        with self.redis as redis:
            redis.delete(f"tasks_{user_id}")  # Очищаем список перед добавлением новых задач
            redis.lpush(f"tasks_{user_id}", *tasks_json)
            redis.expire(f"tasks_{user_id}", self.ttl)  # Устанавливаем время жизни для ключа "tasks"
