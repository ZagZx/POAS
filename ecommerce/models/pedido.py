from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from decimal import Decimal
from datetime import datetime

from utils import get_timestamp_utc_now
from .item_pedido import ItemPedido
if TYPE_CHECKING:
    from .usuario import Usuario
    from .pagamento import Pagamento
    from .produto import Produto

class Pedido(SQLModel, table=True):
    __tablename__ = "pedidos"

    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuarios.id")
    total: Decimal = Field(max_digits=10, decimal_places=2)
    status: str = Field(max_length=50)
    criado_em: datetime = Field(default_factory=get_timestamp_utc_now)

    usuario: "Usuario" = Relationship(back_populates="pedidos")
    pagamentos: list["Pagamento"] = Relationship(back_populates="pedido")
    itens: list["Produto"] = Relationship(back_populates="pedidos", link_model=ItemPedido)
