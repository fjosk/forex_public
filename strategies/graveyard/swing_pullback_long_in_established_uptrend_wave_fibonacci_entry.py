#!/usr/bin/env python3
"""swing_pullback_long_in_established_uptrend_wave_fibonacci_entry -- Swing pullback to Wave in uptrend: EMA21 rising, low dips into Wave band. thirty_days_of_forex_trading_trades_tactics_and_te.

Uptrend: EMA21 slope rising over 5 bars.
Entry: price pulls back into the Wave band from above (low <= sma_high21 while close still above sma_low21).
Deterministic variant of the Wave pullback: 'price re-touches the upper Wave lines'.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "swing_pullback_long_in_established_uptrend_wave_fibonacci_entry",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "close,ema21,sma_high21,sma_low21",
    "long": "EMA21 rising (uptrend) AND low pulls back to touch the upper Wave band (sma_high21)",
    "short": None,
    "desc": "Wave pullback long: EMA21 slope rising; entry when price dips into the 21-bar high MA band",
    "source": "thirty_days_of_forex_trading_trades_tactics_and_te Introduction Figures I.2 I.11 Four Keys",
}


def signal(ind, pos, htf=None):
    """Swing pullback into Wave band during EMA21 uptrend."""
    if pos < 5:
        return None
    c    = ind["close"][pos]
    lo   = ind["low"][pos]
    e21  = ind["ema21"][pos]
    e21p = ind["ema21"][pos - 5]
    sh21 = ind["sma_high21"][pos]
    sl21 = ind["sma_low21"][pos]
    if nan(c, lo, e21, e21p, sh21, sl21):
        return None
    slope_up = e21 > e21p
    # Only longs in uptrend: price above lower Wave but low dips to upper Wave band
    if slope_up and c > sl21 and lo <= sh21:
        return "long"
    return None
