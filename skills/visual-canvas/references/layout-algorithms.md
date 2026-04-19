# Layout Algorithms for Obsidian Canvas

## Spacing Constants

```
HORIZONTAL_GAP = 400   # Minimum horizontal distance between node edges
VERTICAL_GAP   = 250   # Minimum vertical distance between node edges
```

**Overlap check**: Node B must not start within Node A's `(x, y, x+width, y+height)` expanded by the gap values above. Always verify after positioning.

## MindMap: Radial Layout

Root at origin. Children arranged in a circle.

```
root.x = -(root.width / 2)
root.y = -(root.height / 2)

For each child i of N children:
  angle = i * (2π / N)
  child.x = radius * cos(angle) - child.width/2
  child.y = radius * sin(angle) - child.height/2
```

**Radius**: 400px (≤10 children), 500px (11–20), 600px (>20).

**Secondary branches**: Stack vertically to the right of parent, spaced by `VERTICAL_GAP`.

## MindMap: Tree Layout (Top-Down)

For deep hierarchies. Each level is a horizontal row.

```
Level 0: root centered at (0, 0)
Level N: y = N * (node_height + VERTICAL_GAP)
         x = spread nodes evenly, centered under parent
```

## Freeform: Zone Grid

Divide canvas into a grid of zones (one per content group).

```
cols = ceil(sqrt(N_groups))
rows = ceil(N_groups / cols)
zone_width  = canvas_width / cols
zone_height = canvas_height / rows

Zone i: x = (i % cols) * zone_width, y = (i / cols) * zone_height
```

Within each zone, flow nodes left-to-right, top-to-bottom with gaps.

## Edge Side Calculation

Pick connection sides based on relative position:

```
If |dx| > |dy|:   horizontal → fromSide="right", toSide="left" (or reversed)
If |dy| >= |dx|:  vertical   → fromSide="bottom", toSide="top" (or reversed)
```

## Common Patterns

| Pattern | When | Positioning |
|---------|------|-------------|
| Timeline | Chronological content | Nodes in a single horizontal/vertical line, spaced by gap |
| Circular | Cyclical processes | Nodes on a circle of fixed radius |
| Matrix | Comparisons | Rows × columns grid with uniform cell size |
