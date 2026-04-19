# Output Deliverable Page Specification

## Directory Structure

```
output/
├── posts/           # Blog posts, articles
├── reports/         # Research reports, technical survey reports
├── slides/          # Presentations (Marp markdown format)
├── tutorials/       # Tutorials, step-by-step guides
└── newsletters/     # Weekly, monthly, knowledge briefings
```

## Frontmatter

Every deliverable must include:

```yaml
---
title: Deliverable Title
aliases: [alias1, alias2]
tags: [tag1, tag2]
category: post | report | slides | tutorial | newsletter
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - "wiki/page-path"
description: One-sentence summary, no more than 100 characters
---
```

## Format Requirements

### General Rules

- Clear h2/h3 heading hierarchy
- Code blocks specify the language type
- Deliverables must be **standalone readable** — no dependency on wiki-internal `[[wikilinks]]`
- `[[wikilinks]]` → standard Markdown links or plain text
- Source citations use footnotes or bibliography format
- LLM generates draft, human reviews and finalizes

### Type-Specific Adaptation

| Type | Format Requirements |
|------|---------| 
| post | Standard Markdown with title, abstract, body, references |
| report | Standard Markdown with abstract, body, conclusions, references |
| slides | Marp format, `---` page breaks, frontmatter includes `marp: true` |
| tutorial | Clear steps, complete code, independently followable |
| newsletter | Concise item-based structure, summarizing recent key insights |
