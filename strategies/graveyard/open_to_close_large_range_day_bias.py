#!/usr/bin/env python3
"""open_to_close_large_range_day_bias -- Large-range day: open-near-low closes high; open-near-high closes low. long_term_secrets_to_short_term_trading.

If open is within 20% of the bar low (open near low), the bar tends to close near its high -> long.
If open is within 20% of the bar high (open near high), bar tends to close near its low -> short.
Uses confirmed bar (prior bar) to generate next-bar bias signal.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "open_to_close_large_range_day_bias",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "open,high,low,close",
    "long": "prior bar: (open-low)/(high-low) < 0.20 AND close in top 70% of range (large up-range day confirmed)",
    "short": "prior bar: (high-open)/(high-low) < 0.20 AND close in bottom 30% of range (large down-range day confirmed)",
    "desc": "Large directional day bias: open near range extreme + confirmed directional close signals continuation",
    "source": "long_term_secrets_to_short_term_trading, Ch2 pp.33-36",
}


def signal(ind, pos, htf=None):
    """Large-range day directional bias from prior bar open-to-low/high ratio."""
    if pos < 1:
        return None
    o1 = ind["open"][pos - 1]
    h1 = ind["high"][pos - 1]
    l1 = ind["low"][pos - 1]
    c1 = ind["close"][pos - 1]
    if nan(o1, h1, l1, c1):
        return None
    rng = h1 - l1
    if rng <= 0:
        return None
    dip_from_open = (o1 - l1) / rng   # how far open is from low as fraction of range
    rise_from_open = (h1 - o1) / rng  # how far open is from high as fraction of range
    close_pos = (c1 - l1) / rng
    # Open near low (< 20% from low) and close near high (> 70%) -> bullish large day
    if dip_from_open < 0.20 and close_pos > 0.70:
        return "long"
    # Open near high (< 20% from high) and close near low (< 30%) -> bearish large day
    if rise_from_open < 0.20 and close_pos < 0.30:
        return "short"
    return None
