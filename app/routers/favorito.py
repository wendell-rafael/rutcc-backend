from fastapi import APIRouter, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.favorito import Favorito
from app.schemas.favorito import FavoritoResponse
import json

router = APIRouter()


# Função para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Adicionar um favorito
@router.post("/", response_model=FavoritoResponse)
def add_favorito(usuario_id: str, prato: str, db: Session = Depends(get_db)):
    # Verifique se o favorito já existe
    existing_favorito = db.query(Favorito).filter(Favorito.usuario_id == usuario_id, Favorito.prato == prato).first()
    if existing_favorito:
        raise HTTPException(status_code=400, detail="Este prato já está nos favoritos")

    favorito = Favorito(usuario_id=usuario_id, prato=prato)
    db.add(favorito)
    db.commit()
    db.refresh(favorito)
    return favorito  # Retorna o favorito recém-criado


# Listar todos os favoritos de um usuário
@router.get("/{usuario_id}", response_model=list[FavoritoResponse])
def get_favoritos(usuario_id: str, db: Session = Depends(get_db)):
    favoritos = db.query(Favorito).filter(Favorito.usuario_id == usuario_id).all()
    if not favoritos:
        raise HTTPException(status_code=404, detail="Nenhum favorito encontrado para este usuário")
    # Força a serialização usando o modelo Pydantic
    return [FavoritoResponse.from_orm(fav).dict() for fav in favoritos]

# Remover um favorito
@router.delete("/{id}", response_model=dict)
def remove_favorito(id: int, db: Session = Depends(get_db)):
    favorito = db.query(Favorito).filter(Favorito.id == id).first()
    if not favorito:
        raise HTTPException(status_code=404, detail="Favorito não encontrado")
    db.delete(favorito)
    db.commit()
    return {"message": "Favorito removido com sucesso"}
