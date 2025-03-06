# app/main.py
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.routers import cardapio, favorito,notification
from app.database import engine, Base
from app.models.cardapio import Cardapio
from app.models.checkin import Checkin
from app.models.favorito import Favorito
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import credentials, auth, initialize_app
import json
from fastapi.openapi.utils import get_openapi

# Carrega variáveis de ambiente
load_dotenv()
service_account_path = os.getenv("FIREBASE_SERVICE_ACCOUNT")

# Inicializa Firebase Admin se necessário
cred = credentials.Certificate(service_account_path)
initialize_app(cred, {'storageBucket': os.getenv("FIREBASE_STORAGE_BUCKET")})

security = HTTPBearer()


def verify_firebase_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token inválido: {str(e)}")


# Cria as tabelas no banco
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cardápio API")

# Inclui os routers
app.include_router(cardapio.router, prefix="/cardapios", tags=["Cardápios"])
app.include_router(favorito.router, prefix="/favoritos", tags=["Favoritos"])

app.include_router(notification.router, prefix="/notificacoes", tags=["Notificações"])

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Endpoint para exportar OpenAPI
@app.get("/export_openapi")
def export_openapi():
    with open("openapi.json", "w") as f:
        json.dump(get_openapi(title=app.title, version=app.version, routes=app.routes), f, indent=4)
    return {"message": "openapi.json exportado com sucesso"}


# Endpoint de teste de autenticação
@app.get("/auth/test")
def auth_test(user=Depends(verify_firebase_token)):
    return {"message": "Token válido", "uid": user["uid"]}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
