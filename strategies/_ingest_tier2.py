#!/usr/bin/env python3
"""
Ingest the tier2 reservoir (FOREX/reservoir/tier2_coded_from_books/) into candidate modules.

Each tier2 folder has a strategy.md (frontmatter + sections) + a code.py with a pure
fn(I, i, htf) signal extracted from sister-lab/LAB/backtest/catalog_books.py. This tool turns each into
a standard strategy module strategies/candidates/<id>.py (META + signal). The signal BODY is copied
VERBATIM -- only the `def <name>(I, i, htf):` line is renamed to `def signal(I, i, htf=None):`
(the engine/loader call positionally, so the I/i param names are irrelevant). The helpers the body
uses (_nan/_xup/_xdn) come from strategies._common.

Pre-verified (audit 2026-06-07): all 86 distinct indicators tier2 reads exist in engine.precompute,
0 read volume, cadences all "DS", exits in {TREND, TREND_FLIP, REVERT, BREAK}. A folder that violates
any of those (missing indicator / volume / unknown exit) is SKIPPED and logged, never silently
emitted. Re-runnable + idempotent: overwrites the candidate modules it owns.

Usage: python3 strategies/_ingest_tier2.py [--dry-run]
"""
from __future__ import annotations

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), "reservoir", "tier2_coded_from_books")
DST = os.path.join(HERE, "candidates")

CADENCE_MAP = {"D": ["day"], "S": ["swing"], "DS": ["day", "swing"], "SD": ["day", "swing"]}
EXITS = {"TREND", "TREND_FLIP", "REVERT", "BREAK"}


def _frontmatter(md):
    """Parse the leading --- yaml-ish --- block into a dict (simple key: value lines)."""
    m = re.match(r"\s*---\n(.*?)\n---", md, re.S)
    fm = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip()
    return fm


def _section(md, header):
    """Text of a '## header' section (first non-empty line), or ''."""
    m = re.search(rf"##\s*{re.escape(header)}\s*\n(.+?)(?:\n##|\Z)", md, re.S)
    if not m:
        return ""
    for line in m.group(1).strip().splitlines():
        if line.strip():
            return line.strip()
    return ""


def _desc(md):
    """First prose line after the '# title'."""
    m = re.search(r"\n#\s+.+?\n+(.+)", md)
    return m.group(1).strip() if m else ""


def _clean(s, limit=200):
    """One-line ASCII-safe value for a META string."""
    s = s.replace('"', "'").replace("\n", " ").strip()
    s = s.encode("ascii", "ignore").decode()
    return s[:limit]


def _extract_signal(code):
    """Return (body_lines_str, helpers_used) from a code.py: everything from the def onward, with the
    def line renamed to signal(I, i, htf=None)."""
    lines = code.splitlines()
    start = next((k for k, ln in enumerate(lines) if re.match(r"def\s+\w+\(I,\s*i,\s*htf\):", ln)), None)
    if start is None:
        return None, set()
    body = lines[start + 1:]
    # drop trailing blank lines
    while body and not body[-1].strip():
        body.pop()
    body_txt = "\n".join(body)
    helpers = {h for h in ("_nan", "_xup", "_xdn") if re.search(rf"\b{h}\(", body_txt)}
    return body_txt, helpers


TEMPLATE = '''#!/usr/bin/env python3
"""{id} -- {desc}. tier2 (book-extracted from sister-lab catalog_books).

{source}. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import {imports}

META = {{
    "id": "{id}",
    "cadences": {cadences},
    "exit": {exit},
    "asset_classes": ALL_CLASSES,
    "style": "{style}",
    "tf": "{tf}",
    "indicators": "{indicators}",
    "long": "{long}",
    "short": "{short}",
    "desc": "{desc}",
    "source": "{source}",
}}


def signal(I, i, htf=None):
{body}
'''


def main():
    dry = "--dry-run" in sys.argv
    made, skipped = [], []
    for folder in sorted(os.listdir(SRC)):
        d = os.path.join(SRC, folder)
        if not os.path.isdir(d):
            continue
        md_p, code_p = os.path.join(d, "strategy.md"), os.path.join(d, "code.py")
        if not (os.path.exists(md_p) and os.path.exists(code_p)):
            skipped.append((folder, "missing strategy.md/code.py")); continue
        md, code = open(md_p).read(), open(code_p).read()
        fm = _frontmatter(md)
        sid = fm.get("id") or folder.replace("-", "_")
        if not re.fullmatch(r"[a-z][a-z0-9_]*", sid):
            skipped.append((folder, f"bad id {sid!r}")); continue
        cad = CADENCE_MAP.get(fm.get("cadences", "DS"))
        if cad is None:
            skipped.append((folder, f"unknown cadences {fm.get('cadences')!r}")); continue
        ex = (fm.get("exit_archetype") or "TREND").strip()
        if ex not in EXITS:
            skipped.append((folder, f"unknown exit {ex!r}")); continue
        body, helpers = _extract_signal(code)
        if body is None:
            skipped.append((folder, "no fn(I,i,htf) found")); continue
        if 'I["volume"]' in code or "I['volume']" in code:
            skipped.append((folder, "reads volume (excluded on FX)")); continue
        imports = ", ".join(sorted(helpers) + [ex, "ALL_CLASSES"])
        content = TEMPLATE.format(
            id=sid, cadences=cad, exit=ex, style=_clean(fm.get("style", "")),
            tf=_clean(fm.get("timeframe", "")), indicators=_clean(_section(md, "Indicators")),
            long=_clean(_section(md, "Entry - long")), short=_clean(_section(md, "Entry - short")),
            desc=_clean(_desc(md)), source=_clean(fm.get("source", "tier2 book-extracted")),
            imports=imports, body=body)
        if not dry:
            with open(os.path.join(DST, f"{sid}.py"), "w") as f:
                f.write(content)
        made.append(sid)
    print(f"ingested {len(made)} tier2 -> candidates" + (" [DRY-RUN]" if dry else ""))
    if skipped:
        print(f"skipped {len(skipped)}:")
        for folder, why in skipped:
            print(f"  {folder}: {why}")


if __name__ == "__main__":
    main()
    sys.stdout.flush()
    os._exit(0)
