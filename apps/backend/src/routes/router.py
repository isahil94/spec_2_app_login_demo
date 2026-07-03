from fastapi import APIRouter

from apps.backend.src.controllers.admin_controller import router as admin_router
from apps.backend.src.controllers.auth_controller import router as auth_router
from apps.backend.src.controllers.comment_controller import router as comment_router
from apps.backend.src.controllers.notification_controller import (
    router as notification_router,
)
from apps.backend.src.controllers.task_controller import router as task_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(task_router)
api_router.include_router(comment_router)
api_router.include_router(notification_router)
api_router.include_router(admin_router)
