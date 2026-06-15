#!/usr/bin/env python3
"""
Convert HistData M1 zip archives into sister-lab-compatible unified parquet.

Reads the raw per-pair zips in LAB/data/<pair>/ (HistData generic-ASCII M1, semicolon
CSV: "YYYYMMDD HHMMSS;open;high;low;close;volume") and writes, per pair and per interval,
LAB/parquet/unified/<PAIR>/<PAIR>-<iv>.parquet. The backtest reads ONLY this output.

Schema parity (locked in CLAUDE.md): the parquet matches sister-lab/LAB/parquet/unified exactly
so sister-lab's engine/indicators/loaders read FOREX data unchanged. 9 columns, RangeIndex
(NOT a datetime index), open_time = epoch MILLISECONDS in UTC:
  open_time:int64 | open/high/low/close:float64 | volume:float64 | quote_volume:float64 |
  trades:int64 | source:object
FOREX placeholders: volume=0.0 (HistData has no volume), quote_volume=0.0, trades=0,
source="histdata". OHLC is BID-only.

Timezone (the easy-to-get-wrong part): HistData timestamps are US Eastern WITHOUT daylight
saving -- i.e. a FIXED UTC-5 offset year-round. So UTC = local + 5h ALWAYS. We must NOT use
a "US/Eastern" tz (that would apply DST and shift half the year by an hour). We add a flat
5 hours to the naive timestamp and treat the result as UTC.

Intervals: 1m (base, as-is) + resampled 5m/15m/1h/4h/1d. Bars are left-labelled/left-closed
so open_time = bar START (matches Binance/sister-lab). Resampled periods with no underlying 1m
bars (FX weekends/holidays) are dropped, never fabricated.

Usage:
    python3 convert.py                 # all pairs found under LAB/data
    python3 convert.py --pairs eurusd  # one pair
    python3 convert.py --force         # rewrite even if parquet already exists
"""

import argparse
import os
import sys
import zipfile

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # FOREX root
from shared import timeutils as _tu   # single source for epoch/EST math

DEFAULT_DATA_ROOT = "/home/user/FOREX/LAB/data"
DEFAULT_OUT_ROOT = "/home/user/FOREX/LAB/parquet/unified"

# Resample rules for the derived intervals. 1m is the base (no resample). Left-labelled +
# left-closed so open_time is the bar start, matching Binance/sister-lab klines.
RESAMPLE_RULES = {
    "5m": "5min",
    "15m": "15min",
    "1h": "1h",
    "4h": "4h",
    "1d": "1D",
}
ALL_INTERVALS = ["1m"] + list(RESAMPLE_RULES.keys())

OHLC_AGG = {"open": "first", "high": "max", "low": "min", "close": "last"}


def read_pair_m1(pair_dir):
    """Read + concatenate every M1 csv in a pair's zips into one raw frame (ts as str)."""
    zips = sorted(
        os.path.join(pair_dir, f) for f in os.listdir(pair_dir)
        if f.lower().endswith(".zip")
    )
    frames = []
    for zpath in zips:
        with zipfile.ZipFile(zpath) as zf:
            csv_names = [n for n in zf.namelist() if n.lower().endswith(".csv")]
            if not csv_names:
                continue
            with zf.open(csv_names[0]) as fh:
                frames.append(pd.read_csv(
                    fh, sep=";", header=None,
                    names=["ts", "open", "high", "low", "close", "volume"],
                    dtype={"ts": str},
                ))
    if not frames:
        return None
    return pd.concat(frames, ignore_index=True)


def to_unified_schema(open_time_ms, o, h, l, c):
    """Build the exact 9-column sister-lab-compatible frame (RangeIndex). FX placeholders set."""
    n = len(open_time_ms)
    return pd.DataFrame({
        "open_time": pd.Series(open_time_ms, dtype="int64").reset_index(drop=True),
        "open": pd.Series(o, dtype="float64").reset_index(drop=True),
        "high": pd.Series(h, dtype="float64").reset_index(drop=True),
        "low": pd.Series(l, dtype="float64").reset_index(drop=True),
        "close": pd.Series(c, dtype="float64").reset_index(drop=True),
        "volume": pd.Series([0.0] * n, dtype="float64"),         # HistData has no volume
        "quote_volume": pd.Series([0.0] * n, dtype="float64"),   # parity placeholder
        "trades": pd.Series([0] * n, dtype="int64"),             # parity placeholder
        "source": pd.Series(["histdata"] * n, dtype="object"),
    })


def index_to_ms(dt_index):
    """UTC DatetimeIndex (tz-naive, representing UTC) -> epoch milliseconds int64."""
    return _tu.to_epoch_ms(dt_index)


def write_atomic(df, path):
    """Write parquet atomically (tmp + os.replace) so a crash never leaves a partial file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    df.to_parquet(tmp, index=False)
    os.replace(tmp, path)


def convert_pair(pair, data_root, out_root, force):
    pair_dir = os.path.join(data_root, pair)
    out_dir = os.path.join(out_root, pair.upper())
    targets = {iv: os.path.join(out_dir, f"{pair.upper()}-{iv}.parquet") for iv in ALL_INTERVALS}

    if not force and all(os.path.exists(p) for p in targets.values()):
        print(f"  {pair}: all intervals present, skip (use --force to rewrite)")
        return

    raw = read_pair_m1(pair_dir)
    if raw is None or raw.empty:
        print(f"  {pair}: no data found in {pair_dir}, skip")
        return

    # Parse timestamps and shift EST(UTC-5) -> UTC with a flat +5h. Drop unparseable/dup rows.
    dt_utc = pd.to_datetime(raw["ts"], format="%Y%m%d %H%M%S", errors="coerce") \
        + pd.Timedelta(hours=_tu.EST_TO_UTC_HOURS)
    raw = raw.assign(dt=dt_utc).dropna(subset=["dt", "open", "high", "low", "close"])
    raw = raw.drop_duplicates(subset=["dt"], keep="last").sort_values("dt")

    # 1m base: straight schema conversion (no resample).
    m1 = to_unified_schema(
        index_to_ms(pd.DatetimeIndex(raw["dt"])),
        raw["open"].to_numpy(), raw["high"].to_numpy(),
        raw["low"].to_numpy(), raw["close"].to_numpy(),
    )
    write_atomic(m1, targets["1m"])
    counts = {"1m": len(m1)}

    # Resampled intervals: OHLC over a tz-naive-UTC index, drop empty (weekend/holiday) bars.
    base = raw.set_index("dt")[["open", "high", "low", "close"]]
    for iv, rule in RESAMPLE_RULES.items():
        r = base.resample(rule, label="left", closed="left").agg(OHLC_AGG).dropna(how="any")
        frame = to_unified_schema(
            index_to_ms(r.index),
            r["open"].to_numpy(), r["high"].to_numpy(),
            r["low"].to_numpy(), r["close"].to_numpy(),
        )
        write_atomic(frame, targets[iv])
        counts[iv] = len(frame)

    span = f"{raw['dt'].iloc[0]} .. {raw['dt'].iloc[-1]} UTC"
    print(f"  ok  {pair}: " + " ".join(f"{iv}={counts[iv]}" for iv in ALL_INTERVALS) + f"  [{span}]")


def main():
    sys.stdout.reconfigure(line_buffering=True)
    parser = argparse.ArgumentParser(description="HistData M1 zips -> sister-lab-compatible parquet")
    parser.add_argument("--pairs", default="",
                        help="space/comma list of pair codes; default = every folder in --data")
    parser.add_argument("--data", default=DEFAULT_DATA_ROOT)
    parser.add_argument("--out", default=DEFAULT_OUT_ROOT)
    parser.add_argument("--force", action="store_true", help="rewrite parquet even if present")
    args = parser.parse_args()

    if args.pairs.strip():
        pairs = [p.lower() for p in args.pairs.replace(",", " ").split()]
    else:
        pairs = sorted(d for d in os.listdir(args.data)
                       if os.path.isdir(os.path.join(args.data, d)))

    print("=" * 46)
    print(" HistData -> unified parquet (sister-lab-compatible)")
    print(f" pairs : {' '.join(pairs)}")
    print(f" out   : {args.out}")
    print("=" * 46)
    for pair in pairs:
        convert_pair(pair, args.data, args.out, args.force)
    print("=" * 46)
    print("Done.")


if __name__ == "__main__":
    main()
