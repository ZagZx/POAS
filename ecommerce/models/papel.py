from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

from .usuario_papel import UsuarioPapel
if TYPE_CHECKING:
    from .usuario import Usuario


class Papel(SQLModel, table=True):
    __tablename__ = "papeis"

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(max_length=50, unique=True)

    usuarios: list["Usuario"] = Relationship(back_populates="papeis", link_model=UsuarioPapel)