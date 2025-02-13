# app/routers/cardapio.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.cardapio import CardapioSchema
from app.models.cardapio import Cardapio
from app.database import SessionLocal
from app.utils.firebase_utils import download_csv_from_storage
from app.utils.csv_parser import parse_cardapio_csv
import logging

router = APIRouter()

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[CardapioSchema])
def get_cardapios(db: Session = Depends(get_db)):
    """
    Retorna todos os registros de cardápio.
    """
    cardapios = db.query(Cardapio).all()
    return cardapios

@router.post("/import", response_model=dict)
def import_cardapios(file_path: str, db: Session = Depends(get_db)):
    """
    Endpoint para importar os cardápios de um arquivo CSV armazenado no Firebase Storage.
    O parâmetro 'file_path' deve ser o caminho do arquivo no bucket.
    """
    try:
        csv_content = download_csv_from_storage(file_path)
        cardapio_list = parse_cardapio_csv(csv_content)
    except Exception as e:
        logging.exception("Erro ao baixar ou processar o CSV.")
        raise HTTPException(status_code=500, detail="Erro ao processar o arquivo CSV.")

    # Para simplificar, vamos limpar os registros existentes e inserir os novos.
    db.query(Cardapio).delete()
    db.commit()

    for row in cardapio_list:
        try:
            cardapio = Cardapio(
                refeicao=row.get("Refeição"),
                dia=int(row.get("Data") or 0),
                opcao1=row.get("Opção 1"),
                opcao2=row.get("Opção 2"),
                opcao_vegana=row.get("Opção Vegana"),
                opcao_vegetariana=row.get("Opção Vegetariana"),
                salada1=row.get("Salada 1"),
                salada2=row.get("Salada 2"),
                guarnicao=row.get("Guarnição"),
                acompanhamento1=row.get("Acompanhamento 1"),
                acompanhamento2=row.get("Acompanhamento 2"),
                acompanhamento3=row.get("Acompanhamento 3"),
                suco=row.get("Suco"),
                sobremesa=row.get("Sobremesa"),
                cafe=row.get("Café"),
                pao=row.get("Pão")
            )
            db.add(cardapio)
        except Exception as e:
            logging.exception("Erro ao mapear a linha para o modelo Cardapio: %s", row)
    db.commit()
    return {"message": "Cardápios importados com sucesso."}
