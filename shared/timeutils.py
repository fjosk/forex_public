#!/usr/bin/env python3
"""
Shared time helpers -- the SINGLE SOURCE for FOREX's epoch/timezone math.

The epoch-millisecond conversion below was copy-pasted into convert.py, dukascopy_fetch.py and
dukascopy_ingest.py; one of those copies shipped the wrong form (`.astype(int64) // 10**6`, which is
1e6 too small for a datetime64[ms] index) and silently wrote ~1970 timestamps into 25 parquet files
(fixed 2026-06-06). Centralising it here means there is one correct implementation to import.

Pure module (pandas only, no I/O) -- safe to import anywhere, incl. shared/.
"""
import pandas as pd

# HistData stamps EST WITHOUT daylight saving (a flat UTC-5 all year), so UTC = local + 5h.
# (Dukascopy is already native UTC and needs no shift.)
EST_TO_UTC_HOURS = 5

_EPOCH_NAIVE = pd.Timestamp("1970-01-01")
_EPOCH_UTC = pd.Timestamp("1970-01-01", tz="UTC")


def to_epoch_ms(index):
    """A pandas DatetimeIndex -> int64 epoch milliseconds.

    Resolution-SAFE: subtract the epoch and floor-divide by a 1ms Timedelta. Do NOT use
    `.astype('int64') // 10**6` -- for a datetime64[ms] index that value is already in ms, so the
    extra /10**6 lands near 1970 (the bug this module exists to prevent). Works for a tz-aware
    index (uses the UTC epoch) and for a naive index already in UTC (uses the naive epoch).
    """
    base = _EPOCH_NAIVE if getattr(index, "tz", None) is None else _EPOCH_UTC
    return ((index - base) // pd.Timedelta("1ms")).astype("int64")
