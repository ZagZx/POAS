from typing import Optional
from sqlmodel import SQLModel, Field

class UsuarioPapel(SQLModel, table=True):
    __tablename__ = "usuario_papeis"

    usuario_id: Optional[int] = Field(default=None, foreign_key="usuarios.id", primary_key=True)
    papel_id: Optional[int] = Field(default=None, foreign_key="papeis.id", primary_key=True)