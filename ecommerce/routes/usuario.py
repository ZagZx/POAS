from fastapi import (
    APIRouter, 
    HTTPException,
    status
)
from sqlmodel import select, col

from database import SessionDep
from utils import generate_password_hash
from models import Usuario, Papel, Endereco
from schemas.usuario import (
    UsuarioCreate,
    UsuarioRead,
    UsuarioUpdate
)
from schemas.endereco import (
    EnderecoCreate,
    EnderecoRead
)
from schemas.papel import PapelRead
from schemas.avaliacao import AvaliacaoRead
from schemas.usuario_papeis import UsuarioPapeisRequest


usuario_router = APIRouter(prefix="/usuarios", tags=["Usuário"])

@usuario_router.get("", response_model=list[UsuarioRead])
def listar_usuarios(session: SessionDep):
    usuarios = session.exec(
        select(Usuario)
    ).all()

    return usuarios


@usuario_router.get("/{usuario_id}", response_model=UsuarioRead)
def buscar_usuario(usuario_id: int, session: SessionDep):
    usuario: Usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuário não encontrado")
    
    return usuario


@usuario_router.post("", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario_json: UsuarioCreate, session: SessionDep):
    usuario_existente = session.exec(
        select(Usuario).where((Usuario.email == usuario_json.email) | (Usuario.nome == usuario_json.nome))
    ).first()
    if usuario_existente:
        if usuario_existente.nome == usuario_json.nome:
            raise HTTPException(status.HTTP_409_CONFLICT, "Já existe um usuário com esse nome")
        if usuario_existente.email == usuario_json.email:
            raise HTTPException(status.HTTP_409_CONFLICT, "Já existe um usuário com esse email")

    novo_usuario = Usuario(
        nome=usuario_json.nome,
        email=usuario_json.email,
        senha_hash=generate_password_hash(usuario_json.senha)
    )

    session.add(novo_usuario)

    try:
        session.commit()

        return novo_usuario
    except Exception as e:
        print(e)
        session.rollback()
        
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Erro ao criar usuário")


@usuario_router.patch("/{usuario_id}", response_model=UsuarioRead)
def atualizar_usuario(usuario_id: int, usuario_json: UsuarioUpdate, session: SessionDep):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuário não encontrado")
    
    usuario_existente = session.exec(
        select(Usuario).where((Usuario.email == usuario_json.email) | (Usuario.nome == usuario_json.nome))
    ).first()
    if usuario_existente:
        if usuario_existente.nome == usuario_json.nome:
            raise HTTPException(status.HTTP_409_CONFLICT, "Já existe um usuário com esse nome")
        if usuario_existente.email == usuario_json.email:
            raise HTTPException(status.HTTP_409_CONFLICT, "Já existe um usuário com esse email")
    
    if usuario_json.nome:
        usuario.nome = usuario_json.nome
    if usuario_json.email:
        usuario.email = usuario_json.email
    if usuario_json.senha:
        usuario.senha_hash = generate_password_hash(usuario_json.senha)

    try: 
        session.commit()
        session.refresh(usuario)
        
        return usuario
    except Exception as e:
        print(e)
        session.rollback()

        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Erro ao atualizar usuário")


@usuario_router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_usuario(usuario_id: int, session: SessionDep):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuário não encontrado")
   
    session.delete(usuario)

    try:
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()

        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Erro ao deletar usuário")
    

@usuario_router.get("/{usuario_id}/papeis", response_model=list[PapelRead])
def listar_papeis_usuario(usuario_id: int, session: SessionDep):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuário não encontrado")
    
    usuario_papeis = usuario.papeis

    return usuario_papeis 


@usuario_router.put("/{usuario_id}/papeis", response_model=list[PapelRead])
def atualizar_papeis_usuario(usuario_id: int, papeis_ids_json: UsuarioPapeisRequest, session: SessionDep):
    usuario: Usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuário não encontrado")
    
    papeis_ids = papeis_ids_json.papeis_ids
    
    papeis = session.exec(
        select(Papel).where(col(Papel.id).in_(papeis_ids))
    ).all()


    ids_encontrados = [] 
    for papel in papeis:
        ids_encontrados.append(papel.id)

    ids_nao_encontrados = []
    for papel_id in papeis_ids:
        if papel_id not in ids_encontrados:
            ids_nao_encontrados.append(papel_id)

    if ids_nao_encontrados:
        if len(ids_nao_encontrados) == 1:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, f"O papel de id {ids_nao_encontrados[0]} não foi encontrado portanto nenhuma alteração foi feita")
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Os papeis de ids {ids_nao_encontrados} não foram encontrados portanto nenhuma alteração foi feita")

    usuario.papeis = papeis

    try:
        session.commit()
        session.refresh(usuario)

        return usuario.papeis
    except Exception as e:
        print(e)
        session.rollback()

        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Erro ao atualizar os papeis do usuário")
    
@usuario_router.get("/{usuario_id}/enderecos", response_model=list[EnderecoRead])
def listar_enderecos_usuario(usuario_id: int, session: SessionDep):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuário não encontrado")
    
    usuario_enderecos = usuario.enderecos

    return usuario_enderecos

@usuario_router.post("/{usuario_id}/enderecos", response_model=EnderecoRead, status_code=status.HTTP_201_CREATED)
def adicionar_endereco_usuario(usuario_id: int, endereco_json: EnderecoCreate, session: SessionDep):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuário não encontrado")
    
    novo_endereco = Endereco(
        usuario_id=usuario_id,
        rua=endereco_json.rua,
        cidade=endereco_json.cidade,
        estado=endereco_json.estado,
        cep=endereco_json.cep,
    )

    try:
        session.add(novo_endereco)
        session.commit()
        
        return novo_endereco 
    except Exception as e:
        print(e)
        session.rollback()

        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Erro ao criar endereço")

@usuario_router.get("/{usuario_id}/avaliacoes", response_model=list[AvaliacaoRead])
def listar_avaliacoes_usuario(usuario_id: int, session: SessionDep):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuário não encontrado")
    
    usuario_avaliacoes = usuario.avaliacoes

    return usuario_avaliacoes