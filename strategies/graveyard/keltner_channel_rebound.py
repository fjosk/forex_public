#!/usr/bin/env python3
"""keltner_channel_rebound -- Keltner Channel Band Rebound Mean Reversion. mql5 articles 14169."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "keltner_channel_rebound",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h",
    "indicators": "kc_lo, kc_up",
    "long": "prev close < kc_lo AND current close > kc_lo (re-entry from below)",
    "short": "prev close > kc_up AND current close < kc_up (re-entry from above)",
    "desc": "Keltner Channel re-entry fade: price was outside band, now back inside (MQL5 rebound variant)",
    "source": "mql5.com/en/articles/14169 Keltner Channel bands rebound strategy 1",
}


def signal(ind, pos, htf=None):
    """Price re-enters Keltner Channel from beyond the band."""
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    kl = ind["kc_lo"][pos]
    kl1 = ind["kc_lo"][pos - 1]
    ku = ind["kc_up"][pos]
    ku1 = ind["kc_up"][pos - 1]
    if nan(c, c1, kl, kl1, ku, ku1):
        return None
    if c1 < kl1 and c > kl:
        return "long"
    if c1 > ku1 and c < ku:
        return "short"
    return None
