from sqlmodel import Field 
from typing import Optional
from decimal import Decimal
from datetime import datetime

from .base import BaseModel


class PagamentoCreate(BaseModel):
    pedido_id: int
    valor: Decimal = Field(max_digits=10, decimal_places=2)
    metodo: str = Field(max_length=50)
    status: str = Field(max_length=50)
    pago_em: Optional[datetime] = Field(default=None)

class PagamentoUpdate(BaseModel):
    # pedido_id: Optional[int]
    valor: Optional[Decimal] = Field(default=None, max_digits=10, decimal_places=2)
    metodo: Optional[str] = Field(default=None, max_length=50)
    status: Optional[str] = Field(default=None, max_length=50)
    pago_em: Optional[datetime] = Field(default=None)

class PagamentoRead(BaseModel):
    id: int
    pedido_id: int
    valor: Decimal
    metodo: str
    status: str
    pago_em: Optional[datetime]