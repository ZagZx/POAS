# 11 rotas
# cadastro de usuario
# busca de livro
# emprestimo (data de entrega)
# rota para listar livros com emprestimo em atraso

from fastapi import FastAPI
from uuid import UUID

from models import Usuario, Livro, Emprestimo


usuarios: list[Usuario] = []
livros: list[Livro] = []
emprestimos: list[Emprestimo] = []

app = FastAPI()

@app.get("/livro")
def listar_livros():
    # nao msotra livros emprestados
    livros_disponiveis = []

    for livro in livros:
        if livro.status == "Disponível":
            livros_disponiveis.append(livro)

    return livros_disponiveis


@app.post("/livro")
def cadastrar_livro(livro: Livro):
    if livro: 
        livros.append(livro)
        return livro
    
@app.delete("/livro/<id>")
def deletar_livro(id: UUID):
    for livro in livros:
        if livro.id == id:
            livros.remove(livro)
            return {"mensagem": "Livro deletado"}
        
    return {"mensagem": "Livro não encontrado"}

@app.put("/livro/<id>")
def atualizar_livro(id: UUID, livro: Livro):
    for livro in livros:
        if livro.id == id:
            livro = livro
            return livro
        
@app.get("/usuario")
def listar_usuarios():
    return usuarios

@app.post("/usuario")
def cadastrar_usuario(usuario: Usuario):
    if usuario: 
        usuarios.append(usuario)
        return usuario

@app.delete("/usuario/<id>")
def deletar_usuario(id: UUID):
    for usuario in usuarios:
        if usuario.id == id:
            usuarios.remove(usuario)
            return {"mensagem": "Usuário deletado"}
        
    return {"mensagem": "Usuário não encontrado"}
    