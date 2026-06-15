#!/usr/bin/env python3
"""usd_jpy_trend_line_key_level_breakout_entry -- Key-level breakout: close > Donchian high
(daily/weekly prior) plus Ichimoku cloud filter for direction bias.
Currency Trading for Dummies 2nd Ed., Ch.8."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "usd_jpy_trend_line_key_level_breakout_entry",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h-1d",
    "indicators": "dc_up,dc_lo,ich_a,ich_b,close",
    "long": "close > Donchian upper and close > Ichimoku cloud top (ich_a, ich_b max)",
    "short": "close < Donchian lower and close < Ichimoku cloud bottom",
    "desc": "Key-level/trend-line breakout with Ichimoku cloud direction filter (USD/JPY focus)",
    "source": "Currency Trading for Dummies 2nd Ed., Ch.8 USD/JPY tactical trading",
}


def signal(ind, pos, htf=None):
    """Donchian breakout gated by Ichimoku cloud direction."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    dc_hi = ind["dc_up"][pos]
    dc_lo = ind["dc_lo"][pos]
    ich_a = ind["ich_a"][pos]
    ich_b = ind["ich_b"][pos]
    if nan(c, dc_hi, dc_lo, ich_a, ich_b):
        return None
    cloud_hi = max(ich_a, ich_b)
    cloud_lo = min(ich_a, ich_b)
    if c > dc_hi and c > cloud_hi:
        return "long"
    if c < dc_lo and c < cloud_lo:
        return "short"
    return None
