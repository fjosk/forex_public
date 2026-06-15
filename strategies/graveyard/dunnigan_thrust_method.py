#!/usr/bin/env python3
"""dunnigan_thrust_method -- Dunnigan thrust: closing-price reversal + inside/narrow range + thrust. trading_systems_and_methods_kaufman_perry_j_kaufma.

Pattern: closing-price reversal (new swing low + close > prior close) followed by a thrust (next bar
range > ATR threshold) -> long. Mirror for short. Codeable subset of the full 5-pattern system.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "dunnigan_thrust_method",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "high,low,close,open,atr",
    "long": "closing-price reversal buy: bar[pos-2] makes lower low vs bar[pos-3], bar[pos-2] close > bar[pos-3] close; then bar[pos-1] is inside bar (narrow); current bar breaks above bar[pos-2] high (thrust)",
    "short": "mirror: closing-price reversal sell + inside bar + downward thrust below bar low",
    "desc": "Dunnigan thrust: closing-price reversal (swing-low + up-close) + inside bar + breakout thrust",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma, Ch12 pp.290-292",
}


def signal(ind, pos, htf=None):
    """Dunnigan thrust: reversal candle + inside bar + thrust breakout."""
    if pos < 3:
        return None
    # bar pos-2: the reversal bar
    l2 = ind["low"][pos - 2]
    c2 = ind["close"][pos - 2]
    h2 = ind["high"][pos - 2]
    # bar pos-3: the prior bar (reference for new low/high)
    l3 = ind["low"][pos - 3]
    c3 = ind["close"][pos - 3]
    h3 = ind["high"][pos - 3]
    # bar pos-1: the inside/narrow candidate
    h1 = ind["high"][pos - 1]
    l1 = ind["low"][pos - 1]
    # current bar pos: the thrust
    h = ind["high"][pos]
    l = ind["low"][pos]
    c = ind["close"][pos]
    atr = ind["atr"][pos]
    if nan(l2, c2, h2, l3, c3, h3, h1, l1, h, l, c, atr):
        return None
    # Inside bar at pos-1: both high and low within pos-2 range
    inside = h1 <= h2 and l1 >= l2
    # Closing-price reversal buy: new low at pos-2 AND close above pos-3 close
    cpr_buy = l2 < l3 and c2 > c3
    # Thrust up: current bar close > pos-2 high
    thrust_up = c > h2
    if cpr_buy and inside and thrust_up:
        return "long"
    # Closing-price reversal sell: new high at pos-2 AND close below pos-3 close
    cpr_sell = h2 > h3 and c2 < c3
    # Thrust down: current bar close < pos-2 low
    thrust_dn = c < l2
    if cpr_sell and inside and thrust_dn:
        return "short"
    return None
