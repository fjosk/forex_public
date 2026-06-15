#!/usr/bin/env python3
"""settlement_price_reversal_bar -- Bar in trend direction but closing against trend. j_person_a_complete_guide_to_technical_trading_tac.

Settlement reversal: bar makes higher high AND higher low vs prior (moving with uptrend) BUT
closes below prior close. Signals weakness / reversal. Mirror for downtrend: lower high AND
lower low but closes above prior close. Trend context via EMA50.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "settlement_price_reversal_bar",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h-1d",
    "indicators": "high,low,close,ema50",
    "long": "Lower high AND lower low vs prior (downtrend move) BUT close > prior close; prior downtrend (close<ema50)",
    "short": "Higher high AND higher low vs prior (uptrend move) BUT close < prior close; prior uptrend (close>ema50)",
    "desc": "Settlement price reversal bar: bar extends the trend in range but closes against it",
    "source": "book:j_person_a_complete_guide_to_technical_trading_tac",
}


def signal(ind, pos, htf=None):
    """Settlement reversal bar: range extends trend but close reverses."""
    if pos < 1:
        return None
    h   = ind["high"]
    lo  = ind["low"]
    c   = ind["close"]
    ema = ind["ema50"][pos]
    if nan(h[pos], lo[pos], c[pos], h[pos-1], lo[pos-1], c[pos-1], ema):
        return None

    # Bearish settlement reversal: uptrend, higher high+low but close below prior
    if (c[pos] > ema and
            h[pos] > h[pos-1] and
            lo[pos] > lo[pos-1] and
            c[pos] < c[pos-1]):
        return "short"

    # Bullish settlement reversal: downtrend, lower high+low but close above prior
    if (c[pos] < ema and
            h[pos] < h[pos-1] and
            lo[pos] < lo[pos-1] and
            c[pos] > c[pos-1]):
        return "long"

    return None
