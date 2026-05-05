from sqlmodel import SQLModel

class BaseModel(SQLModel):
    model_config = {
        "from_attributes": True
    }