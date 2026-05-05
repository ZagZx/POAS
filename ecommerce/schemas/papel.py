from sqlmodel import Field
from typing import Optional

from .base import BaseModel


class PapelCreate(BaseModel):
    nome: str = Field(max_length=50)

class PapelUpdate(BaseModel):
    nome: Optional[str] = Field(default=None, max_length=50)

class PapelRead(BaseModel):
    id: int
    nome: str