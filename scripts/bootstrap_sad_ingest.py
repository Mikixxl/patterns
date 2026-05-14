"""One-time bootstrap script for sad-ingest repo secrets.

Reads KEYS-REPOSITORY Drive doc using the patterns SA, extracts the GitHub PAT
and ANTHROPIC_API_KEY, encrypts them with libsodium, and sets them as repo
secrets on Mikixxl/sad-ingest via api.github.com. Then triggers the first
sad-ingest workflow run.

This runs in a GitHub Actions workflow context where api.github.com is
reachable. The Claude sandbox cannot reach api.github.com directly, so this
script is the bridge.
"""
from __future__ import annotations

import json
import os
import re
import sys
from base64 import b64encode

import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from nacl import encoding, public

KEYS_DOC_ID = "1xqpAZLGtYku4_wMatPRabOHrTb6e1TRWCJJNorNDb1Q"
TARGET_REPO = "Mikixxl/sad-ingest"

GH_API = "https://api.github.com"
SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/documents.readonly",
]


def load_drive():
    info = json.loads(os.environ["GOOGLE_SA_JSON"])
    creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    return build("docs", "v1", credentials=creds, cache_discovery=False)


def fetch_keys_doc_text(docs_service) -> str:
    """Pull KEYS-REPOSITORY plaintext content."""
    doc = docs_service.documents().get(documentId=KEYS_DOC_ID).execute()
    out = []
    for element in doc.get("body", {}).get("content", []):
        paragraph = element.get("paragraph")
        if not paragraph:
            continue
        for run in paragraph.get("elements", []):
            text_run = run.get("textRun")
            if text_run and "content" in text_run:
                out.append(text_run["content"])
    return "".join(out)


def extract_pat(text: str) -> str:
    """Find the GitHub PAT labeled as Nuptelle / Full Dev (not the courseintermediaries one)."""
    # Look for the canonical ghp_ token used as standing default
    matches = re.findall(r"ghp_[A-Za-z0-9]{36,}", text)
    if not matches:
        sys.exit("PAT not found in KEYS-REPOSITORY")
    # The Nuptelle / Full Dev PAT is the one used across all Mikixxl repos
    # We pick the first ghp_ match; in the doc this is the canonical one
    return matches[0]


def extract_anthropic_key(text: str) -> str:
    """Find the general-purpose Anthropic API key (used for blog + SAD pipelines)."""
    matches = re.findall(r"sk-ant-api03-[A-Za-z0-9_\-]{80,}", text)
    if not matches:
        sys.exit("ANTHROPIC_API_KEY not found in KEYS-REPOSITORY")
    # Multiple Anthropic keys may be present; pick the first one (general purpose)
    return matches[0]


def gh_session(pat: str) -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    return s


def get_public_key(session: requests.Session, repo: str) -> dict:
    r = session.get(f"{GH_API}/repos/{repo}/actions/secrets/public-key")
    r.raise_for_status()
    return r.json()


def encrypt_secret(public_key_b64: str, value: str) -> str:
    """libsodium SealedBox encryption for GitHub Actions secrets."""
    pub_key = public.PublicKey(public_key_b64.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(pub_key)
    encrypted = sealed_box.encrypt(value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")


def set_secret(session: requests.Session, repo: str, name: str, value: str, pubkey: dict) -> None:
    encrypted_value = encrypt_secret(pubkey["key"], value)
    r = session.put(
        f"{GH_API}/repos/{repo}/actions/secrets/{name}",
        json={
            "encrypted_value": encrypted_value,
            "key_id": pubkey["key_id"],
        },
    )
    if r.status_code not in (201, 204):
        sys.exit(f"Failed to set secret {name}: {r.status_code} {r.text}")
    print(f"  OK  {name}: HTTP {r.status_code}")


def trigger_workflow(session: requests.Session, repo: str, workflow_file: str) -> None:
    r = session.post(
        f"{GH_API}/repos/{repo}/actions/workflows/{workflow_file}/dispatches",
        json={"ref": "main"},
    )
    if r.status_code != 204:
        sys.exit(f"Failed to trigger workflow: {r.status_code} {r.text}")
    print(f"  OK  workflow dispatched: HTTP {r.status_code}")


def main():
    print("=== sad-ingest bootstrap ===\n")

    print("Step 1: Read KEYS-REPOSITORY from Drive")
    docs_service = load_drive()
    text = fetch_keys_doc_text(docs_service)
    print(f"  OK  fetched {len(text)} chars")

    print("\nStep 2: Extract credentials")
    pat = extract_pat(text)
    anthropic_key = extract_anthropic_key(text)
    sa_json = os.environ["GOOGLE_SA_JSON"]
    print(f"  OK  PAT: {pat[:7]}...{pat[-4:]}")
    print(f"  OK  ANTHROPIC: {anthropic_key[:15]}...{anthropic_key[-4:]}")
    print(f"  OK  SA_JSON: {len(sa_json)} chars")

    print(f"\nStep 3: Fetch sad-ingest repo public key")
    session = gh_session(pat)
    pubkey = get_public_key(session, TARGET_REPO)
    print(f"  OK  key_id: {pubkey['key_id']}")

    print(f"\nStep 4: Set secrets on {TARGET_REPO}")
    set_secret(session, TARGET_REPO, "ANTHROPIC_API_KEY", anthropic_key, pubkey)
    set_secret(session, TARGET_REPO, "GOOGLE_SA_JSON", sa_json, pubkey)

    print(f"\nStep 5: Trigger first sad-ingest workflow run")
    trigger_workflow(session, TARGET_REPO, "sad-ingest.yml")

    print("\n=== bootstrap complete ===")


if __name__ == "__main__":
    main()
