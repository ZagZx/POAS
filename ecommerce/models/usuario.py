from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from datetime import datetime, timezone


class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(max_length=100)
    email: EmailStr = Field(max_length=150, unique=True)
    senha_hash: str = Field(max_length=255)
    criado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UsuarioCreate(SQLModel):
    nome: str = Field(max_length=100)
    email: EmailStr = Field(max_length=150)
    senha: str = Field(max_length=50)

class UsuarioUpdate(SQLModel):
    nome: Optional[str] = Field(max_length=100)
    email: Optional[EmailStr] = Field(max_length=150)
    senha: Optional[str] = Field(max_length=50)

class UsuarioRead(SQLModel):
    id: int
    nome: str
    email: EmailStr
    criado_em: datetime
