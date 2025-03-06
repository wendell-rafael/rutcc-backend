from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ENUM

Base = declarative_base()

refeicao_tipo = ENUM('Almoço', 'Jantar', name='refeicao_tipo', create_type=True)

class Cardapio(Base):
    __tablename__ = "cardapios"
    __table_args__ = (UniqueConstraint('dia', 'refeicao', name='unique_dia_refeicao'),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    refeicao = Column(refeicao_tipo, nullable=False, index=True)
    dia = Column(Integer, nullable=False, index=True)
    opcao1 = Column(String, nullable=True)
    opcao2 = Column(String, nullable=True)
    opcao_vegana = Column(String, nullable=True)
    opcao_vegetariana = Column(String, nullable=True)
    salada1 = Column(String, nullable=True)
    salada2 = Column(String, nullable=True)
    guarnicao = Column(String, nullable=True)
    acompanhamento1 = Column(String, nullable=True)
    acompanhamento2 = Column(String, nullable=True)
    acompanhamento3 = Column(String, nullable=True)
    suco = Column(String, nullable=True)
    sobremesa = Column(String, nullable=True)
    cafe = Column(String, nullable=True)
    pao = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
