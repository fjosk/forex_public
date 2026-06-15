#!/usr/bin/env python3
"""wilder_arc_vol_trailing_stop_reverse -- Wilder ARC Volatility Trailing Stop-and-Reverse: always-in system where the position flips when close crosses the 3*ATR trailing ARC line. Tharp Ch.8.

Price/OHLC only. No volume.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "wilder_arc_vol_trailing_stop_reverse",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "atr, close, st_dir",
    "long": "Close rises above the 3*ATR ARC stop line (proxied by Supertrend direction flipping to +1)",
    "short": "Close falls below the 3*ATR ARC stop line (proxied by Supertrend direction flipping to -1)",
    "desc": "Wilder ARC always-in system: position reverses when close crosses the 3*ATR trailing stop line; proxied by Supertrend flip",
    "source": "trade_your_way_to_financial_freedom -- Ch.8 Volatility Breakouts (Wilder ARC)",
}


def signal(ind, pos, htf=None):
    """Supertrend direction flip proxies the ARC 3*ATR stop-and-reverse crossover."""
    if pos < 1:
        return None
    sd = ind["st_dir"][pos]
    sd1 = ind["st_dir"][pos - 1]
    if nan(sd, sd1):
        return None
    # Supertrend direction: +1 = uptrend (close above trail), -1 = downtrend
    if sd > 0 and sd1 <= 0:
        return "long"
    if sd < 0 and sd1 >= 0:
        return "short"
    return None
