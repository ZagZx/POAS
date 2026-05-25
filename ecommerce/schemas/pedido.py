from sqlmodel import Field 
from typing import Optional, TYPE_CHECKING
from decimal import Decimal
from datetime import datetime

from .base import BaseModel
from .item_pedido import ItemPedidoCreate
# if TYPE_CHECKING:
#     from .item_pedido import ItemPedidoCreate


class PedidoCreate(BaseModel):
    usuario_id: int
    status: str = Field(max_length=50)
    itens: list["ItemPedidoCreate"]
    # total: Decimal = Field(max_digits=10, decimal_places=2)

class PedidoUpdate(BaseModel):
    # usuario_id: Optional[int]
    # total: Optional[Decimal] = Field(max_digits=10, decimal_places=2)
    status: Optional[str] = Field(default=None, max_length=50)

class PedidoRead(BaseModel):
    id: int
    usuario_id: int 
    total: Decimal
    status: str
    criado_em: datetime