# AGENTS.md — LLM Wiki Schema

> This file is the meta-configuration for LLM-maintained Wiki. The LLM must read this file before every operation and strictly follow the specifications below.

---

## Architecture Overview

| Layer | Location | Owner | Permissions |
|---|---|---|---|
| Schema | `AGENTS.md` | Human + LLM co-evolution | LLM read-only |
| Skills | `skills/` | Human + LLM co-evolution | LLM read-only |
| Raw Sources | `raw/` | Human | LLM read-only, never modify |
| Wiki | `wiki/` | LLM | LLM read-write, human read-only |
| Output | `output/` | LLM generates, human reviews and finalizes | LLM read-write |

## Skill

All wiki operations are executed through the `llm-wiki` skill, supporting four subcommands:

```
/llm-wiki ingest   — Digest raw material into wiki
/llm-wiki query    — Retrieve knowledge from wiki
/llm-wiki lint     — Check wiki health
/llm-wiki publish  — Produce polished output from wiki
```

Full workflow definition: `skills/llm-wiki/SKILL.md`

## Knowledge Lifecycle Management

> Full rules in `skills/llm-wiki/references/lifecycle.md`

**Pluggable**: Deleting `wiki/lifecycle.md` does not affect core wiki functionality.

**Core Mechanisms**:
- **Confidence**: 0.0–1.0, dynamically adjusted based on source count, access frequency, and time decay
- **State Transitions**: active → stale → archived, with recovery support
- **Supersession**: superseded_by/supersedes bidirectional links, version chain traceability
- **Forgetting Curve**: During lint, confidence decay is calculated as days-since-last-access × type coefficient
- **Layered Consolidation**: summaries → entities/concepts → comparisons/synthesis → output, progressive promotion
- **Demotion**: When high-level conclusions are disproven, demote to stale pending re-verification

## Core Principles

1. **Raw is Immutable**: Never modify any file under `raw/`
2. **Wiki is a Compiled Artifact**: All content can be regenerated from raw
3. **Knowledge Compound Interest**: Every operation makes the wiki richer
4. **Cross-references First**: `[[Wikilinks]]` are the wiki's greatest value
5. **Contradictions are Transparent**: Explicitly annotated with sources cited
6. **Complete Logging**: All operations recorded in log.md
7. **Progressive Evolution**: Schema co-maintained by humans and LLM
8. **Progressive Disclosure**: Detailed rules are distilled into skill references, loaded on demand
