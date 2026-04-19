# log.md Format Specification

Operation log, append-only — never modify existing entries. Only keep the most recent 30 days; older entries are archived by lint to `wiki/log-archive/YYYY-MM.md`.

```markdown
# Wiki Log

## [YYYY-MM-DD] ingest | Material Title
- Source: `raw/path/filename`
- Created: [[page1]], [[page2]]
- Updated: [[page3]] (added xxx section)

## [YYYY-MM-DD] query | Query Question
- Consulted: [[page1]], [[page2]]
- Output: [[comparison-page]] (saved to wiki)

## [YYYY-MM-DD] lint | Health Check
- Updated: [[page3]] (added xxx section)
- Check results:
  - xxx
- Fix actions:
  - xxx
- Fixed: N items | Pending: M items

## [YYYY-MM-DD] publish | Deliverable Title
- Type: post | report | slides | tutorial | newsletter
- Output: `output/posts/filename.md`
- Sources: [[page1]], [[page2]]

## [YYYY-MM-DD] refresh | Topic
- Source: `url`
- Created: [[page1]], [[page2]]
- Updated: [[page3]] (added xxx section)

```
