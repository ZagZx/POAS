from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr
from datetime import datetime, timezone

from .usuario_papel import UsuarioPapel

if TYPE_CHECKING:
    from .papel import Papel


class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(max_length=100)
    email: EmailStr = Field(max_length=150, unique=True)
    senha_hash: str = Field(max_length=255)
    criado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    papeis: list["Papel"] = Relationship(back_populates="usuarios", link_model=UsuarioPapel)


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
