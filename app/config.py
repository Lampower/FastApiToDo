import os
from dotenv import load_dotenv
import punq

from app.providers.encryption_provider import EncryptionProvider


load_dotenv()


class Startup:
    host = os.getenv("HOST")
    port = int(os.getenv("PORT"))
    


class Settings:
    startup = Startup()
    
settings = Settings()

## Register providers
container = punq.Container()

# container.register()
container.register(EncryptionProvider)