#!/usr/bin/env python3
"""B10 -- Ichimoku TK cross confirmed by MACD. sister-lab live roster (tier3, forward-test add).

Price/OHLC only (no volume) -> FX-applicable. Signal logic ported from the sister-lab roster; it must
still clear the FOREX gauntlet on Ostium costs to earn a forward/live wiring. Self-contained module:
META (definition the loader reads) + signal() (the decision function the engine + future Ostium
trader both call). See strategies/README.md for the standard + lifecycle.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "B10",
    "cadences": ['day'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "Ichimoku + MACD(12,26,9)",
    "long": "TK cross above cloud & macd>signal",
    "short": "TK cross below cloud & macd<signal",
    "desc": "Ichimoku TK cross confirmed by MACD",
    "source": "sister-lab live roster (tier3, forward-test add)",
}


def signal(ind, pos, htf=None):
    """Ichimoku TK cross confirmed by MACD."""
    c = ind["close"][pos]
    ten, kij = ind["ich_ten"][pos], ind["ich_kij"][pos]
    ten1, kij1 = ind["ich_ten"][pos - 1], ind["ich_kij"][pos - 1]
    a, b = ind["ich_a"][pos], ind["ich_b"][pos]
    m, s = ind["macd"][pos], ind["macd_sig"][pos]
    if nan(c, ten, kij, ten1, kij1, a, b, m, s):
        return None
    cloud_top, cloud_bot = max(a, b), min(a, b)
    if c > cloud_top and ten > kij and ten1 <= kij1 and m > s:
        return "long"
    if c < cloud_bot and ten < kij and ten1 >= kij1 and m < s:
        return "short"
    return None
