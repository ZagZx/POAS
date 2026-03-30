from pydantic import BaseModel, EmailStr

class Usuario(BaseModel):
    nome: str
    cpf: str
    email: EmailStr
