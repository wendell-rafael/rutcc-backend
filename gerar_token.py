import firebase_admin
from firebase_admin import credentials, auth

# 📌 Carregue a conta de serviço
cred = credentials.Certificate('ru-tcc-firebase-adminsdk-xtwyh-c5342a5d78.json')
firebase_admin.initialize_app(cred)

# 📌 Gere um token de teste
custom_token = auth.create_custom_token('admin@ru.com')
print(f"Custom Token: {custom_token}")
