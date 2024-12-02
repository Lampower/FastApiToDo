import bcrypt
import os
from app.config import settings


class EncryptionProvider:
    def __init__(self):
       self.salt = b'$2b$12$VD0NqCSzNr3/3UdnflULKuzJ2egeyhklWQ.h9SzJYDoy175kk0hS6'
       print(self.salt)
    
    def encrypt(self, key: str) -> bytes:
        hashed = bcrypt.hashpw(key.encode(), self.salt)
        return hashed
    
    def verify(self, text_key, hashed_key) -> bool:
        hashed_text = self.encrypt(text_key)
        return hashed_key == hashed_text