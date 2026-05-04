from typing import Optional
from sqlmodel import SQLModel, Field


class Papel(SQLModel, table=True):
    __tablename__ = "papeis"

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(max_length=50, unique=True)


class PapelCreate(SQLModel):
    nome: str = Field(max_length=50)

class PapelUpdate(SQLModel):
    nome: Optional[str] = Field(default=None, max_length=50)

class PapelRead(SQLModel):
    id: int
    nome: str