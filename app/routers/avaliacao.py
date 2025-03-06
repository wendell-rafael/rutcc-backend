# app/routers/avaliacao.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.avaliacao import Avaliacao
from app.schemas.avaliacao import AvaliacaoResponse
from app.database import SessionLocal

router = APIRouter()


# Função para obter o banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Rota para registrar a avaliação
@router.post("/avaliar", response_model=AvaliacaoResponse)
async def avaliar(usuario_id: str, prato_id: str, avaliacao: float, db: Session = Depends(get_db)):
    if not (1 <= avaliacao <= 5):
        raise HTTPException(status_code=400, detail="Avaliação inválida. A nota deve ser entre 1 e 5.")

    db_avaliacao = Avaliacao(usuario_id=usuario_id, prato_id=prato_id, avaliacao=avaliacao)
    db.add(db_avaliacao)
    db.commit()
    db.refresh(db_avaliacao)
    return db_avaliacao
