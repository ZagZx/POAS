from fastapi import (
    APIRouter, 
    HTTPException,
    status,
    Depends
)
from fastapi.security.oauth2 import (OAuth2PasswordRequestForm)
from sqlmodel import select, col
from typing import Annotated
from datetime import timedelta, datetime
from dotenv import load_dotenv
import os
import jwt

from database import SessionDep
from utils import check_password_hash
from models import Usuario

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def create_acess_token(data: dict, expires: timedelta = None):
    to_encode = data.copy()
    
    if expires:
        expires_date = datetime.now() + expires
    else:
        expires_date = datetime.now() + timedelta(minutes=15)
    
    to_encode.update({"exp": expires_date})
    jwt_encode = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return jwt_encode

login_router = APIRouter(prefix="/login", tags=["Login"])

@login_router.post("")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    session: SessionDep
):
    usuario = session.scalar(
        select(Usuario).where(
            Usuario.email == form_data.username
        )
    )

    if not usuario:
        raise HTTPException(400, "Email ou senha incorreta")
    
    if not check_password_hash(form_data.password, usuario.senha_hash):
        raise HTTPException(400, "Email ou senha incorreta")
    
    access_token = create_acess_token({"sub": usuario.email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }