#!/usr/bin/env python3
"""displacement_candle_entry -- Displacement candle FVG retrace entry.

Identifies a large-body displacement candle (body > 1.5 * ATR) that broke a
fractal extreme. The FVG left by the displacement is the entry zone; enter on
retrace into that gap zone.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "displacement_candle_entry",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "scalp",
    "tf": "5m, 15m, 1h",
    "indicators": "close, open, high, low, atr, frac_up_px, frac_dn_px",
    "long": "bullish displacement (body > 1.5*ATR, broke fractal high); retrace into FVG",
    "short": "bearish displacement (body > 1.5*ATR, broke fractal low); retrace into FVG",
    "desc": "Displacement candle FVG: large-body structural break + gap retrace entry",
    "source": "web:https://dailypriceaction.com/blog/smc-trading-strategy/",
}

_BODY_ATR_MULT = 1.5
_LOOKBACK = 30


def signal(ind, pos, htf=None):
    """Displacement candle FVG retrace entry."""
    c = ind["close"][pos]
    hi = ind["high"][pos]
    lo = ind["low"][pos]
    if nan(c, hi, lo):
        return None

    high = ind["high"]
    low = ind["low"]
    open_ = ind["open"]
    close = ind["close"]
    atr = ind["atr"]
    frac_up = ind["frac_up_px"]
    frac_dn = ind["frac_dn_px"]

    # Search for the most recent bullish displacement + its FVG
    for i in range(pos - 2, max(2, pos - _LOOKBACK), -1):
        if i + 1 > pos:
            continue
        o_i = open_[i]; c_i = close[i]; a_i = atr[i]; f_up = frac_up[i - 1]
        if nan(o_i, c_i, a_i, f_up):
            continue
        body = c_i - o_i
        if body > _BODY_ATR_MULT * a_i and c_i > f_up:
            # Bullish displacement found; compute FVG
            g_lo = high[i - 1]
            g_hi = low[i + 1] if (i + 1) <= pos else lo
            if nan(g_lo, g_hi) or g_hi <= g_lo:
                break
            # Check if FVG already mitigated
            mitigated = any(close[j] < g_lo for j in range(i + 1, pos) if not nan(close[j]))
            if mitigated:
                break
            # Entry: current bar retraces into FVG
            if lo <= g_hi and c >= g_lo:
                return "long"
        break

    # Search for the most recent bearish displacement + its FVG
    for i in range(pos - 2, max(2, pos - _LOOKBACK), -1):
        if i + 1 > pos:
            continue
        o_i = open_[i]; c_i = close[i]; a_i = atr[i]; f_dn = frac_dn[i - 1]
        if nan(o_i, c_i, a_i, f_dn):
            continue
        body = o_i - c_i
        if body > _BODY_ATR_MULT * a_i and c_i < f_dn:
            # Bearish displacement found; compute FVG
            g_hi = low[i - 1]
            g_lo = high[i + 1] if (i + 1) <= pos else hi
            if nan(g_lo, g_hi) or g_hi <= g_lo:
                break
            mitigated = any(close[j] > g_hi for j in range(i + 1, pos) if not nan(close[j]))
            if mitigated:
                break
            if hi >= g_lo and c <= g_hi:
                return "short"
        break

    return None
