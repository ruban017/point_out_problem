import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
import io
import shutil
from time import sleep


scopes = ['https://www.googleapis.com/auth/drive']

def auth():
  global creds
  global service
  creds = None
  if (os.path.exists('token.json')):
    print('good')
    creds = Credentials.from_authorized_user_file('token.json', scopes)
    service = build('drive', 'v3', credentials = creds)
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file("secrets.json", scopes)
      creds = flow.run_local_server(port = 0)
    with open('token.json', 'w') as token:
      token.write(creds.to_json())


def up(name):  

  folder_id = '1w8r4R-F1LbvQFzfGh5dTdN-pbjIvS260'
  file_metadata = {
    'name': name,
    'parents': [folder_id]
}
  media = MediaFileUpload(name,
                        mimetype='images/jpeg'
                        )
  file = service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()
  print('done')


def down(path):
    import os
    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)
        files = []
        page_token = None
        folder_id = '1w8r4R-F1LbvQFzfGh5dTdN-pbjIvS260'
        query = f"parents = '{folder_id}'"
        
        # Create the directory if it does not exist
        directory = r"yolov5\data\images"
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        while True:
            # pylint: disable=maybe-no-member
            response = service.files().list(q=query,
                                            spaces='drive',
                                            fields='nextPageToken, '
                                                   'files(id, name)',
                                            pageToken=page_token).execute()
            
            for file in response.get('files', []):
                if file.get("name") == path:
                    print("desired file found")
                    file_id = file.get("id")
                    file_name = path
                    print(file_id)
                    print(file_name)
                    
                    request = service.files().get_media(fileId=file_id)
                    fh = io.BytesIO()
                    downloader = MediaIoBaseDownload(fd=fh, request=request)
                    done = False
                    
                    while not done:
                        status, done = downloader.next_chunk()
                        print(f"Download progress {status.progress()*100}")
                        
                    fh.seek(0)
                    
                    file_path = os.path.join(directory, file_name)
                    with open(file_path, 'wb') as f:
                        f.write(fh.read())
                        f.close()
                    
                    print(f"File downloaded to: {file_path}")
                    shutil.move(file_path, r'yolov5\data\images')

                    return path
                    

            files.extend(response.get('files', []))
            page_token = response.get('nextPageToken', None)
            
            if page_token is None:
                break
                
        # The file was not found in the Google Drive folder
        print(f"Error: File '{path}' not found in Google Drive folder.")
        return None

    except HttpError as error:
        print(F'An error occurred: {error}')
        return None