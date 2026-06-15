#!/usr/bin/env python3
"""
Dukascopy ingestion -> sister-lab-compatible parquet, plus HistData gap-patching.

Runs in /home/user/FOREX/.venv. See dukascopy_fetch.py for the DoH/ISP-block note.

Modes:
  Full pull (Dukascopy-only instruments HistData lacks):
    python3 dukascopy_ingest.py --pull wti copper natgas
    -> writes parquet/unified/<PAIR>/<PAIR>-<iv> for iv in 1m/5m/15m/1h/4h/1d.
  Patch (fill a HistData hole; HistData stays authoritative, Dukascopy fills only the gap):
    python3 dukascopy_ingest.py --patch usdzar 2017-02-10 2017-02-27
    -> merges the window into the existing 1m parquet (dedupe keep HistData), re-resamples all.

Output schema identical to convert.py; resample rules match (left-labelled/left-closed,
weekend/holiday empties dropped). 1m carries per-row source ("dukascopy"/"histdata");
resampled bars get a single source label (informational).
"""

import argparse
import os
import sys
from datetime import datetime, timezone

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # FOREX root
from shared import timeutils as _tu   # single source for epoch math
import dukascopy_fetch as dkf

OUT_ROOT = "/home/user/FOREX/LAB/parquet/unified"
PULL_START = datetime(2007, 1, 1, tzinfo=timezone.utc)   # Dukascopy era floor; it returns from its own start
RESAMPLE_RULES = {"5m": "5min", "15m": "15min", "1h": "1h", "4h": "4h", "1d": "1D"}
OHLC_AGG = {"open": "first", "high": "max", "low": "min", "close": "last"}


def _write_atomic(df, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    df.to_parquet(tmp, index=False)
    os.replace(tmp, path)


def _unified_from_resample(r, source_label):
    """Resampled OHLC frame (tz-aware UTC index) -> sister-lab 9-col schema."""
    n = len(r)
    # Resolution-safe epoch-ms via the shared helper (the // 10**6 bug that produced ~1970 dates
    # is why this math now lives in one place: shared/timeutils.to_epoch_ms).
    open_time = _tu.to_epoch_ms(r.index)
    return pd.DataFrame({
        "open_time": open_time.to_numpy(),
        "open": r["open"].to_numpy("float64"),
        "high": r["high"].to_numpy("float64"),
        "low": r["low"].to_numpy("float64"),
        "close": r["close"].to_numpy("float64"),
        "volume": [0.0] * n,
        "quote_volume": [0.0] * n,
        "trades": [0] * n,
        "source": [source_label] * n,
    })


def _resample_and_write_all(m1, pair, source_label):
    """Given a unified 1m frame, write 1m + every resampled interval for the pair."""
    out_dir = os.path.join(OUT_ROOT, pair.upper())
    _write_atomic(m1.reset_index(drop=True), os.path.join(out_dir, f"{pair.upper()}-1m.parquet"))
    idx = pd.to_datetime(m1["open_time"], unit="ms", utc=True)
    base = pd.DataFrame(
        {"open": m1["open"].to_numpy(), "high": m1["high"].to_numpy(),
         "low": m1["low"].to_numpy(), "close": m1["close"].to_numpy()},
        index=pd.DatetimeIndex(idx),
    )
    counts = {"1m": len(m1)}
    for iv, rule in RESAMPLE_RULES.items():
        r = base.resample(rule, label="left", closed="left").agg(OHLC_AGG).dropna(how="any")
        frame = _unified_from_resample(r, source_label)
        _write_atomic(frame, os.path.join(out_dir, f"{pair.upper()}-{iv}.parquet"))
        counts[iv] = len(frame)
    return counts


def pull_full(pair, end):
    """Fetch a Dukascopy instrument's full 1m history (chunked by year) and write all intervals."""
    frames = []
    for year in range(PULL_START.year, end.year + 1):
        y0 = datetime(year, 1, 1, tzinfo=timezone.utc)
        y1 = datetime(year + 1, 1, 1, tzinfo=timezone.utc)
        if y1 > end:
            y1 = end
        f = dkf.fetch_unified(pair, y0, y1)
        if len(f):
            frames.append(f)
            print(f"    {pair} {year}: {len(f)} rows")
    if not frames:
        print(f"  {pair}: no Dukascopy data, skip")
        return
    m1 = pd.concat(frames, ignore_index=True)
    m1 = m1.drop_duplicates(subset=["open_time"], keep="last").sort_values("open_time").reset_index(drop=True)
    counts = _resample_and_write_all(m1, pair, "dukascopy")
    span = pd.to_datetime([m1.open_time.iloc[0], m1.open_time.iloc[-1]], unit="ms", utc=True)
    print(f"  ok  {pair}: " + " ".join(f"{k}={v}" for k, v in counts.items())
          + f"  [{span[0]} .. {span[1]}]")


def patch(pair, start, end):
    """Fill an existing HistData 1m parquet's gap with Dukascopy for [start,end); HistData wins overlaps."""
    path = os.path.join(OUT_ROOT, pair.upper(), f"{pair.upper()}-1m.parquet")
    existing = pd.read_parquet(path)
    fill = dkf.fetch_unified(pair, start, end)
    print(f"  {pair}: existing 1m={len(existing)}, dukascopy fill rows={len(fill)}")
    # HistData authoritative: keep existing rows on any open_time collision, add Dukascopy elsewhere.
    merged = pd.concat([existing, fill], ignore_index=True)
    merged = merged.drop_duplicates(subset=["open_time"], keep="first").sort_values("open_time").reset_index(drop=True)
    added = len(merged) - len(existing)
    counts = _resample_and_write_all(merged, pair, "histdata")  # dominant source label
    print(f"  ok  {pair}: added {added} bars from Dukascopy; " + " ".join(f"{k}={v}" for k, v in counts.items()))


def main():
    ap = argparse.ArgumentParser(description="Dukascopy ingest + HistData gap patch")
    ap.add_argument("--pull", nargs="*", default=[], help="instrument names for full-history pull")
    ap.add_argument("--patch", nargs=3, metavar=("PAIR", "START", "END"),
                    help="patch a HistData gap: PAIR YYYY-MM-DD YYYY-MM-DD")
    args = ap.parse_args()

    now = datetime.now(timezone.utc)
    if args.pull:
        print("=== Dukascopy full pull ===")
        for pair in args.pull:
            pull_full(pair.lower(), now)
    if args.patch:
        pair, s, e = args.patch
        print("=== Dukascopy patch ===")
        patch(pair.lower(),
              datetime.fromisoformat(s).replace(tzinfo=timezone.utc),
              datetime.fromisoformat(e).replace(tzinfo=timezone.utc))
    print("Done.")


if __name__ == "__main__":
    main()
