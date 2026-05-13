# PATTERNS - Index

Last restructured: 2 May 2026 as part of the memory architecture migration.

This document is the entry point. All patterns moved to 5 thematic files. The original PATTERN content is now distributed across the files below. This doc retains its original ID so existing references continue to resolve.

## File Map

- **PATTERNS-OPERATIONS** (`1DNU3wTPWvY8AoPGfk0YRCKcgh3phIEBQ-Z7331Vj8PI`) - daily workflow patterns
- **PATTERNS-DOCUMENTS** (`1WXs_8ogoVrumuyN0ueY5B4ew_tzwBaQ0PAejUYNeurk`) - DOCX and PPTX standards
- **PATTERNS-WEBAPPS** (`1da7H-VBDQnX0_ldD6fF6nXjWYnJEhdZfFwKBQ72w6ro`) - web and SaaS deployment plus UI patterns
- **PATTERNS-STRATEGIC** (`11ddVlIuCi8YAslcoqK-2uy1j-MeQXisvO4xkeIN7auU`) - SAD and Hegemony Series specific patterns
- **PATTERNS-INFRA** (`1juBBHLyUZpuzG4ZcnWJxFzwDlWFP4gFwB1yCPzw_0Mk`) - auth, secrets, deployment infrastructure

## Pattern Index (sorted by number)

| # | Title | Lives in |
|---|-------|----------|
| 1 | DOCX Document Generation | PATTERNS-DOCUMENTS |
| 2 | Netlify Deployment | PATTERNS-WEBAPPS |
| 3 | Google Drive Operations | PATTERNS-OPERATIONS |
| 4 | Strategic Analysis Documents (legacy v1) | PATTERNS-DOCUMENTS |
| 5 | Supabase Keepalive | PATTERNS-INFRA |
| 6 | PayPal Smart Buttons Integration | PATTERNS-WEBAPPS |
| 7 | PPTX McKinsey-Quality Upgrade | PATTERNS-DOCUMENTS |
| 8 | Single-File React App Architecture | PATTERNS-WEBAPPS |
| 9 | Excel File Verification | PATTERNS-OPERATIONS |
| 10 | Writing Task Startup Sequence | PATTERNS-OPERATIONS |
| 11 | Three.js Interactive Visualization Deployment | PATTERNS-WEBAPPS |
| 12 | Gmail / Contact Database Building | PATTERNS-OPERATIONS |
| 13 | Model Selection Decision | PATTERNS-OPERATIONS |
| 14 | DOCX Generation Validation Workflow | PATTERNS-DOCUMENTS |
| 15 | Auto-filing Outputs to GROUP-OUTPUTS | PATTERNS-OPERATIONS |
| 16 | Website SEO Launch Standards | PATTERNS-WEBAPPS |
| 17 | Forensic / Verification Document Style | PATTERNS-DOCUMENTS |
| 18 | Strategic Report DOCX Standard (locked 2 May 2026) | PATTERNS-DOCUMENTS |
| 19 | Session Checkpoint Routine (locked 2 May 2026) | PATTERNS-OPERATIONS |
| 20 | Self-Contained E2E Test Runner | PATTERNS-WEBAPPS |
| 21 | Adjacent-Pattern Sweep at End of Fix-Session | PATTERNS-OPERATIONS |
| 22 | Proactive Audit-Mode for Open-Ended Reviews + Acorn AST-Walking | PATTERNS-OPERATIONS |
| 23 | Netlify Boost Cache Profile | PATTERNS-WEBAPPS |
| 24 | AI Image Generation for Report Covers | PATTERNS-STRATEGIC |
| 25 | SAD Report/Brief Publishing Pipeline | PATTERNS-STRATEGIC |
| 26 | Featured-Card Square-Cover Layout | PATTERNS-WEBAPPS |
| 27 | Military-Insignia Category Badges | PATTERNS-WEBAPPS |
| 28 | Impressum / Imprint Modal Pattern (formerly Pattern 18 variant) | PATTERNS-WEBAPPS |
| 29 | IFB Group Website Build Recipe (formerly Pattern 19 variant) | PATTERNS-WEBAPPS |
| 30 | Fly.io fly.toml Regeneration Memory Trap | PATTERNS-INFRA |
| 31 | TradingAgents Model Whitelist Silent Hang / Rube-Composio Migration | PATTERNS-WEBAPPS / PATTERNS-INFRA |
| 32 | LangGraph Parallel Agents Break Anthropic tool_use Invariant | PATTERNS-WEBAPPS |
| 33 | CORS DELETE Preflight Requires Explicit allow_methods / GitHub Relay for Drive Upload | PATTERNS-WEBAPPS / PATTERNS-INFRA |
| 34 | Single-Repo Multi-Site Netlify Monorepo | PATTERNS-WEBAPPS |
| 35 | Sandbox Egress Allowlist + Found-Credential Hygiene | PATTERNS-INFRA |

## Notes on Pattern Numbering

Pattern 19 had three variants in the legacy library: a Python brace-matcher (dropped, superseded by Pattern 22 Acorn AST), a Website Build Recipe (preserved as Pattern 29 in PATTERNS-WEBAPPS), and the Session Checkpoint Routine (locked 2 May 2026, the canonical Pattern 19 in PATTERNS-OPERATIONS).

Pattern 18 had three variants: an early Impressum/Imprint pattern (preserved as Pattern 28 in PATTERNS-WEBAPPS), the Modal Variant + Nurdug refinement (folded into Pattern 28), and the Strategic Report DOCX Standard (locked 2 May 2026, the canonical Pattern 18 in PATTERNS-DOCUMENTS).

Pattern 22 had two variants: Proactive Audit-Mode and Acorn AST-Walking. Both kept and merged under Pattern 22 in PATTERNS-OPERATIONS, since Acorn explicitly supersedes the older Pattern 19 brace-matcher and the audit-mode methodology is complementary.

Total patterns indexed: 35+ (the library has grown since the 29-count restructure on 2 May 2026; this index reflects the current state at 13 May 2026).

## How to Use

1. Look up a pattern by number above to find which file it lives in.
2. Open the corresponding PATTERNS-* doc and search for `Pattern N:` to find the full content.
3. Memory entries that reference "PATTERNS-LIBRARY" still resolve here. Updated memory entries reference the specific PATTERNS-* file directly.

## Adding New Patterns

New patterns go in the appropriate thematic file (not this index) and then get registered here in the Pattern Index section. Numbers increment monotonically across the entire library to avoid future collisions.
