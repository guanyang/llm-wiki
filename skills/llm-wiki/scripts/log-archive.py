#!/usr/bin/env python3
"""log.md rolling archive — migrate entries older than 30 days to wiki/log-archive/YYYY-MM.md."""

import re
import sys
from datetime import date, timedelta
from pathlib import Path

LOG = Path("wiki/log.md")
ARCHIVE_DIR = Path("wiki/log-archive")
CUTOFF = date.today() - timedelta(days=30)
DRY_RUN = "--dry-run" in sys.argv


def main():
    if not LOG.exists():
        print("log.md not found")
        return

    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    text = LOG.read_text(encoding="utf-8")

    # Split entries by ## [YYYY-MM-DD] headers
    entries = re.split(r'(?=^## \[\d{4}-\d{2}-\d{2}\])', text, flags=re.MULTILINE)
    header = entries[0] if entries and not entries[0].startswith("## [") else "# Wiki Log\n\n"
    if not entries[0].startswith("## ["):
        entries = entries[1:]

    keep, archived = [], 0
    for entry in entries:
        m = re.match(r'## \[(\d{4}-\d{2}-\d{2})\]', entry)
        if not m:
            keep.append(entry)
            continue
        entry_date = date.fromisoformat(m.group(1))
        if entry_date < CUTOFF:
            ym = m.group(1)[:7]  # YYYY-MM
            archive_file = ARCHIVE_DIR / f"{ym}.md"
            if DRY_RUN:
                print(f"[dry-run] Archive: {m.group(1)} → {archive_file}")
            else:
                with open(archive_file, "a", encoding="utf-8") as f:
                    f.write(entry)
            archived += 1
        else:
            keep.append(entry)

    if not DRY_RUN and archived > 0:
        LOG.write_text(header + "".join(keep), encoding="utf-8")

    print(f"archived={archived} kept={len(keep)} cutoff={CUTOFF} dry_run={DRY_RUN}")


if __name__ == "__main__":
    main()
