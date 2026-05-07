from fastapi import (
    APIRouter, 
    status, 
    HTTPException
)
from sqlmodel import select

from database import SessionDep
from models import Pedido, Pagamento
from schemas.pagamento import (
    PagamentoCreate,
    PagamentoRead,
    PagamentoUpdate
)


pagamento_router = APIRouter(prefix="/pagamentos", tags=["Pagamento"])

# @pagamento_router.get("", response_model=list[PagamentoRead])
# def listar_pagamentos(session: SessionDep):
#     pagamentos = session.exec(
#         select(Pagamento)
#     ).all()

#     return pagamentos


@pagamento_router.get("/{pagamento_id}", response_model=PagamentoRead)
def buscar_pagamento(pagamento_id: int, session: SessionDep):
    pagamento: Pagamento = session.get(Pagamento, pagamento_id)

    if not pagamento:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Pagamento não encontrado")
    
    return pagamento


@pagamento_router.patch("/{pagamento_id}", response_model=PagamentoRead)
def atualizar_pagamento(pagamento_id: int, pagamento_json: PagamentoUpdate, session: SessionDep):    
    pagamento = session.get(Pagamento, pagamento_id)
    if not pagamento:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Pagamento não encontrado")
    
    # if not session.get(Pedido, pagamento_json.pedido_id):
    #     raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Pedido {pagamento_json.pedido_id} não encontrado")

    # if pagamento_json.pedido_id:
    #     pagamento.pedido_id = pagamento_json.pedido_id
    if pagamento_json.valor:
        pagamento.valor = pagamento_json.valor
    if pagamento_json.metodo:
        pagamento.metodo = pagamento_json.metodo
    if pagamento_json.status:
        pagamento.status = pagamento_json.status
    if pagamento_json.pago_em:
        pagamento.pago_em = pagamento_json.pago_em

    try: 
        session.commit()
        session.refresh(pagamento)
    except Exception as e:
        print(e)
        session.rollback()

        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Erro ao atualizar pagamento")

    return pagamento


@pagamento_router.delete("/{pagamento_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_pagamento(pagamento_id: int, session: SessionDep):
    pagamento = session.get(Pagamento, pagamento_id)

    if not pagamento:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Pagamento não encontrado")
   
    session.delete(pagamento)

    try:
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()