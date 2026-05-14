"""Diagnose sad-ingest: get latest run details and failure logs."""
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

m = re.search(r"ghp_[A-Za-z0-9]{36,}", text)
pat = m.group(0)
print(f"PAT: {pat[:7]}...{pat[-4:]}")

headers = {
    "Authorization": f"token {pat}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

# Get most recent COMPLETED run
r = requests.get(
    "https://api.github.com/repos/Mikixxl/sad-ingest/actions/runs?per_page=20",
    headers=headers,
)
runs = r.json().get("workflow_runs", [])
print(f"\n{len(runs)} recent runs found")
for run in runs[:10]:
    print(f"  - run {run['id']}  event={run['event']}  status={run['status']}  conclusion={run.get('conclusion')}  created={run['created_at']}")

# Get jobs for the most recent COMPLETED run with conclusion=failure
target_run = next((r for r in runs if r.get("conclusion") == "failure"), None)
if not target_run:
    print("\nNo failed run found. Inspecting most recent completed run instead.")
    target_run = next((r for r in runs if r["status"] == "completed"), None)

if not target_run:
    print("No completed run found at all")
    sys.exit(0)

run_id = target_run["id"]
print(f"\n=== Inspecting run {run_id} (event={target_run['event']}, conclusion={target_run.get('conclusion')}) ===")

r = requests.get(
    f"https://api.github.com/repos/Mikixxl/sad-ingest/actions/runs/{run_id}/jobs",
    headers=headers,
)
jobs = r.json().get("jobs", [])
for job in jobs:
    print(f"\nJob: {job['name']}  conclusion={job.get('conclusion')}")
    for step in job.get("steps", []):
        print(f"  - {step['number']:2d} {step['name']:50s} status={step['status']}  conclusion={step.get('conclusion')}")

# Try to fetch the logs zip (it's available even for completed runs)
print(f"\n=== Fetching logs for run {run_id} ===")
r = requests.get(
    f"https://api.github.com/repos/Mikixxl/sad-ingest/actions/runs/{run_id}/logs",
    headers=headers,
    allow_redirects=True,
)
print(f"Logs fetch: HTTP {r.status_code}, {len(r.content)} bytes")
if r.status_code == 200 and r.content:
    # Save it for committing
    os.makedirs("logs", exist_ok=True)
    log_path = f"logs/sad-ingest-run-{run_id}.zip"
    with open(log_path, "wb") as f:
        f.write(r.content)
    print(f"Logs saved to {log_path}")

    # Extract and dump the run log for the failing step
    import zipfile
    try:
        with zipfile.ZipFile(log_path) as zf:
            print("\nFiles in log zip:")
            for n in zf.namelist():
                print(f"  - {n}")
            # Find the ingest log
            for n in zf.namelist():
                if "Run ingestion" in n or "ingest" in n.lower():
                    with zf.open(n) as f:
                        body = f.read().decode("utf-8", errors="replace")
                    print(f"\n=== {n} ===")
                    print(body[:5000])
    except Exception as e:
        print(f"Could not unzip: {e}")
