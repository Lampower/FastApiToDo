import bcrypt
import os

class EncryptionProvider:

    def __init__(self):
        self.tobyte = os.getenv("SALT_KEY")
        self.salt = self.tobyte.encode()
        pass
    
    def encrypt(self, key: str) -> bytes:
        hashed = bcrypt.hashpw(key.encode(), self.salt)
        return hashed
    
    def verify(self, text_key, hashed_key) -> bool:
        hashed_text = self.encrypt(text_key)
        return hashed_key == hashed_text