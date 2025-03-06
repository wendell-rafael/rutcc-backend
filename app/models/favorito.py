from sqlalchemy.orm import declarative_base

from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.sql import func

from app.database import Base


class Favorito(Base):
    __tablename__ = 'favoritos'  # Nome da tabela no banco de dados

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(String, nullable=False)  # Alterado para String para aceitar o UID
    prato = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<Favorito(id={self.id}, usuario_id={self.usuario_id}, prato={self.prato})>"
