import base64
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Set up credentials
creds = Credentials.from_authorized_user_file('credentials.json')  # Your credentials file from Google Cloud Console
service = build('gmail', 'v1', credentials=creds)


def send_reply(message_id, response_body):
    try:
        message = service.users().messages().get(userId='me', id=message_id).execute()
        thread_id = message['threadId']

        # Compose reply message
        reply_message = create_message('me', message['payload']['headers'][0]['value'], response_body, thread_id)
        service.users().messages().send(userId='me', body=reply_message).execute()

        print('Reply sent successfully!')
    except Exception as e:
        print('An error occurred:', e)


def create_message(sender, subject, message_text, thread_id):
    message = MIMEText(message_text)
    message['to'] = sender
    message['subject'] = subject
    message['In-Reply-To'] = thread_id
    message['References'] = thread_id
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


# Example usage
message_id = 'YOUR_MESSAGE_ID_HERE'
response_body = "Your response message here."

send_reply(message_id, response_body)
