#!/usr/bin/env python3
"""inside_day_breakout_play_multi -- Two or more consecutive inside bars; breakout above/below cluster. day_trading_swing_trading_kathy_lien."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "inside_day_breakout_play_multi_inside_day_volatility_breakout_stop_and",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "high, low, macd_hist",
    "long": ">=2 consecutive inside days; current high breaks above the most recent inside day high",
    "short": ">=2 consecutive inside days; current low breaks below the most recent inside day low",
    "desc": "Multi inside-day volatility breakout: >=2 inside days, directional break of cluster extreme",
    "source": "day_trading_swing_trading_the_currency_market_tech",
}


def signal(ind, pos, htf=None):
    """Two or more consecutive inside bars followed by breakout."""
    if pos < 3:
        return None
    h = ind["high"]
    l = ind["low"]
    mh = ind["macd_hist"][pos] if "macd_hist" in ind else None

    if nan(h[pos], l[pos], h[pos - 1], l[pos - 1], h[pos - 2], l[pos - 2]):
        return None

    # Check pos-1 is inside bar relative to pos-2
    ib1 = h[pos - 1] <= h[pos - 2] and l[pos - 1] >= l[pos - 2]
    if not ib1:
        return None

    # Check if pos-2 is also inside bar relative to pos-3 (>=2 consecutive)
    double_inside = False
    if pos >= 3 and not nan(h[pos - 3], l[pos - 3]):
        ib2 = h[pos - 2] <= h[pos - 3] and l[pos - 2] >= l[pos - 3]
        if ib2:
            double_inside = True

    if not double_inside:
        return None

    # Breakout of most recent inside bar
    if h[pos] > h[pos - 1]:
        # Optional MACD hist directional bias (favor if > 0 for long)
        if mh is not None and not nan(mh) and mh < 0:
            return None
        return "long"
    if l[pos] < l[pos - 1]:
        if mh is not None and not nan(mh) and mh > 0:
            return None
        return "short"
    return None
