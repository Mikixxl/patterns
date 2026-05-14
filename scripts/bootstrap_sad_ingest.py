"""One-time bootstrap for sad-ingest repo secrets.

v2: uses Drive API files.export instead of Docs API (Docs API may not be
enabled on the patterns SA's GCP project). Drive API IS enabled because
patterns sync works.

Writes a log file to 02-Inbox at the end (success OR failure) so the
result is observable from Claude's sandbox via Composio without needing
api.github.com access.
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
    """Export the keys doc as plain text via Drive API (no Docs API required)."""
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
        raise RuntimeError("PAT not found in KEYS-REPOSITORY (looked for ghp_...)")
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
        raise RuntimeError(f"public-key fetch failed: HTTP {r.status_code} {r.text[:200]}")
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
        raise RuntimeError(f"set_secret {name} failed: HTTP {r.status_code} {r.text[:200]}")
    log(f"  set_secret {name}: HTTP {r.status_code}")


def trigger_workflow(session, repo: str, workflow_file: str) -> None:
    r = session.post(
        f"{GH_API}/repos/{repo}/actions/workflows/{workflow_file}/dispatches",
        json={"ref": "main"},
    )
    if r.status_code != 204:
        raise RuntimeError(f"dispatch failed: HTTP {r.status_code} {r.text[:200]}")
    log(f"  dispatch {workflow_file}: HTTP {r.status_code}")


def write_log_to_drive(drive, status: str, body: str) -> None:
    """Write a log file to 02-Inbox so result is observable from sandbox."""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H%M%S")
    name = f"BOOTSTRAP-LOG-{status}-{ts}.txt"
    body_bytes = body.encode("utf-8")
    media = MediaIoBaseUpload(io.BytesIO(body_bytes), mimetype="text/plain", resumable=False)
    metadata = {"name": name, "parents": [INBOX_FOLDER_ID]}
    f = drive.files().create(body=metadata, media_body=media, fields="id,name").execute()
    print(f"Log written to Drive: {f['name']} (id={f['id']})", flush=True)


def main():
    log("=== sad-ingest bootstrap v2 starting ===")
    creds = load_creds()
    drive = build("drive", "v3", credentials=creds, cache_discovery=False)

    try:
        log("Step 1: export KEYS-REPOSITORY via Drive API")
        text = fetch_keys_doc_text(drive)
        log(f"  got {len(text)} chars")

        log("Step 2: extract PAT and ANTHROPIC_API_KEY")
        pat = extract_pat(text)
        anth = extract_anthropic_key(text)
        sa_json = os.environ["GOOGLE_SA_JSON"]
        log(f"  PAT: {pat[:7]}...{pat[-4:]}")
        log(f"  ANTH: {anth[:15]}...{anth[-4:]}")
        log(f"  SA_JSON: {len(sa_json)} chars")

        log("Step 3: fetch sad-ingest repo public key")
        session = gh_session(pat)
        pubkey = get_public_key(session, TARGET_REPO)
        log(f"  key_id: {pubkey['key_id']}")

        log(f"Step 4: set secrets on {TARGET_REPO}")
        set_secret(session, TARGET_REPO, "ANTHROPIC_API_KEY", anth, pubkey)
        set_secret(session, TARGET_REPO, "GOOGLE_SA_JSON", sa_json, pubkey)

        log("Step 5: trigger first sad-ingest workflow run")
        trigger_workflow(session, TARGET_REPO, "sad-ingest.yml")

        log("=== bootstrap complete ===")
        write_log_to_drive(drive, "SUCCESS", "\n".join(log_lines))

    except Exception as e:
        tb = traceback.format_exc()
        log(f"FAILED: {e}")
        log(tb)
        write_log_to_drive(drive, "FAILURE", "\n".join(log_lines))
        sys.exit(1)


if __name__ == "__main__":
    main()
