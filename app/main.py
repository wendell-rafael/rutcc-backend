# app/main.py
from fastapi import FastAPI
from app.routers import cardapio
from app.database import engine
from app.models.cardapio import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cardápio API")

# Inclui o router de cardápios
app.include_router(cardapio.router, prefix="/cardapios", tags=["Cardápios"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
