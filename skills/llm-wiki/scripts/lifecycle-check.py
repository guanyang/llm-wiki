#!/usr/bin/env python3
"""Lifecycle check — time decay + state transitions + output staleness."""

import json
import re
from datetime import date, datetime
from pathlib import Path

LIFECYCLE = Path("wiki/lifecycle.md")
INDEX = Path("wiki/index.md")
TODAY = date.today()

TYPE_COEFFICIENTS = {
    "Entities": 1.0, "Concepts": 0.5, "Summaries": 1.0,
    "Comparisons": 1.5, "Synthesis": 0.5,
}
DECAY_TIERS = [(180, -0.15), (90, -0.10), (60, -0.05), (30, -0.02)]


def parse_lifecycle():
    if not LIFECYCLE.exists():
        return {}, []
    text = LIFECYCLE.read_text(encoding="utf-8")
    pages, outputs, section = {}, [], None
    for line in text.split("\n"):
        m = re.match(r'^## (Entities|Concepts|Summaries|Comparisons|Synthesis|Output)', line)
        if m:
            section = m.group(1)
            continue
        if section and section != "Output" and line.startswith("| [["):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 5:
                name = re.sub(r'\[\[|\]\]', '', parts[1])
                pages[name] = {
                    "section": section,
                    "access": int(parts[2]) if parts[2].isdigit() else 0,
                    "last_accessed": parts[3] if parts[3] else None,
                }
        if section == "Output" and line.startswith("| `"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 5:
                outputs.append({
                    "file": parts[1].strip("`"),
                    "status": parts[2],
                    "wiki_deps": [d.strip() for d in parts[3].split(",")],
                })
    return pages, outputs


def parse_index():
    if not INDEX.exists():
        return {}
    pages = {}
    for line in INDEX.read_text(encoding="utf-8").split("\n"):
        m = re.match(r'\| \[\[(.+?)\]\] \|.*?\| ([\d.]+) \| (\w+) \|', line)
        if m:
            pages[m.group(1)] = {"confidence": float(m.group(2)), "status": m.group(3)}
    return pages


def calc_decay(lc_pages, idx_pages):
    results = []
    for name, lc in lc_pages.items():
        if not lc["last_accessed"]:
            continue
        try:
            days = (TODAY - datetime.strptime(lc["last_accessed"], "%Y-%m-%d").date()).days
        except ValueError:
            continue
        if days < 30:
            continue
        base = next((d for t, d in DECAY_TIERS if days >= t), 0)
        coeff = TYPE_COEFFICIENTS.get(lc["section"], 1.0)
        actual = round(base * coeff, 3)
        conf = idx_pages.get(name, {}).get("confidence", 0.0)
        results.append({
            "page": name, "days": days, "section": lc["section"],
            "base": base, "coeff": coeff, "actual": actual,
            "confidence": conf, "new_confidence": round(max(0, conf + actual), 2),
        })
    return results


def calc_transitions(lc_pages, idx_pages):
    results = []
    for name, lc in lc_pages.items():
        if not lc["last_accessed"]:
            continue
        try:
            days = (TODAY - datetime.strptime(lc["last_accessed"], "%Y-%m-%d").date()).days
        except ValueError:
            continue
        idx = idx_pages.get(name, {})
        status, conf = idx.get("status", "active"), idx.get("confidence", 0.0)
        if status == "active" and days >= 90 and conf < 0.5:
            results.append({"page": name, "from": "active", "to": "stale", "reason": f"{days}d, conf={conf}"})
        elif status == "stale" and days >= 180:
            results.append({"page": name, "from": "stale", "to": "archived", "reason": f"{days}d, no new sources"})
    return results


def calc_output_staleness(outputs, idx_pages):
    results = []
    for o in outputs:
        if o["status"] == "outdated":
            continue
        stale = [d for d in o["wiki_deps"] if d.strip() and idx_pages.get(d.strip(), {}).get("status") in ("stale", "archived")]
        if stale:
            results.append({"output": o["file"], "stale_deps": stale})
    return results


def main():
    lc_pages, outputs = parse_lifecycle()
    idx_pages = parse_index()
    print(json.dumps({
        "date": str(TODAY),
        "tracked_pages": len(lc_pages),
        "decay_suggestions": calc_decay(lc_pages, idx_pages),
        "status_transitions": calc_transitions(lc_pages, idx_pages),
        "output_staleness": calc_output_staleness(outputs, idx_pages),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
