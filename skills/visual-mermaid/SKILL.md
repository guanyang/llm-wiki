---
name: visual-mermaid
description: Generate syntactically safe Mermaid diagrams from text. Triggers on "Mermaid", "画图", "流程图", "思维导图", "mermaid diagram".
---

# Mermaid Creator

Generate syntactically safe, professional Mermaid diagrams.

## Workflow

- [ ] 1. **Analyze**: Identify graph type (Flowchart, Sequence, Mindmap, etc.) and direction (TB/LR).
- [ ] 2. **Draft**: Create nodes and edges. Strictly adhere to syntax gotchas (especially list syntax conflicts).
- [ ] 3. **Style**: Apply professional semantic colors to nodes.
- [ ] 4. **Output**: Wrap in ` ```mermaid ` code fence. Save output or print directly to user.

## Gotchas & Syntax Rules (CRITICAL)

- **Number List Conflict**: `1. Text` will break Markdown parsers. **MUST USE** `1.Text` (no space), `① Text`, or `[1] Text`.
- **Subgraph Naming**: Subgraphs with spaces MUST use IDs: `subgraph core["Core Process"]`. Never `subgraph Core Process`.
- **Node References**: Edges must connect node IDs, never node labels. (e.g. `A --> B`, not `Title --> B`).
- **Forbidden Characters in Labels**: Replace `"` with `『』` and `()` with `「」`.
- **Line Breaks**: HTML `<br/>` only works reliably in circular nodes `(( ))`. Use separate nodes for long text.

## Color Palette (Inline Styling)

Apply via `style NodeID fill:#hex,stroke:#hex,stroke-width:2px`

- **Input/Success**: `fill:#d3f9d8,stroke:#2f9e44`
- **Process/Logic**: `fill:#e5dbff,stroke:#5f3dc4`
- **Action/Highlight**: `fill:#ffe8cc,stroke:#d9480f`
- **Output/Result**: `fill:#c5f6fa,stroke:#0c8599`
- **Title/Header**: `fill:#1971c2,stroke:#1971c2,color:#ffffff`
- **Neutral/Background**: `fill:#f8f9fa,stroke:#dee2e6`

## References

| File | Content | Tokens |
|------|---------|--------|
| `references/syntax-rules.md` | Detailed syntax edge cases & advanced layout patterns | ~200 |
