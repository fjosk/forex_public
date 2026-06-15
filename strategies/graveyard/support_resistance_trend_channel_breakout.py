#!/usr/bin/env python3
"""support_resistance_trend_channel_breakout -- Donchian-channel SR breakout: close breaks above
20-bar high (resistance) to go long, below 20-bar low (support) to go short.
Currency Strategy, Ch.4, pp.87-92."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "support_resistance_trend_channel_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h-1d",
    "indicators": "dc_up,dc_lo,close",
    "long": "close > 20-bar Donchian upper (prior swing high / resistance)",
    "short": "close < 20-bar Donchian lower (prior swing low / support)",
    "desc": "Horizontal SR via Donchian 20-bar channel breakout; resistance clusters stop orders above",
    "source": "Currency Strategy, Ch.4 sec 4.3.1-4.3.2, pp.87-92",
}


def signal(ind, pos, htf=None):
    """Donchian SR breakout: close exceeds prior 20-bar high/low."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    # dc_up/dc_lo are the N-bar highest high / lowest low (prior bars, not including current)
    r = ind["dc_up"][pos]
    s = ind["dc_lo"][pos]
    if nan(c, r, s):
        return None
    if c > r:
        return "long"
    if c < s:
        return "short"
    return None
