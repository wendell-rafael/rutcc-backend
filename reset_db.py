from app.database import engine, SessionLocal
from app.models.cardapio import Base
from sqlalchemy import text

def reset_database():
    with engine.connect() as connection:
        connection.execute(text("DROP SCHEMA public CASCADE"))
        connection.execute(text("CREATE SCHEMA public"))
        connection.commit()

    # Cria as tabelas definidas nos modelos
    Base.metadata.create_all(bind=engine)
    print("Banco de dados resetado com sucesso!")

if __name__ == "__main__":
    reset_database()
