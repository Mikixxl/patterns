<!-- AUTO-SYNCED FROM GOOGLE DRIVE - DO NOT EDIT HERE.
     Source doc: https://docs.google.com/document/d/11ddVlIuCi8YAslcoqK-2uy1j-MeQXisvO4xkeIN7auU/edit
     Sync script: scripts/sync.py -->

# **PATTERNS-STRATEGIC**

**Scope:** SAD and Hegemony Series specific patterns: AI image generation for covers, SAD publishing pipeline.  
**Patterns in this file: 5**  
**Created:** 2 May 2026 as part of memory architecture migration. Patterns extracted from the original PATTERNS-LIBRARY (doc ID 1LvMjwluhsQMftiV0IpvLZPpH1\_knRkC3utHMrYvjpSA, now PATTERNS-INDEX).  
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

# **Pattern 24: AI Image Generation for Report Covers**

PATTERN 24: AI IMAGE GENERATION FOR REPORT/BRIEF COVERS  
Added: 1 May 2026  
When stock photography (Pexels, Unsplash) does not deliver topic-specific quality, generate cinematic covers via OpenAI image API. SAD aesthetic \+ workflow established.

# **Models verified accessible (1 May 2026\)**

• gpt-image-2-2026-04-21: SOTA, requires verified org, \~$0.04/image, 60-180s generation time  
• dall-e-3 (hd quality): no verification needed, 30-60s generation, very reliable  
• gpt-image-1.5, dall-e-2: legacy fallbacks  
• Gemini Imagen 4 / gemini-2.5-flash-image: requires PAID tier (free quota \= 0\)

# **SAD aesthetic prompt template**

"Cinematic photograph in the style of Denis Villeneuve. \[topic-specific scene\]. Dark navy ocean/sky transitioning to amber-gold horizon. Atmospheric haze. Long shadows. Volumetric lighting. Strategic geography aesthetic, formal and weighted, photorealistic. Sharp focus on \[primary subject\]. No text, no logos, no people \[unless required\], no captions, no watermarks."

# **Standard sizes**

• Featured-card cover (square): 1024x1024 with quality=hd  
• Brief-card cover (16:9 horizontal): 1792x1024 with quality=hd  
• Hero image (square): 1024x1024 with quality=hd  
• Category badges (military insignia, square): 1024x1024 with quality=hd, then resize to 320x320 PNG

# **Workflow**

1\. Generate via api.openai.com/v1/images/generations with response\_format=b64\_json  
2\. Optimize PNG → JPG via PIL: quality=88-90, optimize=True, progressive=True (90% size reduction)  
3\. Upload to Supabase reports-public bucket (public, week-cached)  
4\. Set as cover\_url in DB

# **API endpoint pattern**

POST https://api.openai.com/v1/images/generations  
Authorization: Bearer   
Body: {"model":"dall-e-3", "prompt":"...", "size":"1024x1024", "quality":"hd", "n":1, "response\_format":"b64\_json"}

# **Cost guard**

• SAD volume (\~5 covers/week): under $1/month at dall-e-3 hd  
• Reference: KEYS-REPOSITORY for current keys \+ cached at /home/user/.openai\_key sandbox-side  
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

# **Pattern 25: SAD Report/Brief Publishing Pipeline**

PATTERN 25: SAD REPORT/BRIEF PUBLISHING PIPELINE  
Added: 1 May 2026  
End-to-end workflow for publishing paid reports and free briefs to sad.ifcifb.com.

# **Folder structure (in 04-Areas/SAD-Strategic-Analysis-Division)**

• Reports-Inbox: 1bf6n2ycooolHhXQ8HPf4iUOXxQcOQz0u (Michael drops new PDFs here)  
• Reports-Live: 13\_nLvseku50vZhu7EZgSnL1O1jBs4rUu (Claude moves source after publish)  
• Briefs-Drafts: 1OIxxOt\_UiWgM\_0uNNC\_IRRdBq9N5yJIl  
• SAD-Reports-Pipeline-Protocol doc: 1lsrkBWkYxZm4bonsfdWeQTMaDAw6VxRTGVEJE5ViKeU

# **Workflow per paid report**

1\. Michael drops PDF in Reports-Inbox \+ pings Claude  
2\. Claude reads PDF, extracts: title, subtitle, abstract (3 sentences), importance ("Why this matters" 1 sentence), preview\_md (4 sections of free preview), tags, page count  
3\. Claude generates cover via Pattern 24 (square 1024x1024 dall-e-3 hd)  
4\. Upload PDF to Supabase reports-private/{slug}/{ts}.pdf  
5\. Upload cover JPG to reports-public/{slug}/cover-{ts}.jpg  
6\. INSERT into public.reports with pseudonym='H.M.', published=true, published\_at=now()  
7\. Move source PDF to Reports-Live folder  
8\. Verify on sad.ifcifb.com/r/{slug}

# **Pseudonym discipline**

• All paid reports: H.M. (Michael's pseudonym)  
• Free briefs: 10 SAD aliases by coverage area  
  K.A. middle-east-gulf | D.V. russia-eurasia-arctic | T.R. energy-security  
  M.E. defence-industrial-base | L.W. sanctions-threat-finance | H.T. indo-pacific  
  R.S. maritime | A.B. geopolitics cross-domain | P.K. industrial-strategy/tech  
  C.L. cross-domain Lemma

# **Brief writing standard (institutional grade, post-1 May 2026\)**

• Body length: 2200-2600 chars (not 900-1000)  
• Concrete numbers \+ named institutions \+ explicit dates  
• Probability bands per Methodology page (Remote/Unlikely/Plausible/Even/Likely/Highly likely/Near-certain with % ranges)  
• Sections: "What happened" / "Why X" / context / "Decision implication" with named action  
• Voice: Murray-influenced. Short punchy sentences for emphasis. Concrete \> abstract.

# **Supabase coordinates**

• Project ref: cqixxvhuujmemwqslqmw  
• DB password: wawxiz-fuTpon-jazju9  
• Tables: reports, briefs, purchases, download\_log, profiles  
• Buckets: reports-public (covers, hero), reports-private (PDFs, signed-URL access)  
• 'importance' column added to reports table 1 May 2026  
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

Pattern 26: Fact-Check Living Persons and Current Events Before Writing SAD Analysis  
PATTERN 26: FACT-CHECK LIVING PERSONS AND CURRENT EVENTS BEFORE WRITING SAD ANALYSIS  
Added: 3 May 2026

Before writing any paragraph in a SAD document that names living persons in current roles, references recent strikes / deaths / transitions, cites current office-holders, or quotes recent figures (deal sizes, casualty counts, dates), web-search to verify current status. Training-data assumptions and memory context are not substitutes for present-day verification of post-cutoff facts.

Specifically verify before writing  
\- Named individuals: alive? in the role attributed? capable of the actions described?  
\- Office-holders: current incumbent of head of state, foreign minister, military commander, central banker, etc.  
\- Recent events (last 12 months): current status of strikes, treaties, deals, court rulings, transitions, ceasefires  
\- Quoted figures: deal sizes, casualty counts, transit volumes, dates \- verify against current reporting  
\- Regime structure: succession status, council composition, decision chains, designated successors under decapitation protocols

Memory does not substitute for search  
Memory may carry the broader context (e.g. that a war happened) but the specific consequences (who died in which strike, who replaced whom, what was destroyed, what changed in the regime structure) require verification against live reporting. The cost of three to five web searches per major section is trivial. The cost of a factual error in client-facing SAD work is not.

Trigger  
Any SAD document or brief that mentions: named persons in current roles, current office-holders, recent strikes / deaths / transitions, deal sizes, casualty figures, succession status, current treaty terms.

Failure mode this pattern was extracted from  
3 May 2026 \- 'The Reordering of the Middle East' SAD document (ref SAD/2026/IRM-04-01). Section II described Khamenei as 'absent from active management, with day-to-day decisions devolved to a circle around his son Mojtaba and senior clerics.' Reality: Ali Khamenei was assassinated 28 February 2026 in the joint US-Israeli strike on his compound. Mojtaba Khamenei was named successor by the Assembly of Experts on 9 March 2026 but missed the 40-day commemoration on 9 April; his status (alive / incapacitated / dead) was unconfirmed at the time of writing. The Interim Leadership Council (Pezeshkian, Mohseni Ejei, Arafi) holds nominal authority. Ali Larijani is the designated acting supreme leader under the decapitation protocol. A single web search before writing the paragraph would have caught this. The war context was in memory; the February 2026 succession was not.

Voice note  
When the official position and the analytical reality diverge on a sensitive named figure, the dry voice often holds the official line and lets the analytical content do the work underneath. Spelling out assassinations and succession crises by name can break Murray voice and weight a paragraph that is deliberately compressed. Verify the fact, then choose the appropriate level of explicitness for the document. Verification is non-negotiable; explicitness is a stylistic choice.  
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

Pattern 27: Dual-Measurement Reframe (Stock-Flow Consilience)

Trigger  
Any strategic-competition assessment, power-balance read, or great-power diagnosis. Applies to all Hegemony Series volumes from Doc IV onward and to all SAD strategic-analysis documents that compare states or alliance blocs.

Statement  
When assessing power balances, always carry both flow and stock dimensions. Flow measures activity (GDP, military spending, trade balance, capital flows, alliance density). Stock measures inheritance and substrate (produced capital, human capital, natural capital \- per CWON 2024 / SEEA / Costanza). Neither alone is power. Flow without stock measures activity without solvency; stock without flow measures inheritance without throughput.

Failure mode this pattern was extracted from  
GDP-only assessments of the great-power balance produce systematic errors: China overstated, Russia overstated, the EU read as cyclically weak when stock-side decline is structural, the US read as declining when stock-side advantages persist. These errors propagate into strategy recommendations that misjudge the 2027 window and beyond. The Hegemony Series 2026 (Docs I through III) carries this error and required architectural correction in May 2026 (SAD/2026/HEG-ARCH/01).

Voice note  
The stock-flow distinction is technical but the writing must not become academic. Use plain Murray prose: "China's industrial throughput is rising; its underlying balance sheet is being liquidated to sustain it. Both are true." The dimension is leveraged through dry juxtaposition, not jargon.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

Pattern 28: Wealth Preservation as Hardening-Axis Architecture

Trigger  
Any analysis of nature-related financial risk frameworks (NGFS, IMF Embedded in Nature, TNFD, sovereign nature-risk supervision, CWON-style accounting) in a strategic-competition context. Applies to Hegemony Series Doc V and Doc VI, and to any SAD document discussing alliance institutional density.

Statement  
Nature-related financial-risk frameworks are not ESG soft-stuff. They are alliance architecture in the same class as AUKUS, IP4, the Hague Commitment. Central-bank coordination on nature risk, sovereign nature-risk frameworks, and CWON-style accounting produce hardening-axis institutional density, exclude adversary capital from coordinated supervisory frameworks, and generate measurement asymmetries favouring the wealth-preserving coalition. The retreating axis cannot meaningfully participate without undermining its own rentier-extraction or natural-capital-liquidation revenue base. The exclusion is structural, not ideological.

Failure mode this pattern was extracted from  
Standard analyst practice files NGFS, IMF nature-risk, and CWON under "ESG / climate" and dismisses them as soft-power gestures. This is wrong twice: (a) it misses that participation requirements are exclusionary by design, and (b) it misses that capital-charge implementation has hard financial-supervisory teeth equivalent to Basel-style alliance discipline. Doc V Wealth-Preservation Pillar architecture rests on this corrected reading.

Voice note  
When introducing the nature-risk-as-architecture argument, name the standard error explicitly before refuting it. The reader will arrive with the ESG dismissal pre-loaded; clearing it is the first move. "Most analysts file these frameworks under ESG. They are wrong." Then make the case.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

## **Pattern 26 Amendment \- Filing-Time Extension (14 May 2026\)**

Pattern 26 originally applied only at write-time. This amendment extends it to filing-time. The trigger expands; the discipline stays the same.

### **Extended trigger**

Verification searches run BEFORE banking source material into the vault, not only before writing analysis. Any YouTube transcript, news clip, third-party briefing, podcast extract, or analyst note that names living persons, claims recent events, attributes quotes to officials, or asserts operational facts (strike locations, casualty counts, vessel numbers, dates) must be verified at the moment of filing.

### **Rationale**

Source material that lands in 02-Inbox unverified propagates into 05-Resources, then into draft documents, then into client-facing SAD output. Each propagation step makes the error harder to catch and more expensive to correct. The cheapest catch is at filing. A YouTube creator's framing error becomes a Doc V citation error becomes a published SAD claim error. The chain breaks at the first verification.

### **Filing-time procedure**

At minimum, verify three claim classes before banking a source file:

* Headline claim \- the lede the source leads with (e.g. "Kuwait attacks IRGC")  
* Named-person claims \- alive, in role, capable of action attributed  
* Numerical claims \- vessel counts, missile counts, dates, deal sizes

Flag remaining claims as "verified" / "claimed, not yet verified" / "stale" / "framing wrong" in a verification matrix at the top of the filed document. The matrix is the working notes for any future writer drawing on the source. Future-writer reads the matrix first, not the source.

### **Failure-mode framing correction**

The pattern earlier read "Memory is not a substitute for present-day verification of post-cutoff facts." The amendment extends: source-material framing is also not a substitute for verification. YouTube creators editorialize. Wire services attribute. Open-source intelligence channels speculate. The framing that lands in the vault must be checked against current reporting, not just absorbed.

### **Real-world prompt**

14 May 2026 \- filing the TUC TV transcript on Kuwait-IRGC for Doc V. The transcript framed Kuwait as "launching an attack" on the IRGC. The verified record is that Kuwait *repelled* an IRGC infiltration of Bubiyan Island. Same event, different framing, opposite alliance signal. Doc V argument is actually stronger with the verified framing. The cost was three web searches at filing. The cost of writing Doc V from the unverified framing would have been a structurally wrong opening case.

### **Standing rule**

Always check at filing. Pattern 26 trigger now includes filing-step. Verification matrix becomes a standard frontmatter component of every YouTube-transcript or third-party-briefing file dropped into the vault.

### **History**

Pattern 26 created 3 May 2026 after Khamenei succession error in IRM-04-01 document. Extension added 14 May 2026 after Doc V source-filing session demonstrated the same failure-mode at filing-step rather than write-step.

\---

\#\# Pattern 36: Consensus-Convergence Inversion Check (14 May 2026\)

\#\#\# Trigger

Any strategic-analysis document, brief, or assessment that touches a topic where mainstream analyst consensus is forming or has formed quickly across multiple independent outlets. Applies to all Hegemony Series volumes, all SAD strategic-analysis documents, and any operational brief that draws on Reuters, Bloomberg, Goldman, FT, WSJ, Semafor, or comparable mainstream analyst output.

\#\#\# Statement

When mainstream analyst consensus converges quickly across multiple independent outlets on the same surface-reading of a strategic event, treat that convergence as a data point rather than as confirmation. Truly contested signals split the analyst community; truly engineered signals converge it. The unanimous reading is suspect precisely because it is unanimous.

Apply the inversion default: assume the public reading is what the engineer of the event intends observers to see, then ask what the public reading is covering. The substantive analysis lives in the gap between the consensus surface and the operational substrate.

\#\#\# Failure mode this pattern was extracted from

14 May 2026 Trump-Xi Beijing summit analyst roundup. Reuters, Goldman, Semafor, Independent, Wall Street Journal, CNBC, and the trade press all converged within hours on the same surface reading: "tactical truce, not major reset; trade focus over grand bargain; both sides want stability not decoupling." The convergence was rapid and uniform.

Doc IIIb source-material analysis (file ID \`1XlA2COAHCw9aLPwd6zey0gfcHu59SmVlkFZdBwvtwVY\` in 05-Resources) revealed four operational structures invisible to the mainstream analyst diet:

\- The MFA Chinese-language text contained a four-clause constraint architecture for 建设性战略稳定 that the English coverage collapsed into a single descriptive phrase  
\- The Taiwan formulation in the Chinese readout was near-ultimatum register (water-and-fire idiom, greatest-common-denominator framing, doubled intensifier 慎之又慎); the English captured only the ranking  
\- The MAGA / 中华民族伟大复兴 rhetorical parallel imported the CCP century-horizon framework into the bilateral, a substantive doctrinal move  
\- The Central Asian rail corridor stack (Kazakhstan, Kyrgyzstan-Uzbekistan, northern Russia route, plus the new Tajikistan corridor signalled by Rahmon's overlapping state visit) constituted a Pattern 28 stock-side commitment running in parallel with the verbal flow-side concession on Hormuz transit tolls

The consensus was correct on the surface and missed the operational structure underneath. Without this pattern, SAD analysis risks anchoring to the same surface-reading the mainstream produces and outputting commentariat-grade work rather than SAD-grade work.

\#\#\# Application

In every strategic analysis where mainstream consensus exists:

1\. Write the consensus reading explicitly first. Do not assume the reader knows it.  
2\. Apply the inversion deliberately: if this reading is what the engineer of the event wants observers to see, what is the reading covering?  
3\. Check whether contested signals would naturally produce convergence. If yes, the convergence is information about the signal-engineering, not about the underlying reality.  
4\. Apply Pattern 28 (stock-flow framing) as the inversion tool: surface-readings tend to capture flow concessions; the inversion question is what stock continuities are running underneath.  
5\. Apply Pattern 26 (verification at filing-step) to mainstream sources cited: even high-credibility outlets inherit the analyst-diet's structural blind spots.

\#\#\# Diagnostic markers for engineered convergence

Signs that a consensus is built rather than organic:

\- Convergence speed: multiple major outlets reach the same reading within hours rather than days  
\- Lexical uniformity: the same phrases ("tactical truce," "managed competition," "guardrails") appear across outlets that do not normally share vocabulary  
\- Symmetric inadequacy: every outlet misses the same structural feature in the same way  
\- Source-of-source convergence: pulling the citation chains reveals a small set of upstream analyst voices feeding many downstream outlets  
\- Translation-layer compression: when the original-language event document and the English coverage diverge significantly, English-only convergence is built on a compressed substrate

If three or more markers are present, the inversion check is mandatory, not optional.

\#\#\# Voice discipline

Use this pattern silently in analysis, not didactically. Never tell readers "the mainstream consensus is wrong"; just deliver the deeper reading and let the divergence stand. The Murray voice rejects analytical chest-thumping.

The Doc IIIb opener candidate ("The most successful diplomatic deceptions are the ones the diagnostic community confirms in unison") is the rare case where the inversion is named directly, because it serves as the thesis-statement for the whole document. For paragraph-level work, apply the inversion silently and let the analytical sharpness do the demonstrating.

\#\#\# History

Pattern 36 codified 14 May 2026 after the Trump-Xi Beijing summit source-bundle work demonstrated the failure mode in real time. The trigger observation: six major outlets converged on identical surface-reading within hours while the source-bundle analytical pass had already identified four operational structures the consensus missed. Michael Herzog noted that the critical reflex producing this kind of divergence is the same one his associates characterize as "too critical." That critical reflex is the feature that distinguishes SAD-grade work from commentariat work. The pattern codifies the discipline so the reflex is applied consistently across sessions, not just when triggered by a specific event.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

\#\# Pattern 37: Corrective Discipline \- Strategy Critic, Not Stenographer (15 May 2026\)

\#\#\# Trigger  
Any SAD document, brief, or analytical synthesis that touches a current or proposed strategy by Washington, Brussels, Jerusalem, Riyadh, Abu Dhabi, Tokyo, Taipei, or any allied/partner government. Applies to all Hegemony Series volumes, all Doc IIIb / Doc IV / Doc V drafting, and to every analytical synthesis that extracts strategic implications from filed source material.

\#\#\# Statement  
SAD's job is to correct wrong strategies and propose better ones. Not to describe them. Not to absorb them as fait accompli. Not to pre-emptively concede to whichever direction current decision-makers are signalling. Every analytical observation about a strategic move must be tested against two questions: is this strategy right or wrong, and if wrong, what is the better alternative? Description without prescription is commentariat work. SAD output is prescriptive.

The discipline applies symmetrically. When the consensus reading is that "Trump is moving toward X," do not write "if X happens, then Y will follow" as if X is settled. Write "X would be a strategic error, here is why, and here is the corrective." When an Israeli tactical preference is undermining its own strategic objective, do not write the contradiction as observed tension. Write it as the recommendation: change the tactical preference. When the diversification routes SAD has been treating as the strategic path forward are at risk of being traded away in a short-term deal, do not accept the trade as a backdrop fact. Defend the diversification routes as the correct strategy.

\#\#\# Failure mode this pattern was extracted from  
15 May 2026 \- analytical synthesis session after ingesting the 14 May 2026 corpus (twelve INGEST documents) plus the 15 May 2026 manual ingests (Seaman China hybrid war, Baunov-Chadayev Russia drone disaster, Pinto-Gindin TBN Israel broadcast, German Iran-China oil paper with verification update). Claude drafted the synthesis with descriptive framing: "if Trump trades security signaling for rare earth access guarantees, this undermines the domestic processing investments and Australia-Vietnam-Kazakhstan diversification routes that SAD has been treating as the strategic path forward."

Michael Herzog corrected: the Australia-Vietnam-Kazakhstan diversification routes are not at risk of being abandoned. They are the strategy. The risk is that Trump trades them away. SAD's job is to flag that risk as the error, not to absorb the trade-off as a fact. The diversification routes should be defended in the SAD output, not pre-emptively conceded.

The same drift was present across multiple synthesis observations in the same session:  
\- The Trump trade-first compartmentalization was framed as "regime-level shift" rather than as "regime-level error to call out"  
\- The Israeli Lebanon strategy contradiction was framed as "internal tension" rather than as "tactical preference undermining strategic objective, recommend reversal"  
\- The Iranian tiered internet was framed as "supervisory architecture template" rather than as "template the West should make costly to deploy"  
\- The BRICS fragility was framed as "data point" rather than as "leverage to exploit by ensuring extracted parties understand the extraction"

Each observation had the corrective frame available. Each was filed as description. The pattern codifies the discipline of always writing the corrective frame, not the descriptive frame.

\#\#\# Application  
For every analytical observation that touches a strategy currently being pursued or considered, apply the four-question test before drafting the paragraph:

1\. Is this strategy right or wrong on its strategic merits? (Not "is it likely to happen.")  
2\. If wrong, what specifically is the error? (Stock-flow misalignment, capitulation to wrong terrain, short-term trade for long-term position, etc.)  
3\. What is the better alternative? (Name it concretely. Australia-Vietnam-Kazakhstan rather than HREE-access deal. Lebanese state capacity rather than continued demolition. Densify UAE-Israel architecture rather than wait for calmer environment.)  
4\. Who is the audience that can act on the correction? (US administration, Israeli cabinet, GCC sovereign wealth funds, European Commission, etc.)

Then draft the paragraph as: "The current direction is X. This is wrong because Y. The corrective is Z. The audience that can change this is W." Compress as needed for the document register, but the four elements must be present.

\#\#\# Corrective frames already identified from 15 May 2026 corpus  
The synthesis session identified ten wrong-strategy observations that should appear in SAD output as corrections, not descriptions. Each is now banked for Doc IIIb, Doc IV, Doc V, and synthesis-note drafting:

\- Trump trade-first compartmentalization is the error; the 2021-2025 integrated competition framework was correct and should be held  
\- Israeli Lebanon demolition is self-defeating; corrective is investing in Lebanese state capacity as Hezbollah counterweight  
\- HREE access deals with Beijing are short-term wins drawing down long-term diversification stocks; corrective is accelerating Australia-Vietnam-Kazakhstan investment under cover of negotiation  
\- BRICS as convenience arrangement should be exposed to extracted parties (Brazil, South Africa, India) to drive wedges  
\- Iranian tiered internet should be made costly via Starlink and circumvention tools before the template hardens into the PLA's Taiwan model  
\- Dual-use proxy infrastructure should be targeted at the cross-border militia movement (Shalamcheh, Chazabeh, Khosravi crossings) to degrade external and internal capability simultaneously  
\- Shia spiritual-victory framework breaks pressure-to-capitulation logic; corrective is delegitimization via the January 2026 massacre record and Pahlavi-as-rallying-point rather than material destruction  
\- Selective rule-of-law enforcement (Adani case) should be acknowledged as alliance currency, not pretended principled  
\- GCC reputational depletion forces densification choice; corrective is accelerating Saudi-Israel normalization before the window closes  
\- Services-led development is a strategic opportunity to invest in BRI-hesitating countries via digital infrastructure, education, English-language proficiency, and rule-of-law for service contracts

\#\#\# Voice discipline  
The corrective frame should not produce hectoring prose. Murray voice corrects through compression and concrete alternatives, not through moralizing. "Trump should not trade HREE diversification for short-term access" reads as commentary. "The diversification routes are the strategy. Trading them away for a short-term access deal would extend Chinese leverage permanently in exchange for a quarter or two of supply" reads as analysis. The second version is the SAD register. Name the error, name the cost, name the alternative. Move on.

When the corrective requires naming a head of state or coalition government as the actor making the error, follow Pattern 26 voice discipline: spell out the analytical reality, choose the appropriate level of explicitness for the document register. The corrective is non-negotiable; the framing of who exactly is making the error is a stylistic choice.

\#\#\# Relationship to existing patterns  
\- Pattern 26 prevents factual error in SAD output. Pattern 37 prevents analytical drift into description. Both are anti-absorption disciplines applied at different stages.  
\- Pattern 27 (stock-flow) supplies the diagnostic tool for many corrective frames: most short-term-deal errors are flow gains purchased with stock drawdowns. The stock-flow lens makes the corrective concrete.  
\- Pattern 28 (wealth preservation as hardening axis) supplies the structural model for several correctives: nature-risk frameworks, supervisory architecture, alliance institutional density are all stock-side commitments that resist flow-side concession trades.  
\- Pattern 36 (consensus-inversion) prevents anchoring to surface-reading. Pattern 37 prevents anchoring to current-strategy direction. They are sister patterns. Pattern 36 asks "what is the consensus covering?" Pattern 37 asks "is the current strategy correct, and if not, what is?"

\#\#\# History  
Pattern 37 codified 15 May 2026 after the post-corpus synthesis session demonstrated that even after Pattern 36 was applied (consensus-inversion check), drafted output drifted into descriptive framing of current strategy directions. Michael Herzog corrected: "Our job is to correct wrong strategies or propose better ones." Pattern locks in the discipline before the active Hegemony Series drafting window (Doc IIIb post-summit, Doc IV pre-draft pickup, Doc V synthesis note).  
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_