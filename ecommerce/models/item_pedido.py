from sqlmodel import SQLModel, Field
from typing import Optional
from decimal import Decimal

class ItemPedido(SQLModel, table=True):
    __tablename__ = "itens_pedido"

    id: Optional[int] = Field(default=None, primary_key=True)
    produto_id: int = Field(foreign_key="produtos.id")
    pedido_id: int = Field(foreign_key="pedidos.id")
    quantidade: int
    preco: Decimal = Field(max_digits=10, decimal_places=2)