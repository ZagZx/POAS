from fastapi import (
    APIRouter, 
    HTTPException,
    status
)

from database import SessionDep
from models import Avaliacao
from schemas.avaliacao import (
    AvaliacaoRead,
    AvaliacaoUpdate
)


avaliacao_router = APIRouter(prefix="/avaliacoes", tags=["Avaliação"])

@avaliacao_router.get("/{avaliacao_id}", response_model=AvaliacaoRead)
def buscar_avaliacao(avaliacao_id: int, session: SessionDep):
    avaliacao: Avaliacao = session.get(Avaliacao, avaliacao_id)
    if not avaliacao:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Avaliação não encontrada")
    
    return avaliacao


@avaliacao_router.patch("/{avaliacao_id}", response_model=AvaliacaoRead)
def atualizar_avaliacao(avaliacao_id: int, avaliacao_json: AvaliacaoUpdate, session: SessionDep):    
    avaliacao = session.get(Avaliacao, avaliacao_id)
    if not avaliacao:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Avaliação não encontrada")
    

    if avaliacao_json.nota:
        avaliacao.nota = avaliacao_json.nota
    if avaliacao_json.comentario:
        avaliacao.comentario = avaliacao_json.comentario

    try: 
        session.commit()
        session.refresh(avaliacao)
        
        return avaliacao
    except Exception as e:
        print(e)
        session.rollback()

        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Erro ao atualizar avaliação")


@avaliacao_router.delete("/{avaliacao_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_avaliacao(avaliacao_id: int, session: SessionDep):
    avaliacao = session.get(Avaliacao, avaliacao_id)
    if not avaliacao:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Avaliação não encontrada")
   
    session.delete(avaliacao)

    try:
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()

        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Erro ao deletar avaliação")
