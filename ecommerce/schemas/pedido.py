from sqlmodel import Field 
from typing import Optional
from decimal import Decimal
from datetime import datetime

from .base import BaseModel


class PedidoCreate(BaseModel):
    usuario_id: int
    total: Decimal = Field(max_digits=10, decimal_places=2)
    status: str = Field(max_length=50)

class PedidoUpdate(BaseModel):
    # usuario_id: Optional[int]
    total: Optional[Decimal] = Field(max_digits=10, decimal_places=2)
    status: Optional[str] = Field(max_length=50)

class PedidoRead(BaseModel):
    id: int
    usuario_id: int 
    total: Decimal
    status: str
    criado_em: datetime