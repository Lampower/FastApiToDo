

from fastapi import APIRouter

from app.config import settings


router = APIRouter(prefix=settings.routes.note_route)

router.include_router()