---
name: visual-canvas
description: >
  Create Obsidian Canvas (.canvas) files to visualize information, create mind maps,
  or organize notes spatially. Use this skill when the user wants to "see" their
  data, map out relationships, brainstorm topics, or convert text outlines into
  visual diagrams, even if they don't explicitly mention "Canvas."
---

# Canvas Creator

Generate valid Obsidian `.canvas` JSON from text content. Read `references/canvas-spec.md` first for node/edge schema and a complete example.

## Workflow

- [ ] 1. **Analyze**: Identify Root, Branches, Leaves from input.
- [ ] 2. **Layout**: MindMap (single root → radial) or Freeform (zones). Read `references/layout-algorithms.md` for positioning formulas.
- [ ] 3. **Validate**: All IDs unique · no overlaps (min gap: 400px H, 250px V) · all edge refs valid · groups before children in array.
- [ ] 4. **Output**: Raw JSON only — `{"nodes": [...], "edges": [...]}`. No wrapping text or code fences.

## Gotchas

- **Chinese quotes**: Double → 『』, Single → 「」, Standard double → `\"`. Failing this breaks JSON.
- **Z-index**: Groups → sub-groups → content nodes, in that order in the `nodes` array.
- **No emoji**: Use color presets `"1"`–`"6"` instead.
- **Overlap**: Node A at (0,0) with width=250 → Node B must start at x≥650 (250 + 400 gap).

## References

| File | Content | Tokens |
|------|---------|--------|
| `references/canvas-spec.md` | Node types, edge attrs, colors, complete example | ~700 |
| `references/layout-algorithms.md` | Radial, tree, grid formulas, edge side calc | ~500 |
| `assets/template-mindmap-simple.canvas` | Working MindMap | — |
| `assets/template-freeform-grouped.canvas` | Working Freeform with groups | — |
