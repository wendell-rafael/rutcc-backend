# app/utils/firebase_utils.py
import firebase_admin
from firebase_admin import credentials, storage
import os
from dotenv import load_dotenv

load_dotenv()


def initialize_firebase():
    service_account_path = os.getenv("FIREBASE_SERVICE_ACCOUNT")
    bucket_name = os.getenv("FIREBASE_STORAGE_BUCKET")

    cred = credentials.Certificate(service_account_path)
    try:
        firebase_admin.get_app()
    except ValueError:
        firebase_admin.initialize_app(cred, {
            'storageBucket': bucket_name
        })


def get_bucket():
    initialize_firebase()
    bucket = storage.bucket()
    return bucket


def download_csv_from_storage(file_path: str) -> str:
    """
    Baixa um arquivo CSV do Firebase Storage e retorna o conteúdo como texto.
    :param file_path: Caminho do arquivo no bucket.
    :return: Conteúdo do CSV em forma de string.
    """
    bucket = get_bucket()
    blob = bucket.blob(file_path)
    csv_content = blob.download_as_text()
    return csv_content
