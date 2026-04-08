from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import uuid4, UUID
from datetime import date

class Entidade(BaseModel):
    id: UUID = Field(default_factory=uuid4)

class Usuario(Entidade):
    nome: str
    email: EmailStr 
    senha: str

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None


class Livro(Entidade):
    isbn: str
    titulo: str
    descricao: str
    editora: str
    autor: str
    ano_publicacao: str
    status: str = Field(default="Disponível")

class LivroUpdate(BaseModel):
    isbn: Optional[str] = None
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    editora: Optional[str] = None
    autor: Optional[str] = None
    ano_publicacao: Optional[str] = None
    status: Optional[str] = None

class Emprestimo(Entidade):
    usuario_id: str
    livro_id: str
    data_devolucao: date