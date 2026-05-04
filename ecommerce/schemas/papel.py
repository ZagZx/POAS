from sqlmodel import SQLModel, Field
from typing import Optional


class PapelCreate(SQLModel):
    nome: str = Field(max_length=50)

class PapelUpdate(SQLModel):
    nome: Optional[str] = Field(default=None, max_length=50)

class PapelRead(SQLModel):
    id: int
    nome: str