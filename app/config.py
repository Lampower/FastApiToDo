import os
from dotenv import load_dotenv

load_dotenv()


class Startup:
    host = os.getenv("HOST")
    port = int(os.getenv("PORT"))
    
class ApiAccess:
    bcrypt_salt = os.getenv("SALT_KEY")
    
class JwtSettings:
    access_key = os.getenv("ACCESS_KEY")
    refresh_key = os.getenv("REFRESH_KEY")
    access_exp_time = 10
    refresh_exp_time = 10080

class Settings:
    startup = Startup()
    api = ApiAccess()
    jwt = JwtSettings()
    
settings = Settings()

