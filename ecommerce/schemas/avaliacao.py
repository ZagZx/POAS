from sqlmodel import Field 
from typing import Optional
from datetime import datetime

from .base import BaseModel


class AvaliacaoCreate(BaseModel):
    usuario_id: int
    nota: int
    comentario: Optional[str] = Field(default=None)

class AvaliacaoUpdate(BaseModel):
    nota: Optional[int]
    comentario: Optional[str]

class AvaliacaoRead(BaseModel):
    id: int
    usuario_id: int
    produto_id: int
    nota: int
    comentario: Optional[str] = Field(default=None)
    criado_em: datetime