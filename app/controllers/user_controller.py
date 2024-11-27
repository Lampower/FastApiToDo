

from fastapi import APIRouter

from app.database.db_context import session_scope
from app.database.db_models import User
from app.models.models import CreateResponse, UserRegister


router = APIRouter()


@router.get("/{id}")
async def get_user(id: int):
    with session_scope() as s:
        user: User = s.query(User).get(id)
    return user

@router.post("/create")
async def create_user(form: UserRegister):
    with session_scope() as s:
        user = User()
        user.login = form.login
        user.password = form.password
        s.add(user)
    
    return CreateResponse(message="Created!")