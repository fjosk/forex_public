#!/usr/bin/env python3
"""bandtastic_bb_outer -- Long-only: close below lower BB with RSI < 52 confirms entry. freqtrade Bandtastic."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "bandtastic_bb_outer",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h",
    "indicators": "bb_lo, bb_up, rsi, bb_width",
    "long": "close < bb_lo AND rsi < 52 (oversold below lower band)",
    "short": "close > bb_up AND rsi > 55 (proxy for the sell exit; adds short-side symmetry)",
    "desc": "Bandtastic BB outer band: long on lower band touch + RSI filter; freqtrade community",
    "source": "web:https://github.com/freqtrade/freqtrade-strategies/blob/main/user_data/strategies/Bandtastic.py",
}

# NOTE: original strategy is long-only; the short side added here mirrors the exit logic
# symmetrically (overbought above upper band) for a balanced two-sided signal module.
_RSI_LONG = 52
_RSI_SHORT = 55


def signal(ind, pos, htf=None):
    """Below lower BB + RSI < 52 = long; above upper BB + RSI > 55 = short."""
    c = ind["close"][pos]
    bb_lo = ind["bb_lo"][pos]
    bb_up = ind["bb_up"][pos]
    rsi = ind["rsi"][pos]
    if nan(c, bb_lo, bb_up, rsi):
        return None
    if c < bb_lo and rsi < _RSI_LONG:
        return "long"
    if c > bb_up and rsi > _RSI_SHORT:
        return "short"
    return None
