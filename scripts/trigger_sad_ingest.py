"""Dispatch sad-ingest on main, then watch the run until completion and fetch its log."""
import io
import json
import os
import re
import sys
import time
import zipfile

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

headers = {
    "Authorization": f"token {pat}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

# Get sha of main right now
r = requests.get(
    "https://api.github.com/repos/Mikixxl/sad-ingest/branches/main",
    headers=headers,
)
main_sha = r.json()["commit"]["sha"]
print(f"sad-ingest main is at: {main_sha[:10]}")

# Dispatch on main
print(f"\nDispatching sad-ingest.yml on ref=main...")
r = requests.post(
    "https://api.github.com/repos/Mikixxl/sad-ingest/actions/workflows/sad-ingest.yml/dispatches",
    headers=headers,
    json={"ref": "main"},
)
print(f"Dispatch: HTTP {r.status_code}")
if r.status_code != 204:
    print(f"Body: {r.text}")
    sys.exit(1)

# Wait for the new run to appear (poll)
print("\nWaiting for new run to appear and complete...")
target_run = None
start_time = time.time()
while time.time() - start_time < 600:  # 10 min timeout
    r = requests.get(
        "https://api.github.com/repos/Mikixxl/sad-ingest/actions/runs?per_page=5",
        headers=headers,
    )
    runs = r.json().get("workflow_runs", [])
    # Find a workflow_dispatch run that started after our dispatch and is on the latest main
    for run in runs:
        if run["event"] == "workflow_dispatch" and run["head_sha"] == main_sha:
            target_run = run
            break
    if target_run:
        print(f"  Found run {target_run['id']}: status={target_run['status']}, conclusion={target_run.get('conclusion')}")
        if target_run["status"] == "completed":
            break
    time.sleep(20)

if not target_run:
    print("Could not find the dispatched run within 10 minutes.")
    sys.exit(1)

if target_run["status"] != "completed":
    print(f"Run {target_run['id']} did not complete in 10 minutes (status={target_run['status']}). Logs not available yet.")
    sys.exit(1)

run_id = target_run["id"]
print(f"\n=== Run {run_id} concluded: {target_run.get('conclusion')} ===")

# Fetch jobs/steps
r = requests.get(
    f"https://api.github.com/repos/Mikixxl/sad-ingest/actions/runs/{run_id}/jobs",
    headers=headers,
)
for job in r.json().get("jobs", []):
    print(f"\nJob: {job['name']}  conclusion={job.get('conclusion')}")
    for step in job.get("steps", []):
        marker = " " if step.get("conclusion") == "success" else "!"
        print(f"  {marker} {step['number']:2d} {step['name']:50s} {step.get('conclusion')}")

# Fetch logs
r = requests.get(
    f"https://api.github.com/repos/Mikixxl/sad-ingest/actions/runs/{run_id}/logs",
    headers=headers,
    allow_redirects=True,
)
if r.status_code == 200:
    os.makedirs("logs", exist_ok=True)
    log_path = f"logs/sad-ingest-fresh-run-{run_id}.zip"
    with open(log_path, "wb") as f:
        f.write(r.content)
    print(f"\nLogs saved to {log_path}")

    with zipfile.ZipFile(log_path) as zf:
        # Print summary of any commit step
        for n in zf.namelist():
            if "Commit" in n or "Run ingestion" in n or "Heartbeat" in n:
                with zf.open(n) as f:
                    body = f.read().decode("utf-8", errors="replace")
                print(f"\n=== {n} (last 80 lines) ===")
                for line in body.splitlines()[-80:]:
                    print(line)
else:
    print(f"Logs fetch failed: HTTP {r.status_code}")
