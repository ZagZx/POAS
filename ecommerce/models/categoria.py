from sqlmodel import SQLModel, Field
from typing import Optional


class Categoria(SQLModel, table=True):
    __tablename__ = "categorias"

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(max_length=100, unique=True)