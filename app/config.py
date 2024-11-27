import os
from dotenv import load_dotenv
import punq


load_dotenv()


class Startup:
    host = os.getenv("HOST")
    port = int(os.getenv("PORT"))
    

class Routes:
    note_route = "/notes"
    user_route = "/users"
    
class Settings:
    routes = Routes()
    startup = Startup()
    
settings = Settings()

## Register providers
container = punq.Container()

# container.register()