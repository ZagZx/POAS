from fastapi import (
    APIRouter, 
    status, 
    HTTPException
)
from sqlmodel import select

from database import SessionDep
from utils import generate_password_hash, check_password_hash
from models import Usuario
from schemas.usuario import (
    UsuarioCreate,
    UsuarioRead,
    UsuarioUpdate
)
from schemas.papel import (
    PapelCreate,
    PapelRead,
    PapelUpdate
)


usuario_router = APIRouter(prefix="/usuarios", tags=["Usuário"])

@usuario_router.get("", response_model=list[UsuarioRead])
def listar_usuarios(session: SessionDep):
    usuarios = session.exec(
        select(Usuario)
    ).all()

    return usuarios

@usuario_router.get("/{usuario_id}/papeis", response_model=list[PapelRead])
def listar_papeis_usuario(usuario_id: int, session: SessionDep):
    usuario = session.get(Usuario, usuario_id)

    if not usuario:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuário não encontrado")
    
    usuario_papeis = usuario.papeis

    return usuario_papeis 

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
        
        return HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Erro ao criar usuário")

@usuario_router.patch("/{usuario_id}", response_model=UsuarioRead)
def atualizar_usuario(usuario_id: int, usuario_json: UsuarioUpdate, session: SessionDep):
    usuario_existente = session.exec(
        select(Usuario).where((Usuario.email == usuario_json.email) | (Usuario.nome == usuario_json.nome))
    ).first()

    if usuario_existente:
        if usuario_existente.nome == usuario_json.nome:
            raise HTTPException(status.HTTP_409_CONFLICT, "Já existe um usuário com esse nome")
        if usuario_existente.email == usuario_json.email:
            raise HTTPException(status.HTTP_409_CONFLICT, "Já existe um usuário com esse email")
        
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    
    if usuario_json.nome:
        usuario.nome = usuario_json.nome
    if usuario_json.email:
        usuario.email = usuario_json.email
    if usuario_json.senha:
        usuario.senha_hash = generate_password_hash(usuario_json.senha)

    try: 
        session.commit()
        session.refresh(usuario)
    except Exception as e:
        print(e)
        session.rollback()

        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Erro ao atualizar usuário")

    return usuario

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