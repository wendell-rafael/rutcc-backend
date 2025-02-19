# app/schemas/checkin.py

from pydantic import BaseModel
from datetime import datetime

class CheckinBase(BaseModel):
    usuario_id: str
    status: str

class CheckinResponse(CheckinBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True  # Permite que o Pydantic entenda o modelo SQLAlchemy
