#uvicorn app:app
from fastapi import FastAPI, status, HTTPException
from sqlmodel import select

from database import SessionDep
from utils import (
    generate_password_hash,
    check_password_hash
)
from models import (
    Usuario, 
    UsuarioCreate, 
    UsuarioRead
)


app = FastAPI()

@app.get("/usuarios", response_model=list[UsuarioRead])
def listar_usuarios(session: SessionDep):
    usuarios = session.exec(
        select(Usuario)
    ).all()

    return usuarios

@app.post("/usuarios", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
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
        
        return HTTPException(500, "Erro ao criar usuário")