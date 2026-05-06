from sqlmodel import SQLModel, Field
from typing import Optional
from decimal import Decimal
from datetime import datetime

from utils import get_timestamp_utc_now


class Produto(SQLModel, table=True):
    __tablename__ = "produtos"

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(max_length=150)
    descricao: str 
    preco: Decimal = Field(max_digits=10, decimal_places=2)
    criado_em: datetime = Field(default_factory=get_timestamp_utc_now)