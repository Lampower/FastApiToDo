


from typing import Annotated, Any
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
    
class ResponseModel(BaseModel):
    errors: list[str]
    is_success: bool
    data: object