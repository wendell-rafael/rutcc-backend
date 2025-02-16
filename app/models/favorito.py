from sqlalchemy.orm import declarative_base

from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.sql import func

Base = declarative_base()


class Favorito(Base):
    __tablename__ = "favoritos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(String, nullable=False)
    prato = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
