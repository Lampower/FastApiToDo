


from fastapi import APIRouter
from fastapi import Response, status

from app.config import settings
from app.database.db_context import session_scope
from app.database.db_models import NoteEntity, UserEntity
from app.models.models import UserRegister


router = APIRouter(prefix="/users")

@router.get("/{id}", status_code=200)
async def get_user(id: int, res: Response):
    with session_scope() as s:
        note = s.query(UserEntity).get(id)
    if note == None:
        res.status_code = status.HTTP_404_NOT_FOUND
        return 
    return note

@router.get("")
async def get_all(res: Response):
    with session_scope() as s:
        notes = s.query(UserEntity).all()
    
    if notes == None:
        res.status_code = 404
    
    return notes