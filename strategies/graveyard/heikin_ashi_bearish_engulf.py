#!/usr/bin/env python3
"""heikin_ashi_bearish_engulf -- Heikin-Ashi bearish selling-climax reversal. je-suis-tm quant-trading.

HA candles used for pattern; no volume -> FX-applicable.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "heikin_ashi_bearish_engulf",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "1d",
    "indicators": "ha_open, ha_close, high",
    "long": "current HA bearish (open>close), opens at high (no upper wick), body > prior, prior also bearish",
    "short": "mirror: HA bullish candle at its low with growing body",
    "desc": "Heikin-Ashi selling climax reversal: growing full-body red candle signals exhaustion long",
    "source": "github.com/je-suis-tm/quant-trading Heikin-Ashi backtest.py",
}


def signal(ind, pos, htf=None):
    """HA bearish engulfing reversal: growing full-red HA candle -> long (selling climax)."""
    if pos < 1:
        return None
    hao = ind["ha_open"][pos]
    hac = ind["ha_close"][pos]
    hao1 = ind["ha_open"][pos - 1]
    hac1 = ind["ha_close"][pos - 1]
    hi = ind["high"][pos]
    lo = ind["low"][pos]
    if nan(hao, hac, hao1, hac1, hi, lo):
        return None
    # HA high = max(ha_open, ha_close, real high); HA low = min(ha_open, ha_close, real low)
    ha_hi = max(hao, hac, hi)
    ha_lo = min(hao, hac, lo)
    hi1 = ind["high"][pos - 1]
    lo1 = ind["low"][pos - 1]
    if nan(hi1, lo1):
        return None
    ha_lo1 = min(hao1, hac1, lo1)

    body0 = abs(hao - hac)
    body1 = abs(hao1 - hac1)

    # Long: current HA bearish (open>close), no upper wick (opens at high), growing body, prior also bearish
    curr_bear = hao > hac
    no_upper_wick = abs(hao - ha_hi) < 1e-8
    growing_body = body0 > body1
    prior_bear = hao1 > hac1
    if curr_bear and no_upper_wick and growing_body and prior_bear:
        return "long"

    # Short: current HA bullish (close>open), no lower wick (opens at low), growing body, prior also bullish
    curr_bull = hac > hao
    no_lower_wick = abs(hao - ha_lo) < 1e-8
    prior_bull = hac1 > hao1
    if curr_bull and no_lower_wick and growing_body and prior_bull:
        return "short"

    return None
