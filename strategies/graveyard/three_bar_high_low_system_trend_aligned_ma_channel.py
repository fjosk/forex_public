#!/usr/bin/env python3
"""three_bar_high_low_system -- Williams three-bar high/low channel: enter at 3-MA of lows in uptrend. long_term_secrets_to_short_term_trading.

Swing trend direction determined by EMA50 slope (proxy for fractal swing-point trend).
Uptrend: buy when price low touches or dips below the 3-bar MA of lows (mah3/mal3 or sma3_low).
Downtrend: sell when price high touches or rises above the 3-bar MA of highs.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "three_bar_high_low_system_trend_aligned_ma_channel",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "high,low,sma3_high,sma3_low,ema50",
    "long": "EMA50 rising (uptrend) AND low touches or dips to the 3-bar MA of lows (pullback entry)",
    "short": "EMA50 falling (downtrend) AND high touches or rises to the 3-bar MA of highs (bounce entry)",
    "desc": "Three-bar high/low channel system: enter at the 3-period MA of lows/highs in trend direction",
    "source": "long_term_secrets_to_short_term_trading Ch9 Figures 9.5-9.6 pp136-138",
}


def signal(ind, pos, htf=None):
    """Three-bar channel: touch of 3-MA lows in uptrend, 3-MA highs in downtrend."""
    if pos < 5:
        return None
    lo   = ind["low"][pos]
    hi   = ind["high"][pos]
    sl3  = ind["sma3_low"][pos]
    sh3  = ind["sma3_high"][pos]
    e50  = ind["ema50"][pos]
    e504 = ind["ema50"][pos - 4]
    if nan(lo, hi, sl3, sh3, e50, e504):
        return None
    trend_up = e50 > e504
    trend_dn = e50 < e504
    # Long: uptrend + low touches the 3-bar MA of lows (pullback to channel bottom)
    if trend_up and lo <= sl3:
        return "long"
    # Short: downtrend + high touches the 3-bar MA of highs (bounce to channel top)
    if trend_dn and hi >= sh3:
        return "short"
    return None
