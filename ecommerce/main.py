#uvicorn app:app
from fastapi import FastAPI

from routes import usuario_router
from utils import gerar_env

gerar_env()

app = FastAPI()

app.include_router(usuario_router)