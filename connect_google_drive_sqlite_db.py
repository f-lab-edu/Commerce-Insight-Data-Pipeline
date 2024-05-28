import io
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import time

sqlite_file_path = "./tweet_info.db"

SCOPES = ["https://www.googleapis.com/auth/drive"]
json_path = "./client_secret_889975611963-bbo824bgcdjarj83aa8dl7phi2n00mgs.apps.googleusercontent.com.json"
# 1) IAM 계정 생성: Google Cloud IAM을 사용하여 Google Drive 내 특정 파일에만 액세스 권한을 부여하는 것은 직접적으로 지원되지 않음
# 2) cred.json 파일 전달: 상대 경로로 명시하고 개별 메일로 전달하는 방식
# 3) 스키마.sql 파일 생성
flow = InstalledAppFlow.from_client_secrets_file(json_path, SCOPES)
creds = flow.run_local_server(port=0)
drive_service = build("drive", "v3", credentials=creds)

# 다운로드할 파일의 ID
file_id = "1dybci4R5GmUYWkzOQj458FQ9uMznhPT3"

# 파일 다운로드 요청
request = drive_service.files().get_media(fileId=file_id)

# 다운로드한 파일을 저장할 버퍼
fh = io.BytesIO()
downloader = MediaIoBaseDownload(fh, request)

done = False
while done is False:
    status, done = downloader.next_chunk()
    print(f"Download progress: {int(status.progress() * 100)}%")

# 버퍼의 내용을 파일로 저장
fh.seek(0)
with open("./tweet_info.db", "wb") as f:
    f.write(fh.read())

print("File downloaded successfully.")


def upload_to_drive():
    global file_id

    # 파일 메타데이터
    file_metadata = {"name": "tweet_info.db", "mimeType": "application/octet-stream"}

    # 파일 업로드 요청 생성
    media = MediaFileUpload(sqlite_file_path, resumable=True)

    # 파일 업로드 또는 업데이트
    if file_id:
        # 파일 ID가 있는 경우 파일 업데이트
        file = drive_service.files().update(fileId=file_id, media_body=media).execute()
    else:
        # 파일 ID가 없는 경우 새로운 파일 업로드
        file = (
            drive_service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        file_id = file.get("id")

    # 파일 공개 액세스 권한 설정
    permission = {"type": "anyone", "role": "reader"}
    drive_service.permissions().create(fileId=file_id, body=permission).execute()

    print(f"File ID: {file_id}")


# 데이터베이스 파일 변경 감지 및 주기적인 업로드
last_modified_time = 0
while True:
    # 파일 변경 여부 확인
    if os.path.getmtime(sqlite_file_path) > last_modified_time:
        last_modified_time = os.path.getmtime(sqlite_file_path)
        upload_to_drive()

    # 60초마다 파일 변경 확인
    time.sleep(60)
