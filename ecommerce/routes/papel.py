from fastapi import (
    APIRouter, 
    status, 
    HTTPException
)
from sqlmodel import select

from database import SessionDep
from models import Papel
from schemas.papel import (
    PapelCreate,
    PapelRead,
    PapelUpdate
)


papel_router = APIRouter(prefix="/papeis", tags=["Papel"])

@papel_router.get("", response_model=list[PapelRead])
def listar_papeis(session: SessionDep):
    papeis = session.exec(
        select(Papel)
    ).all()

    return papeis


@papel_router.get("/{papel_id}", response_model=PapelRead)
def buscar_papel(papel_id: int, session: SessionDep):
    papel: Papel = session.get(Papel, papel_id)

    if not papel:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Papel não encontrado")
    
    return papel


@papel_router.post("", response_model=PapelRead, status_code=status.HTTP_201_CREATED)
def criar_papel(papel_json: PapelCreate, session: SessionDep):
    papel_existente = session.exec(
        select(Papel).where(Papel.nome == papel_json.nome)
    ).first()

    if papel_existente:
        if papel_existente.nome == papel_json.nome:
            raise HTTPException(status.HTTP_409_CONFLICT, "Já existe um papel com esse nome")

    novo_papel = Papel(
        nome=papel_json.nome
    )

    session.add(novo_papel)

    try:
        session.commit()

        return novo_papel
    except Exception as e:
        print(e)
        session.rollback()
        
        return HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Erro ao criar usuário")


@papel_router.patch("/{papel_id}", response_model=PapelRead)
def atualizar_papel(papel_id: int, papel_json: PapelUpdate, session: SessionDep):
    papel = session.get(Papel, papel_id)
    if not papel:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Papel não encontrado")
    
    papel_existente = session.exec(
        select(Papel).where(Papel.nome == papel_json.nome)
    ).first()
    if papel_existente:
        if papel_existente.nome == papel_json.nome:
            raise HTTPException(status.HTTP_409_CONFLICT, "Já existe um papel com esse nome")
        
    
    if papel_json.nome:
        papel.nome = papel_json.nome


    try: 
        session.commit()
        session.refresh(papel)

        return papel

    except Exception as e:
        print(e)
        session.rollback()

        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Erro ao atualizar papel")


@papel_router.delete("/{papel_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_papel(papel_id: int, session: SessionDep):
    papel = session.get(Papel, papel_id)

    if not papel:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Papel não encontrado")
   
    session.delete(papel)

    try:
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()