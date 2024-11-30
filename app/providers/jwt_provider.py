from datetime import timedelta, datetime
import time
from typing import Any
from app.models.models import User
from app.config import settings
from app.dependencies import container
import jwt


class JwtProvider:
    def __init__(self):
        self.access_key = settings.jwt.access_key
        self.refresh_key = settings.jwt.refresh_key
        self.access_exp = settings.jwt.access_exp_time
        self.refresh_exp = settings.jwt.refresh_exp_time
        self.algorythm = "HS256"
    
    def create_access_token(self, user: User):
        payload = user
        
        token = self.__sign_token(payload, )
        
        return token
    
    def verify_access_token(self, token: str = None):
        try:
            decoded: User = self.jwt.decode(token, 
                                      self.access_key, 
                                      self.algorythm
                                      )
            return decoded
        except:
            return None
        
    def create_refresh_token(self, user: User):
        payload = user
        
        token = self.jwt.encode(payload, 
                                self.access_key, 
                                self.algorythm
                                )
        
    def __sign_token(self,
        payload: dict[str, Any]={},
        ttl: timedelta=None,
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
            
        # Собираем полезную нагрузку токена:
        data = dict(
            # Указываем себя в качестве издателя
            iss='test_author',
            # Рандомно генерируем идентификатор токена ( UUID )
            jti=self.__generate_jti(),
            # Временем выдачи ставим текущее
            iat=current_timestamp, 
            # Временем начала действия токена ставим текущее или то, что было передано в payload
            nbf=payload['nbf'] if payload.get('nbf') else current_timestamp
        )
        # Добавляем exp- время, после которого токен станет невалиден, если был передан ttl
        data.update(dict(exp=data['nbf'] + int(ttl.total_seconds()))) if ttl else None
        # Изначальный payload обновляем получившимся словарём
        payload.update(data)
        
        return jwt.encode(payload=payload, key=key, algorithm='HS256')