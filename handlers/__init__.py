from handlers.tasks import router as task_router
from handlers.auth import router as auth_router
from handlers.user import router as user_router

routers = [task_router, auth_router, user_router]