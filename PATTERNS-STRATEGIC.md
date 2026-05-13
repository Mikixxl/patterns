# PATTERNS-STRATEGIC

Scope: SAD and Hegemony Series specific patterns - AI image generation for covers, SAD publishing pipeline, fact-checking, stock-flow consilience, wealth-preservation architecture.

Patterns in this file: 5

Created: 2 May 2026 as part of memory architecture migration.

Canonical Drive doc: `11ddVlIuCi8YAslcoqK-2uy1j-MeQXisvO4xkeIN7auU`

---

## Pattern 24: AI Image Generation for Report/Brief Covers

Added: 1 May 2026

When stock photography (Pexels, Unsplash) does not deliver topic-specific quality, generate cinematic covers via OpenAI image API. SAD aesthetic + workflow established.

### Models verified accessible (1 May 2026)
- `gpt-image-2-2026-04-21`: SOTA, requires verified org, ~$0.04/image, 60-180s generation time
- `dall-e-3` (hd quality): no verification needed, 30-60s generation, very reliable
- `gpt-image-1.5`, `dall-e-2`: legacy fallbacks
- Gemini Imagen 4 / `gemini-2.5-flash-image`: requires PAID tier (free quota = 0)

### SAD aesthetic prompt template

> "Cinematic photograph in the style of Denis Villeneuve. [topic-specific scene]. Dark navy ocean/sky transitioning to amber-gold horizon. Atmospheric haze. Long shadows. Volumetric lighting. Strategic geography aesthetic, formal and weighted, photorealistic. Sharp focus on [primary subject]. No text, no logos, no people [unless required], no captions, no watermarks."

### Standard sizes
- Featured-card cover (square): 1024x1024 with `quality=hd`
- Brief-card cover (16:9 horizontal): 1792x1024 with `quality=hd`
- Hero image (square): 1024x1024 with `quality=hd`
- Category badges (military insignia, square): 1024x1024 with `quality=hd`, then resize to 320x320 PNG

### Workflow
1. Generate via `api.openai.com/v1/images/generations` with `response_format=b64_json`
2. Optimize PNG → JPG via PIL: `quality=88-90, optimize=True, progressive=True` (90% size reduction)
3. Upload to Supabase `reports-public` bucket (public, week-cached)
4. Set as `cover_url` in DB

### API endpoint pattern
```
POST https://api.openai.com/v1/images/generations
Authorization: Bearer {key}
Body: {"model":"dall-e-3", "prompt":"...", "size":"1024x1024", "quality":"hd", "n":1, "response_format":"b64_json"}
```

### Cost guard
- SAD volume (~5 covers/week): under $1/month at dall-e-3 hd
- Reference: KEYS-REPOSITORY for current keys + cached at `/home/user/.openai_key` sandbox-side

---

## Pattern 25: SAD Report/Brief Publishing Pipeline

Added: 1 May 2026

End-to-end workflow for publishing paid reports and free briefs to sad.ifcifb.com.

### Folder structure (in 04-Areas/SAD-Strategic-Analysis-Division)
- Reports-Inbox: `1bf6n2ycooolHhXQ8HPf4iUOXxQcOQz0u` (Michael drops new PDFs here)
- Reports-Live: `13_nLvseku50vZhu7EZgSnL1O1jBs4rUu` (Claude moves source after publish)
- Briefs-Drafts: `1OIxxOt_UiWgM_0uNNC_IRRdBq9N5yJIl`
- SAD-Reports-Pipeline-Protocol doc: `1lsrkBWkYxZm4bonsfdWeQTMaDAw6VxRTGVEJE5ViKeU`

### Workflow per paid report
1. Michael drops PDF in Reports-Inbox + pings Claude
2. Claude reads PDF, extracts: title, subtitle, abstract (3 sentences), importance ("Why this matters" 1 sentence), preview_md (4 sections of free preview), tags, page count
3. Claude generates cover via Pattern 24 (square 1024x1024 dall-e-3 hd)
4. Upload PDF to Supabase `reports-private/{slug}/{ts}.pdf`
5. Upload cover JPG to `reports-public/{slug}/cover-{ts}.jpg`
6. INSERT into `public.reports` with `pseudonym='H.M.'`, `published=true`, `published_at=now()`
7. Move source PDF to Reports-Live folder
8. Verify on `sad.ifcifb.com/r/{slug}`

### Pseudonym discipline
- All paid reports: **H.M.** (Michael's pseudonym)
- Free briefs: 10 SAD aliases by coverage area

| Alias | Coverage |
|---|---|
| K.A. | middle-east-gulf |
| D.V. | russia-eurasia-arctic |
| T.R. | energy-security |
| M.E. | defence-industrial-base |
| L.W. | sanctions-threat-finance |
| H.T. | indo-pacific |
| R.S. | maritime |
| A.B. | geopolitics cross-domain |
| P.K. | industrial-strategy/tech |
| C.L. | cross-domain Lemma |

### Brief writing standard (institutional grade, post-1 May 2026)
- Body length: 2200-2600 chars (not 900-1000)
- Concrete numbers + named institutions + explicit dates
- Probability bands per Methodology page (Remote/Unlikely/Plausible/Even/Likely/Highly likely/Near-certain with % ranges)
- Sections: "What happened" / "Why X" / context / "Decision implication" with named action
- Voice: Murray-influenced. Short punchy sentences for emphasis. Concrete > abstract.

### Supabase coordinates
- Project ref: `cqixxvhuujmemwqslqmw`
- DB password: `wawxiz-fuTpon-jazju9`
- Tables: `reports`, `briefs`, `purchases`, `download_log`, `profiles`
- Buckets: `reports-public` (covers, hero), `reports-private` (PDFs, signed-URL access)
- `importance` column added to `reports` table 1 May 2026

---

## Pattern 26: Fact-Check Living Persons and Current Events Before Writing SAD Analysis

Added: 3 May 2026

Before writing any paragraph in a SAD document that names living persons in current roles, references recent strikes / deaths / transitions, cites current office-holders, or quotes recent figures (deal sizes, casualty counts, dates), web-search to verify current status. Training-data assumptions and memory context are not substitutes for present-day verification of post-cutoff facts.

### Specifically verify before writing
- Named individuals: alive? in the role attributed? capable of the actions described?
- Office-holders: current incumbent of head of state, foreign minister, military commander, central banker, etc.
- Recent events (last 12 months): current status of strikes, treaties, deals, court rulings, transitions, ceasefires
- Quoted figures: deal sizes, casualty counts, transit volumes, dates - verify against current reporting
- Regime structure: succession status, council composition, decision chains, designated successors under decapitation protocols

### Memory does not substitute for search

Memory may carry the broader context (e.g. that a war happened) but the specific consequences (who died in which strike, who replaced whom, what was destroyed, what changed in the regime structure) require verification against live reporting. The cost of three to five web searches per major section is trivial. The cost of a factual error in client-facing SAD work is not.

### Trigger

Any SAD document or brief that mentions: named persons in current roles, current office-holders, recent strikes / deaths / transitions, deal sizes, casualty figures, succession status, current treaty terms.

### Failure mode this pattern was extracted from

3 May 2026 - "The Reordering of the Middle East" SAD document (ref SAD/2026/IRM-04-01). Section II described Khamenei as "absent from active management, with day-to-day decisions devolved to a circle around his son Mojtaba and senior clerics." Reality: Ali Khamenei was assassinated 28 February 2026 in the joint US-Israeli strike on his compound. Mojtaba Khamenei was named successor by the Assembly of Experts on 9 March 2026 but missed the 40-day commemoration on 9 April; his status (alive / incapacitated / dead) was unconfirmed at the time of writing. The Interim Leadership Council (Pezeshkian, Mohseni Ejei, Arafi) holds nominal authority. Ali Larijani is the designated acting supreme leader under the decapitation protocol. A single web search before writing the paragraph would have caught this. The war context was in memory; the February 2026 succession was not.

### Voice note

When the official position and the analytical reality diverge on a sensitive named figure, the dry voice often holds the official line and lets the analytical content do the work underneath. Spelling out assassinations and succession crises by name can break Murray voice and weight a paragraph that is deliberately compressed. Verify the fact, then choose the appropriate level of explicitness for the document. Verification is non-negotiable; explicitness is a stylistic choice.

---

## Pattern 27: Dual-Measurement Reframe (Stock-Flow Consilience)

### Trigger

Any strategic-competition assessment, power-balance read, or great-power diagnosis. Applies to all Hegemony Series volumes from Doc IV onward and to all SAD strategic-analysis documents that compare states or alliance blocs.

### Statement

When assessing power balances, always carry both flow and stock dimensions. Flow measures activity (GDP, military spending, trade balance, capital flows, alliance density). Stock measures inheritance and substrate (produced capital, human capital, natural capital - per CWON 2024 / SEEA / Costanza). Neither alone is power. Flow without stock measures activity without solvency; stock without flow measures inheritance without throughput.

### Failure mode this pattern was extracted from

GDP-only assessments of the great-power balance produce systematic errors: China overstated, Russia overstated, the EU read as cyclically weak when stock-side decline is structural, the US read as declining when stock-side advantages persist. These errors propagate into strategy recommendations that misjudge the 2027 window and beyond. The Hegemony Series 2026 (Docs I through III) carries this error and required architectural correction in May 2026 (SAD/2026/HEG-ARCH/01).

### Voice note

The stock-flow distinction is technical but the writing must not become academic. Use plain Murray prose: "China's industrial throughput is rising; its underlying balance sheet is being liquidated to sustain it. Both are true." The dimension is leveraged through dry juxtaposition, not jargon.

---

## Pattern 28: Wealth Preservation as Hardening-Axis Architecture

### Trigger

Any analysis of nature-related financial risk frameworks (NGFS, IMF Embedded in Nature, TNFD, sovereign nature-risk supervision, CWON-style accounting) in a strategic-competition context. Applies to Hegemony Series Doc V and Doc VI, and to any SAD document discussing alliance institutional density.

### Statement

Nature-related financial-risk frameworks are not ESG soft-stuff. They are alliance architecture in the same class as AUKUS, IP4, the Hague Commitment. Central-bank coordination on nature risk, sovereign nature-risk frameworks, and CWON-style accounting produce hardening-axis institutional density, exclude adversary capital from coordinated supervisory frameworks, and generate measurement asymmetries favouring the wealth-preserving coalition. The retreating axis cannot meaningfully participate without undermining its own rentier-extraction or natural-capital-liquidation revenue base. The exclusion is structural, not ideological.

### Failure mode this pattern was extracted from

Standard analyst practice files NGFS, IMF nature-risk, and CWON under "ESG / climate" and dismisses them as soft-power gestures. This is wrong twice: (a) it misses that participation requirements are exclusionary by design, and (b) it misses that capital-charge implementation has hard financial-supervisory teeth equivalent to Basel-style alliance discipline. Doc V Wealth-Preservation Pillar architecture rests on this corrected reading.

### Voice note

When introducing the nature-risk-as-architecture argument, name the standard error explicitly before refuting it. The reader will arrive with the ESG dismissal pre-loaded; clearing it is the first move. "Most analysts file these frameworks under ESG. They are wrong." Then make the case.
