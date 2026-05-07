from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .usuario import Usuario

class Endereco(SQLModel, table=True):
    __tablename__ = "enderecos"

    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuarios.id")
    rua: str = Field(max_length=150)
    cidade: str = Field(max_length=100)
    estado: str = Field(max_length=100)
    cep: str = Field(max_length=20)

    usuario: "Usuario" = Relationship(back_populates="enderecos")