"""One-off: dispatch the sad-ingest workflow on Mikixxl/sad-ingest.

Reads the PAT from KEYS-REPOSITORY using the patterns SA (which has Viewer on
that doc), then POSTs to api.github.com to dispatch the workflow.
"""
import io
import json
import os
import re
import sys

import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

KEYS_DOC_ID = "1xqpAZLGtYku4_wMatPRabOHrTb6e1TRWCJJNorNDb1Q"
SCOPES = ["https://www.googleapis.com/auth/drive"]

creds = service_account.Credentials.from_service_account_info(
    json.loads(os.environ["GOOGLE_SA_JSON"]), scopes=SCOPES,
)
drive = build("drive", "v3", credentials=creds, cache_discovery=False)

buf = io.BytesIO()
req = drive.files().export_media(fileId=KEYS_DOC_ID, mimeType="text/plain")
downloader = MediaIoBaseDownload(buf, req)
done = False
while not done:
    _, done = downloader.next_chunk()
text = buf.getvalue().decode("utf-8", errors="replace")
print(f"Read KEYS-REPOSITORY: {len(text)} chars")

m = re.search(r"ghp_[A-Za-z0-9]{36,}", text)
if not m:
    sys.exit("No PAT found in KEYS-REPOSITORY")
pat = m.group(0)
print(f"PAT prefix: {pat[:7]}")

r = requests.post(
    "https://api.github.com/repos/Mikixxl/sad-ingest/actions/workflows/sad-ingest.yml/dispatches",
    headers={
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    },
    json={"ref": "main"},
)
print(f"Dispatch status: {r.status_code}")
if r.status_code != 204:
    print(f"Body: {r.text}")
    sys.exit(1)
print("sad-ingest workflow dispatched.")
