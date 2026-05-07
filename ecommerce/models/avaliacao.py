from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime

from utils import get_timestamp_utc_now
if TYPE_CHECKING:
    from .produto import Produto
    from .usuario import Usuario

class Avaliacao(SQLModel, table=True):
    __tablename__ = "avaliacoes"

    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuarios.id")
    produto_id: int = Field(foreign_key="produtos.id")
    nota: int
    comentario: Optional[str] = Field(default=None)
    criado_em: datetime = Field(default_factory=get_timestamp_utc_now)

    usuario: "Usuario" = Relationship(back_populates="avaliacoes")
    produto: "Produto" = Relationship(back_populates="avaliacoes")