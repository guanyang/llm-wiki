---
name: visual-excalidraw
description: Generate Excalidraw diagrams from text content. Supports Obsidian (.md), Standard (.excalidraw), and Animated (.excalidraw with animation order) modes. Triggers on "Excalidraw", "画图", "流程图", "思维导图", "可视化", "diagram", "standard excalidraw", "animate".
---

# Excalidraw Creator

Generate valid Excalidraw JSON from text content. Read `references/excalidraw-schema.md` for element schemas and color palettes.

## Workflow

- [ ] 1. **Detect Mode**: Based on user keywords (`Obsidian` = default, `Standard` = standard excalidraw, `Animated` = animate).
- [ ] 2. **Analyze**: Identify structure, nodes, and relationships.
- [ ] 3. **Draft**: Calculate positions. Account for minimum gaps (20-30px) and text widths. Text centering: `x = centerX - (text.length * fontSize * 0.5)`. Note: CJK uses `* 1.0` instead of `* 0.5`.
- [ ] 4. **Generate JSON**: Create elements with unique IDs.
- [ ] 5. **Output**: Use the appropriate file format and wrapping based on the mode. Save to the current working directory.

## Output Modes & Formats

### 1. Obsidian Format (Default)

**Required file extension:** `.md`

**Wrapper format:**

```markdown
---
excalidraw-plugin: parsed
tags: [excalidraw]
---
==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠== You can decompress Drawing data with the command palette: 'Decompress current Excalidraw file'. For more info check in plugin settings under 'Saving'

# Excalidraw Data

## Text Elements
%%
## Drawing
\`\`\`json
{ JSON Data }
\`\`\`
%%
```

*(Leave `## Text Elements` empty. Obsidian auto-populates it.)*

### 2. Standard Format

**Required file extension:** `.excalidraw`

**Wrapper format:** None. Raw JSON only. `source` must be `"https://excalidraw.com"`.

### 3. Animated Format

**Required file extension:** `.animate.excalidraw`

Raw JSON, but each element must include an animation order:

```json
"customData": { "animate": { "order": 1, "duration": 500 } }
```

*(Order 1 plays first. Same order = simultaneous).*

## Gotchas & Design Rules

- **DO NOT include**: `frameId`, `index`, `versionNonce`, or `rawText` fields.
- **Required defaults**: `boundElements: null` (not `[]`), `updated: 1` (not timestamp), `locked: false`.
- **Text Font**: All text must use `fontFamily: 5` (Excalifont) and `lineHeight: 1.25`.
- **Chinese Quotes**: Use `『』` for double quotes and `「」` for single quotes. Standard `"` will break JSON.
- **No Emoji**: Use colors/shapes to indicate meaning instead.
- **Text Visibility**: Minimum font size is 14px (but usually 16-20px). Contrast: dark text on light backgrounds (not lighter than `#757575` on white).
- **Coordinate Canvas**: Recommended bounds are `0-1200` width, `0-800` height.

## References

| File | Content | Tokens |
|------|---------|--------|
| `references/excalidraw-schema.md` | Element templates, bindings, palettes | ~600 |
