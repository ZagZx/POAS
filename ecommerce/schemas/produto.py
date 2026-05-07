from sqlmodel import Field 
from typing import Optional
from decimal import Decimal
from datetime import datetime

from .base import BaseModel


class ProdutoCreate(BaseModel):
    nome: str = Field(max_length=150)
    descricao: str 
    preco: Decimal = Field(max_digits=10, decimal_places=2)
    estoque: int

class ProdutoUpdate(BaseModel):
    nome: Optional[str] = Field(default=None, max_length=150)
    descricao: Optional[str] = Field(default=None)
    preco: Optional[Decimal] = Field(default=None, max_digits=10, decimal_places=2)

class ProdutoRead(BaseModel):
    id: int
    nome: str
    descricao: str 
    preco: Decimal
    criado_em: datetime