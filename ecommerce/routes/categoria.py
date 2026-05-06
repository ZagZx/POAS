from fastapi import (
    APIRouter, 
    status, 
    HTTPException
)
from sqlmodel import select

from database import SessionDep
from models import Categoria
from schemas.categoria import (
    CategoriaCreate,
    CategoriaRead,
    CategoriaUpdate
)


categoria_router = APIRouter(prefix="/categorias", tags=["Categoria"])

@categoria_router.get("", response_model=list[CategoriaRead])
def listar_categorias(session: SessionDep):
    categorias = session.exec(
        select(Categoria)
    ).all()

    return categorias


@categoria_router.get("/{categoria_id}", response_model=CategoriaRead)
def buscar_categoria(categoria_id: int, session: SessionDep):
    categoria: Categoria = session.get(Categoria, categoria_id)

    if not categoria:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Categoria não encontrada")
    
    return categoria


@categoria_router.post("", response_model=CategoriaRead, status_code=status.HTTP_201_CREATED)
def criar_categoria(categoria_json: CategoriaCreate, session: SessionDep):
    categoria_existente = session.exec(
        select(Categoria).where(Categoria.nome == categoria_json.nome)
    ).first()

    if categoria_existente:
        if categoria_existente.nome == categoria_json.nome:
            raise HTTPException(status.HTTP_409_CONFLICT, "Já existe uma categoria com esse nome")


    novo_categoria = Categoria(
        nome=categoria_json.nome
    )

    session.add(novo_categoria)

    try:
        session.commit()

        return novo_categoria
    except Exception as e:
        print(e)
        session.rollback()
        
        return HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Erro ao criar categoria")


@categoria_router.patch("/{categoria_id}", response_model=CategoriaRead)
def atualizar_categoria(categoria_id: int, categoria_json: CategoriaUpdate, session: SessionDep):    
    categoria_existente = session.exec(
        select(Categoria).where(Categoria.nome == categoria_json.nome)
    ).first()

    if categoria_existente:
        if categoria_existente.nome == categoria_json.nome:
            raise HTTPException(status.HTTP_409_CONFLICT, "Já existe uma categoria com esse nome")
 
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    
    if categoria_json.nome:
        categoria.nome = categoria_json.nome

    try: 
        session.commit()
        session.refresh(categoria)
    except Exception as e:
        print(e)
        session.rollback()

        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Erro ao atualizar categoria")

    return categoria


@categoria_router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_categoria(categoria_id: int, session: SessionDep):
    categoria = session.get(Categoria, categoria_id)

    if not categoria:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Categoria não encontrada")
   
    session.delete(categoria)

    try:
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()