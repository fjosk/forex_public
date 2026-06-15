#!/usr/bin/env python3
"""trend_vs_range_checklist -- Currency pair checklist: ADX+BB+SMA score >= 2 for trend regime. day_trading_swing_trading_the_currency_market_tech.

Trend: ADX(14)>25, close tags/crosses upper or lower Bollinger band, and/or breaks SMA50/100/200 (count each).
Long entry: score >= 2 AND newly crossed SMA50 to upside (freshest confirming signal).
Short entry: score >= 2 AND newly crossed SMA50 to downside.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "trend_vs_range_regime_classification_checklist_adx_bollinger_sma_rsi_s",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "adx,bb_up,bb_lo,close,sma50,sma100,sma200,rsi,stoch_k",
    "long": "Trend-score>=2 AND close freshly crosses above SMA50",
    "short": "Trend-score>=2 AND close freshly crosses below SMA50",
    "desc": "Daily checklist regime classifier: ADX+BB+SMA count>=2 gates trend-following MA cross signal",
    "source": "day_trading_swing_trading_the_currency_market_tech Ch8 Currency Pair Checklist Table 8.1",
}


def signal(ind, pos, htf=None):
    """Trend-score >= 2 gates an SMA50 cross signal."""
    if pos < 1:
        return None
    c    = ind["close"][pos]
    c1   = ind["close"][pos - 1]
    dx   = ind["adx"][pos]
    bbu  = ind["bb_up"][pos]
    bbl  = ind["bb_lo"][pos]
    s50  = ind["sma50"][pos]
    s501 = ind["sma50"][pos - 1]
    s100 = ind["sma100"][pos]
    s200 = ind["sma200"][pos]
    if nan(c, c1, dx, bbu, bbl, s50, s501, s100, s200):
        return None
    trend_score = (int(dx > 25) + int(c >= bbu or c <= bbl)
                   + int(c > s50) + int(c > s100) + int(c > s200))
    dn_score    = (int(dx > 25) + int(c >= bbu or c <= bbl)
                   + int(c < s50) + int(c < s100) + int(c < s200))
    cross_up = c > s50 and c1 <= s501
    cross_dn = c < s50 and c1 >= s501
    if trend_score >= 2 and cross_up:
        return "long"
    if dn_score >= 2 and cross_dn:
        return "short"
    return None
