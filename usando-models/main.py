from models import Usuario
from fastapi import FastAPI

usuarios:list[Usuario] = [Usuario(nome="John Doe", cpf="123456789-10", email="john.doe@test.com")]

app = FastAPI()

@app.get("/usuarios", response_model=list[Usuario])
def listar():
    return usuarios

@app.post("/usuarios", response_model=Usuario)
def criar(usuario: Usuario):
    if usuario:
        usuarios.append(usuario)
        return usuario 