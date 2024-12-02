from datetime import timedelta, datetime
import time
from typing import Any
from app.models.models import User
from app.config import settings
import jwt


class JwtProvider:
    def __init__(self):
        self.access_key = settings.jwt.access_key
        self.refresh_key = settings.jwt.refresh_key
        self.access_exp = settings.jwt.access_exp_time
        self.refresh_exp = settings.jwt.refresh_exp_time
        self.algorythm = "HS256"
        
        print(self.refresh_key, self.access_key)
    
    def create_access_token(self, user: User):
        payload = vars(user)
        
        token = self.__sign_token(payload, 
                                  self.access_exp, 
                                  self.access_key)
        
        return token
    
    def verify_access_token(self, token: str = None):
        try:
            decoded: User = jwt.decode(token, 
                                      self.access_key, 
                                      self.algorythm
                                      )
            return decoded
        except:
            return None
        
    def create_refresh_token(self, user: User):
        payload = vars(user)
        
        token = self.__sign_token(payload, 
                                  self.refresh_exp, 
                                  self.refresh_key)
        
        return token
    
    def verify_refresh_token(self, token: str = None):
        try:
            decoded_payload: dict[str, Any] = jwt.decode(token, 
                                      self.refresh_key, 
                                      self.algorythm
                                      )
            user: User = User(id=decoded_payload["id"], login=decoded_payload["login"])
            return user
        except:
            return None
        
    def __sign_token(self,
        payload: dict[str, Any]={},
        exp: int = 1,
        key: str = None
        ) -> str:
        """
        Keyword arguments:
        type -- тип токена(access/refresh);
        subject -- субъект, на которого выписывается токен;
        payload -- полезная нагрузка, которую хочется добавить в токен;
        ttl -- время жизни токена
        """
        # Берём текущее UNIX время
        current_timestamp = int(datetime.now().timestamp())
        
        exp_time = self.add_time_to_now(exp)
            
        # Собираем полезную нагрузку токена:
        data = dict(
            # Указываем себя в качестве издателя
            iss='test_author',
            # Временем выдачи ставим текущее
            iat=current_timestamp, 
            exp=exp_time
        )
        # Добавляем exp- время, после которого токен станет невалиден, если был передан ttl
        # Изначальный payload обновляем получившимся словарём
        payload.update(data)
        
        return jwt.encode(payload=payload, key=key, algorithm='HS256')
    
    def add_time_to_now(self, minutes: int):
        minutes_to_add = timedelta(minutes=minutes)
        return int((datetime.now() + minutes_to_add).timestamp())
    
    def get_now_as_timestamp(self):
        return int(datetime.now().timestamp())