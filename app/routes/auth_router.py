


from fastapi import APIRouter, Response

from app.database.db_context import session_scope
from app.database.db_models import UserEntity
from app.models.models import Error, ResponseModel, TokenResponse, User, UserLogin, UserRegister
from app.providers.encryption_provider import EncryptionProvider
from app.dependencies import container
from app.providers.jwt_provider import JwtProvider


router = APIRouter(prefix="/auth")

@router.post("/register", response_model=ResponseModel)
async def register(form: UserRegister, res: Response):
    encription: EncryptionProvider = container.resolve(EncryptionProvider)
    jwt_provider: JwtProvider = container.resolve(JwtProvider)
    with session_scope() as s:
        is_exists = s.query(UserEntity).filter(UserEntity.login == form.login).first()
        if is_exists:
            print("exists!!!")
            res.status_code = 400
            return Error(message="user already exists")
        
        user = UserEntity()
        user.login = form.login
        user.password = encription.encrypt(form.password)
        
        s.add(user)
    
    access_token = jwt_provider.create_access_token(user)
    refresh_token = jwt_provider.create_refresh_token(user)
    
    return ResponseModel[TokenResponse](
        data = TokenResponse(access_token, refresh_token)
    )

@router.post("/login")
async def login(form: UserLogin, res: Response):
    encription: EncryptionProvider = container.resolve(EncryptionProvider)
    with session_scope() as s:
        user = s.query(UserEntity).filter(UserEntity.login == form.login).first()
        if not user:
            res.status_code = 400
            return ResponseModel[None](errors = ["user with this login wasn't found"])
    
    is_verified = encription.verify(form.password, user.password)    
    
    if not is_verified:
        res.status_code = 401
        return Error(message="wrong password")
    
    return ResponseModel[User](
        data = User(id=user.id, login = user.login)
    )

@router.get("/refresh")
async def resfresh_token():
    return

@router.get("/logout")
async def logout():
    return