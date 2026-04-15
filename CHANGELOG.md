# Changelog

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
