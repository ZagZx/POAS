from dotenv import load_dotenv
from os import getenv
import requests

from fastapi import FastAPI

load_dotenv(".env")
API_KEY = getenv("API_KEY")
HEADERS = {"chave-api-dados": API_KEY}
URL = "https://api.portaldatransparencia.gov.br/api-de-dados"

app = FastAPI()


@app.get("/consulta/{cpf}")
def consulta(cpf: str):
    pessoa_fisica = requests.get(URL+"/pessoa-fisica", params={"cpf":cpf}, headers=HEADERS)
    viagens_por_cpf = requests.get(URL+"/viagens-por-cpf", params={"cpf": cpf}, headers=HEADERS)
    peti_por_cpf = requests.get(URL+"/peti-por-cpf-ou-nis", params={"codigo": cpf}, headers=HEADERS)
    bpc_por_cpf = requests.get(URL+"/bpc-por-cpf-ou-nis", params={"codigo": cpf}, headers=HEADERS)

    return {
        "pessoaFisica": pessoa_fisica.json(),
        "viagens": viagens_por_cpf.json(),
        "peti": peti_por_cpf.json(),
        "bpc": bpc_por_cpf.json()
    }