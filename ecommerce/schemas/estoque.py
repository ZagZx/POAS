from sqlmodel import Field 
from typing import Optional
from datetime import datetime

from .base import BaseModel


class EstoqueCreate(BaseModel):
    produto_id: int
    quantidade: int

class EstoqueUpdate(BaseModel):
    quantidade: Optional[int] = Field(default=None)

class EstoqueRead(BaseModel):
    id: int
    produto_id: int
    quantidade: int
    atualizado_em: datetime