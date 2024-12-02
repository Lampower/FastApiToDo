


from typing import Union
from fastapi import APIRouter, Request, Response
import jwt

from app.database.db_context import session_scope
from app.database.db_models import TokenEntity, UserEntity
from app.models.models import Error, ResponseModel, TokenResponse, User, UserLogin, UserRegister
from app.providers.encryption_provider import EncryptionProvider
from app.dependencies import container
from app.providers.jwt_provider import JwtProvider


router = APIRouter(prefix="/auth")

@router.post("/register", response_model=ResponseModel[Union[TokenResponse, Error]],
            responses= {
                400: { "model": ResponseModel[Error], "description": "user already exists" },
                200: { "model": ResponseModel[TokenResponse]}
            })
async def register(form: UserRegister, req: Request, res: Response):
    encription: EncryptionProvider = container.resolve(EncryptionProvider)
    jwt_provider: JwtProvider = container.resolve(JwtProvider)
    
    with session_scope() as s:
        is_exists = s.query(UserEntity).filter(UserEntity.login == form.login).first()
        if is_exists:
            print("exists!!!")
            res.status_code = 400
            return ResponseModel[Error](errors=["User already exists"], 
                                        is_success=False, 
                                        data=Error(message="User already exists"))
        
        user = UserEntity()
        user.login = form.login
        user.password = encription.encrypt(form.password)
        
        s.add(user)
    
    with session_scope() as s:
        user = s.query(UserEntity).filter(UserEntity.login == form.login).first()
        payload = User(id=user.id, login=user.login)
        access_token = jwt_provider.create_access_token(payload)
        refresh_token = jwt_provider.create_refresh_token(payload)
        
        token_entity = TokenEntity()
        token_entity.token = refresh_token
        token_entity.exp_time = jwt_provider.add_time_to_now(jwt_provider.refresh_exp)
        
        check_tokens_of_user(user, jwt_provider)
        
        user.tokens.append(token_entity)
        
    res.set_cookie(key="refresh_token")
    
    return ResponseModel[TokenResponse](
        data = TokenResponse(
            user=payload,
            access_token=access_token, 
            refresh_token=refresh_token
            ) 
        )

@router.post("/login", response_model=ResponseModel[Union[TokenResponse, Error]],
            responses= {
                400: { "model": ResponseModel[Error], "description": "user already exists" },
                200: { "model": ResponseModel[TokenResponse]}
            })
async def login(form: UserLogin, req: Request, res: Response):
    encription: EncryptionProvider = container.resolve(EncryptionProvider)
    jwt_provider: JwtProvider = container.resolve(JwtProvider)
    
    with session_scope() as s:
        user = s.query(UserEntity).filter(UserEntity.login == form.login).first()
        if not user:
            res.status_code = 400
            return ResponseModel[Error](errors = ["User with this login wasn't found"], 
                                        is_success=False,
                                        data = Error(message="User with this login wasn't found"))
        
        is_verified = encription.verify(form.password, user.password)    
        
        if not is_verified:
            res.status_code = 400
            return ResponseModel[Error](errors = ["Wrong password"], 
                                        is_success=False,
                                        data="Wrong password")
            
        payload = User(id=user.id, login=user.login)
        access_token = jwt_provider.create_access_token(payload)
        refresh_token = jwt_provider.create_refresh_token(payload)
        
        token_entity = TokenEntity()
        token_entity.token = refresh_token
        token_entity.exp_time = jwt_provider.add_time_to_now(jwt_provider.refresh_exp)
        
        check_tokens_of_user(user, jwt_provider)
        
        user.tokens.append(token_entity)
    
    res.set_cookie(key="refresh_token", value=refresh_token)
    
    return ResponseModel[TokenResponse](
        data = TokenResponse(
            user=payload,
            access_token=access_token, 
            refresh_token=refresh_token
            )
    )

@router.get("/refresh")
async def resfresh_token(req: Request, res: Response):
    jwt_provider: JwtProvider = container.resolve(JwtProvider)

    with session_scope() as s:    
        token = req.cookies["refresh_token"]
        
        payload = jwt_provider.verify_refresh_token(token)
        
        if payload is None:
            # unauthorized!
            return 
        
        user = s.query(UserEntity).filter(UserEntity.id == payload.id).first()
      
        is_found = False
        _user_token = None
        for user_token in user.tokens:
            if token == user_token.token:
                is_found = True
                _user_token = user_token
                break
        
        if not is_found:
            res.status_code = 401
            return ResponseModel[Error](
                errors = ["Unauthorized"],
                is_success=False
            )
        
        user.tokens.remove(_user_token)
        
        access_token = jwt_provider.create_access_token(payload)
        refresh_token = jwt_provider.create_refresh_token(payload)
    
        token_entity = TokenEntity()
        token_entity.token = refresh_token
        token_entity.exp_time = jwt_provider.add_time_to_now(jwt_provider.refresh_exp)
        
        user.tokens.append(token_entity)
    
    res.set_cookie(key="refresh_token", value=refresh_token)    
        
    return ResponseModel[TokenResponse](
        data = TokenResponse(
            user=payload,
            access_token=access_token, 
            refresh_token=refresh_token
            )
    )

@router.get("/logout")
async def logout():
    return


def check_tokens_of_user(user: UserEntity, jwt_provider: JwtProvider):
    tokens = user.tokens
    time_now = jwt_provider.get_now_as_timestamp()
    for entity in tokens:
        exp = entity.exp_time
        if  exp < time_now:
            user.tokens.remove(entity)       
            
    return user