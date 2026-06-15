#!/usr/bin/env python3
"""gsv_intraday_contra_trend_fade_180_225 -- GSV intraday contra-trend fade: buy below open at
1.80x average daily swing (ATR proxy), stop at 2.25x; mirror short above open.

Source: long_term_secrets_to_short_term_trading, Ch.8 Table 8.1 pp.127-128.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "gsv_intraday_contra_trend_fade_180_225",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h-4h",
    "indicators": "day_open, close, atr",
    "long": "Close <= day_open - 1.80*ATR (price fell 1.8 swing units below open); fade long",
    "short": "Close >= day_open + 1.80*ATR (price rose 1.8 swing units above open); fade short",
    "desc": "GSV contra-trend fade: buy/short when price overshoots the open by 1.80x ATR",
    "source": "long_term_secrets_to_short_term_trading Ch.8 pp.127-128",
}


def signal(ind, pos, htf=None):
    """GSV fade: price extends 1.80*ATR from day open -> fade."""
    c = ind["close"][pos]
    d_open = ind["day_open"][pos]
    a = ind["atr"][pos]
    if nan(c, d_open, a) or a <= 0:
        return None
    swing = 1.80 * a
    if c <= d_open - swing:
        return "long"
    if c >= d_open + swing:
        return "short"
    return None
