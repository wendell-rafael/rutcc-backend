from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from firebase_admin import messaging

from app.database import SessionLocal

router = APIRouter()


# Função para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Modelo para o payload da notificação
class NotificationPayload(BaseModel):
    token: str  # Token do dispositivo (obtido no Flutter)
    title: str  # Título da notificação
    body: str  # Corpo da notificação


app = FastAPI(title="Cardápio API")


@app.post("/send_notification")
def send_notification(payload: NotificationPayload):
    message = messaging.Message(
        notification=messaging.Notification(
            title=payload.title,
            body=payload.body,
        ),
        token=payload.token,
    )
    try:
        response = messaging.send(message)
        return {"message": "Notificação enviada com sucesso", "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
