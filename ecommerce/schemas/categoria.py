from sqlmodel import Field 
from typing import Optional
from decimal import Decimal
from datetime import datetime

from .base import BaseModel


class CategoriaCreate(BaseModel):
    nome: str = Field(max_length=100)

class CategoriaUpdate(BaseModel):
    nome: Optional[str] = Field(default=None, max_length=100)

class CategoriaRead(BaseModel):
    id: int
    nome: str
