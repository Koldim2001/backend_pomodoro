from database.cache import TaskCache
from database.queries import SQLQueriesTasks
from database.queries import SQLQueriesUsers

# Нужно ли очищать таблицы при перезапуске (при разработке полезно)
drop_table = True

# Инитциализация постграс и редис для тасок 
sql_queries_tasks = SQLQueriesTasks(table_name="tasks", drop_table=drop_table)
task_cache = TaskCache(ttl=5)  # Создаем экземпляр TaskCache с ttl=5 секунд

# Инитциализация постграс для таблицы юзеров 
sql_queries_users = SQLQueriesUsers(table_name="users", drop_table=drop_table)