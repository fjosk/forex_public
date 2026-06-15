#!/usr/bin/env python3
"""the_fader_false_breakout_fade_of_previous_day_high_low -- The Fader: in a low-ADX environment,
a false break of prior-day high/low reverses; enter in the opposite direction.

Source: day_trading_swing_trading_the_currency_market_tech, Ch.9 pp.129-132.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "the_fader_false_breakout_fade_of_previous_day_high_low",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h-4h",
    "indicators": "adx, close, prev_dhh, prev_dll, atr",
    "long": "ADX < 35 AND price broke below prev_dll (>0.1*ATR) AND now close > prev_dll (false break confirmed, fade long)",
    "short": "ADX < 35 AND price broke above prev_dhh (>0.1*ATR) AND now close < prev_dhh (false break confirmed, fade short)",
    "desc": "The Fader: false breakout of prior-day high/low in weak-trend (ADX<35) -> fade back inside range",
    "source": "day_trading_swing_trading_the_currency_market_tech Ch.9 pp.129-132",
}

_ADX_MAX = 35.0


def signal(ind, pos, htf=None):
    """Fader: prior-day range false break then re-entry -> fade signal."""
    if pos < 1:
        return None
    adx = ind["adx"][pos]
    c = ind["close"][pos]
    pdh = ind["prev_dhh"][pos]
    pdl = ind["prev_dll"][pos]
    a = ind["atr"][pos]
    lo = ind["low"][pos]
    hi = ind["high"][pos]
    if nan(adx, c, pdh, pdl, a, lo, hi) or a <= 0 or pdh <= pdl:
        return None
    if adx >= _ADX_MAX:
        return None
    min_break = 0.10 * a
    # false break down: bar's low pierced below prev_dll but close is back above prev_dll
    if lo < pdl - min_break and c > pdl:
        return "long"
    # false break up: bar's high pierced above prev_dhh but close is back below prev_dhh
    if hi > pdh + min_break and c < pdh:
        return "short"
    return None
