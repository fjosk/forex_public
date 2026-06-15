#!/usr/bin/env python3
"""stochastic_pullback_trend_swing -- Stochastic oversold pullback in EMA50 trend. Dukascopy."""
from strategies._common import nan, _xup, _xdn, REVERT, ALL_CLASSES

META = {
    "id": "stochastic_pullback_trend_swing",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "daily",
    "indicators": "stoch_k, stoch_d, ema50, close",
    "long": "close above ema50, stoch_k and stoch_d both below 20, K crosses above D",
    "short": "close below ema50, stoch_k and stoch_d both above 80, K crosses below D",
    "desc": "Stochastic pullback in trend: oversold stoch cross in EMA50-defined trend",
    "source": "web:https://www.dukascopy.com/swiss/english/marketwatch/articles/stochastic-oscillator-strategy-traders-guide/",
}


def signal(ind, pos, htf=None):
    """Trend pullback via stochastic: in uptrend, stoch oversold and K crosses above D."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    e50 = ind["ema50"][pos]
    sk0 = ind["stoch_k"][pos]
    sd0 = ind["stoch_d"][pos]
    sk1 = ind["stoch_k"][pos - 1]
    sd1 = ind["stoch_d"][pos - 1]
    if nan(c, e50, sk0, sd0, sk1, sd1):
        return None

    os_zone = sk0 < 20 and sd0 < 20
    k_xup = _xup(sk0, sk1, sd0, sd1)
    if c > e50 and os_zone and k_xup:
        return "long"

    ob_zone = sk0 > 80 and sd0 > 80
    k_xdn = _xdn(sk0, sk1, sd0, sd1)
    if c < e50 and ob_zone and k_xdn:
        return "short"

    return None
