# LLM Wiki — Personal Knowledge Base

[简体中文](README.md) | **English**

A personal knowledge base continuously maintained by Obsidian + LLM. Inspired by [Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

Core idea: knowledge is **compiled once and continuously accumulated**, not re-derived from scratch on every query. Humans curate sources and ask questions; the LLM handles all the tedious work — summarizing, cross-referencing, filing, and consistency maintenance.

## How It Differs from Traditional RAG

| | Traditional RAG | LLM Wiki |
|---|---|---|
| Knowledge storage | Raw documents + vector index | Structured, interlinked Markdown pages |
| Query approach | Retrieve and assemble from scratch each time | Synthesize answers from pre-compiled knowledge |
| Knowledge accumulation | None — re-derived every time | Yes — every operation makes the wiki richer |
| Cross-references | None | Automatically maintained `[[wikilink]]` network |
| Contradiction handling | Unaware | Proactively flagged with source attribution |

## Architecture

```
├── AGENTS.md          # Schema (OpenAI Codex and other generic agents)
├── CLAUDE.md          # Schema (Claude Code adaptation)
├── GEMINI.md          # Schema (Gemini CLI adaptation)
├── raw/               # Raw sources (human-curated, LLM read-only)
│   ├── articles/      # Web articles, blog posts
│   ├── papers/        # Academic papers, whitepapers
│   ├── docs/          # Official documentation excerpts
│   ├── transcripts/   # Meeting notes, talk transcripts, podcast notes
│   └── assets/        # Images, diagrams, data files
├── wiki/              # LLM-compiled artifacts (LLM read-write, human read-only)
│   ├── index.md       # Global index
│   ├── log.md         # Operation log
│   ├── entities/      # Entity pages (tools, frameworks, people)
│   ├── concepts/      # Concept pages (patterns, methodologies)
│   ├── summaries/     # Source summary pages
│   ├── comparisons/   # Comparison & analysis pages
│   └── synthesis/     # Synthesis pages (cross-source analysis)
└── output/            # Finished outputs (LLM-generated, human-reviewed)
    ├── posts/         # Blog posts, articles
    ├── reports/       # Research reports, technical assessments
    ├── slides/        # Presentations (Marp markdown format)
    ├── tutorials/     # Step-by-step tutorials
    └── newsletters/   # Weekly/monthly knowledge digests
```

## Workflows

| Operation | Trigger | Description |
|---|---|---|
| Ingest | Drop new source into `raw/`, tell LLM to process | LLM reads source → extracts key points → creates/updates wiki pages → maintains cross-references |
| Query | Ask the LLM a question | LLM answers from pre-compiled wiki knowledge; valuable answers can be filed back into wiki |
| Lint | Periodically ask LLM to check | Detects contradictions, orphan pages, missing references, stale content — keeps wiki healthy |
| Publish | Ask LLM to distill output from wiki | LLM generates draft, human reviews and finalizes |

## Core Principles

- **Schema layer** (`AGENTS.md` / `CLAUDE.md` / `GEMINI.md`): tells the LLM how to maintain the wiki
- **Raw layer** (`raw/`): immutable source materials, the source of truth
- **Wiki layer** (`wiki/`): LLM's compiled artifacts, structured representation of all knowledge
- **Output layer** (`output/`): polished deliverables distilled from wiki, standalone and audience-facing
- Compound knowledge: every operation makes the wiki richer
- See [AGENTS.md](AGENTS.md) for full specification

## Quick Start

### 1. Choose Your LLM Agent

This project provides three equivalent schema files — pick the one matching your tool:

| Tool | Schema File | Notes |
|------|-----------|------|
| OpenAI Codex / Generic | `AGENTS.md` | Universal schema |
| Claude Code | `CLAUDE.md` | Adapted for Claude's tool calling |
| Gemini CLI | `GEMINI.md` | Adapted for Gemini's tools and context window |
| Kiro | `AGENTS.md` | Kiro auto-reads AGENTS.md |

### 2. Add Sources

Place source materials into the appropriate `raw/` subdirectory:

```bash
# Web articles (recommend using Obsidian Web Clipper to save as Markdown)
raw/articles/2026-04-13-some-article.md

# Academic papers
raw/papers/2026-04-13-some-paper.pdf

# Meeting notes, reading notes
raw/transcripts/2026-04-13-meeting-notes.md
```

Tip: include source URL, author, and date at the top of each file.

### 3. Let the LLM Ingest

Tell your LLM agent:

```
Ingest raw/articles/2026-04-13-some-article.md
```

The LLM will:
1. Read the source and discuss key takeaways with you
2. Create a summary page in `wiki/summaries/`
3. Create or update relevant entity and concept pages
4. Maintain all cross-references
5. Update the global index and operation log

### 4. Ask Questions

Ask the LLM directly — it answers from pre-compiled wiki knowledge:

```
Compare the pros and cons of Playwright vs Cypress
```

Valuable answers can be filed as wiki pages (comparisons or synthesis).

### 5. Publish Outputs

Distill audience-facing deliverables from the wiki:

```
Turn the wiki knowledge about Playwright vs Cypress into a blog post
```

The LLM distills content from wiki, converts to standalone Markdown, and saves to `output/posts/`. You review and finalize.

Supported output types: blog posts, research reports, Marp slides, tutorials, newsletters.

### 6. Lint

Periodically ask the LLM to health-check the wiki:

```
Lint the wiki
```

The LLM checks for contradictions, orphan pages, missing concept pages, stale information, etc.

## Obsidian Configuration Guide

The wiki layer is fully compatible with [Obsidian](https://obsidian.md/). Use Obsidian as your browser — the LLM edits on one side, you browse in real time on the other.

### Basic Setup

1. Open this project's root directory as an Obsidian Vault

2. Go to **Settings → Files and links**:

   | Setting | Recommended Value | Notes |
   |---------|-------------------|-------|
   | Default location for new notes | `raw/articles` | New notes go to raw by default |
   | New link format | Shortest path when possible | Clean link format |
   | Use `[[Wikilinks]]` | Enabled | Enable wikilink syntax |
   | Attachment folder path | `raw/assets/` | Centralized attachment storage |
   | Detect all file extensions | Enabled | Recognize PDFs and other non-md files |

3. Go to **Settings → Editor**:

   | Setting | Recommended Value | Notes |
   |---------|-------------------|-------|
   | Show frontmatter | Enabled | Display YAML metadata |
   | Readable line length | Enabled | Better reading experience |

### Recommended Plugins

#### Obsidian Community Plugins

Search and install in **Settings → Community plugins**:

| Plugin | Purpose | Configuration |
|--------|---------|---------------|
| **Dataview** | Dynamic metadata queries | Use `dataview` code blocks to query frontmatter fields (tags, sources, etc.) and generate dynamic tables |
| **Excalidraw** | Hand-drawn style whiteboard & diagrams | Embed architecture diagrams, flowcharts, concept maps in wiki pages. Store files in `raw/assets/`, embed via `![[filename.excalidraw]]` |
| **Local Images Plus** | Auto-download remote images to local | Set download path to `raw/assets/`. Automatically downloads remote images to local and replaces links when pasting or importing articles |

#### Browser Extensions

| Extension | Browser | Purpose | Configuration |
|-----------|---------|---------|---------------|
| **Obsidian Web Clipper** | Chrome / Firefox / Safari | One-click save web articles as Markdown | Set save path to `raw/articles/`. Pairs with Local Images Plus to auto-download article images |

### Graph View Configuration

Obsidian's Graph View is the best way to visualize your knowledge structure:

1. Open Graph View (`Ctrl/Cmd + G`)
2. Recommended filter settings:
   - **Filters → Search files**: enter `path:wiki/` to show only wiki pages
   - **Groups**: color-code by directory to distinguish page types
     - `path:wiki/entities` → Blue
     - `path:wiki/concepts` → Green
     - `path:wiki/summaries` → Yellow
     - `path:wiki/comparisons` → Orange
     - `path:wiki/synthesis` → Purple
3. What to look for:
   - Most-connected nodes are knowledge hubs
   - Isolated nodes may need more cross-references
   - Clusters reveal natural groupings of knowledge domains

### Dataview Query Examples

With the Dataview plugin installed, use these queries in any Markdown file:

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

**List all source summaries**:

````markdown
```dataview
TABLE sources, description, created
FROM "wiki/summaries"
SORT created DESC
```
````

### Downloading Images Locally

To prevent broken external image links:

- **Recommended**: Install the **Local Images Plus** plugin (see above). It automatically downloads remote images to `raw/assets/` and replaces links when you paste or import articles.
- **Manual**: Go to **Settings → Hotkeys**, search "Download", and bind "Download attachments for current file" to a hotkey (e.g. `Ctrl+Shift+D`). After clipping an article with Web Clipper, press the hotkey.

## License

> Project structure and schema design inspired by [Karpathy's LLM Wiki concept](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

MIT License — see [LICENSE](LICENSE).
