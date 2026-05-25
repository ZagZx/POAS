from .base import BaseModel


class ItemPedidoCreate(BaseModel):
    produto_id: int
    quantidade: int

# class ItemPedidoUpdate(BaseModel):
#     produto_id: int
#     quantidade: int

# class ItemPedidoRead(BaseModel):
#     pass