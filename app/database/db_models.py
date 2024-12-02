from typing import List
from sqlalchemy import *
from sqlalchemy.orm import *

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    pass

class NoteEntity(Base):
    __tablename__ = "note"
    
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    author: Mapped[int] = mapped_column(ForeignKey("user.id"))
        
class UserEntity(Base):
    __tablename__ = "user"
    
    login: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    
    tokens: Mapped[List["TokenEntity"]] = relationship()
    notes: Mapped[List["NoteEntity"]] = relationship()
    
class TokenEntity(Base):
    __tablename__ = "token"
    
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    exp_time: Mapped[str] = mapped_column()
    token: Mapped[str] = mapped_column()