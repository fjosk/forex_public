#!/usr/bin/env python3
"""williams_r_swing_daily -- Williams %R pullback swing in EMA20 trend direction. QuantifiedStrategies."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "williams_r_swing_daily",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "daily/4h",
    "indicators": "willr, ema20",
    "long": "close above ema20 AND willr crosses back above -80 (exits oversold zone)",
    "short": "close below ema20 AND willr crosses back below -20 (exits overbought zone)",
    "desc": "Williams %R pullback swing: oversold/overbought exit in EMA20 trend",
    "source": "web:https://www.quantifiedstrategies.com/williams-r-trading-strategy/",
}


def signal(ind, pos, htf=None):
    """Trend pullback via W%R: in uptrend, cross back above -80 from below."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    e20 = ind["ema20"][pos]
    wr0 = ind["willr"][pos]
    wr1 = ind["willr"][pos - 1]
    if nan(c, e20, wr0, wr1):
        return None

    # Long: trend up, W%R exits oversold (crosses above -80)
    if c > e20 and wr0 > -80 and wr1 <= -80:
        return "long"

    # Short: trend down, W%R exits overbought (crosses below -20)
    if c < e20 and wr0 < -20 and wr1 >= -20:
        return "short"

    return None
