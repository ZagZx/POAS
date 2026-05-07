from fastapi import (
    APIRouter, 
    HTTPException,
    status
)

from database import SessionDep
from models import Endereco
from schemas.endereco import (
    EnderecoRead,
    EnderecoUpdate
)


endereco_router = APIRouter(prefix="/enderecos", tags=["Endereço"])

@endereco_router.get("/{endereco_id}", response_model=EnderecoRead)
def buscar_endereco(endereco_id: int, session: SessionDep):
    endereco: Endereco = session.get(Endereco, endereco_id)

    if not endereco:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Endereço não encontrado")
    
    return endereco


@endereco_router.patch("/{endereco_id}", response_model=EnderecoRead)
def atualizar_endereco(endereco_id: int, endereco_json: EnderecoUpdate, session: SessionDep):    
    endereco = session.get(Endereco, endereco_id)
    if not endereco:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Endereço não encontrado")
    

    if endereco_json.rua:
        endereco.rua = endereco_json.rua
    if endereco_json.cidade:
        endereco.cidade = endereco_json.cidade
    if endereco_json.estado:
        endereco.estado = endereco_json.estado
    if endereco_json.cep:
        endereco.cep = endereco_json.cep

    try: 
        session.commit()
        session.refresh(endereco)
        
        return endereco
    except Exception as e:
        print(e)
        session.rollback()

        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Erro ao atualizar endereço")


@endereco_router.delete("/{endereco_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_endereco(endereco_id: int, session: SessionDep):
    endereco = session.get(Endereco, endereco_id)
    if not endereco:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Endereço não encontrado")
   
    session.delete(endereco)

    try:
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()

        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Erro ao deletar endereço")
