



from fastapi import APIRouter

from app.database.db_context import session_scope
from app.database.db_models import Note


router = APIRouter()

@router.get("{id}")
async def get_note(id: int):
    with session_scope() as s:
        note = s.query(Note).get(id)
        
    return note