import bcrypt
import os
from app.config import settings

salt = bcrypt.gensalt()


class EncryptionProvider:
    
    def encrypt(self, key: str) -> bytes:
        hashed = bcrypt.hashpw(key.encode(), salt)
        return hashed
    
    def verify(self, text_key, hashed_key) -> bool:
        hashed_text = self.encrypt(text_key)
        return hashed_key == hashed_text