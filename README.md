# Patterns

Operational pattern library for the IFB/SAD entity group. Mirror of the Google Drive canonical source.

## Structure

| File | Scope | Patterns |
|------|-------|----------|
| [PATTERNS.md](./PATTERNS.md) | Index - lookup by pattern number, links to thematic files | 29 cataloged |
| [PATTERNS-OPERATIONS.md](./PATTERNS-OPERATIONS.md) | Daily workflow patterns (Drive ops, model selection, audits, checkpoints) | 9 |
| [PATTERNS-DOCUMENTS.md](./PATTERNS-DOCUMENTS.md) | DOCX and PPTX standards (strategic reports, forensic docs, validation) | 6 |
| [PATTERNS-WEBAPPS.md](./PATTERNS-WEBAPPS.md) | Web and SaaS deployment, UI patterns, SEO baseline, legal modals | 11+ |
| [PATTERNS-STRATEGIC.md](./PATTERNS-STRATEGIC.md) | SAD-specific patterns (covers, publishing pipeline, stock-flow framing) | 5 |
| [PATTERNS-INFRA.md](./PATTERNS-INFRA.md) | Auth, secrets, deployment infra (Fly, Composio migration, GitHub relay) | 3+ |

## Source of truth

Google Drive is canonical. This repo is a snapshot mirror, refreshed daily by GitHub Actions. To edit a pattern, update the Drive doc - the next sync run pulls the change here automatically. Do not edit the `PATTERNS-*.md` files in this repo directly; auto-sync will overwrite them.

| Local file | Drive doc ID |
|------------|--------------|
| PATTERNS.md | `1LvMjwluhsQMftiV0IpvLZPpH1_knRkC3utHMrYvjpSA` |
| PATTERNS-OPERATIONS.md | `1DNU3wTPWvY8AoPGfk0YRCKcgh3phIEBQ-Z7331Vj8PI` |
| PATTERNS-DOCUMENTS.md | `1WXs_8ogoVrumuyN0ueY5B4ew_tzwBaQ0PAejUYNeurk` |
| PATTERNS-WEBAPPS.md | `1da7H-VBDQnX0_ldD6fF6nXjWYnJEhdZfFwKBQ72w6ro` |
| PATTERNS-STRATEGIC.md | `11ddVlIuCi8YAslcoqK-2uy1j-MeQXisvO4xkeIN7auU` |
| PATTERNS-INFRA.md | `1juBBHLyUZpuzG4ZcnWJxFzwDlWFP4gFwB1yCPzw_0Mk` |

## Auto-sync

The workflow at `.github/workflows/sync-patterns.yml` runs daily at 05:00 UTC and can also be triggered manually from the Actions tab. It calls `scripts/sync.py`, which:

1. Authenticates to Drive via a service account JSON stored as a GitHub secret (`GOOGLE_SA_JSON`).
2. Exports each canonical doc as `text/markdown` via the Drive API.
3. Writes the result to the corresponding local file, prefixed with an "auto-synced - do not edit" header.
4. Commits and pushes only if anything changed.

The script touches only the six mapped files. `README.md` and anything else are left alone.

### One-time setup

Required once, then the workflow runs autonomously:

1. **Create a service account.** In Google Cloud Console, pick or create any project. Enable the Google Drive API. Create a service account, then under "Keys" generate a new JSON key and download it.
2. **Add the secret.** In this repo: Settings → Secrets and variables → Actions → New repository secret. Name: `GOOGLE_SA_JSON`. Value: the full contents of the JSON key file.
3. **Share the six docs.** For each of the six Drive doc IDs in the table above, open the doc, click Share, paste the service account email (looks like `name@project-id.iam.gserviceaccount.com`), set role to Viewer, untick "Notify people", and Share.
4. **Trigger a first run.** Actions tab → "Sync Patterns from Drive" → Run workflow. Confirm it commits the first auto-synced versions of the six files. After that, the daily cron handles the rest.

If the service account key is ever rotated or revoked, regenerate it in Google Cloud and update the `GOOGLE_SA_JSON` secret. No other change needed.

## Naming convention

Patterns are numbered monotonically across the entire library (1-35+). When a pattern moves between thematic files, the number stays the same and the index file routes lookups. New patterns get the next free number and are registered in the index.

## History

- 2 May 2026: original PATTERNS-LIBRARY split into the five thematic files plus index.
- 13 May 2026: snapshot mirror established at github.com/Mikixxl/patterns.
- 13 May 2026: auto-sync via GitHub Actions cron live.
