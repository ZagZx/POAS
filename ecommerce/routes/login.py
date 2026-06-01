from fastapi import (
    APIRouter, 
    HTTPException,
    status,
    Depends
)
from fastapi.security.oauth2 import (
    OAuth2PasswordRequestForm,
    OAuth2PasswordBearer
)
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

oauth_schema = OAuth2PasswordBearer(tokenUrl="token")

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

def get_usuario(token: Annotated[str, Depends(oauth_schema)], session: SessionDep) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Email ou senha incorreta",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        dados = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = dados["sub"]
        if not email:
            raise credentials_exception
        
        usuario = session.scalar(
            select(Usuario).where(
                Usuario.email == email
            )
        )
        if not usuario:
            raise credentials_exception
        
        return usuario
    except Exception:
        raise credentials_exception

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
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, 
            "Email ou senha incorreta")
    
    if not check_password_hash(form_data.password, usuario.senha_hash):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, 
            "Email ou senha incorreta")
    
    access_token = create_acess_token({"sub": usuario.email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }