#!/usr/bin/env python3
"""oops_with_9day_ma_filter -- Oops! gap fade with 9-day MA overbought/oversold filter. long_term_secrets_to_short_term_trading.

Oops! BUY only when 9-day MA is falling (oversold). Oops! SELL only when 9-day MA is rising (overbought).
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "oops_with_9day_ma_filter",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean_revert",
    "tf": "1h-4h",
    "indicators": "open,close,prev_dhh,prev_dll,sma10",
    "long": "Oops! gap-down AND sma10 falling (9-day MA declining = oversold)",
    "short": "Oops! gap-up AND sma10 rising (9-day MA advancing = overbought)",
    "desc": "Oops! gap-fade with 9-bar MA direction filter: only fade when MA confirms oversold/overbought",
    "source": "long_term_secrets_to_short_term_trading, Ch7 pp.118-119",
}


def signal(ind, pos, htf=None):
    """Oops! gap fade filtered by SMA direction."""
    if pos < 2:
        return None
    op = ind["open"][pos]
    c = ind["close"][pos]
    dhh = ind["prev_dhh"][pos]
    dll = ind["prev_dll"][pos]
    # sma10 as closest available proxy for 9-day MA
    ma = ind["sma10"][pos]
    ma1 = ind["sma10"][pos - 1]
    if nan(op, c, dhh, dll, ma, ma1):
        return None
    ma_falling = ma < ma1
    ma_rising = ma > ma1
    if op < dll and c >= dll and ma_falling:
        return "long"
    if op > dhh and c <= dhh and ma_rising:
        return "short"
    return None
