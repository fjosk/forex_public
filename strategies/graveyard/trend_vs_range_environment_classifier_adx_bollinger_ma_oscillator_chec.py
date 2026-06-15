#!/usr/bin/env python3
"""trend_vs_range_adx_bb_ma -- ADX/Bollinger/SMA trend-score classifier with direction signal. day_trading_swing_trading_the_currency_market_tech.

Trend-score: ADX>25 + close tags BB band + close crosses SMA50/100/200 (count).
Long in trending regime when score >= 2 AND close above SMAs (uptrend side).
Short in trending regime when score >= 2 AND close below SMAs (downtrend side).
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "trend_vs_range_environment_classifier_adx_bollinger_ma_oscillator_chec",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "adx,bb_up,bb_lo,close,sma50,sma100,sma200",
    "long": "Trend-score>=2 (ADX>25, close>=upperBB, close>SMA50/100/200 each count) AND close above all SMAs",
    "short": "Trend-score>=2 AND close below all SMAs",
    "desc": "Trend/range regime classifier: ADX+BB+MA score >= 2 gates trend signals in direction of price vs MAs",
    "source": "day_trading_swing_trading_the_currency_market_tech Ch8 Tables 8.1,8.2 pp93-103",
}


def signal(ind, pos, htf=None):
    """Trend-score >= 2 AND directional MA alignment -> trend signal."""
    if pos < 1:
        return None
    c    = ind["close"][pos]
    c1   = ind["close"][pos - 1]
    dx   = ind["adx"][pos]
    bbu  = ind["bb_up"][pos]
    bbl  = ind["bb_lo"][pos]
    s50  = ind["sma50"][pos]
    s100 = ind["sma100"][pos]
    s200 = ind["sma200"][pos]
    if nan(c, c1, dx, bbu, bbl, s50, s100, s200):
        return None
    score = int(dx > 25) + int(c >= bbu or c <= bbl) + int(c > s50) + int(c > s100) + int(c > s200)
    score_dn = int(dx > 25) + int(c >= bbu or c <= bbl) + int(c < s50) + int(c < s100) + int(c < s200)
    if score >= 2 and c > s50 and c > s100 and c > c1:
        return "long"
    if score_dn >= 2 and c < s50 and c < s100 and c < c1:
        return "short"
    return None
