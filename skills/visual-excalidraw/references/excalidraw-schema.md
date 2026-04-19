# Excalidraw JSON Schema Reference

## Full JSON Structure & Required Defaults

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [ ... ],
  "appState": { "gridSize": null, "viewBackgroundColor": "#ffffff" },
  "files": {}
}
```

**Common attributes for ALL elements:**

`id` (string), `type` (string), `x` (int), `y` (int), `width` (int), `height` (int), `angle` (int, default 0), `strokeColor` (hex), `backgroundColor` (hex or "transparent"), `fillStyle` ("solid" | "hachure" | "cross-hatch"), `strokeWidth` (int, default 2), `roughness` (int, default 1), `opacity` (int, default 100), `roundness` ({"type": 3} for rounded, null for sharp), `groupIds` ([]), `seed` (int), `isDeleted` (false), `locked` (false).

**CRITICAL DEFAULTS**: `boundElements: null`, `updated: 1`, `version: 1`, `link: null`.

*(Never use `rawText`, `frameId`, `index`, or `versionNonce`)*

## Element Types

### Shapes (Rectangle, Ellipse, Diamond)

```json
{"id": "rect1", "type": "rectangle", "x": 100, "y": 100, "width": 200, "height": 80, "strokeColor": "#1e40af", "backgroundColor": "#dbeafe", "fillStyle": "solid", "strokeWidth": 2, "roughness": 1, "opacity": 100, "roundness": {"type": 3}, "groupIds": [], "seed": 1, "version": 1, "isDeleted": false, "boundElements": null, "updated": 1, "link": null, "locked": false, "angle": 0}
```

### Text

Add these attributes to common attributes:

`text` (string), `fontSize` (int, min 14), `fontFamily` (always `5` for Excalifont), `textAlign` ("left"|"center"|"right"), `verticalAlign` ("top"|"middle"|"bottom"), `originalText` (string), `autoResize` (true), `lineHeight` (always `1.25`), `containerId` (null or string of rect id).

```json
{"id": "txt1", "type": "text", "x": 150, "y": 130, "width": 100, "height": 25, "text": "Content", "fontSize": 20, "fontFamily": 5, "textAlign": "center", "verticalAlign": "middle", "originalText": "Content", "autoResize": true, "lineHeight": 1.25, "strokeColor": "#1e40af", "backgroundColor": "transparent", ...common_vars}
```

### Arrow & Line

Add these attributes (omit backgroundColor / fillStyle):

`points` (array of `[dx, dy]` from x,y orig), `startArrowhead` (null|"arrow"), `endArrowhead` (null|"arrow").

```json
{"id": "arr1", "type": "arrow", "x": 300, "y": 140, "width": 100, "height": 0, "points": [[0, 0], [100, 0]], "strokeColor": "#374151", "strokeWidth": 2, "startArrowhead": null, "endArrowhead": "arrow", ...common_vars}
```

## Bindings

**Text to Container (e.g. text inside a rectangle):**

1. Rectangle sets `boundElements: [{ "id": "txt1", "type": "text" }]`
2. Text sets `containerId: "rect1"`

**Arrow to Shapes:**

Arrow object adds `startBinding` and `endBinding`:

```json
"startBinding": { "elementId": "rect1", "focus": 0, "gap": 5 },
"endBinding": { "elementId": "rect2", "focus": 0, "gap": 5 }
```

## Color Palette

**Text (strokeColor):**

- `#1e40af` (Deep Blue - Main Title)
- `#3b82f6` (Medium Blue - Subtitle)
- `#374151` (Dark Gray - Body Text)
- `#f59e0b` (Orange - Emphasis)

**Shape background (backgroundColor):**

- `#dbeafe` (Light Blue - Default)
- `#d1fae5` (Light Green - Success/Output)
- `#fef3c7` (Light Orange - Warning/Input)
- `#ede9fe` (Light Purple - Processing)
- `#f3f4f6` (Light Gray - Neutral)
