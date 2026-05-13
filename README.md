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

Google Drive is canonical. This repo is a snapshot mirror updated periodically. To edit a pattern, update the Drive doc first; the GitHub copy is regenerated from Drive.

| Local file | Drive doc ID |
|------------|--------------|
| PATTERNS.md | `1LvMjwluhsQMftiV0IpvLZPpH1_knRkC3utHMrYvjpSA` |
| PATTERNS-OPERATIONS.md | `1DNU3wTPWvY8AoPGfk0YRCKcgh3phIEBQ-Z7331Vj8PI` |
| PATTERNS-DOCUMENTS.md | `1WXs_8ogoVrumuyN0ueY5B4ew_tzwBaQ0PAejUYNeurk` |
| PATTERNS-WEBAPPS.md | `1da7H-VBDQnX0_ldD6fF6nXjWYnJEhdZfFwKBQ72w6ro` |
| PATTERNS-STRATEGIC.md | `11ddVlIuCi8YAslcoqK-2uy1j-MeQXisvO4xkeIN7auU` |
| PATTERNS-INFRA.md | `1juBBHLyUZpuzG4ZcnWJxFzwDlWFP4gFwB1yCPzw_0Mk` |

## Naming convention

Patterns are numbered monotonically across the entire library (1-35+). When a pattern moves between thematic files, the number stays the same and the index file routes lookups. New patterns get the next free number and are registered in the index.

## History

- 2 May 2026: original PATTERNS-LIBRARY split into the five thematic files plus index.
- 13 May 2026: snapshot mirror established at github.com/Mikixxl/patterns.

Last sync: 13 May 2026.
