# app/schemas/cardapio.py
from pydantic import BaseModel

class CardapioSchema(BaseModel):
    id: int
    refeicao: str
    dia: int
    opcao1: str | None = None
    opcao2: str | None = None
    opcao_vegana: str | None = None
    opcao_vegetariana: str | None = None
    salada1: str | None = None
    salada2: str | None = None
    guarnicao: str | None = None
    acompanhamento1: str | None = None
    acompanhamento2: str | None = None
    acompanhamento3: str | None = None
    suco: str | None = None
    sobremesa: str | None = None
    cafe: str | None = None
    pao: str | None = None

    class Config:
        orm_mode = True
