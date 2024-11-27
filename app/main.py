import os
from typing import Union
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.responses import JSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.config import settings
from app.models.models import CreateResponse, Note
from app.routes import router


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

notes_list = []

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router)

def main():
    print(f"\ndocs are avalible at: http://{settings.startup.host}:{settings.startup.port}/docs\n")
    uvicorn.run("app.main:app", host=settings.startup.host, port=settings.startup.port, reload=True)
      
if __name__ == "__main__":
    main()