---
name: llm-wiki
description: >
  Manage a personal knowledge base built from raw notes and articles.
  Use this skill when the user wants to digest new material into the wiki,
  query existing knowledge, run a health check on wiki pages, or produce
  polished output (blog posts, reports, slides) from wiki content —
  even if they don't explicitly say "wiki." Covers: ingest raw sources,
  query and synthesize answers, lint for contradictions and staleness,
  publish deliverables. Includes knowledge lifecycle management with
  confidence scoring and memory-tier promotion.
metadata:
  author: guanyang
  version: "3.1"
  category: knowledge-management
---

# LLM Wiki

## Usage

| Subcommand | Usage | When to Use |
|--------|------|---------|
| `ingest` | `/llm-wiki ingest <raw/path/filename>` | User provides new material to digest |
| `query` | `/llm-wiki query <question>` | User asks a question to be answered from wiki |
| `lint` | `/llm-wiki lint` | User requests a wiki health check |
| `publish` | `/llm-wiki publish <type> [topic]` | User requests polished output |

Types: `post` | `report` | `slides` | `tutorial` | `newsletter`

## References (Load on Demand)

Do not pre-load. Only load when the corresponding trigger condition is met:

| Document | Trigger Condition |
|------|---------|
| [references/wiki-page-spec.md](references/wiki-page-spec.md) | When creating a new wiki page — need frontmatter format |
| [references/output-page-spec.md](references/output-page-spec.md) | When generating polished output — need output format and directory conventions |
| [references/tags-spec.md](references/tags-spec.md) | When tagging a page — unsure which tags are available |
| [references/naming-spec.md](references/naming-spec.md) | When naming a new page — unsure of naming rules |
| [references/index-spec.md](references/index-spec.md) | When updating index.md for the first time — need to confirm table format |
| [references/log-spec.md](references/log-spec.md) | When writing a log for the first time — need to confirm record format |
| [references/lifecycle-spec.md](references/lifecycle-spec.md) | When encountering confidence anomalies, needing to understand decay formulas, or handling supersession/demotion |

## Gotchas

- **Never modify any file in `raw/`**. Raw is the immutable source of truth.
- **lifecycle.md is pluggable**. All lifecycle steps are conditional on "if lifecycle.md exists" — skip if it doesn't.
- **index.md uses table format** — each row contains confidence and status columns, not list format.
- **Deliverables must be standalone readable**. Publish output must not contain `[[wikilinks]]` — convert to standard links or plain text.
- **A single ingest may update 10–15 pages** — this is normal. Don't hesitate because of many changes.
- **Stale pages can be referenced but must be annotated**. When a query references a stale page, note "this information may be outdated" in the answer.

---

## ingest

Read source files from `raw/`, extract knowledge, create/update wiki pages.

1. **Read source file**: Read the specified file from `raw/`
2. **Extract key information**: Identify entities, concepts, core arguments, data, conclusions
3. **Discuss key points with user**: Report key findings, confirm focus areas
4. **Create/update wiki pages**:
   - Summary page → `wiki/summaries/`
   - Entity page → `wiki/entities/`
   - Concept page → `wiki/concepts/`
   - Page format: see `wiki-page-spec`; tags: see `tags-spec`; naming: see `naming-spec`
5. **Handle contradictions**: New material contradicts existing content → explicitly annotate in the page, citing both old and new sources; if lifecycle.md exists, contradiction page confidence −0.15
6. **Maintain cross-references**: `[[wikilinks]]` between all related pages
7. **Lifecycle assessment** (if lifecycle.md exists):
   - New page: set initial confidence (thin 0.55 / substantial 0.65 / multi-source 0.75 / synthesis 0.80)
   - Existing page confirmed by new source: confidence +0.10
   - Check promotion: entity/concept in summary mentioned by 2+ materials → create entity/concept
   - Check supersession: core conclusion overturned → old page superseded_by → new page, status → archived, add supersession notice to body
8. **Update index.md**: Add/update entries with confidence and status (format: see `index-spec`)
9. **Update lifecycle.md** (if exists): New pages get new rows; existing pages update access and last_accessed
10. **Record log**: Append to `wiki/log.md` (format: see `log-spec`)

### Verification

After completion, check:
- [ ] All new pages have complete frontmatter
- [ ] All `[[wikilinks]]` point to existing pages
- [ ] index.md page count is updated
- [ ] log.md has a new entry appended

---

## query

Retrieve knowledge from wiki and synthesize answers to user questions.

1. **Read index.md**: Locate relevant pages, prioritizing high confidence and active status
2. **Read relevant pages**: Deep-read entities, concepts, summaries, etc.
3. **Synthesize answer**: Answer based on wiki content — do not re-derive from raw. When referencing stale pages, note "this may be outdated"
4. **Update lifecycle** (if lifecycle.md exists): Hit pages → lifecycle.md access +1, last_accessed updated; index.md confidence +0.05. Do not modify the queried pages themselves
5. **Provide citations**: Reference specific wiki pages and original material sources in the answer
6. **Offer archival**: If the answer has reuse value → ask user whether to save to comparisons/ or synthesis/
7. **Record log**

> When wiki information is insufficient, you may refer back to `raw/` for supplementation, and update the wiki accordingly.

---

## lint

Check wiki health and fix issues.

1. **Structural checks**:
   - Contradiction detection: Contradictory claims between pages
   - Orphan pages: Pages with no incoming links (index.md links don't count)
   - Missing pages: Referenced by multiple `[[wikilinks]]` but not yet created
   - Cross-references: Bidirectional links between related pages
   - Frontmatter: Required field completeness (title/tags/category/created/updated/sources/description)
2. **Lifecycle checks** (if lifecycle.md exists):
   - Time decay: Calculate confidence decay based on days since last_accessed (rules in `lifecycle-spec`), update index.md and lifecycle.md
   - State transitions: active → stale (90 days unaccessed and confidence < 0.5) → archived (180 days with no new sources)
   - Demotion: synthesis/comparison core conclusion disproven → set status to stale, confidence −0.15, add warning to body
   - Promotion suggestions: Pages meeting promotion criteria but not yet promoted
   - Outdated deliverables: Dependent pages are stale/archived → mark deliverable as outdated
   - Lint pass reward: Pages with no contradictions get confidence +0.02
3. **Log archival**: Records older than 30 days → `wiki/log-archive/YYYY-MM.md`
4. **Generate fix list**: Output issue list, execute fixes after user confirmation
5. **Record log**

### Verification

After fixes, re-scan to confirm:
- [ ] All confirmed items in the issue list are fixed
- [ ] No new broken links
- [ ] index.md page count is accurate

---

## publish

Produce polished, audience-facing deliverables from wiki content.

1. **Clarify requirements**: Confirm type (post/report/slides/tutorial/newsletter), audience, length
2. **Locate source material**: Read index.md, prioritize high-confidence active pages
3. **Read sources**: Deep-read relevant pages
4. **Generate draft**: Write deliverable based on wiki content, save to appropriate `output/` subdirectory (format: see `output-page-spec`)
5. **Format adaptation**: `[[wikilinks]]` → standard links or plain text; citations use footnotes; adapt format by type (see `output-page-spec`)
6. **Update lifecycle** (if lifecycle.md exists): Referenced pages → lifecycle.md access +1, last_accessed updated; index.md confidence +0.15; add new deliverable record to Output section
7. **User review**: Present draft, revise based on feedback
8. **Record log**

> When synthesis confidence ≥ 0.85, proactively suggest publishing. For briefing types, semi-automation is possible: read recent log.md entries and summarize.
