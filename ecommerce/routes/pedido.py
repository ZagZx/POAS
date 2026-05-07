from fastapi import (
    APIRouter, 
    HTTPException,
    status
)
from sqlmodel import select

from database import SessionDep
from models import Pedido, Usuario, Pagamento
from schemas.pedido import (
    PedidoCreate,
    PedidoRead,
    PedidoUpdate
)
from schemas.pagamento import (
    PagamentoCreate,
    PagamentoRead,
    PagamentoUpdate
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

    novo_pedido = Pedido(
        usuario_id=pedido_json.usuario_id,
        total=pedido_json.total,
        status=pedido_json.status
    )

    session.add(novo_pedido)

    try:
        session.commit()

        return novo_pedido
    except Exception as e:
        print(e)
        session.rollback()
        
        return HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Erro ao criar pedido")


@pedido_router.patch("/{pedido_id}", response_model=PedidoRead)
def atualizar_pedido(pedido_id: int, pedido_json: PedidoUpdate, session: SessionDep):    
    pedido = session.get(Pedido, pedido_id)
    if not pedido:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Pedido não encontrado")
    
    # if not session.get(Usuario, pedido_json.usuario_id):
    #     raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Usuário {pedido_json.usuario_id} não encontrado")

    # if pedido_json.usuario_id:
    #     pedido.usuario_id = pedido_json.usuario_id
    if pedido_json.total:
        pedido.total = pedido_json.total
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