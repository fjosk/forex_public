#!/usr/bin/env python3
"""momentum_breakout_macd_hist -- Donchian breakout confirmed by MACD histogram above/below zero.
thirty_days_of_forex_trading.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "momentum_breakout_macd_hist",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h-4h",
    "indicators": "dc_up, dc_lo, macd_hist",
    "long": "close breaks above N-bar Donchian high AND MACD histogram > 0",
    "short": "close breaks below N-bar Donchian low AND MACD histogram < 0",
    "desc": "Momentum breakout from Donchian channel confirmed by MACD histogram sign",
    "source": "book: thirty_days_of_forex_trading_trades_tactics_and_te",
}


def signal(ind, pos, htf=None):
    """Donchian breakout with MACD histogram zero-line gate."""
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1] if pos >= 1 else None
    dc_up = ind["dc_up"][pos - 1] if pos >= 1 else None
    dc_lo = ind["dc_lo"][pos - 1] if pos >= 1 else None
    hist = ind["macd_hist"][pos]
    if nan(c, c1, dc_up, dc_lo, hist):
        return None
    if c > dc_up and hist > 0:
        return "long"
    if c < dc_lo and hist < 0:
        return "short"
    return None
