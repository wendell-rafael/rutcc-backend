# app/models/avaliacao.py

from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Avaliacao(Base):
    __tablename__ = 'avaliacoes'

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(String, ForeignKey('usuarios.id'))  # Relacionamento com a tabela de usuários
    prato_id = Column(String)  # Identificador do prato
    avaliacao = Column(Float)  # Avaliação entre 1 e 5
    timestamp = Column(DateTime, server_default=func.now())  # Data e hora da avaliação

    usuario = relationship("Usuario", back_populates="avaliacoes")

    def __repr__(self):
        return f"<Avaliacao(usuario_id={self.usuario_id}, prato_id={self.prato_id}, avaliacao={self.avaliacao})>"
