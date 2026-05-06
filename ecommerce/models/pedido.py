from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from decimal import Decimal
from datetime import datetime

from utils import get_timestamp_utc_now
if TYPE_CHECKING:
    from .usuario import Usuario

class Pedido(SQLModel, table=True):
    __tablename__ = "pedidos"

    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuarios.id")
    total: Decimal = Field(max_digits=10, decimal_places=2)
    status: str = Field(max_length=50)
    criado_em: datetime = Field(default_factory=get_timestamp_utc_now)

    usuario: "Usuario" = Relationship(back_populates="pedidos")