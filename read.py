from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from ollama import ollama
from edenAI import EDEN
import base64
import json
import os

# Configurar los permisos necesarios y el alcance
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.modify']

def list_labels(service, user_id):
    """List all labels in the user's Gmail account."""
    try:
        response = service.users().labels().list(userId=user_id).execute()
        labels = response['labels']
        return labels
    except Exception as error:
        print('An error occurred: %s' % error)


def get_messages(service, user_id, label_id):
    """Obtener todos los mensajes de la bandeja de entrada."""
    try:
        response = service.users().messages().list(userId=user_id, labelIds=[label_id]).execute()
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
            'id': message_id,
            'thread_id': message['threadId'],
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


def cat_resp(body):
    response = EDEN(body)
    categories = ['queja/reclamo', 'consultas/solicitud de información', 'agradecimiento/conformidad']
    out = {'category': "",
           'response': ""}
    for category in categories:
        if category in response:
            out['category'] = category
    text = response.split(";;;;")[-1].strip()
    out['response'] = text
    return out


def create_message(to, subject, message_text, thread_id):
    message = MIMEText(message_text)
    message['to'] = to
    message['subject'] = subject
    message['threadId'] = thread_id
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


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



    # Obtener los mensajes
    messages = get_messages(service, "me", "UNREAD")
    if len(messages) == 0:
        print('No hay emails sin leer.')


    # GENERAR RESPUESTA CON IA

    for i in messages:
        msg_id = i['id']
        email = get_message_content(service, 'me', msg_id)
        resp = cat_resp(email['body'])
        email['categorizacion'] = resp['category']
        email['respuesta'] = resp['response']
        print(email)
        print('BODY EMAIL')
        print(email['body'])
        print('------------------------------------------------------------------------------------')
        print('CATEGORIA POR IA')
        print(email['categorizacion'])
        print('------------------------------------------------------------------------------------')
        print('RESPUESTA GENERADA POR IA')
        print(email['respuesta'])




    # Enviar una respuesta a cada mensaje
    #for i in messages:
    #    msg_id = i['id']
    #    email = get_message_content(service, 'me', msg_id)
    #    #print(i)
    #    try:
    #        respuesta = 'Hola desde Python !'
    #        reply_message = create_message(email['remitente'], 'Probando gmail api python !', respuesta, email['thread_id'])
    #        service.users().messages().send(userId='me', body=reply_message).execute()  #
    #        print('Reply sent successfully!')
#
    #        service.users().messages().modify(
    #            userId='me',
    #            id=msg_id,
    #            body={'removeLabelIds': ['UNREAD']}
    #        ).execute()
#
    #    except Exception as e:
    #        print('An error occurred:', e)




if __name__ == '__main__':
    main()
