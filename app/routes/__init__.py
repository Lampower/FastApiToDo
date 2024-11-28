from fastapi.routing import APIRouter

from app.routes import auth_router, note_router, user_router


router = APIRouter(prefix="/api")

router.include_router(user_router.router)
router.include_router(note_router.router)
router.include_router(auth_router.router)
