#!/usr/bin/env python3
"""swing_point_trend_identification -- Trend reversal confirmed when price breaks the most recent
fractal swing high (uptrend) or fractal swing low (downtrend). long_term_secrets_to_short_term_trading.

Pattern A: uptrend confirmed when close breaks above the last confirmed fractal high (frac_up_px).
Downtrend confirmed when close breaks below the last confirmed fractal low (frac_dn_px).
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "swing_point_trend_identification",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "close,frac_up_px,frac_dn_px",
    "long": "close breaks above the most recent confirmed fractal swing high (uptrend confirmed)",
    "short": "close breaks below the most recent confirmed fractal swing low (downtrend confirmed)",
    "desc": "Swing-point trend identification: fractal high/low break confirms trend direction per Williams/Williams",
    "source": "long_term_secrets_to_short_term_trading Ch.9 Figures 9.2-9.4",
}


def signal(ind, pos, htf=None):
    """Trend confirmed on fractal pivot break."""
    if pos < 1:
        return None
    c  = ind["close"][pos]
    fu = ind["frac_up_px"][pos]
    fd = ind["frac_dn_px"][pos]
    c1 = ind["close"][pos - 1]
    fu1 = ind["frac_up_px"][pos - 1]
    fd1 = ind["frac_dn_px"][pos - 1]
    if nan(c, c1):
        return None
    # Uptrend: close crosses above the fractal swing high
    if not nan(fu, fu1) and c > fu and c1 <= fu1:
        return "long"
    # Downtrend: close crosses below the fractal swing low
    if not nan(fd, fd1) and c < fd and c1 >= fd1:
        return "short"
    return None
