#!/usr/bin/env python3
"""
Dukascopy ingest -> sister-lab-compatible unified parquet (SECONDARY source).

Purpose (decided 2026-06-06): (1) pull the commodities HistData lacks but Ostium trades --
WTI, copper, natural gas; (2) cross-validate HistData quality + opportunistically patch the
isolated Feb-2017 USD/ZAR + USD/MXN hole. NOT for the 2000-2003 majors holes (Dukascopy only
starts ~2007 there; unfixable -- see CLAUDE.md).

RUNTIME: the dedicated FOREX venv /home/user/FOREX/.venv (dukascopy-python has a heavy dep
tree kept OUT of /home/user/global-venv, which runs sister-lab live).

ISP / DNS NOTE (verified 2026-06-06): this host's resolver (Tailscale MagicDNS) returns a
POISONED record for *.dukascopy.com (NAT64-wrapped sinkhole 64:ff9b::2bad:3930) and TLS to it
resets. The real AWS-Zurich servers ARE reachable; the block is DNS-poisoning ONLY, not
SNI/DPI. So we resolve dukascopy hostnames via DoH (Cloudflare 1.1.1.1) and connect to the
real IP with normal SNI. A socket.getaddrinfo shim (installed on import) does this
transparently for requests/urllib3 -- no system DNS change, no root, Tailscale untouched.

SCHEMA: identical to convert.py / sister-lab (9 cols, RangeIndex, open_time epoch-ms UTC). We take
BID OHLC (parity with HistData's bid-only bars). Dukascopy is native UTC (no EST shift).
volume/quote_volume/trades = 0 for homogeneity with the HistData pairs; source = "dukascopy".
"""

import os
import socket
import sys
import numpy as np
import pandas as pd
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # FOREX root
from shared import instruments as _instr   # the single instrument registry
from shared import timeutils as _tu        # single source for epoch math

# --- DoH getaddrinfo shim for *.dukascopy.com (ISP poisons their DNS) -----------------
_real_getaddrinfo = socket.getaddrinfo
_doh_cache = {}


def _doh_resolve(host):
    if host not in _doh_cache:
        r = requests.get("https://1.1.1.1/dns-query",
                         params={"name": host, "type": "A"},
                         headers={"accept": "application/dns-json"}, timeout=20)
        _doh_cache[host] = [a["data"] for a in r.json().get("Answer", []) if a.get("type") == 1]
    return _doh_cache[host]


def _patched_getaddrinfo(host, *args, **kwargs):
    if isinstance(host, str) and host.endswith("dukascopy.com"):
        ips = _doh_resolve(host)
        if ips:
            return _real_getaddrinfo(ips[0], *args, **kwargs)
    return _real_getaddrinfo(host, *args, **kwargs)


socket.getaddrinfo = _patched_getaddrinfo  # installed on import; idempotent enough for our use

import dukascopy_python as dk                       # noqa: E402 (must follow the shim)
from dukascopy_python import instruments as _I      # noqa: E402

# Friendly name -> dukascopy_python instrument constant. Pair codes match the HistData lab so
# the two sources land in the same parquet/unified/<PAIR> folders.
# {lowercase code -> dukascopy_python INSTRUMENT_* const}, single-sourced from the registry. Covers
# the 12 FX (for cross-validation + patching HistData) + the 3 commodities HistData lacks
# (WTI/copper/natgas). Brent (bcousd) is HistData-only, so it has no Dukascopy id and is absent here.
INSTRUMENTS = _instr.dukascopy_map()


def _to_unified(df):
    """dukascopy_python OHLC frame (tz-aware UTC DatetimeIndex) -> sister-lab 9-col schema."""
    n = len(df)
    open_time = _tu.to_epoch_ms(df.index)
    return pd.DataFrame({
        "open_time": open_time.to_numpy(),
        "open": df["open"].to_numpy("float64"),
        "high": df["high"].to_numpy("float64"),
        "low": df["low"].to_numpy("float64"),
        "close": df["close"].to_numpy("float64"),
        "volume": np.zeros(n, dtype="float64"),        # homogeneity with HistData (no volume)
        "quote_volume": np.zeros(n, dtype="float64"),
        "trades": np.zeros(n, dtype="int64"),
        "source": np.array(["dukascopy"] * n, dtype=object),
    })


def fetch_unified(name, start, end, interval=None, offer=None):
    """
    Fetch BID 1m (default) bars for `name` between start/end (datetime, UTC-naive ok) and
    return the sister-lab-compatible 9-col frame (empty frame if Dukascopy has nothing).
    """
    const = INSTRUMENTS[name]
    instrument = getattr(_I, const)
    interval = interval or dk.INTERVAL_MIN_1
    offer = offer or dk.OFFER_SIDE_BID
    df = dk.fetch(instrument, interval, offer, start, end)
    if df is None or len(df) == 0:
        return _to_unified(pd.DataFrame(columns=["open", "high", "low", "close"],
                                        index=pd.DatetimeIndex([], tz="UTC")))
    return _to_unified(df)
