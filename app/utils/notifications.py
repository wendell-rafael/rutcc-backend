from firebase_admin import messaging

def send_menu_update_notification():
    message = messaging.Message(
        data={'type': 'cardapio_updated'},
        topic='menu_update'  # Todos os dispositivos inscritos nesse tópico receberão a notificação
    )
    response = messaging.send(message)
    # Opcional: logar a resposta para depuração
    print("Notificação enviada com sucesso:", response)
