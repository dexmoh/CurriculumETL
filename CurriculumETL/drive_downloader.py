# This tool downloads all of the JSON data from Google Drive and stores it in a local folder.

from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

SERVICE_ACCOUNT_JSON = r"curriculumetl-9019948c547c.json"
FOLDER_ID: str       = "1bSOM6vmbmylWbWCqgAnXPiBLRCF7xs4b"
SCOPES: list[str]    = ['https://www.googleapis.com/auth/drive.readonly']
DOWNLOAD_DIR: str    = "data" # Where should the files be stored.

# Download all JSON files from Google Drive and store them locally.
def download_drive_data():
    # Fetch Google service.
    print("Creating Google drive service...")
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_JSON, scopes=SCOPES
    )
    service = build('drive', 'v3', credentials=creds)

    # Find all files stored on the drive.
    files = []

    def recurse(fid, level=0):
        query = f"'{fid}' in parents and trashed=false"
        page_token = None

        while True:
            response = service.files().list(
                q=query,
                spaces='drive',
                fields='nextPageToken, files(id, name, mimeType)',
                pageToken=page_token
            ).execute()

            for file in response.get('files', []):
                if file['mimeType'] == 'application/vnd.google-apps.folder':
                    recurse(file['id'], level + 1)
                else:
                    files.append({'id': file['id'], 'name': file['name']})

            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

    print("Looking for files on the drive... (This may take a while.)")
    recurse(FOLDER_ID)

    file_count = len(files)
    print(f"Found {file_count} files.")

    # Download all files locally.
    print("Downloading files...")

    counter = 0
    Path(DOWNLOAD_DIR).mkdir(parents=True, exist_ok=True)

    for file in files:
        counter += 1
        file_name = file["name"]
        file_id = file["id"]

        if not file_name.endswith(".json"):
            continue

        file_path = f"{DOWNLOAD_DIR}/{file_name}"

        # Don't download the same file twice.
        if Path(file_path).exists():
            continue

        # Create a file.
        Path(file_path).touch()

        # Download file.
        with open(file_path, "wb") as file_stream:
            request = service.files().get_media(fileId=file_id)
            downloader = MediaIoBaseDownload(file_stream, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()

        if counter % 10 == 0:
            print(f"Download progress: {round((counter / file_count) * 100.0, 2)}% ({counter} files downloaded.)")
    
    print("Download complete.")

def main():
    download_drive_data()

if __name__ == "__main__":
    main()
