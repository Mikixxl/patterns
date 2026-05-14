"""Read KEYS-REPOSITORY from Drive, extract credentials, output as shell env vars.

Designed to be sourced by a bash step. Outputs to stdout in `KEY=VALUE` form
suitable for `source` or `eval`. Values are shell-escaped via printf %q.

Reads from KEYS-REPOSITORY using the patterns SA (granted Viewer access),
extracts the canonical GitHub PAT and the general-purpose Anthropic API key,
writes them as EXTRACTED_PAT and EXTRACTED_ANTHROPIC variables.

Status messages go to stderr so stdout stays clean for sourcing.
"""
from __future__ import annotations

import json
import os
import re
import shlex
import sys

from google.oauth2 import service_account
from googleapiclient.discovery import build

KEYS_DOC_ID = "1xqpAZLGtYku4_wMatPRabOHrTb6e1TRWCJJNorNDb1Q"
SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/documents.readonly",
]


def log(msg: str) -> None:
    print(msg, file=sys.stderr)


def load_docs_service():
    raw = os.environ.get("GOOGLE_SA_JSON", "")
    if not raw:
        sys.exit("GOOGLE_SA_JSON env var empty in extraction script")
    info = json.loads(raw)
    creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    return build("docs", "v1", credentials=creds, cache_discovery=False)


def fetch_doc_text(service, doc_id: str) -> str:
    doc = service.documents().get(documentId=doc_id).execute()
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


def main():
    log("Loading SA credentials...")
    service = load_docs_service()

    log("Fetching KEYS-REPOSITORY doc...")
    text = fetch_doc_text(service, KEYS_DOC_ID)
    log(f"  fetched {len(text)} chars")

    log("Extracting PAT...")
    pat_matches = re.findall(r"ghp_[A-Za-z0-9]{36,}", text)
    if not pat_matches:
        sys.exit("PAT not found")
    pat = pat_matches[0]
    log(f"  PAT: {pat[:7]}...{pat[-4:]}")

    log("Extracting ANTHROPIC API key...")
    ant_matches = re.findall(r"sk-ant-api03-[A-Za-z0-9_\-]{80,}", text)
    if not ant_matches:
        sys.exit("ANTHROPIC API key not found")
    anthropic_key = ant_matches[0]
    log(f"  ANTHROPIC: {anthropic_key[:15]}...{anthropic_key[-4:]}")

    # Emit shell-sourceable output to stdout
    print(f"EXTRACTED_PAT={shlex.quote(pat)}")
    print(f"EXTRACTED_ANTHROPIC={shlex.quote(anthropic_key)}")

    log("OK extraction complete")


if __name__ == "__main__":
    main()
