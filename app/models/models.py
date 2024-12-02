


from typing import Annotated, Any, Generic, Optional
from annotated_types import T
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
    
class User(BaseModel):
    id: int
    login: str
    
class TokenResponse(BaseModel):
    user: User
    access_token: str
    refresh_token: str
    
class CreateResponse(BaseModel):
    message: str
    
class Error(BaseModel):
    message: str
    

class ResponseModel(BaseModel, Generic[T]):
    errors: Optional[list[str]] = []
    is_success: bool = True
    data: Optional[T | None]