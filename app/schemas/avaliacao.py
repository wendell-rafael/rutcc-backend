# app/schemas/avaliacao.py

from pydantic import BaseModel
from datetime import datetime

class AvaliacaoBase(BaseModel):
    usuario_id: str
    prato_id: str
    avaliacao: float  # Avaliação de 1 a 5

class AvaliacaoResponse(AvaliacaoBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True  # Permite que o Pydantic entenda o modelo SQLAlchemy
