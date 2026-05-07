from fastapi import (
    APIRouter, 
    HTTPException,
    status
)
from sqlmodel import select

from database import SessionDep
from models import Produto, Avaliacao, Estoque
from schemas.produto import (
    ProdutoCreate,
    ProdutoRead,
    ProdutoUpdate
)
from schemas.avaliacao import (
    AvaliacaoRead, 
    AvaliacaoCreate
)
from schemas.estoque import (
    EstoqueRead,
    EstoqueUpdate
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
    if produto_json.preco < 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Preço não pode ser negativo")

    novo_produto = Produto(
        nome=produto_json.nome,
        descricao=produto_json.descricao,
        preco=produto_json.preco,
    )
    session.add(novo_produto)

    if produto_json.estoque < 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Estoque não pode ser negativo")
    estoque_produto = Estoque(
        produto=novo_produto,
        quantidade=produto_json.estoque
    )
    session.add(estoque_produto)

    try:
        session.commit()

        return novo_produto
    except Exception as e:
        print(e)
        session.rollback()
        
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Erro ao criar produto")


@produto_router.patch("/{produto_id}", response_model=ProdutoRead)
def atualizar_produto(produto_id: int, produto_json: ProdutoUpdate, session: SessionDep):    
    produto = session.get(Produto, produto_id)
    if not produto:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Produto não encontrado")
    
    if produto_json.nome:
        produto.nome = produto_json.nome
    if produto_json.descricao:
        produto.descricao = produto_json.descricao
    if produto_json.preco:
        produto.preco = produto_json.preco

    try: 
        session.commit()
        session.refresh(produto)
        
        return produto
    except Exception as e:
        print(e)
        session.rollback()

        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Erro ao atualizar produto")


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


@produto_router.get("/{produto_id}/avaliacoes", response_model=list[AvaliacaoRead])
def listar_avaliacoes_produto(produto_id: int, session: SessionDep):
    produto = session.get(Produto, produto_id)
    if not produto:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Produto não encontrado")
    
    produto_avaliacoes = produto.avaliacoes

    return produto_avaliacoes

@produto_router.post("/{produto_id}/avaliacoes", response_model=AvaliacaoRead, status_code=status.HTTP_201_CREATED)
def adicionar_avaliacao_produto(produto_id: int, avaliacao_json: AvaliacaoCreate, session: SessionDep):
    produto = session.get(Produto, produto_id)
    if not produto:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Produto não encontrado")
    
    novo_avaliacao = Avaliacao(
        produto_id=produto_id,
        usuario_id=avaliacao_json.usuario_id,
        nota=avaliacao_json.nota,
        comentario=avaliacao_json.comentario
    )

    session.add(novo_avaliacao)
    
    try:
        session.commit()
        
        return novo_avaliacao 
    except Exception as e:
        print(e)
        session.rollback()

        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Erro ao criar avaliação")
    
@produto_router.get("/{produto_id}/estoque", response_model=EstoqueRead)
def ver_estoque_produto(produto_id: int, session: SessionDep):
    produto = session.get(Produto, produto_id)
    if not produto:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Produto não encontrado")
    
    produto_estoque = produto.estoque

    return produto_estoque


@produto_router.patch("/{produto_id}/estoque", response_model=EstoqueRead)
def atualizar_estoque_produto(produto_id: int, estoque_json: EstoqueUpdate, session: SessionDep):    
    produto = session.get(Produto, produto_id)
    if not produto:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Produto não encontrado")
    if estoque_json.quantidade < 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Estoque não pode ser negativo")

    if estoque_json.quantidade:
        produto.estoque.quantidade = estoque_json.quantidade

    try: 
        session.commit()
        session.refresh(produto)
        
        return produto.estoque
    except Exception as e:
        print(e)
        session.rollback()

        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Erro ao atualizar produto")
