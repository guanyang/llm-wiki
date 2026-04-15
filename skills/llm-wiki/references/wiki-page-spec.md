# Wiki Page Format Specification

## Directory Structure

```
wiki/
├── index.md                   # Global index (with confidence, status)
├── log.md                     # Operation log (most recent 30 days)
├── log-archive/               # Log archive (by month)
├── lifecycle.md               # [Pluggable] Detailed lifecycle data
├── entities/                  # Entity pages (tools, frameworks, organizations, people)
├── concepts/                  # Concept pages (design patterns, methodologies, theoretical frameworks)
├── summaries/                 # Material summary pages (one file per digested material)
├── comparisons/               # Comparative analysis pages (A vs B)
└── synthesis/                 # Synthesis analysis pages (cross-material synthesis, trend analysis)
```

## Frontmatter

Every wiki page must include:

```yaml
---
title: Page Title
aliases: [alias1, alias2]
tags: [tag1, tag2]
category: entities | concepts | summaries | comparisons | synthesis
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - "[[raw/path/source-filename]]"
description: One-sentence summary, no more than 100 characters
---
```

## Body Structure Requirements

- Clear h2/h3 heading hierarchy
- Key terms use `[[wikilinks]]` to reference other wiki pages
- Raw material references use `[[raw/path/filename]]` format
- Every page ends with a `## Related Pages` section listing all cross-references
- Code blocks specify the language type
