


from typing import Annotated, Any, Optional
from pydantic import BaseModel


class Note(BaseModel):
    title: str
    description: str
    
class UserRegister(BaseModel):
    login: str
    password: str

class UserLogin(BaseModel):
    login: str
    password: str
    
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    
class CreateResponse(BaseModel):
    message: str
    
class Error(BaseModel):
    message: str
    
class User(BaseModel):
    id: int
    login: str
    
class ResponseModel[T](BaseModel):
    errors: Optional[list[str]] = []
    is_success: bool = True
    data: Optional[T | None]