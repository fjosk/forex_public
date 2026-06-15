#!/usr/bin/env python3
"""bb_mean_reversion_rsi7 -- BB band-touch fade with RSI14 extreme filter. web:sahi.com."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "bb_mean_reversion_rsi7",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "5m",
    "indicators": "bb_up, bb_lo, bb_mid, bb_width, rsi",
    "long": "close <= bb_lo AND rsi < 40 (RSI14 proxy for RSI7<35) AND bb_width low",
    "short": "close >= bb_up AND rsi > 60 AND bb_width low",
    "desc": "Bollinger Band mean reversion fade at band extremes with RSI filter",
    "source": "web:https://www.sahi.com/blogs/bollinger-bands-scalping-squeeze-breakouts-and-mean-reversion-setups",
}


def signal(ind, pos, htf=None):
    """Fade BB band extremes in range-bound conditions with RSI confirmation."""
    bb_up = ind["bb_up"][pos]
    bb_lo = ind["bb_lo"][pos]
    bbw = ind["bb_width"][pos]
    rsi = ind["rsi"][pos]
    c = ind["close"][pos]
    if nan(bb_up, bb_lo, bbw, rsi, c):
        return None
    # require non-expanding band (use bb_width percentile proxy: compare to prev 20 bars)
    if pos < 20:
        return None
    bbw_hist = ind["bb_width"][pos - 20:pos]
    bbw_max = max(bbw_hist)
    range_bound = bbw < bbw_max * 0.6
    if not range_bound:
        return None
    if c <= bb_lo and rsi < 40:
        return "long"
    if c >= bb_up and rsi > 60:
        return "short"
    return None
