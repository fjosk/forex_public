"""
Build the strategy-workspace reference folder.

Gathers three tiers of trading strategies into /home/user/strategy-workspace so they can be
combed one by one in a dedicated forex session:

  tier1_raw_codeable     557 raw book-mined strategies (engine_fit == codeable), prefer-raw,
                         one markdown per strategy, grouped by category. No code yet.
  tier2_coded_from_books 124 book strategies that were wired into the sister-lab backtest engine.
                         Per-strategy folder: raw spec (strategy.md) + the engine code (code.py).
  tier3_live_deployed    10 strategies currently live on the sister-lab trader. Per-strategy folder:
                         spec (strategy.md) + the live TRADE module + the shared signal function.

Every strategy is flagged fx_compatible: NO when it is volume-based (forex bars have volume = 0,
so those indicators are dead on FX data). Nothing is dropped; flagged only, for manual review.

Re-runnable: overwrites the generated files in place. Reads only, writes only under OUT.
Sources:
  /home/user/research-archive/_text/raw_strategies.json   (1114 raw entries, 557 codeable)
  /home/user/sister-lab/LAB/backtest/catalog_books.py (124 wired entries + their functions)
  /home/user/sister-lab/TRADE/trade/strategy/*.py      (live modules)
  /home/user/sister-lab/shared/strategies.py           (shared signal functions)
"""
import ast
import json
import os
import re
import unicodedata

# OUT = this archive's own root (reservoir/), derived from this file's location -- the folder was
# moved (strategy-workspace -> FOREX/strat -> FOREX/reservoir), so deriving it avoids a stale hardcoded path.
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # .../FOREX/reservoir
RAW = "/home/user/research-archive/_text/raw_strategies.json"
CATBOOKS = "/home/user/sister-lab/LAB/backtest/catalog_books.py"
TRADE_STRAT = "/home/user/sister-lab/TRADE/trade/strategy"
SHARED = "/home/user/sister-lab/shared/strategies.py"

# ---- volume-based detector (these die on forex: volume is always 0) ----
VOL_WORDS = re.compile(
    r"\b(volume|obv|vwap|vwma|mfi|chaikin|cmf|klinger|kvo|money[ _-]?flow|force[ _-]?index|"
    r"force13|accumulation|distribution|on[- ]?balance|a/?d[ _-]?line|adl|ease[ _-]?of[ _-]?movement|"
    r"eom|pvt|bwmfi|effort|vsa)\b",
    re.I,
)


def is_volume(*texts):
    blob = " ".join(t for t in texts if t)
    return bool(VOL_WORDS.search(blob))


# Volume-based strategies are dead on forex (FX bars have volume = 0, and Ostium's oracle feed
# carries no volume either). Excluded from the gathered set. Flip to True to gather them anyway.
INCLUDE_VOLUME = False


# ---- ascii sanitiser (authored files stay plain ASCII, OS agnostic) ----
_REPL = {
    "‘": "'", "’": "'", "“": '"', "”": '"',
    "–": "-", "—": "-", "−": "-", "…": "...",
    "→": "->", "←": "<-", "≥": ">=", "≤": "<=",
    "×": "x", "±": "+/-", "°": "deg", " ": " ",
    "•": "-", "′": "'", "″": '"',
}


def ascii_clean(s):
    if s is None:
        return ""
    if not isinstance(s, str):
        s = str(s)
    for k, v in _REPL.items():
        s = s.replace(k, v)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    return s


def slug(name, maxlen=70):
    s = ascii_clean(name).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return (s[:maxlen].rstrip("-")) or "unnamed"


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text)


def uniq(used, base):
    name = base
    n = 2
    while name in used:
        name = "%s-%d" % (base, n)
        n += 1
    used.add(name)
    return name


# ============================================================ TIER 1: raw codeable
def build_tier1():
    raw = json.load(open(RAW))
    codeable = [s for s in raw if s.get("engine_fit") == "codeable"]
    base = os.path.join(OUT, "tier1_raw_codeable")
    rows = []
    used_per_cat = {}
    for s in codeable:
        cat = slug(s.get("category") or "other", 40)
        name = ascii_clean(s.get("name") or "unnamed")
        vol = is_volume(name, s.get("indicators"), s.get("category"),
                        s.get("entry_long"), s.get("entry_short"), s.get("formula"))
        if vol and not INCLUDE_VOLUME:
            continue
        used = used_per_cat.setdefault(cat, set())
        fn = uniq(used, slug(name))
        fx = "NO  (volume-based, dead on forex)" if vol else "yes"
        md = []
        md.append("---")
        md.append("name: %s" % name)
        md.append("tier: 1-raw-codeable")
        md.append("category: %s" % ascii_clean(s.get("category")))
        md.append("market_origin: %s" % ascii_clean(s.get("market")))
        md.append("timeframe: %s" % ascii_clean(s.get("timeframe")))
        md.append("fx_compatible: %s" % fx)
        md.append("engine_fit: codeable")
        md.append("confidence: %s" % ascii_clean(s.get("confidence")))
        md.append("source_book: %s" % ascii_clean(s.get("book")))
        md.append("---")
        md.append("")
        md.append("# %s" % name)
        if s.get("aliases"):
            md.append("")
            md.append("**Aliases:** %s" % ascii_clean(s.get("aliases")))
        sect = [
            ("Entry - long", s.get("entry_long")),
            ("Entry - short", s.get("entry_short")),
            ("Exit", s.get("exit")),
            ("Indicators", s.get("indicators")),
            ("Formula", s.get("formula")),
            ("Sizing", s.get("sizing")),
            ("Timeframe note", s.get("timeframe_note")),
            ("Engine-fit note", s.get("engine_fit_note")),
        ]
        for title, val in sect:
            val = ascii_clean(val)
            if val.strip():
                md.append("")
                md.append("## %s" % title)
                md.append(val)
        md.append("")
        md.append("## Source")
        md.append("- Book: %s" % ascii_clean(s.get("book")))
        md.append("- Location: %s" % ascii_clean(s.get("source_location")))
        md.append("- Chunk index: %s" % ascii_clean(s.get("chunk_idx")))
        md.append("")
        write(os.path.join(base, cat, fn + ".md"), "\n".join(md))
        rows.append((cat, name, fx, fn))

    # index
    idx = ["# Tier 1 - raw codeable book strategies (%d)" % len(codeable), ""]
    idx.append("Mined from trading books, tagged engine_fit=codeable (authorable into the engine).")
    idx.append("Raw specs only - no code yet. Group = source category. fx flag marks volume-based.")
    idx.append("")
    by_cat = {}
    for cat, name, fx, fn in rows:
        by_cat.setdefault(cat, []).append((name, fx, fn))
    for cat in sorted(by_cat):
        items = by_cat[cat]
        idx.append("## %s (%d)" % (cat, len(items)))
        for name, fx, fn in sorted(items):
            flag = "" if fx == "yes" else "  [FX: NO - volume]"
            idx.append("- [%s](%s/%s.md)%s" % (name, cat, fn, flag))
        idx.append("")
    write(os.path.join(base, "_INDEX.md"), "\n".join(idx))
    excluded = len(codeable) - len(rows) if not INCLUDE_VOLUME else 0
    return len(rows), excluded


# ============================================================ TIER 2: coded from books
def build_tier2():
    src = open(CATBOOKS).read()
    tree = ast.parse(src)
    func_src = {}
    catalog_node = None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            func_src[node.name] = ast.get_source_segment(src, node)
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == "CATALOG_BOOKS":
                    catalog_node = node.value
    entries = {}
    if isinstance(catalog_node, ast.Dict):
        for k, v in zip(catalog_node.keys, catalog_node.values):
            if not isinstance(k, ast.Constant):
                continue
            sid = k.value
            if not (isinstance(v, ast.Call) and isinstance(v.func, ast.Name) and v.func.id == "_e"):
                continue
            a = v.args
            def seg(i):
                return ast.get_source_segment(src, a[i]) if i < len(a) else ""
            def const(i):
                return a[i].value if i < len(a) and isinstance(a[i], ast.Constant) else seg(i)
            entries[sid] = {
                "fn": seg(0),
                "style": const(1),
                "cadences": seg(2),
                "exit": seg(3),
                "tf": const(4),
                "indicators": const(5),
                "long": const(6),
                "short": const(7),
                "desc": const(8),
                "source": const(9),
            }

    base = os.path.join(OUT, "tier2_coded_from_books")
    rows = []
    for sid, e in entries.items():
        fn_name = e["fn"]
        code = func_src.get(fn_name, "# (function source not found: %s)" % fn_name)
        vol = is_volume(sid, e["indicators"], e["desc"], code)
        if vol and not INCLUDE_VOLUME:
            continue
        fx = "NO  (volume-based, dead on forex)" if vol else "yes"
        folder = os.path.join(base, slug(sid))
        md = []
        md.append("---")
        md.append("id: %s" % sid)
        md.append("tier: 2-coded-from-books")
        md.append("style: %s" % ascii_clean(e["style"]))
        md.append("cadences: %s" % ascii_clean(e["cadences"]))
        md.append("timeframe: %s" % ascii_clean(e["tf"]))
        md.append("exit_archetype: %s" % ascii_clean(e["exit"]))
        md.append("fx_compatible: %s" % fx)
        md.append("source: %s" % ascii_clean(e["source"]))
        md.append("---")
        md.append("")
        md.append("# %s" % sid)
        md.append("")
        md.append(ascii_clean(e["desc"]))
        md.append("")
        md.append("## Entry - long")
        md.append(ascii_clean(e["long"]))
        md.append("")
        md.append("## Entry - short")
        md.append(ascii_clean(e["short"]))
        md.append("")
        md.append("## Indicators")
        md.append(ascii_clean(e["indicators"]))
        md.append("")
        md.append("## Exit archetype")
        md.append("%s (preset in sister-lab/LAB/backtest/catalog.py)" % ascii_clean(e["exit"]))
        md.append("")
        md.append("## Code")
        md.append("Engine signal function is in code.py (same folder). Signature fn(I, i, htf) ->")
        md.append("'long' | 'short' | None, reads precomputed indicator arrays I at bar i.")
        md.append("")
        write(os.path.join(folder, "strategy.md"), "\n".join(md))
        codehdr = "# Engine signal function for '%s' (extracted from sister-lab/LAB/backtest/catalog_books.py)\n" % sid
        codehdr += "# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.\n\n"
        write(os.path.join(folder, "code.py"), codehdr + (code or "") + "\n")
        rows.append((sid, fx))

    idx = ["# Tier 2 - book strategies coded into the engine (%d)" % len(rows), ""]
    idx.append("These cleared the codeable bar and were wired into the sister-lab backtest catalog")
    idx.append("(catalog_books.py). Each folder has the raw spec (strategy.md) + engine code (code.py).")
    idx.append("None survived the full gauntlet on crypto - they are candidates, not proven edges.")
    idx.append("")
    for sid, fx in sorted(rows):
        flag = "" if fx == "yes" else "  [FX: NO - volume]"
        idx.append("- [%s](%s/strategy.md)%s" % (sid, slug(sid), flag))
    idx.append("")
    write(os.path.join(base, "_INDEX.md"), "\n".join(idx))
    excluded = len(entries) - len(rows) if not INCLUDE_VOLUME else 0
    return len(rows), excluded


# ============================================================ TIER 3: live deployed
# key -> (TRADE module file, shared signal function name, one-line note)
LIVE = {
    "B1":    ("b1.py",          "b1",            "MACD weak-rally SELL, short-only, 1h. Scoped: DOGE."),
    "ICHI":  ("ichimoku_tk.py", "ichi",          "Ichimoku Tenkan/Kijun cross + cloud, 4h. Scoped: SOL/SUI/NEAR/ONDO/TON. Only full-gauntlet survivor (the live mainnet pick)."),
    "QQE":   ("qqe.py",         "qqe",           "Smoothed-RSI trailing-line cross, 4h. Scoped: SOL/ONDO."),
    "ATRC":  ("atrc.py",        "atrc",          "ATR-channel breakout, 4h. Scoped: HYPE."),
    "COPP":  ("copp.py",        "copp",          "Coppock curve flip, 4h. Scoped: HYPE."),
    "RSI14": ("rsi14.py",       "rsi14",         "RSI(14) reversal + EMA200, 4h. Scoped: ETH/DOGE. Lone ETH coverage; survived walk-forward on a major."),
    "CMO":   ("cmo.py",         "cmo_zero",      "Chande Momentum zero-cross + EMA200, 4h. Scoped: HYPE/NEAR. Forward-test add (fragile under stress)."),
    "CHAND": ("chand.py",       "chandelier",    "Chandelier-exit flip, 4h. Scoped: SUI. Forward-test add."),
    "B10":   ("b10.py",         "b10",           "Ichimoku + MACD confirm, 1h. Scoped: ONDO. Forward-test add (rolling-WFO overfit)."),
    "CHOP":  ("chop_breakout.py", "chop_breakout", "Choppiness-Index-exit breakout, 4h. Scoped: SOL/NEAR. Strongest of the forward-test adds; fails only stress."),
}


def build_tier3():
    shared_src = open(SHARED).read()
    stree = ast.parse(shared_src)
    sfunc = {n.name: ast.get_source_segment(shared_src, n)
             for n in stree.body if isinstance(n, ast.FunctionDef)}
    base = os.path.join(OUT, "tier3_live_deployed")
    rows = []
    for key, (modfile, fnname, note) in LIVE.items():
        folder = os.path.join(base, key)
        # spec
        md = []
        md.append("---")
        md.append("key: %s" % key)
        md.append("tier: 3-live-deployed")
        md.append("fx_compatible: yes  (price/OHLC only, no volume)")
        md.append("status: live on sister-lab paper+testnet roster")
        md.append("---")
        md.append("")
        md.append("# %s" % key)
        md.append("")
        md.append(note)
        md.append("")
        md.append("## Files in this folder")
        md.append("- %s : the live TRADE builder module (assembles the indicator window, carries exit config)." % modfile)
        md.append("- shared_signal.py : the shared long/short decision function `%s` (the SAME function" % fnname)
        md.append("  the LAB backtest calls - this is the strategy's actual signal logic).")
        md.append("")
        md.append("## How it runs in sister-lab")
        md.append("The builder fetches candles, computes indicators, and delegates the side decision to the")
        md.append("shared function. Exit (ATR stop/target + chandelier trail + time stop) is carried on the")
        md.append("signal and executed by the shared exit core. For forex, the same split works: port the")
        md.append("builder to FX candles + Ostium exit math, keep the shared signal function as-is.")
        md.append("")
        write(os.path.join(folder, "strategy.md"), "\n".join(md))
        # copy TRADE module
        modpath = os.path.join(TRADE_STRAT, modfile)
        if os.path.exists(modpath):
            write(os.path.join(folder, modfile), open(modpath).read())
        # shared signal fn
        code = sfunc.get(fnname, "# (shared signal fn not found: %s)" % fnname)
        hdr = "# Shared signal function '%s' (from sister-lab/shared/strategies.py).\n" % fnname
        hdr += "# Form: fn(ind, pos, htf) -> 'long'|'short'|None. Pure: no I/O, no state.\n\n"
        write(os.path.join(folder, "shared_signal.py"), hdr + code + "\n")
        rows.append(key)

    idx = ["# Tier 3 - live deployed strategies (%d)" % len(rows), ""]
    idx.append("The current sister-lab trader roster (enabled_strategies). Each cleared the gauntlet (or was")
    idx.append("a deliberate forward-test add) and has full, working code. All are price/OHLC-based -")
    idx.append("none use volume, so all are forex-portable in principle (still need an FX gauntlet pass).")
    idx.append("")
    for key in LIVE:
        idx.append("- [%s](%s/strategy.md) - %s" % (key, key, LIVE[key][2]))
    idx.append("")
    write(os.path.join(base, "_INDEX.md"), "\n".join(idx))
    return len(rows)


def main():
    n1, x1 = build_tier1()
    n2, x2 = build_tier2()
    n3 = build_tier3()
    state = "EXCLUDED (not gathered)" if not INCLUDE_VOLUME else "INCLUDED"
    note = ["# Volume-based strategies - %s" % state, "",
            "Forex bars have volume = 0, and Ostium's oracle price feed carries no volume either,",
            "so any volume indicator (OBV, VWAP, MFI, Chaikin, Force Index, Klinger, A/D, EoM, PVT,",
            "VSA, etc.) is dead on FX. They are left OUT of this archive by default.", "",
            "Excluded this build:",
            "- Tier 1 (raw codeable): %d" % x1,
            "- Tier 2 (coded from books): %d" % x2,
            "- Tier 3 (live): 0 (none use volume)", "",
            "Total excluded: %d." % (x1 + x2), "",
            "They are NOT lost - they still live in the source archives",
            "(/home/user/research-archive/_text/raw_strategies.json and",
            "/home/user/sister-lab/LAB/backtest/catalog_books.py). To gather them here too, set",
            "INCLUDE_VOLUME = True in _build/build.py and re-run.", "",
            "If you ever pull tick data (Dukascopy), tick-volume is the FX proxy that could revive",
            "them - but that is a separate data project + a fresh backtest, not a free win.", ""]
    write(os.path.join(OUT, "_EXCLUDED_volume_note.md"), "\n".join(note))
    print("tier1 raw codeable : %d  (excluded %d volume)" % (n1, x1))
    print("tier2 coded books  : %d  (excluded %d volume)" % (n2, x2))
    print("tier3 live deployed: %d  (0 volume)" % n3)
    print("TOTAL gathered: %d  | excluded: %d" % (n1 + n2 + n3, x1 + x2))


if __name__ == "__main__":
    main()
