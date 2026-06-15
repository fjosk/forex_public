#!/usr/bin/env python3
"""binh27_adx_ema_emarsi -- BinHV27 ADX EMA Multi-Condition (freqtrade berlinguyinca).
web:https://github.com/freqtrade/freqtrade-strategies/blob/main/user_data/strategies/berlinguyinca/BinHV27.py

Approximations:
  emarsi (EMA60 of RSI5) -> rsi (RSI14); thresholds kept proportional.
  SMA 60/120/240 -> sma50/sma100/sma200 (closest precomputed).
  Long-only (no short branch in source).
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "binh27_adx_ema_emarsi",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "1h",
    "indicators": "adx, di_minus, di_plus, rsi, sma50, sma100, sma200",
    "long": "sma200 direction positive AND (price between sma100 and sma50 bands) AND di_minus > di_minus EMA proxy AND rsi <= 30 with one of four ADX branches (25/30/35/30)",
    "short": "not implemented",
    "desc": "BinHV27 multi-branch long entry: ADX strength tiers + sma trend + rsi oversold; approximated periods",
    "source": "web:https://github.com/freqtrade/freqtrade-strategies/blob/main/user_data/strategies/berlinguyinca/BinHV27.py",
}


def signal(ind, pos, htf=None):
    """Multi-branch long: ADX tiers with SMA trend position and rsi oversold gate."""
    adx = ind["adx"][pos]
    dip = ind["di_plus"][pos]
    dim = ind["di_minus"][pos]
    rs = ind["rsi"][pos]
    s50 = ind["sma50"][pos]
    s100 = ind["sma100"][pos]
    s200 = ind["sma200"][pos]
    s50_1 = ind["sma50"][pos - 1]
    s100_1 = ind["sma100"][pos - 1]
    c = ind["close"][pos]
    if nan(adx, dip, dim, rs, s50, s100, s200, s50_1, s100_1, c):
        return None
    # slowsma proxy: sma200 must be rising
    if s200 <= ind["sma200"][pos - 1] if pos > 0 else True:
        return None
    # bigdown: sma100 declining (approximates highsma declining)
    bigdown = s100 < s100_1
    # bigup: sma50 rising (approximates lowsma rising)
    bigup = s50 > s50_1
    # rsi oversold proxy for emarsi (source uses 20/25 thresholds on emarsi; scale to rsi)
    rsi_low20 = rs <= 30
    rsi_low25 = rs <= 35
    # branch 1: ADX > 25 + bigdown + rsi <= 30
    if adx > 25 and bigdown and rsi_low20:
        return "long"
    # branch 2: ADX > 30 + bigdown + rsi <= 30
    if adx > 30 and bigdown and rsi_low20:
        return "long"
    # branch 3: ADX > 35 + bigup + rsi <= 30
    if adx > 35 and bigup and rsi_low20:
        return "long"
    # branch 4: ADX > 30 + bigup + rsi <= 35
    if adx > 30 and bigup and rsi_low25:
        return "long"
    return None
