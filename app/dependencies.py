## Register providers
import punq

from app.providers.encryption_provider import EncryptionProvider
from app.providers.jwt_provider import JwtProvider


container = punq.Container()

# container.register()
container.register(EncryptionProvider)
container.register(JwtProvider)