#!/usr/bin/env python3
"""atr_volatility_regime_filter -- ATR/BB-width volatility regime filter. AlgoTrader Substack.

bbw_pct < 25 (low-vol regime) -> mean reversion via RSI extremes.
bbw_pct > 75 (high-vol regime) -> trend-follow via ema50/sma200 direction.
Source: web:https://algotr.substack.com/p/stop-leaving-money-on-the-table-a
"""
from strategies._common import nan, REVERT, TREND, ALL_CLASSES

META = {
    "id": "atr_volatility_regime_filter",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "4h",
    "indicators": "bbw_pct, bb_width, atr_pct, atr, bb_pctb, rsi, ema50, sma200, close",
    "long": "low-vol (bbw_pct<25): RSI<30 or bb_pctb<0; high-vol (bbw_pct>75): close>sma200 and ema50>sma200",
    "short": "low-vol: RSI>70 or bb_pctb>1; high-vol: close<sma200 and ema50<sma200",
    "desc": "ATR/BB volatility regime switch: mean reversion in squeeze, trend-follow in expansion",
    "source": "web:https://algotr.substack.com/p/stop-leaving-money-on-the-table-a",
}

_LOW_VOL = 25.0
_HIGH_VOL = 75.0


def signal(ind, pos, htf=None):
    """Volatility regime gate: bbw_pct drives mode; RSI in squeeze, ema trend in expansion."""
    bbwp = ind["bbw_pct"][pos]
    bbpb = ind["bb_pctb"][pos]
    rsi = ind["rsi"][pos]
    e50 = ind["ema50"][pos]
    s200 = ind["sma200"][pos]
    c = ind["close"][pos]
    if nan(bbwp, bbpb, rsi, e50, s200, c):
        return None

    if bbwp < _LOW_VOL:
        # Low vol: fade RSI / bb extremes
        if rsi < 30 or bbpb < 0.0:
            return "long"
        if rsi > 70 or bbpb > 1.0:
            return "short"
    elif bbwp > _HIGH_VOL:
        # High vol: ride the trend
        if c > s200 and e50 > s200:
            return "long"
        if c < s200 and e50 < s200:
            return "short"

    return None
