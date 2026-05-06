from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from pydantic import EmailStr
from datetime import datetime

from utils import get_timestamp_utc_now
from .usuario_papel import UsuarioPapel
if TYPE_CHECKING:
    from .papel import Papel
    from .pedido import Pedido


class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(max_length=100)
    email: EmailStr = Field(max_length=150, unique=True)
    senha_hash: str = Field(max_length=255)
    criado_em: datetime = Field(default_factory=get_timestamp_utc_now)

    papeis: list["Papel"] = Relationship(back_populates="usuarios", link_model=UsuarioPapel)
    pedidos: list["Pedido"] = Relationship(back_populates="usuario")