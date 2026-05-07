from sqlmodel import Field 
from typing import Optional

from .base import BaseModel


class EnderecoCreate(BaseModel):
    # não tem usuario_id porque tá na rota
    # usuario_id: int
    rua: str = Field(max_length=150)
    cidade: str = Field(max_length=100)
    estado: str = Field(max_length=100)
    cep: str = Field(max_length=20)

class EnderecoUpdate(BaseModel):
    rua: Optional[str] = Field(default=None, max_length=150)
    cidade: Optional[str] = Field(default=None, max_length=100)
    estado: Optional[str] = Field(default=None, max_length=100)
    cep: Optional[str] = Field(default=None, max_length=20)

class EnderecoRead(BaseModel):
    id: int
    usuario_id: int
    rua: str
    cidade: str
    estado: str 
    cep: str