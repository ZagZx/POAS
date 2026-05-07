from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime

from utils import get_timestamp_utc_now
if TYPE_CHECKING:
    from .produto import Produto

class Estoque(SQLModel, table=True):
    __tablename__ = "estoque"

    id: Optional[int] = Field(default=None, primary_key=True)
    produto_id: int = Field(foreign_key="produtos.id", unique=True)
    quantidade: int
    atualizado_em: datetime = Field(default_factory=get_timestamp_utc_now)

    produto: "Produto" = Relationship(back_populates="estoque")