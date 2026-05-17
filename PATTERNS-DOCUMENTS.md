<!-- AUTO-SYNCED FROM GOOGLE DRIVE - DO NOT EDIT HERE.
     Source doc: https://docs.google.com/document/d/1WXs_8ogoVrumuyN0ueY5B4ew_tzwBaQ0PAejUYNeurk/edit
     Sync script: scripts/sync.py -->

# **PATTERNS-DOCUMENTS**

**Scope:** DOCX and PPTX standards: document generation, validation, forensic style, strategic report standard, McKinsey-quality presentation upgrade.  
**Patterns in this file:** 6  
**Created:** 2 May 2026 as part of memory architecture migration. Patterns extracted from the original PATTERNS-LIBRARY (doc ID 1LvMjwluhsQMftiV0IpvLZPpH1\_knRkC3utHMrYvjpSA, now PATTERNS-INDEX).  
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

# **Pattern 1: DOCX Document Generation**

PATTERN 1: DOCX DOCUMENT GENERATION  
When to use: Any request for a professional Word document \- strategic analyses, legal opinions, compliance docs, presentations.  
Standard workflow:  
1\. Read /mnt/skills/public/docx/SKILL.md first  
2\. For writing tasks: fetch Writing Guardrails (doc ID: 1EGu4QCi27yhabbIJlXFYvrKiQgvgUrtFaZ5YXRnxXTc) and Text DNA Bible (doc ID: 1GpDT6VAGQ8LFhcDyScBbMU67ooQvP3n9M79GqNaFRfA)  
3\. For strategic docs: read /mnt/skills/user/strategic-analysis/SKILL.md  
4\. Generate charts as PNGs first using Python matplotlib with matplotlib.use('Agg') backend  
5\. Build Node.js docx-js script at /home/claude/  
6\. Execute with node filename.js  
7\. Validate with python /mnt/skills/public/docx/scripts/office/validate.py  
8\. Copy to /mnt/user-data/outputs/  
Key constants:  
\- Colors: NAVY (\#1B3A5C), ACCENT/GOLD (\#C8941E), DARK (\#2D2D2D), GREY (\#666666)  
\- Cover page: separate section with no header/footer  
\- TOC: TableOfContents with headingStyleRange: "1-3" and hyperlink: true  
\- Main section: running headers \+ page numbers  
\- Footnotes: unique ID per reference, never reuse IDs  
\- Branding: "Strategic Analysis Division" only, never "IFB International Finance Bank"  
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

# **Pattern 4: Strategic Analysis Documents (legacy v1)**

PATTERN 4: STRATEGIC ANALYSIS DOCUMENTS  
Standard structure (per skill):  
1\. Executive Summary  
2\. Context / Background  
3\. Level 1 Analysis (strategic landscape)  
4\. Level 2 Analysis (operational deep dive)  
5\. Level 3 Analysis (third-order ramifications)  
6\. Counter-strategy / Adversary response modeling  
7\. Probability-weighted scenarios  
8\. Self-critique section (mandatory)  
9\. Recommendations (tiered)  
10\. Source index  
Branding rule: Strategic Analysis Division only. No IFB prefix.  
Format constants: Navy header tables, color-coded callout boxes, embedded charts, numbered footnotes with unique IDs.  
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

# **Pattern 7: PPTX McKinsey-Quality Upgrade**

PATTERN 7: PPTX MCKINSEY-QUALITY UPGRADE  
What separates McKinsey quality from standard:  
\- Slide titles are action statements ("X delivers Y% advantage"), not labels ("Comparison")  
\- No dead white space \- every slide fully utilized  
\- Charts have annotated callouts explaining the insight  
\- Capital flow / process diagrams showing how value moves  
\- Stage-gate markers on timelines  
\- Verdict badges (PROCEED / STAGE-GATE / ASPIRATIONAL) for option slides  
\- Combined slides for density \- eliminate filler content  
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

# **Pattern 14: DOCX Generation Validation Workflow**

PATTERN 14: DOCX GENERATION VALIDATION WORKFLOW  
Standard sequence for every DOCX build:  
node /home/claude/document.js 2\>&1           \# Build  
python /mnt/skills/public/docx/scripts/office/validate.py /home/claude/output.docx 2\>&1  \# Validate  
cp /home/claude/output.docx /mnt/user-data/outputs/final\_name.docx  \# Deliver  
Post-build check:  
pandoc output.docx \-t plain 2\>/dev/null | grep \-i "IFB|International Finance"  
Should return nothing \- confirms no branding violations  
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
Last compiled: April 6, 2026\. Add new patterns after each session where a recurring workflow is successfully established.  
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

# **Pattern 17: Forensic / Verification Document Style**

PATTERN 17: FORENSIC / VERIFICATION DOCUMENT STYLE (STANDING TEMPLATE)  
Standing template for any forensic, verification, authenticity-assessment or document-review deliverable (DOCX). Use whenever Michael asks for a forensic opinion, scam-analysis, document-verification report, cross-check of another analyst's findings, or similar review work. This is the visual and structural default for that category.  
Reference implementation: Forensische\_Dokumentenanalyse\_Upload-Serie.docx (21.04.2026) \- cross-check of Greg's MI6/UFA scam analysis.  
When to apply  
• Any forensic document analysis (fake letter, suspect invoice, lookalike domain, BEC/social-engineering review)  
• Verification or authenticity opinions on uploaded documents  
• Cross-check / replic / second-opinion reports on another analyst's work  
• Due-diligence memos that need a confidential, expert-witness tone  
Not to be used for: strategic analysis (use Pattern 4), legal opinions (own stack), marketing content, investor docs.  
Page setup  
• Format: A4 (width 11906 DXA, height 16838 DXA)  
• Margins: 1 inch all around (1440 DXA top/right/bottom/left)  
• Body font: Calibri, 11pt (size 22 in docx-js half-points)  
• Line spacing: 300 (1.25 lines), spacing after 120  
• Paragraph alignment: justified (AlignmentType.JUSTIFIED) for all body text  
Colour palette (fixed)  
• NAVY: \#0B2545 (primary \- titles, headings, header/footer borders, signature line, table header background)  
• GOLD: \#B8860B (accent \- title eyebrow text, horizontal rules, footer top border, bullet markers)  
• GREY\_DARK: \#333333 (body text)  
• GREY\_LIGHT: \#D9D9D9 (meta-table borders)  
• Severity gradient for probability table: cream \#FFF4E5 (low), light-red \#FCE4E4 (medium), red-pink \#F8D0D0 (high)  
Do NOT substitute navy/gold with IFB/SAD navy-gold (\#1B3A5C/\#C8941E) \- forensic docs use their own palette to signal independent expert-witness tone.  
Page header (every page)  
• Left: "FORENSISCHES GUTACHTEN" in Calibri 9pt bold navy, character spacing 40, uppercase  
• Right tab (TabStopPosition.MAX): "Vertraulich" in Calibri 9pt italic grey  
• Bottom border: single line, size 8, navy, space 4  
Page footer (every page)  
• Top border: single line, size 6, gold, space 4  
• Left: "\[Document subtitle\]  |  \[Date in German format\]" in Calibri 8pt grey  
• Right tab: "Seite \[CURRENT\] von \[TOTAL\_PAGES\]" in Calibri 8pt grey  
Title block (page 1 only, above meta table)  
1\. Eyebrow: "FORENSISCHE DOKUMENTENANALYSE" \- Calibri 10pt bold gold, uppercase, character spacing 80, centered, spacing before 600  
2\. Main title: Calibri 20pt bold navy, centered, with bottom border (single, size 12, navy, space 8\)  
3\. Subtitle: Calibri 12pt italic grey, centered, describing the specific document purpose  
Meta table (directly under title)  
Two-column table, width 9360 DXA (full content width on A4 with 1" margins), columnWidths \[2800, 6560\].  
• Borders: single, size 4, grey \#D9D9D9 on all sides  
• Left column (label): background fill F2F2F2, Calibri 10pt bold navy  
• Right column (value): no fill, Calibri 10pt grey  
• Cell margins: top/bottom 100, left/right 140  
Standard rows: Dokumenttyp | Gegenstand | Datum der Begutachtung | Beweiswert | Klassifizierung. Adapt rows to the specific assessment but keep five rows as the norm.  
Headings  
• H1: Calibri 15pt bold navy, spacing before 360 / after 180, outlineLevel 0\. Used for top-level sections (Kurzfazit, numbered main sections, Endverdikt).  
• H2: Calibri 13pt bold navy, spacing before 280 / after 120, outlineLevel 1\. Used for sub-sections like Schlussbemerkung.  
• H3: Calibri 11.5pt bold italic navy, spacing before 200 / after 100, outlineLevel 2\. Used for in-section pivots ("Was X zutreffend erkannt hat", "Wo eine Präzisierung angezeigt wäre").  
Override built-in Heading1/Heading2/Heading3 style IDs directly in the styles block.  
Lists  
• Bullets: square marker U+25A0 in GOLD (\#B8860B), indent left 720 / hanging 360\. Reference name "bullets".  
• Numbered: DECIMAL format "%1." in NAVY bold, indent left 720 / hanging 360\. Reference name "numbers".  
• Spacing after each list item: 80, line spacing 300\.  
• List items are justified like body text.  
Never use Unicode bullet characters directly in TextRun \- always use the numbering config with LevelFormat.BULLET.  
Horizontal rule (section breaks)  
Empty paragraph with bottom border: single, size 6, gold (\#B8860B), space 1\. Spacing before/after 120\.  
Use between major narrative blocks (e.g. between meta table and Kurzfazit, between Endverdikt table and Schlussbemerkung).  
Probability / verdict table (Endverdikt)  
Two-column table, same 9360 DXA width, columnWidths \[4680, 4680\].  
• Borders: single, size 4, navy on all sides  
• Header row: navy fill, Calibri 11pt bold white text, left-aligned, cell margins 120/120/160/160  
• Body rows: white fill for left column, severity-graded fill for right column (low=\#FFF4E5, medium=\#FCE4E4, high=\#F8D0D0)  
• Right column text: Calibri 11pt bold grey, showing probability range ("95 bis 98 Prozent", "99 Prozent plus" etc.)  
• Left column: Calibri 11pt normal grey, document identifier  
Signature block (end of document)  
1\. Navy top border (single, size 6, space 6\)  
2\. First line: "Erstellt: \[Date\]" in Calibri 10pt bold navy  
3\. Second line: document subtitle in Calibri 10pt italic grey  
Content conventions  
• Language: German for Michael's forensic work unless specified otherwise  
• Quotation marks: German low-high („...“) using XML entities \\u201E / \\u201C  
• No em dashes \- ever. Use " \- " or commas.  
• Douglas-Murray-adjacent register: direct, confident, analytically precise, dry wit where appropriate  
• Structural rhythm: Kurzfazit → numbered main sections → Endverdikt with probability table → Schlussbemerkung → signature block  
• Probability ranges expressed as "X bis Y Prozent" or "Y Prozent plus"  
• Section naming pattern for review work: "Was \[analyst\] zutreffend erkannt hat" / "Was an seiner Begründung forensisch trägt" / "Wo eine schärfere Präzisierung angezeigt wäre"  
Build workflow  
1\. Read /mnt/skills/public/docx/SKILL.md  
2\. Build Node.js docx-js script at /home/claude/work/build.js using the parameters above  
3\. Execute: node /home/claude/work/build.js  
4\. Validate: python /mnt/skills/public/docx/scripts/office/validate.py \[output\].docx  
5\. Render preview via soffice \+ pdftoppm, spot-check pages 1, middle, last  
6\. present\_files to Michael  
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
Added: 21 April 2026 \- Michael explicitly requested this style be saved as the standing template for future verification documents.  
Filing destination (Pattern 15 exception)  
Forensic/verification DOCX outputs do not go to GROUP-OUTPUTS. They have their own dedicated folder:  
• Veritas (ID 1-zfoU1\_PrEwz-4LrESM-2XRC0SW6eBfR) \- top-level folder in 2nd Brain root (1lBhyv3-vSUeMQTT\_tmXi40-XFjUPwmur)  
This overrides the Pattern 15 auto-filing rule for any document built under Pattern 17 (forensic opinions, authenticity assessments, verification reports, scam analyses, second-opinion reviews). The Veritas folder is the single destination regardless of which entity the analysed material relates to \- the filing axis is document function (forensic verification), not subject entity.  
When Michael drops a forensic DOCX into \_INBOX (ID 1NgzGbDOspeT36y1OSDNw0h68zHAf8HZV), move it to Veritas via GOOGLEDRIVE\_MOVE\_FILE with add\_parents=1-zfoU1\_PrEwz-4LrESM-2XRC0SW6eBfR and remove\_parents=1NgzGbDOspeT36y1OSDNw0h68zHAf8HZV.  
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
Updated: 21 April 2026 \- Veritas folder created as the dedicated destination for forensic/verification deliverables.  
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

# **Pattern 18: Strategic Report DOCX Standard (locked 2 May 2026\)**

# **PATTERN 18: STRATEGIC REPORT DOCX STANDARD (locked 2 May 2026\)**

Binding format for all Strategic Analysis Division reports (Hegemony Series, individual SAD reports, group strategy memos). Established after Doc II review where format inconsistencies between Doc I and Doc II were flagged.  
\--- 1\. TABLE OF CONTENTS \---  
ALWAYS include automatic Table of Contents on page 2 (right after title page, before Section I). TOC must reflect H1 and H2 headings minimum, with page numbers. Use python-docx WD\_TAB\_ALIGNMENT.RIGHT with leader dots, or insert Word TOC field for automatic update on open.  
\--- 2\. HEADING COLOR \---  
All headings (H1, H2, H3) in NAVY \#0B2545 (RGBColor(0x0B, 0x25, 0x45)). No exceptions. Body text also navy. Subtitle italics in ACCENT \#2E75B6.  
\--- 3\. H1 STYLING \---  
\- Font: Calibri 18pt bold, navy \#0B2545, ALL CAPS  
\- Below each H1: gold horizontal line (\#B8860B, weight 8\) running full page width  
\- ALWAYS preceded by page break (every H1 starts on a new page)  
\- Implementation: doc.add\_paragraph().add\_run().add\_break(WD\_BREAK.PAGE) immediately before H1 paragraph  
\- Border via OxmlElement w:pBdr w:bottom val=single sz=8 color=B8860B space=4  
\--- 4\. H2 STYLING \---  
\- Font: Calibri 14pt bold, ACCENT \#2E75B6  
\- Space before 14pt, space after 6pt  
\- No border, no page break  
\--- 5\. H3 STYLING \---  
\- Font: Calibri 12pt bold, DARK \#2C3E50  
\- Space before 10pt, space after 4pt  
\--- 6\. BODY TEXT (BLOCKSATZ / JUSTIFIED) \---  
All body paragraphs use WD\_ALIGN\_PARAGRAPH.JUSTIFY (Blocksatz). Set in the helper function P() and inherited by all subsequent prose. Calibri 11pt navy. Space after 8pt.  
\--- 7\. CALLOUT BOXES, TABLES, FIGURES \---  
\- Callout boxes: single-cell tables with 24pt left border in accent color, BG\_CORE/ACTION/WARNING/RISK/CRITIQUE color palette  
\- Data tables: navy \#0B2545 header row with white bold text, navy 10pt body text  
\- Figure captions: Calibri 9pt grey italic, centered  
\--- 8\. PAGE STRUCTURE \---  
\- A4 portrait, 1 inch margins all sides  
\- Header: 'STRATEGIC ANALYSIS DIVISION | \[Series Name\] | Confidential' right-aligned, navy 9pt bold, with bottom border  
\- Footer: '\[Document Title\] | Page X of Y' centered, grey 9pt  
\--- 9\. FIGURES \---  
All figures generated with OpenAI gpt-image-2-2026-04-21 (SOTA model, $0.04/image). Imagen 4 Ultra and Gemini are NOT used \- quality consistency requires single-model pipeline. Matplotlib retained only for pure-data charts (timelines, probability tables) where typographic accuracy is critical and AI-generated text would risk errors.  
\--- 10\. STYLE GUARDRAILS \---  
Fetch Writing-Guardrails (doc 16WA5CUO2YNI4RsXuv1t5PQnS\_IU51nxa09pWEpkuiCQ) and Text DNA Bible (doc 1RCvNntxiD9VNjpntk96g3JEsrmwtiCR3r0K6j7YYftA) before every report. No em dashes, no leverage/demonstrate/comprehensive/journey/embark/ecosystem/paradigm/landscape, no overall/in conclusion, no fake emphasis ('it is important to note'), break sentence rhythm.  
\--- IMPLEMENTATION HELPERS \---  
The build\_part\_a.py template in any /home/user/doc\[N\]/ workbench should include:  
1\. add\_toc() function \- inserts Word TOC field at start  
2\. H1() function with built-in page break \+ gold bottom border  
3\. P() function with WD\_ALIGN\_PARAGRAPH.JUSTIFY default  
4\. All color tokens: NAVY=0B2545, GOLD=B8860B, ACCENT=2E75B6, DARK=2C3E50  
\--- VALIDATION CHECKLIST PRE-DELIVERY \---  
1\. TOC present and functional  
2\. All H1s start on new page with gold underline  
3\. All headings navy  
4\. All body text justified (Blocksatz)  
5\. No forbidden words (run regex scan)  
6\. No em dashes  
7\. Figures embedded at proper width (6.5 inches for full-width)  
8\. Footer page numbers working (PAGE/NUMPAGES fields)  
\--- SOURCE-FIDELITY RULE (LOCKED 17 May 2026, after a dropped-table failure) \---  
NEVER reconstruct the Word document by retyping or transcribing the Google Doc's text into a docx-js or python-docx script. GET\_DOCUMENT\_PLAINTEXT and any text-extraction path silently discard every non-text element: tables, embedded charts and images placed in the body, footnotes, equations, drawing objects. A text-based rebuild looks complete and validates clean while having lost structural content. This rule was extracted after Doc V (European Fracture) was rebuilt from the Doc's text and a table was deleted in the process; the validation passed and the loss was not caught, which is itself part of the failure.  
Binding method for any SAD report whose master is a native Google Doc:  
1\. The Word file is produced by EXPORTING the Google Doc, not by rebuilding it. Use GOOGLEDOCS\_EXPORT\_DOCUMENT\_AS\_PDF only for PDF; for the .docx use GOOGLEDRIVE\_EXPORT\_GOOGLE\_WORKSPACE\_FILE / GOOGLEDRIVE\_DOWNLOAD\_FILE with mime\_type application/vnd.openxmlformats-officedocument.wordprocessingml.document on the Doc's file ID. That preserves tables, images and footnotes.  
2\. Pattern 18 styling that the export does not carry (cover section, gold H1 rules, header/footer, TOC field, navy palette) is then applied by UNPACKING the exported .docx and editing its XML per the docx skill's "Editing Existing Documents" path \- never by regenerating the body from text.  
3\. If the master is not a Google Doc but assembled in-script from the start, the docx-js build path is still valid; the prohibition is specifically on round-tripping an existing Doc through plain text.  
\--- PRE-DELIVERY STRUCTURAL-PARITY CHECK (added 17 May 2026\) \---  
Before delivering any SAD .docx whose source is a Google Doc, diff structure not just text: count tables, body images, and footnotes in the source Doc (GET\_DOCUMENT\_BY\_ID structural JSON, not plaintext) and confirm the same counts in the built .docx. A clean validate.py and a correct word count are NOT sufficient and must never again be reported as "passed every check" when this parity check has not been run. State the table/image/footnote counts explicitly in the delivery message.  
\--- HISTORY \---  
Doc I had H1-H3 styling and Blocksatz but no TOC. Doc II had inconsistent heading formatting and no Blocksatz, but introduced the gold-line aesthetic which Michael liked. Pattern 18 consolidates the best of both. 17 May 2026: source-fidelity rule and structural-parity check added after the Doc V build dropped a table during a text-based reconstruction and the loss was not detected before delivery.  
\========================================  
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
