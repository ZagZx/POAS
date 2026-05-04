from sqlmodel import SQLModel, Field 
from typing import Optional
from pydantic import EmailStr
from datetime import datetime


class UsuarioCreate(SQLModel):
    nome: str = Field(max_length=100)
    email: EmailStr = Field(max_length=150)
    senha: str = Field(max_length=50)

class UsuarioUpdate(SQLModel):
    nome: Optional[str] = Field(default=None, max_length=100)
    email: Optional[EmailStr] = Field(default=None, max_length=150)
    senha: Optional[str] = Field(default=None, max_length=50)

class UsuarioRead(SQLModel):
    id: int
    nome: str
    email: EmailStr
    criado_em: datetime
