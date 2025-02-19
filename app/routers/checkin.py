# app/routers/checkin.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.checkin import Checkin
from app.schemas.checkin import CheckinResponse
from app.database import SessionLocal

router = APIRouter()


# Função para obter o banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Rota para registrar o check-in
@router.post("/checkin", response_model=CheckinResponse)
async def checkin(usuario_id: str, db: Session = Depends(get_db)):
    db_checkin = Checkin(usuario_id=usuario_id, status="presente")
    db.add(db_checkin)
    db.commit()
    db.refresh(db_checkin)
    return db_checkin


# Rota para registrar o check-out
@router.post("/checkout", response_model=CheckinResponse)
async def checkout(usuario_id: str, db: Session = Depends(get_db)):
    db_checkin = db.query(Checkin).filter(Checkin.usuario_id == usuario_id, Checkin.status == "presente").first()
    if not db_checkin:
        raise HTTPException(status_code=404, detail="Check-in não encontrado")

    db_checkin.status = "não presente"
    db.commit()
    db.refresh(db_checkin)
    return db_checkin
