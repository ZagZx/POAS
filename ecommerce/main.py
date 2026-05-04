#uvicorn app:app
from fastapi import FastAPI
from dotenv import load_dotenv

from routes import usuario_router
from utils import gerar_env

gerar_env()
load_dotenv()

app = FastAPI()

app.include_router(usuario_router)