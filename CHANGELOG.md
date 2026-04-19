# Changelog

## [2026-04-19] — v4.2: Visual Compilation Engines

### Overview

Expanded the wiki ecosystem with native visual compilation capabilities. Introduced three specialized diagramming engines (Canvas, Excalidraw, Mermaid) to generate highly precise architecture diagrams and mind maps, treating visual thinking as a first-class citizen alongside text.

### New Features

- **`visual-canvas` skill** — Built-in Obsidian Canvas visualization engine with native layout algorithms for spatially organizing concepts and mind maps.
- **`visual-excalidraw` skill** — Specialized Excalidraw architecture diagram engine featuring strict JSON crash-prevention rules for reliable drawing.
- **`visual-mermaid` skill** — Dedicated Mermaid graph generation workflow with guidelines to avoid common Markdown rendering conflicts.
- **Visual Mind Library** — Added `raw/visual/` directory to store and manage the raw source files for these three visual engines.

## [2026-04-19] — v4.1: Web Re-verification, Refresh Subcommand & Skill Optimization

### Overview

Major upgrade to the `llm-wiki` skill (v3.1 → v4.1). Introduces the `refresh` subcommand for web-based knowledge re-verification, enhances `query` with proactive freshness checks, strengthens `lint` with semantic evaluation, and removes output deliverable lifecycle tracking to reduce complexity.

### New Features

- **`refresh` subcommand** — Re-verify a specific topic via web search, compare with existing wiki content, persist updates to `raw/` after user confirmation, then trigger ingest
- **`query` freshness check** — Pages with confidence < 0.6 or stale status now trigger proactive web search for latest information
- **`lint` semantic enhancements** — One-way link semantic relevance assessment; staleness probing suggests `refresh` for high-frequency topics in stale pages
- **`publish` verification checklist** — Added 3-item verification checklist (no wikilinks, complete frontmatter, proper citations)
- **Web re-verification reinforcement** — New +0.20 confidence boost when web re-verification finds no conflict; any refresh/web verification resets time decay timer

### Removed

- **Output deliverable lifecycle tracking** — Removed `## Output Deliverable Tracking` section from `lifecycle-spec.md`, removed `calc_output_staleness()` from `lifecycle-check.py`, removed output-related references from `SKILL.md`. Layered consolidation (including Procedural layer) is preserved.

### Modified

- **skills/llm-wiki/SKILL.md** (v3.1 → v4.1) — Added `refresh` subcommand workflow; enhanced `query` step 3-4 with freshness check and incremental save; enhanced `lint` step 3 with one-way link evaluation and staleness probing; added `publish` verification checklist; added gotcha about refresh requiring user confirmation; updated description with natural language trigger phrases
- **skills/llm-wiki/references/lifecycle-spec.md** — Added +0.20 reinforcement event for web re-verification; added clarification paragraph about refresh resetting time decay; removed `Output tracking` from data distribution table; removed `## Output Deliverable Tracking` section
- **skills/llm-wiki/references/log-spec.md** — Enriched `lint` log format (check results + fix actions sections); added source field to `publish` log; added `refresh` log entry type
- **skills/llm-wiki/references/output-page-spec.md** — Aligned frontmatter with wiki-page-spec pattern (`aliases`, `tags`, `sources`, `description` instead of `type`, `audience`, `status`, `wiki_sources`); added body structure rules (h2/h3 hierarchy, code block language annotation)
- **skills/llm-wiki/scripts/lifecycle-check.py** — Removed `calc_output_staleness()` function and Output section parsing; simplified `parse_lifecycle()` return value
- **AGENTS.md** — Fixed lifecycle reference path (`lifecycle.md` → `lifecycle-spec.md`); updated subcommand count to five; added `refresh` subcommand; added core principle #9 (Web Re-verification)
- **CLAUDE.md** — Updated subcommand count to five; added `refresh` subcommand; added core principle #9
- **GEMINI.md** — Added core principle #9 (Web Re-verification)
- **README.md** — Updated subcommand count to five; added Refresh capability and workflow rows; updated Query descriptions with freshness check; added "Web Re-verification & Fact Preservation" section; added "7. Re-verify Topics" Quick Start section

## [2026-04-15] — i18n: Full English Translation + Architecture Upgrade to Skill-based System

### Overview

Translated the entire project from Chinese to English (except `docs/`), and restructured the schema from monolithic inline specs to a modular skill-based architecture with progressive disclosure.

### Architecture Changes

The three schema files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) were significantly refactored:

- **Before**: Each file was a self-contained ~220-line monolith embedding all rules inline — page format specs, tag system, naming conventions, index/log format, full workflow steps, and directory structure descriptions.
- **After**: Each file is a ~50-70 line overview referencing the shared `skills/llm-wiki/` skill. Detailed rules are loaded on demand via 7 reference spec documents.

Key structural additions:
- Added `Skills` layer to the architecture table (between Schema and Raw Sources)
- Added knowledge lifecycle management section (confidence scoring, state transitions, forgetting curve, supersession, demotion, layered consolidation)
- Added "Progressive Disclosure" as the 8th core principle

### Modified (tracked files)

- **AGENTS.md** (295 → 53 lines) — Translated to English; refactored from monolithic spec to concise overview referencing `skills/llm-wiki/SKILL.md`
- **CLAUDE.md** (221 → 70 lines) — Translated to English; refactored from monolithic spec to concise overview with Claude Code tool adaptation notes (`Read`/`Write`/`Edit`/`MultiEdit`/`Glob`/`Grep`, `TodoWrite` for task management)
- **GEMINI.md** (224 → 76 lines) — Translated to English; refactored from monolithic spec to concise overview with Gemini CLI tool adaptation notes (`read_file`/`write_file`/`edit_file`/`list_directory`/`shell`, context window management)
- **README.md** — Translated to English; language switcher flipped from `简体中文 | English` to `English | 简体中文`; added sections on lifecycle management, layered consolidation (four-tier memory model), progressive disclosure, core capabilities table; architecture tree now includes `skills/`, `log-archive/`, `lifecycle.md`

### Deleted

- **README.en.md** — Removed; `README.md` is now the English version (was previously the Chinese version)

### Added (new untracked files)

- **README.zh.md** — Placeholder for future Chinese version (referenced by README.md language switcher, not yet created with content)
- **CHANGELOG.md** — This file
- **docs/Agent-Skills-Specification.md** — Agent Skills specification document
- **skills/llm-wiki/SKILL.md** — Main skill definition with four subcommands (ingest/query/lint/publish), including detailed workflow steps, verification checklists, gotchas, and on-demand reference loading table
- **skills/llm-wiki/references/wiki-page-spec.md** — Wiki page format spec (directory structure, frontmatter schema, body structure requirements)
- **skills/llm-wiki/references/output-page-spec.md** — Output deliverable page spec (directory structure, frontmatter, type-specific format requirements)
- **skills/llm-wiki/references/tags-spec.md** — Tag system (3 dimensions: domain/type/maturity); tags converted from Chinese to lowercase hyphenated English (e.g. `软件工程` → `software-engineering`, `对比分析` → `comparative-analysis`)
- **skills/llm-wiki/references/naming-spec.md** — Page naming conventions by type
- **skills/llm-wiki/references/index-spec.md** — index.md table format spec (with confidence and status columns)
- **skills/llm-wiki/references/log-spec.md** — log.md append-only format spec with 30-day retention and archive rules
- **skills/llm-wiki/references/lifecycle-spec.md** — Full lifecycle management spec (confidence initial values/reinforcement/event decay/time decay with type coefficients, state transition diagram, supersession mechanism, demotion mechanism, layered consolidation promotion rules, output deliverable tracking)
- **wiki/lifecycle.md** — Lifecycle registry (pluggable module tracking access counts, last_accessed, supersession chains, and output deliverables)

### Not Changed

- `docs/` — Excluded from translation per request
- `wiki/index.md`, `wiki/log.md` — Already minimal English content, unchanged
- `LICENSE`, `.gitignore` — Not applicable
