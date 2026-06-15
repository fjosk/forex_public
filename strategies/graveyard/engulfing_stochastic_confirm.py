#!/usr/bin/env python3
"""engulfing_stochastic_confirm -- Engulfing candle confirmed by Stochastic overbought/oversold. MQL5 CodeBase 2011.

Price/OHLC only (no volume) -> FX-applicable.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "engulfing_stochastic_confirm",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "1h",
    "indicators": "stoch_d, open, close",
    "long": "bullish engulfing AND stoch_d < 30",
    "short": "bearish engulfing AND stoch_d > 70",
    "desc": "Engulfing reversal pattern confirmed by Stochastic oversold/overbought level",
    "source": "mql5.com/en/code/305 MetaQuotes 2011; mql5.com/en/code/18487 barabashkakvn 2017",
}


def signal(ind, pos, htf=None):
    """Engulfing candle with Stochastic confirmation."""
    if pos < 1:
        return None
    o0 = ind["open"][pos]
    c0 = ind["close"][pos]
    o1 = ind["open"][pos - 1]
    c1 = ind["close"][pos - 1]
    sd = ind["stoch_d"][pos]
    if nan(o0, c0, o1, c1, sd):
        return None
    # bull engulf: prior bearish, current bullish, current opens below prior close, closes above prior open
    bull_engulf = (o1 > c1) and (c0 > o0) and (o0 <= c1) and (c0 >= o1)
    # bear engulf: prior bullish, current bearish, current opens above prior close, closes below prior open
    bear_engulf = (o1 < c1) and (c0 < o0) and (o0 >= c1) and (c0 <= o1)
    if bull_engulf and sd < 30:
        return "long"
    if bear_engulf and sd > 70:
        return "short"
    return None
