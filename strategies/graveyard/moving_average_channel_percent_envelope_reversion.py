#!/usr/bin/env python3
"""moving_average_channel_percent_envelope_reversion -- EMA13 percent envelope: buy at lower band,
sell at upper band; uses kc_lo/kc_up (Keltner = ATR-based envelope equivalent) as proxy.

Source: elder_alexander_trading_for_a_living, Sec.45 pp.247-251.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "moving_average_channel_percent_envelope_reversion",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h-4h",
    "indicators": "ema13, kc_lo, kc_up, close",
    "long": "Close <= kc_lo (lower Keltner/ATR-envelope band): buy at undervalued extreme",
    "short": "Close >= kc_up (upper Keltner/ATR-envelope band): sell at overvalued extreme",
    "desc": "EMA13 percent-envelope channel reversion: fade closes at band extremes (Keltner as envelope proxy)",
    "source": "elder_alexander_trading_for_a_living Sec.45 pp.247-251",
}


def signal(ind, pos, htf=None):
    """Percent-envelope mean-reversion: close at or beyond Keltner band -> fade."""
    c = ind["close"][pos]
    klo = ind["kc_lo"][pos]
    kup = ind["kc_up"][pos]
    if nan(c, klo, kup):
        return None
    if c <= klo:
        return "long"
    if c >= kup:
        return "short"
    return None
