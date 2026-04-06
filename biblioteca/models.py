from pydantic import BaseModel, EmailStr, Field
from uuid import uuid4, UUID
from datetime import date

class Entidade(BaseModel):
    id: UUID = Field(default_factory=uuid4)

class Usuario(Entidade):
    nome: str
    email: EmailStr 
    senha: str

class Livro(Entidade):
    titulo: str
    descricao: str
    editora: str
    autor: str
    ano_publicacao: str
    status: str = Field(default="Disponível")

class Emprestimo(Entidade):
    usuario_id: str
    livro_id: str
    data_devolucao: date