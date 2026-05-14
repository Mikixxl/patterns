"""One-off: dispatch the sad-ingest workflow on Mikixxl/sad-ingest."""
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

# First, check whether Actions is enabled on the repo
r0 = requests.get(
    "https://api.github.com/repos/Mikixxl/sad-ingest/actions/permissions",
    headers={
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github+json",
    },
)
print(f"Actions permissions: HTTP {r0.status_code} body={r0.text[:300]}")

# List workflows on sad-ingest to confirm what GitHub sees
r1 = requests.get(
    "https://api.github.com/repos/Mikixxl/sad-ingest/actions/workflows",
    headers={
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github+json",
    },
)
print(f"Workflows list: HTTP {r1.status_code}")
if r1.status_code == 200:
    for wf in r1.json().get("workflows", []):
        print(f"  - {wf['name']}  state={wf['state']}  path={wf['path']}  id={wf['id']}")

# List recent workflow runs to see what's been running
r2 = requests.get(
    "https://api.github.com/repos/Mikixxl/sad-ingest/actions/runs?per_page=10",
    headers={
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github+json",
    },
)
print(f"\nRecent runs: HTTP {r2.status_code}")
if r2.status_code == 200:
    for run in r2.json().get("workflow_runs", []):
        print(f"  - run {run['id']}  event={run['event']}  status={run['status']}  conclusion={run.get('conclusion')}  created={run['created_at']}  name={run['name']}")

# Dispatch
r = requests.post(
    "https://api.github.com/repos/Mikixxl/sad-ingest/actions/workflows/sad-ingest.yml/dispatches",
    headers={
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    },
    json={"ref": "main"},
)
print(f"\nDispatch status: HTTP {r.status_code}")
if r.status_code != 204:
    print(f"Body: {r.text}")
    sys.exit(1)
print("sad-ingest workflow dispatched.")
