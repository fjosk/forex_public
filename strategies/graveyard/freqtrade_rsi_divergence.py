#!/usr/bin/env python3
"""freqtrade_rsi_divergence -- Bullish RSI divergence: price LL but RSI HL, confirmed by ADX+Stoch.

Uses frac_dn (fractal pivot low) to locate prior pivot lows and compare RSI.
Searches back up to 60 bars for the most recent prior pivot low. Long-only per source.
No volume -> FX-applicable.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "freqtrade_rsi_divergence",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "1h",
    "indicators": "rsi, adx, stoch_d, frac_dn, low",
    "long": "bullish RSI divergence (price LL, RSI HL at pivot lows) AND rsi in 30-60 AND adx>25 AND stoch_d in 20-80",
    "short": "not implemented (source is long-only)",
    "desc": "RSI divergence long: price makes lower low but RSI higher low at fractal pivot, with ADX+Stoch filter",
    "source": "github.com/thierryjmartin/freqtrade-stuff/RSIDivergence.py",
}

_LOOKBACK = 60


def signal(ind, pos, htf=None):
    """Bullish RSI divergence using fractal pivot lows."""
    if pos < _LOOKBACK + 1:
        return None
    # Detect if current bar-1 is a pivot low (fractal low)
    fd1 = ind["frac_dn"][pos - 1]
    if nan(fd1) or fd1 == 0:
        return None
    # Current pivot low values
    rs_cur = ind["rsi"][pos - 1]
    lo_cur = ind["low"][pos - 1]
    if nan(rs_cur, lo_cur):
        return None
    # Search back for a prior pivot low within lookback
    prior_rsi = None
    prior_low = None
    for k in range(2, _LOOKBACK):
        if pos - k < 0:
            break
        fd_k = ind["frac_dn"][pos - k]
        if nan(fd_k) or fd_k == 0:
            continue
        rs_k = ind["rsi"][pos - k]
        lo_k = ind["low"][pos - k]
        if nan(rs_k, lo_k):
            continue
        prior_rsi = rs_k
        prior_low = lo_k
        break
    if prior_rsi is None:
        return None
    # Bullish divergence: price lower low, RSI higher low
    price_ll = lo_cur < prior_low
    rsi_hl = rs_cur > prior_rsi
    if not (price_ll and rsi_hl):
        return None
    # Confirm with filters at current bar
    rs0 = ind["rsi"][pos]
    dx = ind["adx"][pos]
    sd = ind["stoch_d"][pos]
    if nan(rs0, dx, sd):
        return None
    # RSI 30-60, ADX>25, stoch_d 20-80
    if 30 < rs0 < 60 and dx > 25 and 20 < sd < 80:
        return "long"
    return None
