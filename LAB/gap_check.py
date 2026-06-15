#!/usr/bin/env python3
"""
Continuity audit for the unified 1m parquet.

Answers "is there missing data INSIDE the trading week?" -- the question raw year/month
file counts cannot. For FX the hard part is that WEEKEND gaps (Fri ~21:00 UTC close to Sun
~21:00 UTC open) are EXPECTED, not defects, so a naive calendar diff would flag every
weekend. This tool classifies each gap and reports only the suspicious intra-week ones.

What counts as normal vs suspicious:
- 1-minute steps: normal.
- Small intra-week gaps (a few quiet minutes with no quote): normal for HistData M1, which
  only emits a bar when a quote prints -- thin hours (overnight metals/exotics) legitimately
  skip minutes. These are counted but not listed individually.
- Weekend gaps (Friday -> Sunday/Monday, < ~60h): EXPECTED, reported as a count only.
- Large intra-week gaps (>= --min-gap, default 60 min, not over a weekend): SUSPICIOUS --
  either a market holiday (e.g. Dec 25, eyeball by date) or genuinely missing data. Listed.

Reads ONLY the open_time column (fast, low memory). Read-only; never modifies data.

Usage:
    python3 gap_check.py                 # all pairs under parquet/unified
    python3 gap_check.py --pairs eurusd
    python3 gap_check.py --min-gap 120   # only list intra-week gaps >= 120 min
"""

import argparse
import os
import sys

import numpy as np
import pandas as pd

DEFAULT_OUT_ROOT = "/home/user/FOREX/LAB/parquet/unified"
WEEKEND_MAX_HOURS = 60          # a Fri->Sun/Mon gap longer than this is not a plain weekend
BIG_GAP_HOURS = 6.0            # intra-week gaps beyond this are highlighted as notable


def classify_weekend(prev_ts, next_ts, missing_hours):
    """True if this gap is a normal forex weekend close (Fri -> Sun/Mon, under ~60h)."""
    return (prev_ts.dayofweek == 4                      # last bar on a Friday
            and next_ts.dayofweek in (6, 0)            # next bar on Sunday or Monday
            and missing_hours < WEEKEND_MAX_HOURS)


def audit_pair(pair, out_root, min_gap_min):
    path = os.path.join(out_root, pair.upper(), f"{pair.upper()}-1m.parquet")
    if not os.path.exists(path):
        print(f"  {pair}: no 1m parquet, skip")
        return None

    ot = pd.read_parquet(path, columns=["open_time"])["open_time"].to_numpy()
    bars = len(ot)
    if bars < 2:
        print(f"  {pair}: <2 bars, skip")
        return None

    dt = pd.to_datetime(ot, unit="ms", utc=True)
    diff_min = np.diff(ot) / 60000.0               # minutes between consecutive bars
    gap_pos = np.where(diff_min > 1.5)[0]          # any step beyond one minute

    weekend_n = 0
    weekend_missing = 0.0
    intraweek = []                                  # (missing_minutes, prev_ts, next_ts)
    for i in gap_pos:
        missing = diff_min[i] - 1.0                 # missing minute-slots in the gap
        prev_ts, next_ts = dt[i], dt[i + 1]
        if classify_weekend(prev_ts, next_ts, diff_min[i] / 60.0):
            weekend_n += 1
            weekend_missing += missing
        else:
            intraweek.append((missing, prev_ts, next_ts))

    # Coverage = filled minute-slots / trading minute-slots (total span minus weekend slots).
    span_min = (ot[-1] - ot[0]) / 60000.0 + 1
    trading_slots = span_min - weekend_missing
    coverage = 100.0 * bars / trading_slots if trading_slots > 0 else 0.0

    intraweek.sort(reverse=True, key=lambda x: x[0])
    big = [g for g in intraweek if g[0] >= min_gap_min]
    notable = [g for g in intraweek if g[0] / 60.0 >= BIG_GAP_HOURS]

    span = f"{dt[0].date()}..{dt[-1].date()}"
    print(f"  {pair.upper():7s} bars={bars:>10,}  {span}  coverage={coverage:5.1f}%"
          f"  weekendGaps={weekend_n:>5}  intraweekGaps>={int(min_gap_min)}m={len(big)}")
    for missing, prev_ts, next_ts in big[:8]:
        hrs = missing / 60.0
        tag = "  <-- NOTABLE" if hrs >= BIG_GAP_HOURS else ""
        print(f"        {prev_ts:%Y-%m-%d %a %H:%M} -> {next_ts:%Y-%m-%d %a %H:%M}  "
              f"missing {hrs:6.1f}h{tag}")
    return {"pair": pair, "coverage": coverage, "notable": len(notable)}


def main():
    sys.stdout.reconfigure(line_buffering=True)
    parser = argparse.ArgumentParser(description="Intra-week continuity audit of 1m parquet")
    parser.add_argument("--pairs", default="")
    parser.add_argument("--out", default=DEFAULT_OUT_ROOT)
    parser.add_argument("--min-gap", type=float, default=60.0,
                        help="list intra-week gaps with at least this many missing minutes")
    args = parser.parse_args()

    if args.pairs.strip():
        pairs = [p.lower() for p in args.pairs.replace(",", " ").split()]
    else:
        pairs = sorted(d for d in os.listdir(args.out)
                       if os.path.isdir(os.path.join(args.out, d)))

    print("=" * 70)
    print(" Intra-week continuity audit (weekend gaps are expected, not defects)")
    print("=" * 70)
    results = [audit_pair(p, args.out, args.min_gap) for p in pairs]
    results = [r for r in results if r]

    notable_pairs = [r["pair"] for r in results if r["notable"] > 0]
    print("=" * 70)
    if notable_pairs:
        print(f"Pairs with intra-week gaps >= {BIG_GAP_HOURS}h (eyeball for holiday vs hole): "
              + ", ".join(notable_pairs))
    else:
        print(f"No intra-week gaps >= {BIG_GAP_HOURS}h on any pair.")
    print("Note: large gaps near year-end / mid-week single days are usually market holidays,"
          " not missing data. Re-run download.sh only if a gap looks like a real hole.")


if __name__ == "__main__":
    main()
