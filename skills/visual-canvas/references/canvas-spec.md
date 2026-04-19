# JSON Canvas Specification (Obsidian)

Top-level structure:

```json
{
  "nodes": [...],
  "edges": [...]
}
```

## Node Types

All nodes share: `id` (string), `type` (string), `x` (int), `y` (int), `width` (int), `height` (int), `color` (optional, string).

### text

```json
{"id": "abc123", "type": "text", "x": 0, "y": 0, "width": 250, "height": 100, "text": "# Title\n\nContent", "color": "4"}
```

### file

```json
{"id": "def456", "type": "file", "x": 300, "y": 0, "width": 400, "height": 300, "file": "path/to/file.md"}
```

Optional: `subpath` (string, e.g. `"#Heading"`) to link a specific section.

### link

```json
{"id": "jkl012", "type": "link", "x": 0, "y": -200, "width": 250, "height": 100, "url": "https://example.com"}
```

### group

Visual container. Must appear **before** child nodes in the `nodes` array.

```json
{"id": "group1", "type": "group", "x": -50, "y": -50, "width": 600, "height": 400, "label": "Section Title", "color": "4"}
```

Optional: `background` (string, image path), `backgroundStyle` (`"cover"` | `"ratio"` | `"repeat"`).

## Edges

Required: `id`, `fromNode`, `toNode`.

Optional: `fromSide` / `toSide` (`"top"` | `"right"` | `"bottom"` | `"left"`), `fromEnd` / `toEnd` (`"none"` | `"arrow"`, defaults: fromEnd=`"none"`, toEnd=`"arrow"`), `color`, `label`.

```json
{"id": "e1", "fromNode": "abc123", "fromSide": "right", "toNode": "def456", "toSide": "left", "toEnd": "arrow", "label": "relates to"}
```

## Color Presets

`"1"` Red · `"2"` Orange · `"3"` Yellow · `"4"` Green · `"5"` Cyan · `"6"` Purple

Custom hex: `"#4A90E2"`. Pick one format per canvas. Presets adapt to Obsidian's light/dark theme.

## Chinese Text Encoding

- Chinese double quotes → 『』
- Chinese single quotes → 「」
- English double quotes → `\"`

```json
{"text": "『核心概念』包含:「子概念A」和「子概念B」"}
```

## Complete Example

```json
{
  "nodes": [
    {"id": "group001", "type": "group", "x": -50, "y": -50, "width": 700, "height": 500, "label": "Core Concepts", "color": "4"},
    {"id": "center01", "type": "text", "x": 0, "y": 0, "width": 300, "height": 120, "text": "# Central Topic\n\nMain idea", "color": "4"},
    {"id": "branch01", "type": "text", "x": 400, "y": -100, "width": 220, "height": 100, "text": "Subtopic A", "color": "5"},
    {"id": "branch02", "type": "text", "x": 400, "y": 100, "width": 220, "height": 100, "text": "Subtopic B", "color": "5"}
  ],
  "edges": [
    {"id": "e1", "fromNode": "center01", "fromSide": "right", "toNode": "branch01", "toSide": "left", "toEnd": "arrow"},
    {"id": "e2", "fromNode": "center01", "fromSide": "right", "toNode": "branch02", "toSide": "left", "toEnd": "arrow"}
  ]
}
```
