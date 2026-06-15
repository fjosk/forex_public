#!/usr/bin/env python3
"""e0v1en_rsi_sma_cti -- E0V1E RSI SMA CTI Dip. freqtrade ssssi E0V1E.py."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "e0v1en_rsi_sma_cti",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h",
    "indicators": "rsi, rsi2, sma10, cci",
    "long": "RSI slow declining, rsi2 < 40, rsi > 42, close < sma10*0.973, cci < 100",
    "short": "not implemented",
    "desc": "E0V1E two-tier dip-buy: slow RSI declining + fast RSI oversold + below SMA discount + CCI filter",
    "source": "github.com/ssssi/freqtrade_strs E0V1E.py",
}

# RSI-slow (20-period) approximated by rsi; rsi_fast (4-period) by rsi2 (closest available).
# CTI (Correlation Trend Indicator) approximated by cci with threshold 100 (neutral zone).
# sma15 approximated by sma10 (closest available).


def signal(ind, pos, htf=None):
    """Two-tier dip entry: RSI slow declining, fast oversold, below SMA, CCI subdued."""
    c = ind["close"][pos]
    r = ind["rsi"][pos]       # rsi14 -> stands in for rsi_slow(20) + rsi14
    r1 = ind["rsi"][pos - 1]
    r2 = ind["rsi2"][pos]    # rsi2 as rsi_fast proxy
    s10 = ind["sma10"][pos]  # sma10 as sma15 proxy
    cci_v = ind["cci"][pos]
    if nan(c, r, r1, r2, s10, cci_v):
        return None
    rsi_declining = r < r1
    buy_1 = (rsi_declining and r2 < 40 and r > 42
             and c < s10 * 0.973 and cci_v < 100)
    buy_new = (rsi_declining and r2 < 34 and r > 28
               and c < s10 * 0.96 and cci_v < 100)
    if buy_1 or buy_new:
        return "long"
    return None
