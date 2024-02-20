import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64
import os

# Configurar los permisos necesarios y el alcance
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def list_labels(service, user_id):
    """List all labels in the user's Gmail account."""
    try:
        response = service.users().labels().list(userId=user_id).execute()
        labels = response['labels']
        return labels
    except Exception as error:
        print('An error occurred: %s' % error)

#def get_messages(service, user_id, label_ids):
#    """Get all messages with a specific label."""
#    try:
#        response = service.users().messages().list(userId=user_id, labelIds=label_ids).execute()
#        messages = []
#        if 'messages' in response:
#            messages.extend(response['messages'])
#
#        while 'nextPageToken' in response:
#            page_token = response['nextPageToken']
#            response = service.users().messages().list(userId=user_id, labelIds=label_ids,
#                                                       pageToken=page_token).execute()
#            messages.extend(response['messages'])
#
#        return messages
#    except Exception as error:
#        print('An error occurred: %s' % error)

def get_messages(service, user_id):
    """Obtener todos los mensajes de la bandeja de entrada."""
    try:
        response = service.users().messages().list(userId=user_id).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages
    except Exception as error:
        print('Ocurrió un error: %s' % error)


def get_message_content(service, user_id, message_id):
    try:
        message = service.users().messages().get(userId=user_id, id=message_id).execute()
        email = {
            'destinatario': '',
            'remitente': '',
            'fecha': '',
            'asunto': '',
            'body': '',
            'categorizacion': '',
            'respuesta': ''
        }
        for i in message['payload']['headers']:
            if i['name'] == "Delivered-To":
                email['destinatario'] = i['value']
            elif i['name'] == 'From':
                email['remitente'] = i['value']
            elif i['name'] == 'Date':
                email['fecha'] = i['value']
            elif i['name'] == 'Subject':
                email['asunto'] = i['value']

        for part in message['payload']['parts']:
            #print(part)
            if part['mimeType'] == 'text/plain':
                if 'data' in part['body']:
                    data = part['body']['data']
                    #print(data)
                    #print(base64.urlsafe_b64decode(data).decode('utf-8'))
                    email['body'] += base64.urlsafe_b64decode(data).decode('utf-8')

        return email

    except Exception as error:
        print('Ocurrió un error al obtener el contenido del mensaje: %s' % error)



def main():
    """Shows basic usage of the Gmail API."""
    creds = None
    # El archivo token.json almacena los tokens de acceso y actualización del usuario y se
    # crea automáticamente cuando se completa el flujo de autorización para la primera vez.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    # Si no hay credenciales válidas disponibles, se pide al usuario que inicie sesión.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print("Run the authentication process again.")
            return

    # Construir el servicio de Gmail
    service = build('gmail', 'v1', credentials=creds)


    # Obtener la lista de etiquetas
    labels = list_labels(service, "me")
    etiquetas = []
    # Imprimir el ID y el nombre de cada etiqueta
    if labels:
        for label in labels:
            etiquetas.append(label['id'])
            #print("Label ID:", label['id'])
            #print("Label Name:", label['name'])
    else:
        print("No labels found.")

    # ID de la etiqueta
    label_id = 'SENT'


    # Obtener os mensajes
    messages = get_messages(service, "me")

    for i in messages:
        msg_id = i['id']
        email = get_message_content(service, 'me', msg_id)
        print(email)



if __name__ == '__main__':
    main()
