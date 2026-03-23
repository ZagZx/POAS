from fastapi import FastAPI
from math import sqrt

app = FastAPI()

@app.get("/")
def home():
    return {"mensagem": "OLAA"}

@app.get("/soma")
def soma(n1: int, n2: int):
    return n1+n2

@app.get("/subtracao")
def subtracao(n1: int, n2: int):
    return n1-n2

@app.get("/divisao")
def divisao(n1: int, n2: int):
    return n1/n2

@app.get("/multiplicacao")
def multiplicacao(n1: int, n2: int):
    return n1*n2

@app.get("/raiz")
def raiz(n: int):
    return sqrt(n)