from pydantic import BaseModel
from datetime import datetime

class FavoritoSchema(BaseModel):
    id: int
    usuario_id: str
    prato: str
    created_at: datetime

    class Config:
        from_attributes = True  # Para compatibilidade com o SQLAlchemy

class FavoritoCreate(BaseModel):
    usuario_id: str
    prato: str
