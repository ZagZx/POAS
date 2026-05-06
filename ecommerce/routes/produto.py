from fastapi import (
    APIRouter, 
    status, 
    HTTPException
)
from sqlmodel import select

from database import SessionDep
from models import Produto
from schemas.produto import (
    ProdutoCreate,
    ProdutoRead,
    ProdutoUpdate
)


produto_router = APIRouter(prefix="/produtos", tags=["Produto"])

@produto_router.get("", response_model=list[ProdutoRead])
def listar_produtos(session: SessionDep):
    produtos = session.exec(
        select(Produto)
    ).all()

    return produtos


@produto_router.get("/{produto_id}", response_model=ProdutoRead)
def buscar_produto(produto_id: int, session: SessionDep):
    produto: Produto = session.get(Produto, produto_id)

    if not produto:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Produto não encontrado")
    
    return produto


@produto_router.post("", response_model=ProdutoRead, status_code=status.HTTP_201_CREATED)
def criar_produto(produto_json: ProdutoCreate, session: SessionDep):
    novo_produto = Produto(
        nome=produto_json.nome,
        descricao=produto_json.descricao,
        preco=produto_json.preco,

    )

    session.add(novo_produto)

    try:
        session.commit()

        return novo_produto
    except Exception as e:
        print(e)
        session.rollback()
        
        return HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Erro ao criar produto")


@produto_router.patch("/{produto_id}", response_model=ProdutoRead)
def atualizar_produto(produto_id: int, produto_json: ProdutoUpdate, session: SessionDep):    
    produto = session.get(Produto, produto_id)
    if not produto:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    
    if produto_json.nome:
        produto.nome = produto_json.nome
    if produto_json.descricao:
        produto.descricao = produto_json.descricao
    if produto_json.preco:
        produto.preco = produto_json.preco

    try: 
        session.commit()
        session.refresh(produto)
    except Exception as e:
        print(e)
        session.rollback()

        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Erro ao atualizar produto")

    return produto


@produto_router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(produto_id: int, session: SessionDep):
    produto = session.get(Produto, produto_id)

    if not produto:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Produto não encontrado")
   
    session.delete(produto)

    try:
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()