


from fastapi import APIRouter, Response

from app.database.db_context import session_scope
from app.database.db_models import UserEntity
from app.models.models import ResponseModel, UserRegister
from app.config import container
from app.providers.encryption_provider import EncryptionProvider


router = APIRouter(prefix="/auth")

@router.post("/register", response_model=ResponseModel)
async def register(form: UserRegister, res: Response):
    with session_scope() as s:
        is_exists = s.query(UserEntity).filter(UserEntity.login == form.login).first()
        if is_exists:
            print("exists!!!")
            res.status_code = 400
            return ResponseModel(errors=["this login already esists"], is_success=False, data=None)
        
        user = UserEntity()
        user.login = form.login
        user.password = form.password
        
        s.add(user)
    
    return ResponseModel(is_success=True, data = user)

@router.post("/login")
async def login():
    return

@router.get("/refresh")
async def resfresh_token():
    return

@router.get("/logout")
async def logout():
    return