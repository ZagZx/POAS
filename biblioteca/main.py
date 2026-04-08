# 11 rotas
# cadastro de usuario
# busca de livro
# emprestimo (data de entrega)
# rota para listar livros com emprestimo em atraso

from fastapi import FastAPI
from uuid import UUID
from datetime import date

from models import Usuario, Livro, Emprestimo, LivroUpdate, UsuarioUpdate


usuarios: list[Usuario] = []
livros: list[Livro] = []
emprestimos: list[Emprestimo] = []

app = FastAPI()

@app.get("/livro")
def listar_livros():
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

@app.patch("/livro/<id>")
def atualizar_livro(id: UUID, livroUpdate: LivroUpdate):
    for livro in livros:
        if livro.id == id:
            if livroUpdate.isbn and livroUpdate.isbn != livro.isbn:
                livro.isbn = livroUpdate.isbn
            if livroUpdate.titulo and livroUpdate.titulo != livro.titulo:
                livro.titulo = livroUpdate.titulo
            if livroUpdate.descricao and livroUpdate.descricao != livro.descricao:
                livro.descricao = livroUpdate.descricao
            if livroUpdate.editora and livroUpdate.editora != livro.editora:
                livro.editora = livroUpdate.editora
            if livroUpdate.autor and livroUpdate.autor != livro.autor:
                livro.autor = livroUpdate.autor
            if livroUpdate.ano_publicacao and livroUpdate.ano_publicacao != livro.ano_publicacao:
                livro.ano_publicacao = livroUpdate.ano_publicacao
            if livroUpdate.status and livroUpdate.status != livro.status:
                livro.status = livroUpdate.status

            return livro

@app.post("/livro/alocar")
def alocar_livro(emprestimo: Emprestimo):
    for usuario in usuarios:
        if emprestimo.usuario_id == usuario.id:
            for livro in livros:
                if livro.id == emprestimo.livro_id:
                    if livro.status != "Indisponível":
                        emprestimos.append(emprestimo)
                        livro.status = "Indisponível"

                    return emprestimo
            return {"mensagem": "Livro não existe"}
    return {"mensagem": "Usuário não existe"}
    

@app.get("/livros/emprestados")
def listar_livros_emprestados():
    livros_emprestados: list[Livro] = []

    for emprestimo in emprestimos:
        for livro in livros:
            if livro.id == emprestimo.livro_id:
                livros_emprestados.append(livro)
    
    return livros_emprestados

@app.get("/emprestimos/atrasados")
def listar_emprestimos_atrasados():
    emprestimos_atrasados: list[Emprestimo] = []

    for emprestimo in emprestimos:
        if not emprestimo.devolvido and emprestimo.data_devolucao < date.today():
            emprestimos_atrasados.append(emprestimo)

    return emprestimos_atrasados

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
    
@app.patch("/usuario/<id>")
def atualizar_usuario(id: UUID, usuarioUpdate: UsuarioUpdate):
    for usuario in usuarios:
        if usuario.id == id:
            if usuarioUpdate.nome and usuarioUpdate.nome != usuario.nome:
                usuario.nome = usuarioUpdate.nome
            if usuarioUpdate.email and usuarioUpdate.email != usuario.email:
                usuario.email = usuarioUpdate.email
            if usuarioUpdate.senha and usuarioUpdate.senha != usuario.senha:
                usuario.senha = usuarioUpdate.senha
                
            return usuario
        
