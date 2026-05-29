from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from decimal import Decimal
from datetime import datetime

from utils import get_timestamp_utc_now
from .item_pedido import ItemPedido
if TYPE_CHECKING:
    from .avaliacao import Avaliacao
    from .estoque import Estoque
    from .pedido import Pedido


class Produto(SQLModel, table=True):
    __tablename__ = "produtos"

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(max_length=150)
    descricao: str 
    preco: Decimal = Field(max_digits=10, decimal_places=2)
    criado_em: datetime = Field(default_factory=get_timestamp_utc_now)

    avaliacoes: list["Avaliacao"] = Relationship(back_populates="produto")
    estoque: "Estoque" = Relationship(back_populates="produto")
    pedidos: list["Pedido"] = Relationship(back_populates="itens", link_model=ItemPedido)