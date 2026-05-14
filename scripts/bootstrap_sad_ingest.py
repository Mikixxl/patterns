"""v5 bootstrap - logs via git push to patterns repo (no Drive write).

The v4 attempt revealed that the patterns SA cannot write files to personal
Drive folders: service accounts attached to personal Google accounts have no
storage quota and cannot own files. This affects sad-ingest too - that's why
no INGEST-* files appeared in 02-Inbox.

This v5:
1. Same primary logic: extract creds from KEYS-REPOSITORY, set secrets on
   sad-ingest, trigger first run
2. Writes detailed log to logs/bootstrap-{ts}.log in the patterns repo
3. Verifies secrets ARE actually set by listing them after PUT
4. Captures the exact Drive HttpError text so we can confirm the storage-quota
   diagnosis from outside the runner
"""
from __future__ import annotations

import io
import json
import os
import re
import sys
import traceback
from base64 import b64encode
from datetime import datetime, timezone
from pathlib import Path

import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
from nacl import encoding, public

KEYS_DOC_ID = "1xqpAZLGtYku4_wMatPRabOHrTb6e1TRWCJJNorNDb1Q"
INBOX_FOLDER_ID = "18_dJnTLcSLp6vTn9xu2hbgAOex-fYJBi"
TARGET_REPO = "Mikixxl/sad-ingest"

GH_API = "https://api.github.com"
SCOPES = ["https://www.googleapis.com/auth/drive"]

log_lines: list[str] = []


def log(msg: str) -> None:
    line = f"[{datetime.now(timezone.utc).isoformat()}] {msg}"
    print(line, flush=True)
    log_lines.append(line)


def load_creds():
    info = json.loads(os.environ["GOOGLE_SA_JSON"])
    return service_account.Credentials.from_service_account_info(info, scopes=SCOPES)


def fetch_keys_doc_text(drive) -> str:
    request = drive.files().export_media(fileId=KEYS_DOC_ID, mimeType="text/plain")
    buf = io.BytesIO()
    downloader = MediaIoBaseDownload(buf, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    return buf.getvalue().decode("utf-8", errors="replace")


def extract_pat(text: str) -> str:
    matches = re.findall(r"ghp_[A-Za-z0-9]{36,}", text)
    if not matches:
        raise RuntimeError("PAT not found in KEYS-REPOSITORY")
    log(f"  found {len(matches)} ghp_ PAT(s)")
    return matches[0]


def extract_anthropic_key(text: str) -> str:
    matches = re.findall(r"sk-ant-api03-[A-Za-z0-9_\-]{80,}", text)
    if not matches:
        raise RuntimeError("ANTHROPIC_API_KEY not found in KEYS-REPOSITORY")
    log(f"  found {len(matches)} sk-ant-api03-... key(s)")
    return matches[0]


def gh_session(pat: str) -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    return s


def get_public_key(session, repo: str) -> dict:
    r = session.get(f"{GH_API}/repos/{repo}/actions/secrets/public-key")
    if r.status_code != 200:
        raise RuntimeError(f"public-key fetch failed: HTTP {r.status_code} {r.text[:300]}")
    return r.json()


def encrypt_secret(public_key_b64: str, value: str) -> str:
    pub_key = public.PublicKey(public_key_b64.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(pub_key)
    encrypted = sealed_box.encrypt(value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")


def set_secret(session, repo: str, name: str, value: str, pubkey: dict) -> None:
    enc = encrypt_secret(pubkey["key"], value)
    r = session.put(
        f"{GH_API}/repos/{repo}/actions/secrets/{name}",
        json={"encrypted_value": enc, "key_id": pubkey["key_id"]},
    )
    if r.status_code not in (201, 204):
        raise RuntimeError(f"set_secret {name} failed: HTTP {r.status_code} {r.text[:300]}")
    log(f"  set_secret {name}: HTTP {r.status_code}")


def list_secrets(session, repo: str) -> list[str]:
    r = session.get(f"{GH_API}/repos/{repo}/actions/secrets")
    if r.status_code != 200:
        raise RuntimeError(f"list_secrets failed: HTTP {r.status_code} {r.text[:300]}")
    data = r.json()
    return [s["name"] for s in data.get("secrets", [])]


def trigger_workflow(session, repo: str, workflow_file: str) -> dict:
    r = session.post(
        f"{GH_API}/repos/{repo}/actions/workflows/{workflow_file}/dispatches",
        json={"ref": "main"},
    )
    if r.status_code != 204:
        raise RuntimeError(f"dispatch failed: HTTP {r.status_code} {r.text[:300]}")
    log(f"  dispatch {workflow_file}: HTTP {r.status_code}")
    return {"status": r.status_code}


def probe_drive_write(drive) -> str:
    """Try to write a 1-byte file to 02-Inbox and return either OK or the full error text."""
    try:
        body_bytes = b"probe"
        media = MediaIoBaseUpload(io.BytesIO(body_bytes), mimetype="text/plain", resumable=False)
        metadata = {"name": "BOOTSTRAP-DRIVE-PROBE.txt", "parents": [INBOX_FOLDER_ID]}
        f = drive.files().create(body=metadata, media_body=media, fields="id,name").execute()
        return f"OK probe wrote: id={f['id']} name={f['name']}"
    except Exception as exc:  # noqa: BLE001
        return f"FAIL Drive write: {type(exc).__name__}: {exc}"


def write_log_to_repo(status: str) -> None:
    """Write log to logs/bootstrap-{ts}.log in this repo and git push."""
    repo_root = Path(__file__).resolve().parent.parent
    logs_dir = repo_root / "logs"
    logs_dir.mkdir(exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H%M%S")
    log_file = logs_dir / f"bootstrap-{status}-{ts}.log"
    log_file.write_text("\n".join(log_lines) + "\n", encoding="utf-8")

    # git add/commit/push
    import subprocess
    subprocess.run(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"], check=True, cwd=repo_root)
    subprocess.run(["git", "config", "user.name", "github-actions[bot]"], check=True, cwd=repo_root)
    subprocess.run(["git", "add", str(log_file.relative_to(repo_root))], check=True, cwd=repo_root)
    subprocess.run(["git", "commit", "-m", f"log: bootstrap {status} {ts}"], check=True, cwd=repo_root)
    subprocess.run(["git", "push"], check=True, cwd=repo_root)
    print(f"Log committed: {log_file.relative_to(repo_root)}", flush=True)


def main():
    log("=== sad-ingest bootstrap v5 starting ===")
    creds = load_creds()
    drive = build("drive", "v3", credentials=creds, cache_discovery=False)

    try:
        log("Step 1: probe SA Drive write to 02-Inbox (diagnostic)")
        probe = probe_drive_write(drive)
        log(f"  {probe}")

        log("Step 2: export KEYS-REPOSITORY via Drive API")
        text = fetch_keys_doc_text(drive)
        log(f"  got {len(text)} chars")

        log("Step 3: extract PAT and ANTHROPIC_API_KEY")
        pat = extract_pat(text)
        anth = extract_anthropic_key(text)
        sa_json = os.environ["GOOGLE_SA_JSON"]
        log(f"  PAT: {pat[:7]}...{pat[-4:]}")
        log(f"  ANTH: {anth[:15]}...{anth[-4:]}")
        log(f"  SA_JSON: {len(sa_json)} chars")

        log("Step 4: fetch sad-ingest repo public key")
        session = gh_session(pat)
        pubkey = get_public_key(session, TARGET_REPO)
        log(f"  key_id: {pubkey['key_id']}")

        log(f"Step 5: set secrets on {TARGET_REPO}")
        set_secret(session, TARGET_REPO, "ANTHROPIC_API_KEY", anth, pubkey)
        set_secret(session, TARGET_REPO, "GOOGLE_SA_JSON", sa_json, pubkey)

        log(f"Step 6: verify secrets exist on {TARGET_REPO}")
        names = list_secrets(session, TARGET_REPO)
        log(f"  secrets present: {names}")
        if "ANTHROPIC_API_KEY" not in names or "GOOGLE_SA_JSON" not in names:
            raise RuntimeError(f"verification FAILED, only saw {names}")
        log("  both secrets present and visible")

        log("Step 7: trigger first sad-ingest workflow run")
        trigger_workflow(session, TARGET_REPO, "sad-ingest.yml")

        log("=== bootstrap complete ===")
        write_log_to_repo("SUCCESS")

    except Exception as e:
        tb = traceback.format_exc()
        log(f"FAILED: {type(e).__name__}: {e}")
        log(tb)
        try:
            write_log_to_repo("FAILURE")
        except Exception as e2:
            print(f"Could not write log: {e2}", flush=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
