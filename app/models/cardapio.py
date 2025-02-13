# app/models/cardapio.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Cardapio(Base):
    __tablename__ = "cardapios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    refeicao = Column(String, nullable=False)  # Ex.: "Almoço" ou "Jantar"
    dia = Column(Integer, nullable=False)  # Dia do mês
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
