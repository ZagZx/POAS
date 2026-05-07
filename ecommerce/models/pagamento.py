from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from decimal import Decimal
from datetime import datetime

if TYPE_CHECKING:
    from .pedido import Pedido

class Pagamento(SQLModel, table=True):
    __tablename__ = "pagamentos"

    id: Optional[int] = Field(default=None, primary_key=True)
    pedido_id: int = Field(foreign_key="pedidos.id")
    valor: Decimal = Field(max_digits=10, decimal_places=2)
    metodo: str = Field(max_length=50)
    status: str = Field(max_length=50)
    pago_em: Optional[datetime] = Field(default=None)

    pedido: "Pedido" = Relationship(back_populates="pagamentos")