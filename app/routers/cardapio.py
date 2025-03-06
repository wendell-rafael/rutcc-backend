import logging
from fastapi import APIRouter, HTTPException, Depends, Security
from sqlalchemy import case
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.cardapio import Cardapio
from app.schemas.cardapio import CardapioSchema
from app.database import SessionLocal
from app.utils.firebase_utils import download_csv_from_storage
from app.utils.csv_parser import parse_cardapio_csv
from firebase_admin import auth

from app.utils.notifications import send_menu_update_notification

# Importe a função de notificação

router = APIRouter()
security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_firebase_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        decoded_token = auth.verify_id_token(credentials.credentials)
        return decoded_token
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")


@router.get("/", response_model=list[CardapioSchema])
def get_cardapios(db: Session = Depends(get_db)):
    refeicao_order = case(
        (Cardapio.refeicao == 'Almoço', 1),
        (Cardapio.refeicao == 'Jantar', 2),
        else_=3
    )
    return (
        db.query(Cardapio)
        .order_by(Cardapio.dia.asc(), refeicao_order.asc())
        .all()
    )


@router.post("/import", response_model=dict)
def import_cardapios(nome_cardapio: str, db: Session = Depends(get_db)):
    file_path = f"uploads/csv/{nome_cardapio}"
    logging.info(f"📂 Iniciando importação: {file_path}")
    try:
        csv_content = download_csv_from_storage(file_path)
        cardapio_list = parse_cardapio_csv(csv_content)
        logging.info(f"✅ CSV lido com {len(cardapio_list)} registros.")
    except Exception as e:
        logging.error(f"🚨 Erro ao baixar/processar CSV: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao baixar/processar CSV: {str(e)}")

    try:
        db.query(Cardapio).delete()
        db.commit()
        for row in cardapio_list:
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
        db.commit()

        # Envia notificação de atualização
        try:
            send_menu_update_notification()
        except Exception as notif_error:
            logging.error(f"🚨 Erro ao enviar notificação: {notif_error}")

        logging.info("✅ Cardápios importados com sucesso.")
        return {"message": f"Cardápio '{nome_cardapio}' importado com sucesso"}
    except Exception as e:
        logging.error(f"🚨 Erro ao salvar no banco: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao salvar no banco: {str(e)}")


@router.post("/", response_model=CardapioSchema, status_code=201)
def create_cardapio(cardapio: CardapioSchema, user=Depends(verify_firebase_token), db: Session = Depends(get_db)):
    new_cardapio = Cardapio(**cardapio.dict())
    db.add(new_cardapio)
    db.commit()
    db.refresh(new_cardapio)

    try:
        send_menu_update_notification()
    except Exception as notif_error:
        logging.error(f"🚨 Erro ao enviar notificação: {notif_error}")

    return new_cardapio


@router.put("/{id}", response_model=CardapioSchema)
def update_cardapio(id: int, cardapio: CardapioSchema, user=Depends(verify_firebase_token),
                    db: Session = Depends(get_db)):
    existing_cardapio = db.query(Cardapio).filter(Cardapio.id == id).first()
    if not existing_cardapio:
        raise HTTPException(status_code=404, detail="Cardápio não encontrado")
    for key, value in cardapio.dict().items():
        setattr(existing_cardapio, key, value)
    db.commit()
    db.refresh(existing_cardapio)

    try:
        send_menu_update_notification()
    except Exception as notif_error:
        logging.error(f"🚨 Erro ao enviar notificação: {notif_error}")

    return existing_cardapio


@router.patch("/{id}", response_model=CardapioSchema)
def patch_cardapio(id: int, cardapio: dict, user=Depends(verify_firebase_token), db: Session = Depends(get_db)):
    existing_cardapio = db.query(Cardapio).filter(Cardapio.id == id).first()
    if not existing_cardapio:
        raise HTTPException(status_code=404, detail="Cardápio não encontrado")
    for key, value in cardapio.items():
        setattr(existing_cardapio, key, value)
    db.commit()
    db.refresh(existing_cardapio)

    try:
        send_menu_update_notification()
    except Exception as notif_error:
        logging.error(f"🚨 Erro ao enviar notificação: {notif_error}")

    return existing_cardapio


@router.delete("/{id}", response_model=dict)
def delete_cardapio(id: int, user=Depends(verify_firebase_token), db: Session = Depends(get_db)):
    cardapio = db.query(Cardapio).filter(Cardapio.id == id).first()
    if not cardapio:
        raise HTTPException(status_code=404, detail="Cardápio não encontrado")
    db.delete(cardapio)
    db.commit()

    try:
        send_menu_update_notification()
    except Exception as notif_error:
        logging.error(f"🚨 Erro ao enviar notificação: {notif_error}")

    return {"message": "Cardápio removido com sucesso"}
