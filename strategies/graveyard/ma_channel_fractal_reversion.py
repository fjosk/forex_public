#!/usr/bin/env python3
"""ma_channel_fractal_reversion -- MA Channel Fractal Reversion EA (simplified inline geometry)."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "ma_channel_fractal_reversion",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h",
    "indicators": "frac_up_px, frac_dn_px, frac_up_bar_low, frac_dn_bar_high, atr",
    "long": "channel slopes up, width > 5*atr, price near lower channel boundary + bullish bar",
    "short": "channel slopes down, width > 5*atr, price near upper channel boundary + bearish bar",
    "desc": "Fractal-anchored channel reversion: entry near boundary with reversal bar confirmation",
    "source": "mql5.com/en/articles/1375 Expert Advisor for Trading in the Channel",
}

_MIN_WIDTH_ATR = 5.0   # minimum channel width in ATR multiples
_PROX_ATR = 1.0        # proximity to boundary in ATR multiples


def signal(ind, pos, htf=None):
    """Fractal channel boundary proximity entry with bar reversal confirmation."""
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    fu_px = ind["frac_up_px"][pos]
    fd_px = ind["frac_dn_px"][pos]
    fu_bl = ind["frac_up_bar_low"][pos]
    fd_bh = ind["frac_dn_bar_high"][pos]
    atr_v = ind["atr"][pos]
    if nan(c, c1, fu_px, fd_px, fu_bl, fd_bh, atr_v) or atr_v <= 0:
        return None
    # upper fractal = recent swing high anchor; lower fractal = recent swing low anchor
    upper_ch = fu_px
    lower_ch = fd_px
    ch_width = upper_ch - lower_ch
    if ch_width < _MIN_WIDTH_ATR * atr_v:
        return None
    prox = _PROX_ATR * atr_v
    # long: price near lower channel boundary and bar closes higher
    if abs(c - lower_ch) <= prox and c > c1:
        return "long"
    # short: price near upper channel boundary and bar closes lower
    if abs(c - upper_ch) <= prox and c < c1:
        return "short"
    return None
