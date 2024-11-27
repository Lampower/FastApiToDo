


from fastapi import APIRouter

from app.controllers import user_controller
from app.config import settings


router = APIRouter(prefix=settings.routes.user_route)

router.include_router(user_controller.router)