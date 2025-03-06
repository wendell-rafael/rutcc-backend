# app/models/checkin.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

from app.database import Base
class Checkin(Base):
    __tablename__ = 'checkins'

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(String, index=True)  # UID do Firebase como String
    status = Column(String, default="não presente")  # "presente" ou "não presente"
    timestamp = Column(DateTime, server_default=func.now())  # Data e hora do check-in

    def __repr__(self):
        return f"<Checkin(usuario_id={self.usuario_id}, status={self.status}, timestamp={self.timestamp})>"
