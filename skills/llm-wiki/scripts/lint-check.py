#!/usr/bin/env python3
"""Wiki structural health check — outputs a JSON report for LLM consumption."""

import json
import re
from datetime import date
from pathlib import Path

WIKI_DIR = Path("wiki")
INDEX = WIKI_DIR / "index.md"
ADMIN_FILES = {"index.md", "log.md", "lifecycle.md"}


def get_wiki_pages():
    pages = {}
    for f in WIKI_DIR.rglob("*.md"):
        if f.name in ADMIN_FILES or "log-archive" in str(f) or f.name == ".gitkeep":
            continue
        pages[f.stem] = f
    return pages


def extract_wikilinks(filepath):
    text = filepath.read_text(encoding="utf-8")
    return set(re.findall(r'\[\[([^\]|]+)\]\]', text))


def check_page_count(pages):
    text = INDEX.read_text(encoding="utf-8")
    m = re.search(r'Total pages:\s*(\d+)', text)
    declared = int(m.group(1)) if m else 0
    actual = len(pages)
    return {"actual": actual, "declared": declared, "match": actual == declared}


def check_orphan_pages(pages):
    ref_count = {name: 0 for name in pages}
    for name, filepath in pages.items():
        for link in extract_wikilinks(filepath):
            if link in ref_count and link != name:
                ref_count[link] += 1
    return [name for name, count in ref_count.items() if count == 0]


def check_missing_pages(pages):
    all_refs = set()
    for filepath in pages.values():
        all_refs.update(extract_wikilinks(filepath))
    missing = []
    for ref in sorted(all_refs):
        if ref.startswith("raw/"):
            continue
        if ref not in pages:
            missing.append(ref)
    return missing


def check_frontmatter(pages):
    required = ["title", "tags", "category", "created", "updated", "sources", "description"]
    issues = []
    for name, filepath in pages.items():
        text = filepath.read_text(encoding="utf-8")
        if not text.startswith("---"):
            issues.append({"page": name, "missing": required})
            continue
        end = text.find("---", 3)
        if end == -1:
            issues.append({"page": name, "missing": required})
            continue
        fm = text[3:end]
        missing = [f for f in required if not re.search(rf'^{f}:', fm, re.MULTILINE)]
        if missing:
            issues.append({"page": name, "missing": missing})
    return issues


def check_one_way_links(pages):
    one_way = []
    for name, filepath in pages.items():
        refs = extract_wikilinks(filepath)
        for ref in refs:
            if ref.startswith("raw/") or ref not in pages:
                continue
            back_refs = extract_wikilinks(pages[ref])
            if name not in back_refs:
                one_way.append({"from": name, "to": ref})
    return one_way


def main():
    pages = get_wiki_pages()
    report = {
        "date": str(date.today()),
        "page_count": check_page_count(pages),
        "orphan_pages": check_orphan_pages(pages),
        "missing_pages": check_missing_pages(pages),
        "frontmatter_issues": check_frontmatter(pages),
        "one_way_links": check_one_way_links(pages),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
