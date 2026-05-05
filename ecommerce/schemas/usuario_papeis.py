from sqlmodel import Field

from .base import BaseModel
# from .papel import PapelRead


class UsuarioPapeisRequest(BaseModel):
    papeis_ids: list[int] = Field(min_length=1)

# class UsuarioPapeisResponse(BaseModel):    
#     usuario_id: int
#     papeis: list[PapelRead]