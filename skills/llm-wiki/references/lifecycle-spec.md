# Knowledge Lifecycle Management

> Pluggable extension. Deleting `wiki/lifecycle.md` does not affect core wiki functionality.

## Data Distribution

| File | Fields Carried | Read Frequency |
|------|---------|---------|
| `wiki/index.md` | confidence, status | High |
| `wiki/lifecycle.md` | access, last_accessed, superseded_by, supersedes, Output tracking | Low |

## Confidence

### Initial Values

| Condition | confidence |
|------|-----------|
| Single source, thin content | 0.55 |
| Single source, substantial content | 0.65 |
| Multi-source cross-confirmation | 0.75 |
| Synthesis page | 0.80 |

### Reinforcement (capped at 1.0)

| Event | Change |
|------|------|
| Referenced by publish | +0.15 |
| Confirmed by new source (ingest) | +0.10 |
| Hit by query | +0.05 |
| Lint pass with no contradictions | +0.02 |

### Event Decay (floor at 0.0)

| Event | Change |
|------|------|
| Contradictory claim discovered | −0.15 |
| Source marked as outdated | −0.10 |

### Time Decay (executed during lint)

| Days Since Last Access | Base Decay |
|-----------|---------|
| 30–59 days | −0.02 |
| 60–89 days | −0.05 |
| 90–179 days | −0.10 |
| ≥ 180 days | −0.15 |

Actual decay = base decay × type coefficient:

| Page Type | Coefficient |
|---------|------|
| concepts / synthesis | ×0.5 |
| entities / summaries | ×1.0 |
| comparisons | ×1.5 |

**Reinforcement Reset**: Any reinforcement event updates last_accessed to the current day, resetting the time decay timer to zero.

## State Transitions

```
active ──(90 days unaccessed AND confidence < 0.5)──→ stale
active ──(superseded)──→ archived
stale  ──(hit by query/publish OR confirmed by new source)──→ active
stale  ──(180 days unaccessed AND no new sources)──→ archived
archived ──(manual decision to restore)──→ active
```

## Supersession Mechanism

1. lifecycle.md old page superseded_by → new page
2. lifecycle.md new page supersedes → old page (bidirectional link, A→B→C version chain traceability)
3. index.md old page status → archived
4. Old page body top: `> ⚠️ This page has been superseded by [[new-page]] (YYYY-MM-DD)`
5. New page "Related Pages" references old page, noting "supersedes"

Only triggered when core conclusions are overturned — partial updates do not count as supersession.

## Demotion Mechanism

When synthesis/comparison core conclusions are disproven:
1. status → stale
2. confidence −0.15
3. Body top: `> ⚠️ Some conclusions on this page have been challenged by new material — pending re-verification`
4. Dependent entities/concepts are unaffected
5. After re-verification, if conclusions hold → restore to active, confidence +0.10

## Layered Consolidation

```
Procedural    output/* (posts/reports/slides/tutorials/newsletters)
Semantic      wiki/comparisons/ + wiki/synthesis/
Episodic      wiki/entities/ + wiki/concepts/
Working       wiki/summaries/
```

| Promotion Direction | Condition | Action |
|---------|------|------|
| Working → Episodic | Entity/concept in summary mentioned by 2+ materials | Create/update entity/concept |
| Episodic → Semantic | 3+ entities/concepts form a comparable or synthesizable theme | Create comparison/synthesis |
| Semantic → Procedural | User triggers publish, or synthesis confidence ≥ 0.85 | Execute publish |

Confidence inheritance: new page = weighted average of dependent pages (floor at 0.65). Promotion does not delete the source.

## Output Deliverable Tracking

lifecycle.md Output section: status (current/outdated), wiki_deps, created.
During lint: if dependent pages are stale/archived → mark deliverable as outdated.
