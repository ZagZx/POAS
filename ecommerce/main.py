#uvicorn app:app
from fastapi import FastAPI

from utils import gerar_env
from routes import (
    usuario_router, 
    papel_router
)

gerar_env()

app = FastAPI()

app.include_router(usuario_router)
app.include_router(papel_router)