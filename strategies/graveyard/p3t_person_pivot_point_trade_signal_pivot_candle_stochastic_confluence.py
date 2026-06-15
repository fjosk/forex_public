#!/usr/bin/env python3
"""p3t_person_pivot_point_trade_signal_pivot_candle_stochastic_confluence -- P3T: price at S1/R1 pivot AND stochastic at extreme with uptick/downtick -> entry. Person.

tier1 multi-timeframe. Price/OHLC only.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "p3t_person_pivot_point_trade_signal_pivot_candle_stochastic_confluence",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h-4h",
    "indicators": "piv_s1, piv_r1, stoch_k, stoch_d, atr, close",
    "long": "Close near S1 pivot (within 0.5 ATR) AND stoch_k < 30 AND stoch_k turning up",
    "short": "Close near R1 pivot (within 0.5 ATR) AND stoch_k > 70 AND stoch_k turning down",
    "desc": "P3T: price at daily pivot support/resistance AND stochastic extreme turning = confluence entry",
    "source": "Person, Complete Guide to Technical Trading Tactics, Ch.6-7 P3T Signals, pp.103-130",
}


def signal(ind, pos, htf=None):
    """Pivot confluence + stochastic extreme reversal."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    s1 = ind["piv_s1"][pos]
    r1 = ind["piv_r1"][pos]
    sk = ind["stoch_k"][pos]
    sk1 = ind["stoch_k"][pos - 1]
    at = ind["atr"][pos]
    if nan(c, s1, r1, sk, sk1, at):
        return None
    band = 0.5 * at
    # Long: price near S1 support AND stoch oversold turning up
    if abs(c - s1) <= band and sk < 30 and sk > sk1:
        return "long"
    # Short: price near R1 resistance AND stoch overbought turning down
    if abs(c - r1) <= band and sk > 70 and sk < sk1:
        return "short"
    return None
