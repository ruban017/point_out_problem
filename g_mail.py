#g_mail.py

from email.mime.message import MIMEMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mimetypes
from email.mime.base import MIMEBase
from email import encoders
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
import base64
import os


scopes = ["https://mail.google.com/"]

def auth_gmail():
  global creds
  global service
  creds = None
  if (os.path.exists('token1.json')):
    print('good')
    creds = Credentials.from_authorized_user_file('token1.json', scopes)
    service = build('gmail', 'v1', credentials = creds)

  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file("secrets.json", scopes)
      creds = flow.run_local_server(port = 0)
    with open('token1.json', 'w') as token:
      token.write(creds.to_json())


def send_mail(msg, file):

    file_attachments = [file, 'location.html']
    global message
    global create_msg
    message = MIMEMultipart()
    message['To'] = 'rishywanth05@gmail.com'
    message['Subject'] = 'regarding crime'
    message.attach(MIMEText(msg, 'plain'))

    for attachment in file_attachments:
      content_type, encoding = mimetypes.guess_type(attachment)
      main_type, sub_type = content_type.split('/', 1)
      file_name = os.path.basename(attachment)

      f = open(attachment, 'rb')
      myFile = MIMEBase(main_type, sub_type)
      myFile.set_payload(f.read())
      myFile.add_header('Content-Disposition', 'attachment', filename=file_name)

      encoders.encode_base64(myFile)

      f.close()
      message.attach(myFile)





    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

   

    create_msg = {'message': {
                  'raw': encoded_message
    }}
    
    send_gmail = service.users().messages().send(userId = 'me', body = {'raw': encoded_message}).execute()
    print("Mail sent!!")