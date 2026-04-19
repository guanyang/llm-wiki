# LLM Wiki — Personal Knowledge Base

**English** | [简体中文](README.zh.md)

A personal knowledge base continuously maintained with Obsidian + LLM Wiki. Inspired by [Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

Core idea: Knowledge is not derived from scratch on every query — it is **compiled once and continuously accumulated**. Humans curate materials and ask questions; the LLM handles all the tedious organization work — summarization, cross-referencing, archiving, and consistency maintenance.

## How It Differs from Traditional RAG

| | Traditional RAG | LLM Wiki |
|---|---|---|
| Knowledge Storage | Raw documents + vector index | Structured, interlinked Markdown pages |
| Query Method | Retrieve and assemble from scratch each time | Answer based on pre-compiled knowledge |
| Knowledge Accumulation | None — re-derived every time | Yes — every operation makes the wiki richer |
| Cross-references | None | Automatically maintained `[[wikilink]]` network |
| Contradiction Handling | Unaware | Proactively annotated with sources cited |

## Architecture

```
├── AGENTS.md          # Schema spec (OpenAI Codex and other general agents)
├── CLAUDE.md          # Schema spec (Claude Code adaptation)
├── GEMINI.md          # Schema spec (Gemini CLI adaptation)
├── skills/                # Agent Skills (detailed workflow rules, loaded on demand)
│   └── llm-wiki/          # LLM Wiki skill
│       ├── SKILL.md       # Five subcommands: ingest/query/lint/publish/refresh
│       └── references/    # Shared spec documents (7 *-spec.md files)
├── raw/               # Raw materials (human-curated, LLM read-only)
│   ├── articles/      # Web articles, blog posts
│   ├── papers/        # Academic papers, white papers
│   ├── docs/          # Official documentation excerpts
│   ├── transcripts/   # Meeting notes, talks, podcast notes
│   └── assets/        # Images, diagrams, data files
├── wiki/              # LLM compiled artifacts (LLM read-write, human read-only)
│   ├── index.md       # Global index
│   ├── log.md         # Operation log
│   ├── log-archive/   # Log archive (by month)
│   ├── lifecycle.md   # [Pluggable] Detailed lifecycle data
│   ├── entities/      # Entity pages (tools, frameworks, people)
│   ├── concepts/      # Concept pages (patterns, methodologies)
│   ├── summaries/     # Material summary pages
│   ├── comparisons/   # Comparative analysis pages
│   └── synthesis/     # Synthesis analysis pages
└── output/            # Polished output (LLM generates, human reviews and finalizes)
    ├── posts/         # Blog posts, articles
    ├── reports/       # Research reports, technical survey reports
    ├── slides/        # Presentations (Marp format)
    ├── tutorials/     # Tutorials, step-by-step guides
    └── newsletters/   # Weekly, monthly, knowledge briefings
```

## Core Principles

### Compilation over Retrieval

Traditional RAG retrieves from raw documents and assembles answers from scratch on every query — knowledge never accumulates. LLM Wiki takes the opposite approach: each time material is ingested, the LLM **compiles** knowledge into structured wiki pages, and subsequent queries are answered based on pre-compiled knowledge. Knowledge is compiled, linked, and continuously optimized — just like code.

### Knowledge Lifecycle Management

Knowledge doesn't stay valid forever once written. This project introduces a complete lifecycle management mechanism:

- **Confidence Scoring**: Each page carries a confidence score (0.0–1.0), dynamically adjusted based on source count, access frequency, and time decay. Knowledge cross-confirmed by multiple sources is more trustworthy than single-source knowledge.
- **Forgetting Curve**: Inspired by the Ebbinghaus forgetting curve, knowledge that hasn't been accessed or reinforced over time naturally decays in confidence. Different types decay at different rates — conceptual knowledge decays slowly, comparative analysis decays quickly.
- **State Transitions**: active → stale → archived. Being queried or confirmed by new sources can restore active status.
- **Supersession**: When new information explicitly refutes old conclusions, superseded_by/supersedes bidirectional links enable version chain traceability. Old versions are preserved but marked as outdated.
- **Demotion**: When high-level synthesis is disproven, it is demoted to stale pending re-verification. Lower-level entities and concepts are unaffected.

### Web Re-verification & Fact Preservation

- **Fact Preservation**: The wiki is no longer a sealed black box. During `query` and `lint` workflows, the system probes for outdated or low-confidence information and suggests web re-verification. You can also proactively target a specific knowledge area with `/llm-wiki refresh`.
- **Core Safeguard**: The system retrieves the latest information via web search, but **new findings must be confirmed by the user and persisted as new files in `raw/`**, which then automatically triggers an Ingest to re-evaluate and refresh stale knowledge in the wiki. This ensures knowledge stays fresh while upholding the immutable "append-only, never modify" principle for raw materials.

### Layered Consolidation (Four-Tier Memory Model)

Knowledge progressively promotes from lower to higher tiers. Each tier is more compressed, more reliable, and has a longer lifecycle:

```
┌─────────────────────────────────────────────────┐
│  Procedural    output/*                          │  Ready-to-use deliverables
├─────────────────────────────────────────────────┤
│  Semantic      wiki/comparisons/ + synthesis/    │  Cross-material insights
├─────────────────────────────────────────────────┤
│  Episodic      wiki/entities/ + concepts/        │  Structured knowledge
├─────────────────────────────────────────────────┤
│  Working       wiki/summaries/                   │  Single-material summaries
└─────────────────────────────────────────────────┘
```

Promotion criteria: An entity/concept in a summary is mentioned by 2+ materials → create entity/concept; 3+ entities/concepts form a pattern → create comparison/synthesis; synthesis confidence ≥ 0.85 → suggest publishing as a deliverable.

### Progressive Disclosure

Detailed rules are distilled into [Agent Skills](https://agentskills.io/) (`skills/llm-wiki/`). AGENTS.md only retains a quick overview of core concepts. When executing specific operations, the LLM loads skill instructions and references on demand, avoiding heavy context consumption on every conversation.

## Core Capabilities

| Capability | Description |
|------|------|
| **Ingest** | Read materials from raw/, extract entities and concepts, create/update wiki pages, automatically maintain cross-references |
| **Query** | Answer based on compiled wiki knowledge, prioritize high-confidence pages, proactively search the web for stale/low-confidence topics, archive valuable answers |
| **Lint** | Contradiction detection, orphan pages, missing references, cross-reference integrity, lifecycle decay and state transitions |
| **Publish** | Produce blog posts, reports, slides, tutorials, briefings, and other standalone deliverables from wiki |
| **Refresh** | Re-verify a specific topic via web search, compare with existing wiki content, persist updates after user confirmation |
| **Lifecycle Management** | Confidence scoring, forgetting curve decay, state transitions, supersession/demotion, layered consolidation promotion |
| **Pluggable Extension** | Lifecycle is an enhancement layer — deleting lifecycle.md does not affect core wiki functionality |

## Workflow

All operations are executed through the `llm-wiki` skill (see `skills/llm-wiki/SKILL.md` for details):

| Operation | Usage | Description |
|---|---|---|
| Ingest | `/llm-wiki ingest <raw/path/file>` | Read material → extract key points → create/update wiki pages → maintain cross-references → update lifecycle |
| Query | `/llm-wiki query <question>` | Answer based on compiled wiki knowledge, prioritize high-confidence pages, proactively verify stale topics via web search |
| Lint | `/llm-wiki lint` | Check for contradictions, orphan pages, missing references, lifecycle decay and state transitions — keep wiki healthy |
| Publish | `/llm-wiki publish <type> [topic]` | Produce polished output from wiki; LLM generates draft, human reviews and finalizes |
| Refresh | `/llm-wiki refresh <topic>` | Re-verify a specific topic via web search; persist new information to raw/ after user confirmation |

## General Principles

- **Schema Layer** (`AGENTS.md`): Tells the LLM how to maintain the wiki — quick overview of core concepts
- **Skills Layer** (`skills/llm-wiki/`): Detailed workflow rules, loaded on demand, progressive disclosure
- **Raw Layer** (`raw/`): Immutable raw materials — the source of truth
- **Wiki Layer** (`wiki/`): LLM's compiled artifacts — structured representation of all knowledge
- **Output Layer** (`output/`): Deliverables distilled from wiki — standalone, audience-facing, independently readable
- Knowledge compound interest: Every operation makes the wiki richer
- Lifecycle management: Knowledge has temperature — frequently used knowledge warms up, long-dormant knowledge cools down
- Web re-verification: Query/lint triggers web search on demand, keeping knowledge fresh
- Detailed specs in [AGENTS.md](AGENTS.md), full workflow in [skills/llm-wiki/SKILL.md](skills/llm-wiki/SKILL.md)

## Quick Start

### 1. Choose Your LLM Agent

This project provides three equivalent schema files — pick the one matching your tool:

| Tool | Schema File | Description |
|------|-----------|------|
| OpenAI Codex / General | `AGENTS.md` | General spec |
| Claude Code | `CLAUDE.md` | Adapted for Claude's tool invocation patterns |
| Gemini CLI | `GEMINI.md` | Adapted for Gemini's tools and context window |
| Kiro | `AGENTS.md` | Kiro automatically reads AGENTS.md |

### 2. Add Materials

Place materials you want to digest into the appropriate `raw/` subdirectory:

```bash
# Web articles (recommended: save as Markdown using Obsidian Web Clipper)
raw/articles/2026-04-13-some-article.md

# Academic papers
raw/papers/2026-04-13-some-paper.pdf

# Meeting notes, reading notes
raw/transcripts/2026-04-13-meeting-notes.md
```

It's recommended to note the source URL, author, and date at the beginning of each file.

### 3. Let the LLM Digest

Tell your LLM Agent:

```
Digest raw/articles/2026-04-13-some-article.md
```

The LLM will:
1. Read the material and discuss key points with you
2. Create a material summary page (`wiki/summaries/`)
3. Create or update related entity and concept pages
4. Maintain all cross-references
5. Update the global index and operation log

### 4. Ask Questions

Ask the LLM directly — it will answer based on compiled knowledge in the wiki:

```
Compare the pros and cons of Playwright vs Cypress
```

Valuable answers can be archived as wiki pages (comparisons or synthesis).

### 5. Publish Deliverables

Produce audience-facing deliverables from wiki content:

```
Turn the wiki knowledge about Playwright vs Cypress into a blog post
```

The LLM will distill content from the wiki, convert it to standalone standard Markdown, and save it to `output/posts/`. You review and finalize.

Supported output types: blog posts, research reports, Marp slides, tutorials, knowledge briefings.

### 6. Health Check

Periodically have the LLM check wiki health:

```
Run a health check on the wiki
```

The LLM will check for contradictions, orphan pages, missing concept pages, outdated information, and more.

### 7. Re-verify Topics

When you suspect certain wiki knowledge may be outdated:

```
Refresh the wiki knowledge about Playwright
```

The LLM will search the web for latest developments, compare with existing wiki content, and ask you whether to persist updates.

## Obsidian Configuration Guide

This project's wiki layer is fully compatible with [Obsidian](https://obsidian.md/). Obsidian is recommended as the browser. The LLM edits on one side while you browse in real-time in Obsidian.

### Basic Configuration

1. Open this project's root directory as a Vault in Obsidian

2. Go to **Settings → Files and links** and adjust the following:

   | Setting | Recommended Value | Description |
   |--------|--------|------|
   | Default location for new notes | `raw/articles` | New notes default to the raw directory |
   | New link format | Shortest path when possible | Concise link format |
   | Use `[[Wikilinks]]` | Enabled | Enable wikilink syntax |
   | Attachment folder path | `raw/assets/` | Centralized attachment storage |
   | Detect all file extensions | Enabled | Recognize non-md files like PDFs |

3. Go to **Settings → Editor**:

   | Setting | Recommended Value | Description |
   |--------|--------|------|
   | Show frontmatter | Enabled | Display YAML metadata |
   | Readable line length | Enabled | Improve reading experience |

### Recommended Plugins

#### Obsidian Community Plugins

Search and install in **Settings → Community plugins**:

| Plugin | Purpose | Configuration Notes |
|------|------|---------|
| **Dataview** | Dynamic querying of page metadata | Use `dataview` code blocks to query frontmatter fields like tags, sources, etc., generating dynamic tables |
| **Excalidraw** | Hand-drawn style whiteboard and diagrams | Embed architecture diagrams, flowcharts, concept relationship maps in wiki pages. Store files in `raw/assets/`, embed via `![[filename.excalidraw]]` |
| **Local Images Plus** | Auto-download remote images to local | Set download path to `raw/assets/`. When pasting or importing articles with remote images, automatically downloads images locally and replaces links, preventing broken external links |

#### Browser Extensions

| Extension | Browser | Purpose | Configuration Notes |
|------|--------|------|---------|
| **Obsidian Web Clipper** | Chrome / Firefox / Safari | One-click save web articles as Markdown | After installation, set save path to `raw/articles/`. Works with Local Images Plus to auto-download images from articles |

### Graph View Configuration

Obsidian's Graph View is the best way to browse knowledge structure:

1. Open Graph View (`Ctrl/Cmd + G`)
2. Recommended filter settings:
   - **Filters → Search files**: Enter `path:wiki/` to show only wiki pages
   - **Groups**: Color-code by directory to distinguish entities, concepts, summaries, etc.
     - `path:wiki/entities` → Blue
     - `path:wiki/concepts` → Green
     - `path:wiki/summaries` → Yellow
     - `path:wiki/comparisons` → Orange
     - `path:wiki/synthesis` → Purple
3. Observe:
   - Nodes with the most connections are knowledge hubs
   - Isolated nodes may need additional cross-references
   - Clusters reveal natural groupings of knowledge domains

### Dataview Query Examples

After installing the Dataview plugin, you can use the following queries in any Markdown file:

**List all pages by tag**:

````markdown
```dataview
TABLE tags, description, updated
FROM "wiki"
WHERE contains(tags, "testing")
SORT updated DESC
```
````

**List recently updated pages**:

````markdown
```dataview
TABLE category, description, updated
FROM "wiki"
SORT updated DESC
LIMIT 10
```
````

**List all material summaries with their sources**:

````markdown
```dataview
TABLE sources, description, created
FROM "wiki/summaries"
SORT created DESC
```
````

### Downloading Images Locally

To prevent external image links from breaking, it's recommended to download article images locally:

- **Recommended**: Install the **Local Images Plus** plugin (see recommended plugins above). It automatically downloads remote images to `raw/assets/` and replaces links when you paste or import articles — fully automatic.
- **Manual**: Go to **Settings → Hotkeys**, search for "Download", and bind a shortcut (e.g., `Ctrl+Shift+D`) for "Download attachments for current file". After saving an article with Web Clipper, press the shortcut.

## License

> This project's structure and schema design is based on [Karpathy's LLM Wiki concept](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

MIT License — see [LICENSE](LICENSE).
