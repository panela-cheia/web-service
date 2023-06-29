from googleapiclient.discovery import build
from google.auth import credentials
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import os

def send_email():
    # Carregar as credenciais do arquivo token.json (que você deve obter ao criar um projeto e ativar a API do Gmail)
    creds = None
    if os.path.exists('token.json'):
        creds, _ = load_credentials_from_file('token.json')

    # Se as credenciais não estiverem válidas ou expiradas, solicitar a autenticação do usuário
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = credentials.Credentials.from_authorized_user_file(
                'credentials.json', ['https://www.googleapis.com/auth/gmail.send']
            )
            creds = flow.run_local_server(port=0)

        # Salvar as credenciais atualizadas para uso futuro
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Criar um serviço do Gmail usando as credenciais autenticadas
    service = build('gmail', 'v1', credentials=creds)

    # Criar a mensagem de e-mail
    message = create_message(
        sender='ufvcafbots@gmail.com',
        to='vinicius.o.mendes@ufv.br',
        subject='Assunto do e-mail',
        body='Corpo do e-mail'
    )

    # Enviar o e-mail
    send_message(service, 'me', message)

def create_message(sender, to, subject, body):
    message = {
        'to': to,
        'subject': subject,
        'body': {
            'text': body
        }
    }
    return message

def send_message(service, user_id, message):
    try:
        service.users().messages().send(userId=user_id, body=message).execute()
        print('E-mail enviado com sucesso!')
    except Exception as e:
        print('Erro ao enviar o e-mail:', str(e))

if __name__ == "__main__":
    send_email()