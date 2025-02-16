from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.favorito import Favorito

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=dict)
def add_favorito(usuario_id: str, prato: str, db: Session = Depends(get_db)):
    favorito = Favorito(usuario_id=usuario_id, prato=prato)
    db.add(favorito)
    db.commit()
    db.refresh(favorito)
    return {"message": "Favorito adicionado com sucesso"}


@router.get("/{usuario_id}", response_model=list)
def get_favoritos(usuario_id: str, db: Session = Depends(get_db)):
    favoritos = db.query(Favorito).filter(Favorito.usuario_id == usuario_id).all()
    return favoritos


@router.delete("/{id}", response_model=dict)
def remove_favorito(id: int, db: Session = Depends(get_db)):
    favorito = db.query(Favorito).filter(Favorito.id == id).first()
    if not favorito:
        raise HTTPException(status_code=404, detail="Favorito não encontrado")
    db.delete(favorito)
    db.commit()
    return {"message": "Favorito removido com sucesso"}

# Lógica de monitoramento (a ser implementada):
# - Uma função que roda diariamente, busca o cardápio do dia e compara com os pratos favoritos de cada usuário.
# - Se houver correspondência, envia notificação via Firebase Cloud Messaging.
