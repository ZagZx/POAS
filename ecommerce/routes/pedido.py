from fastapi import (
    APIRouter, 
    HTTPException,
    status
)
from sqlmodel import select

from database import SessionDep
from models import Pedido, Usuario, Pagamento, Produto, ItemPedido
from schemas.pedido import (
    PedidoCreate,
    PedidoRead,
    PedidoUpdate
)
from schemas.pagamento import (
    PagamentoCreate,
    PagamentoRead,
)
from schemas.item_pedido import (
    ItemPedidoCreate,
    ItemPedidoRead,
)


pedido_router = APIRouter(prefix="/pedidos", tags=["Pedido"])

@pedido_router.get("", response_model=list[PedidoRead])
def listar_pedidos(session: SessionDep):
    pedidos = session.exec(
        select(Pedido)
    ).all()

    return pedidos


@pedido_router.get("/{pedido_id}", response_model=PedidoRead)
def buscar_pedido(pedido_id: int, session: SessionDep):
    pedido: Pedido = session.get(Pedido, pedido_id)

    if not pedido:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Pedido não encontrado")
    
    return pedido


@pedido_router.post("", response_model=PedidoRead, status_code=status.HTTP_201_CREATED)
def criar_pedido(pedido_json: PedidoCreate, session: SessionDep):
    if not session.get(Usuario, pedido_json.usuario_id):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Usuário {pedido_json.usuario_id} não encontrado")


    pedido = Pedido(
        usuario_id=pedido_json.usuario_id,
        status=pedido_json.status
    )
    session.add(pedido)

    total = 0
    for item in pedido_json.itens:
        produto = session.get(Produto, item.produto_id)
        if not produto:
            # trocar para mostrar todos os ids não encontrados igual nos papeis?
            raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Produto de {item.produto_id} não encontrado")
        if produto.estoque.quantidade == 0:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Produto {item.produto_id} está fora de estoque")
        elif item.quantidade > produto.estoque.quantidade:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Produto {item.produto_id} não possui {item.quantidade} unidades no estoque, restam apenas {produto.estoque.quantidade} unidades")

        item_pedido = ItemPedido(
            produto_id=produto.id,
            pedido_id=pedido.id,
            quantidade=item.quantidade,
            preco=produto.preco
        )
        session.add(item_pedido)

        produto.estoque.quantidade -= item.quantidade
        total += produto.preco * item.quantidade
    pedido.total = total
    try:
        session.commit()

        return pedido
    except Exception as e:
        print(e)
        session.rollback()
        
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Erro ao criar pedido")

@pedido_router.get("/{pedido_id}/itens", response_model=list[ItemPedidoRead])
def listar_itens_pedido(pedido_id: int, session: SessionDep):
    pedido = session.get(Pedido, pedido_id)
    if not pedido:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Pedido não encontrado")

    response: list[ItemPedidoRead] = []
    for produto in pedido.itens:
        response.append(
            ItemPedidoRead.from_pedido_and_produto(pedido, produto, session)
        )

    return response


@pedido_router.patch("/{pedido_id}/status", response_model=PedidoRead)
def atualizar_status_pedido(pedido_id: int, pedido_json: PedidoUpdate, session: SessionDep):    
    pedido = session.get(Pedido, pedido_id)
    if not pedido:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Pedido não encontrado")

    if pedido_json.status:
        pedido.status = pedido_json.status

    try: 
        session.commit()
        session.refresh(pedido)
        
        return pedido
    except Exception as e:
        print(e)
        session.rollback()

        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Erro ao atualizar pedido")



@pedido_router.delete("/{pedido_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_pedido(pedido_id: int, session: SessionDep):
    pedido = session.get(Pedido, pedido_id)

    if not pedido:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Pedido não encontrado")
   
    session.delete(pedido)

    try:
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()

        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Erro ao deletar pedido")
    

@pedido_router.get("/{pedido_id}/pagamentos", response_model=list[PagamentoRead])
def listar_pagamentos_pedido(pedido_id: int, session: SessionDep):
    pedido: Pedido = session.get(Pedido, pedido_id)

    if not pedido:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Pedido não encontrado")
    
    pedido_papeis = pedido.pagamentos

    return pedido_papeis


@pedido_router.post("/{pedido_id}/pagamentos", response_model=PagamentoRead, status_code=status.HTTP_201_CREATED)
def criar_pagamento_pedido(pedido_id: int, pagamento_json: PagamentoCreate, session: SessionDep):
    if not session.get(Pedido, pedido_id):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Pedido {pedido_id} não encontrado")

    novo_pagamento = Pagamento(
        pedido_id=pagamento_json.pedido_id,
        valor=pagamento_json.valor,
        metodo=pagamento_json.metodo,
        status=pagamento_json.status,
        pago_em=pagamento_json.pago_em,
    )

    session.add(novo_pagamento)

    try:
        session.commit()

        return novo_pagamento
    except Exception as e:
        print(e)
        session.rollback()
        
        return HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Erro ao criar pagamento")