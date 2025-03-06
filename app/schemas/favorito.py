from pydantic import BaseModel
from datetime import datetime

class FavoritoBase(BaseModel):
    usuario_id: str
    prato: str

class FavoritoResponse(FavoritoBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Atualizado para Pydantic V2
