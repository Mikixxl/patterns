"""
Auto-sync the Patterns Library from Google Drive to this repo.

For each canonical pattern doc, export it as markdown via the Drive API
and write to the corresponding local file. The CI workflow handles git
commit/push afterward.

Authentication: a service account JSON blob in the GOOGLE_SA_JSON env
var. The service account email must have Viewer access to every doc
ID listed in PATTERN_DOCS (share each doc from Drive UI).

This script is intentionally narrow: it touches only the six mapped
files. README.md and anything else in the repo are left alone.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

PATTERN_DOCS: dict[str, str] = {
    "PATTERNS.md":            "1LvMjwluhsQMftiV0IpvLZPpH1_knRkC3utHMrYvjpSA",
    "PATTERNS-OPERATIONS.md": "1DNU3wTPWvY8AoPGfk0YRCKcgh3phIEBQ-Z7331Vj8PI",
    "PATTERNS-DOCUMENTS.md":  "1WXs_8ogoVrumuyN0ueY5B4ew_tzwBaQ0PAejUYNeurk",
    "PATTERNS-WEBAPPS.md":    "1da7H-VBDQnX0_ldD6fF6nXjWYnJEhdZfFwKBQ72w6ro",
    "PATTERNS-STRATEGIC.md":  "11ddVlIuCi8YAslcoqK-2uy1j-MeQXisvO4xkeIN7auU",
    "PATTERNS-INFRA.md":      "1juBBHLyUZpuzG4ZcnWJxFzwDlWFP4gFwB1yCPzw_0Mk",
}

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


def load_credentials() -> service_account.Credentials:
    raw = os.environ.get("GOOGLE_SA_JSON", "").strip()
    if not raw:
        sys.exit("GOOGLE_SA_JSON env var is empty or missing")
    try:
        info = json.loads(raw)
    except json.JSONDecodeError as exc:
        sys.exit(f"GOOGLE_SA_JSON is not valid JSON: {exc}")
    return service_account.Credentials.from_service_account_info(
        info, scopes=SCOPES
    )


def export_markdown(service, doc_id: str) -> str:
    """Export a Google Doc as text/markdown via the Drive API."""
    request = service.files().export(fileId=doc_id, mimeType="text/markdown")
    raw = request.execute()
    if isinstance(raw, bytes):
        return raw.decode("utf-8")
    return raw


def render(doc_id: str, body: str) -> str:
    """Prepend a canonical header so the file is self-explanatory."""
    header = (
        f"<!-- AUTO-SYNCED FROM GOOGLE DRIVE - DO NOT EDIT HERE.\n"
        f"     Source doc: https://docs.google.com/document/d/{doc_id}/edit\n"
        f"     Sync script: scripts/sync.py -->\n\n"
    )
    return header + body.lstrip()


def main() -> int:
    creds = load_credentials()
    service = build("drive", "v3", credentials=creds, cache_discovery=False)
    repo_root = Path(__file__).resolve().parent.parent

    updated: list[str] = []
    errors: list[str] = []

    for filename, doc_id in PATTERN_DOCS.items():
        target = repo_root / filename
        try:
            body = export_markdown(service, doc_id)
        except HttpError as exc:
            print(f"ERROR: fetching {filename} ({doc_id}): {exc}")
            errors.append(filename)
            continue
        except Exception as exc:  # noqa: BLE001
            print(f"ERROR: unexpected for {filename} ({doc_id}): {exc}")
            errors.append(filename)
            continue

        if not body.strip():
            print(f"WARN: empty body for {filename}, skipping write")
            errors.append(filename)
            continue

        new_text = render(doc_id, body)
        if target.exists() and target.read_text(encoding="utf-8") == new_text:
            print(f"OK   {filename}: unchanged")
            continue

        target.write_text(new_text, encoding="utf-8")
        updated.append(filename)
        print(f"OK   {filename}: updated")

    print()
    print(f"Updated: {len(updated)} file(s)")
    if updated:
        for f in updated:
            print(f"  + {f}")
    if errors:
        print(f"Errors:  {len(errors)} file(s)")
        for f in errors:
            print(f"  ! {f}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
