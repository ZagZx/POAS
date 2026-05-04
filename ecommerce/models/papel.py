from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

from .usuario_papel import UsuarioPapel

if TYPE_CHECKING:
    from .usuario import Usuario


class Papel(SQLModel, table=True):
    __tablename__ = "papeis"

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(max_length=50, unique=True)

    usuarios: list[Usuario] = Relationship(back_populates="papeis", link_model=UsuarioPapel)


class PapelCreate(SQLModel):
    nome: str = Field(max_length=50)

class PapelUpdate(SQLModel):
    nome: Optional[str] = Field(default=None, max_length=50)

class PapelRead(SQLModel):
    id: int
    nome: str