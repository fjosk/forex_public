#!/usr/bin/env python3
"""breakout_entry_new_high_low_consolidation -- Classic Donchian channel breakout on N-bar high/low. the_new_market_wizards."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "breakout_entry_new_high_low_or_consolidation_break",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d-4h",
    "indicators": "dc_up, dc_lo, close",
    "long": "close moves beyond a previous high (above Donchian upper)",
    "short": "close falls below a previous low (below Donchian lower)",
    "desc": "Breakout entry on new high/low or consolidation break per Market Wizards glossary",
    "source": "the_new_market_wizards",
}


def signal(ind, pos, htf=None):
    """Donchian N-bar breakout: long on new high, short on new low."""
    if pos < 2:
        return None
    c = ind["close"][pos]
    dc_up = ind["dc_up"][pos - 1]
    dc_lo = ind["dc_lo"][pos - 1]
    if nan(c, dc_up, dc_lo):
        return None
    if c > dc_up:
        return "long"
    if c < dc_lo:
        return "short"
    return None
