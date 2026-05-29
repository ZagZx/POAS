from sqlmodel import select
from decimal import Decimal

from database import SessionDep
from models import Pedido, ItemPedido, Produto
from .base import BaseModel


class ItemPedidoCreate(BaseModel):
    produto_id: int
    quantidade: int

# class ItemPedidoUpdate(BaseModel):
#     produto_id: int
#     quantidade: int

class ItemPedidoRead(BaseModel):
    produto_id: int
    nome: str
    descricao: str
    preco: Decimal
    quantidade: int


    @classmethod
    def from_pedido_and_produto(cls, pedido: Pedido, produto: Produto, session: SessionDep):
        item_pedido = session.scalar(
            select(ItemPedido).where(
                ItemPedido.pedido_id == pedido.id,
                ItemPedido.produto_id == produto.id
            )
        )

        return cls( 
            produto_id = produto.id,
            nome = produto.nome,
            descricao = produto.descricao,
            preco = item_pedido.preco,
            quantidade = item_pedido.quantidade
        )