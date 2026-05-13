# PATTERNS-OPERATIONS

**Scope:** Workflow patterns for daily operations: Drive operations, Gmail/Excel handling, model selection, auto-filing outputs, session checkpoints, audit methodology.

**Patterns in this file:** 9

Created 2 May 2026 as part of memory architecture migration. Patterns extracted from the original PATTERNS-LIBRARY (`1LvMjwluhsQMftiV0IpvLZPpH1_knRkC3utHMrYvjpSA`, now PATTERNS-INDEX).

---

## Pattern 3: Google Drive Operations

Read vault files (cheap - no Rube needed): `google_drive_search` → `google_drive_fetch`

Write new docs (2 tool calls via Rube): `GOOGLEDOCS_CREATE_DOCUMENT_MARKDOWN` → `GOOGLEDRIVE_MOVE_FILE`

Move file correctly:
- `add_parents = destination_folder_id`
- `remove_parents = source_folder_id` (`0AMEEbnIjsU8AUk9PVA` for My Drive root)
- NEVER use `folder_id` parameter

2nd Brain folder IDs (memorize these):
- Root: `1lBhyv3-vSUeMQTT_tmXi40-XFjUPwmur`
- 01-Context: `1zHr4WonNsF_U_5bllrcrRsNtBXvETUKx`
- 05-Resources: `1jkAR41f6QB8oQs3HX-TdM5go5ckt7EW9`
- 06-Daily-Notes: `1lamaoGQ0UOufiIfsOC3ZVoUptTWNNNom`

---

## Pattern 9: Excel File Verification (detecting fake data)

Quick verification script:

```python
import openpyxl
wb = openpyxl.load_workbook(filepath)
for ws in wb.worksheets:
    for row in ws.iter_rows(min_row=1, max_row=min(ws.max_row, 30), values_only=True):
        print([str(c)[:70] if c else '' for c in row])
```

Red flags for fabricated data:
- US 555 phone numbers
- Sequential algorithmic email patterns (`name1@domain1.com`, `name2@domain2.com`)
- Arithmetically incremented numeric fields (100, 101, 102...)
- All companies follow identical naming patterns

---

## Pattern 10: Writing Task Startup Sequence

Before any writing task:
1. Fetch Writing Guardrails: `google_drive_fetch(["1EGu4QCi27yhabbIJlXFYvrKiQgvgUrtFaZ5YXRnxXTc"])`
2. Fetch Text DNA Bible: `google_drive_fetch(["1GpDT6VAGQ8LFhcDyScBbMU67ooQvP3n9M79GqNaFRfA"])`
3. Apply both: Guardrails remove synthetic habits; Text DNA Bible defines the positive voice.
4. Check 02-Inbox for any unsorted Brain Dump items relevant to the task.

Voice signature: intellectually serious, high-register, forceful without theatrical excess. Douglas Murray influence: dry wit, short punchy sentences after longer analytical ones, rhetorical confidence, concrete over abstract.

---

## Pattern 12: Gmail / Contact Database Building

Verified contact extraction from Gmail:
1. Search sent: `in:sent subject:(onboarding OR "account opening" OR KYC) has:attachment`
2. Search inbox for received correspondence with date filters.
3. Read individual messages via `gmail_read_message` to confirm context.
4. Fetch contact pages directly (vital-cap.com/contact-vital-capital) - more reliable than homepage for emails.
5. Web search combining domain name with "contact email" for confirmed addresses.

Fraud flagging: cross-reference with Trustpilot and search patterns before including in database.

---

## Pattern 13: Model Selection Decision

**Opus for:**
- Strategic analysis and geopolitical documents
- Complex multi-step reasoning
- High-quality writing tasks requiring Douglas Murray voice
- New project architecture decisions
- Vault maintenance and knowledge organization

**Sonnet for:**
- Daily notes and inbox sorting
- Simple file creation and moves
- Web searches
- Calendar and email tasks
- Straightforward document edits
- RegMantle blog auto-generation

---

## Pattern 15: Auto-filing Outputs to GROUP-OUTPUTS (STANDING RULE)

This is a standing instruction. Every finished document produced in any session must be filed to the correct GROUP-OUTPUTS subfolder in Drive as the final step. No exceptions.

**Filing decision:** identify the entity the document belongs to, then the document type. Move using `GOOGLEDRIVE_MOVE_FILE` with `add_parents = correct subfolder ID` and `remove_parents = current parent`.

**Document type mapping:**
- DOCX reports, legal opinions, compliance docs, briefings, policies → Documents
- PPTX presentations, pitch decks, investor decks, slide decks → Presentations
- Strategic analysis, geopolitical advisories, threat assessments, intelligence docs → Strategic-Analysis
- Websites, landing pages, brochures, social content, SEO → Marketing
- Financial models, calculators, budgets, investment docs, P&L → Financial
- Legal opinions, contracts, licenses, compliance frameworks → Legal

**Entity assignment:**
- Any document branded IFB Bank / Banque Financiere / AOFA license → IFB International Finance Bank LTD
- IMEC investor portal, IFBH content → IFBH GmbH - Berlin
- IFC consulting presentations, certification platform → IFC International Finance Corporation LLC
- RegMantle documents → IFC International Finance Corporation LLC (RegMantle is an IFC product)
- Strategic analysis documents → SAD Strategic Analysis Division
- Personal legal/financial → _Personal - Von Schoenborn
- Beaufort / TERA / NURDUG / EnergyFlow → their respective entity folders

**GROUP-OUTPUTS entity folder IDs:**
- IFB International Finance Bank LTD: `12yVuQaZq1F49-AGMXgWn_zM6qQ-EggwH`
- IFBH GmbH - Berlin: `178EVy4ORVzpyjO_OeY8yz0oNsKJvlB2t`
- IFC Holdings LLC - Miami: `1qLhQa_R3_Bh1DtM4XT5eT2iePQgU9tvT`
- IFC International Finance Corporation LLC: `1RqbVN1tiIQ6jz6rd098TpO1nJlaixCuU`
- International Finance Corporation LTD Israel: `1fUbXGDW4HsInsW9CNwPiNXyAlOr4Rryd`
- IFB Holdings LLC - Miami: `1HOo1axBbBR1P7aNF_9qgpq2vRxOaIVw5`
- Beaufort Securitisation Holdings LLC: `1QnEkq1TN8AE88krH4WOjJr2qLtfEBgpZ`
- TERA AG: `1CXA1rNKc25YBHZtWVONOGum-CPRrDs4d`
- NURDUG AG: `1-c1DaBGJnUrHFFWkoLf_bDVNkcCOnmyi`
- EnergyFlow GmbH: `15youfboBqC7Ivv5PkdOvOx4NYUSX3Xo0`
- SAD Strategic Analysis Division: `1ve7kWDQkZiWq-2LZwGbC5mb2U6iDf0EC`
- _Personal - Von Schoenborn: `1dzV2H1C4kopu8krrV97gKrXYYQVk0Fmx`

Subfolder IDs per entity follow the pattern: each entity folder above contains 6 subfolders (Documents, Presentations, Strategic-Analysis, Marketing, Financial, Legal). The full subfolder map is stored in the GROUP-OUTPUTS section of the Entity Bible (doc ID `1UIn5RveY4OayAW7jmDfS0jDGsahKroITn6P-mu7Im6I`).

**Filing workflow (every session end):**
1. Identify all documents produced this session.
2. For each: determine entity + document type.
3. Create Google Doc via `GOOGLEDOCS_CREATE_DOCUMENT_MARKDOWN` OR upload file via `GOOGLEDRIVE_UPLOAD_FILE`.
4. Move to correct subfolder via `GOOGLEDRIVE_MOVE_FILE`.
5. Note in daily note what was filed and where.

**Constraint:** the Rube remote workbench cannot access Claude's container filesystem (`/home/claude/` or `/mnt/user-data/`). Binary files (DOCX, PPTX, PDF, PNG) must be uploaded by Michael directly to Drive. Google Docs (text/markdown content) can be created and filed fully automatically by Claude via `GOOGLEDOCS_CREATE_DOCUMENT_MARKDOWN` + `GOOGLEDRIVE_MOVE_FILE`.

*Added 6 April 2026 as standing instruction.*

---

## Pattern 19: Session Checkpoint Routine (locked 2 May 2026)

**Problem solved:** Anthropic-side context compaction strikes without warning and sometimes drops operationally critical small details (recent file IDs, URLs, debug findings, mid-task decisions). The compaction summary is good but not perfect.

**Solution:** at every natural milestone Claude writes a checkpoint to the 09-Session-Checkpoints folder (root ID `1jJj1Dc5KtpolKFV8KmJ-cxMO6LXN4CI2`) in 2nd Brain. On subsequent sessions, when context is compacted or a new chat begins, Claude reads the latest checkpoint to recover full operational state.

### Trigger Events (dynamic, not fixed cadence)

Write a checkpoint at the END of any of these milestones:
1. Document delivered (DOCX, PPTX, PDF, XLSX, code file uploaded)
2. Pattern codified or updated in Patterns Library
3. Module deployed or made live (Netlify push, GitHub commit, Supabase migration)
4. API key, credential, or new resource added to KEYS-REPOSITORY
5. Strategic decision locked (e.g. "use OpenAI gpt-image-2 for figures")
6. Significant tool failure or recovery (anything that would be valuable to remember if context is lost)
7. End of substantial topic (when conversation pivots to a new theme)
8. Memory edit modified (any add/replace/remove)

Do NOT write a checkpoint for every minor turn - only milestones. Aim for one checkpoint every 4-8 substantive Claude turns under normal pace, more often if many milestones cluster.

### Checkpoint File Format

File naming: `SESSION-CHECKPOINT-YYYY-MM-DD-HHMM.md` (UTC time, monotonically sortable).

File type: native Google Doc (`mimeType application/vnd.google-apps.document`) for in-Drive readability, OR plain markdown text file.

Contents (markdown):

```
Session Checkpoint - [YYYY-MM-DD HHMM UTC]

Active Topic
[1-2 sentence description of what we are working on right now]

Decisions This Session
- [bulleted list of locked decisions since session start, with timestamps]

Files / Resources Delivered
- [Filename | URL | Date | One-line description] for each deliverable

Open Items
- [Active to-dos that are NOT yet locked or delivered]

Trigger That Created This Checkpoint
[Brief: what milestone triggered this checkpoint write]

Carry-Forward Notes
[Anything weird, edge cases, debug findings, or operational details that a fresh-context Claude would otherwise miss. THIS IS THE MOST IMPORTANT FIELD.]
```

### Recovery Protocol (fresh session or post-compaction)

First action when starting a new session OR detecting compaction in current session:
1. Search 09-Session-Checkpoints folder for the most recent checkpoint by date in filename.
2. Read its full contents.
3. Internally reconstruct active state from Active Topic, Open Items, Carry-Forward Notes.
4. Mention to Michael in first response: "Loaded checkpoint from [date], picking up at [active topic]".

### Tooling

Write via `GOOGLEDRIVE_CREATE_FILE_FROM_TEXT` (`mime_type=application/vnd.google-apps.document`, `parent_id=1jJj1Dc5KtpolKFV8KmJ-cxMO6LXN4CI2`). Read via `GOOGLEDOCS_GET_DOCUMENT_PLAINTEXT`.

### Token Cost

Approx 200-400 tokens per checkpoint write. Acceptable cost for compaction-resilience. Aim for compact prose, not narrative bloat.

### Edge Case: Dual-Write Protection

If Michael interrupts a long-running task (e.g. builds out a new direction mid-session), Claude writes a checkpoint immediately even if no other milestone has been hit. The interrupt itself counts as Trigger 7 (topic pivot).

### History

Pattern 19 created 2 May 2026 after Doc II compaction event lost mid-session details (figure-quality experimentation results, billing diagnostics). Memory pointer in slot replacing less-critical entry. Folder 09-Session-Checkpoints created same date, ID above.

---

## Pattern 21: Adjacent-Pattern Sweep at End of Fix-Session (STANDING RULE)

Before declaring any bug fix, refactor, or feature commit done, run a 5-minute scan for adjacent instances of the same pattern across the rest of the codebase. The fix never lives in isolation. If `renderDashboard` needs try-catch, the other 23 render functions probably do too. If `vendor-inquiry` has unsafe `JSON.parse`, four other Netlify functions likely have it. The first instance found is rarely the only instance.

**Workflow at end of every fix session:**
1. Take the bug-pattern that was fixed and translate it into a one-liner detection script (grep regex, AST query, or shell pipeline).
2. Run it against the whole repo. Capture every hit.
3. If scope permits in this session, fix all hits. Same commit or sibling commits with own stable-tag.
4. If scope does not permit, file each remaining hit as a separate Reminder in the Arbeit list with the same priority class as the original bug.
5. Mention in the commit message: "X other instances of this pattern found - filed as Reminders for follow-up" or "X other instances also fixed in this commit".

This rule prevents the recurring problem of finding the same bug class across multiple sessions instead of in one. The discipline is mechanical: every fix triggers a sweep. No exceptions for trivial fixes - even a one-character typo fix can have adjacent instances.

Do not ask Michael whether to do this sweep. It runs by default at the end of every fix-session. Michael only sees the output: a list of additional findings, either fixed in-line or filed as Reminders.

---

## Pattern 22: Proactive Audit-Mode for Open-Ended Reviews + Acorn AST-Walking (STANDING RULE)

When Michael's prompt is open-ended on a codebase - phrasings like "bug hunt", "review the code", "QA pass", "what should I worry about", "go in as a client", "audit this" - default to categorical detection scans across the repo, not manual tab-by-tab inspection. The categorical approach finds 5-10x more real bugs in a fraction of the time.

**Run all 8 detection categories in parallel as the first action:**
1. Render functions without try-catch wrap.
2. `JSON.parse(event.body)` without try-catch in Netlify functions.
3. Hardcoded English UI strings inside render functions.
4. `innerHTML` concatenation with user-input fields without `escapeHTML`.
5. Async window handlers without disabled-button pattern.
6. `console.log` calls left in production index.html or equivalent.
7. Admin endpoints without proper Supabase JWT validation.
8. Missing CORS headers on 4xx/5xx error responses (browser-facing only).

For non-Nuptelle repos, adapt the categories to that stack but keep the same 8-axis coverage: error-handling, input-validation, i18n, XSS, double-submit, debug-leaks, auth, CORS. The principle generalizes.

After the scan, output a priority list: **HIGH** = security/PII, **MED** = resilience/i18n, **LOW** = UX polish. File each finding as a separate Reminder. Do not start fixing until Michael picks the next target - the audit's deliverable is the list, not the fix.

Audit-mode is the DEFAULT for open-ended reviews. Michael does not need to ask for it explicitly. If a prompt is ambiguous between "please fix this one bug I noticed" and "please tell me what else is broken", run the audit first then propose the priority list.

Do not run audit-mode for scoped requests. If Michael says "fix QA1 and QA2", that is scope-discipline - execute exactly that, run only the Pattern 21 adjacent-sweep at end, do not expand into a full audit unless asked.

### Acorn AST-Walking for JS Refactoring (supersedes Pattern 19's brace counter)

Pattern 19's hand-written brace counter is unreliable on real-world code. Concrete failure observed in nuptelle index.html on 2026-04-28: `openRsvpShareModal` closes at L11752 but the Python brace-matcher matched L12482, walking past three intervening top-level functions. Cause was almost certainly an unhandled edge case around HTML-string template literals containing dollar-sign-brace expressions whose nested code blocks the matcher mis-counted. Debug time would have exceeded the rebuild time, so a parser-based replacement was built.

The replacement pattern uses **acorn** (`npm install acorn`, currently 8.16.0) to parse each inline script block and extract exact AST byte ranges. Acorn handles every JavaScript edge case correctly: template literals, nested template-expression code blocks, regex literals, all comment forms, escape sequences, JSX-adjacent syntax, async generators. The transform code only needs to know the AST shape it is looking for.

**Reference workflow** (from Bug 7, commit `920e2ce` in nuptelle):
1. Read whole HTML file once.
2. Find every inline script block.
3. Parse each through acorn.
4. Walk the AST to find target nodes by shape (e.g. `FunctionDeclaration` named `openRsvpShareModal`).
5. Extract exact `start`/`end` byte offsets.
6. Splice the new content at those byte boundaries.
