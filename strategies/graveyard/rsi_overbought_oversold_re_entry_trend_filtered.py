#!/usr/bin/env python3
"""rsi_overbought_oversold_re_entry_trend_filtered -- RSI 7-period re-entry on cross back through 30/70, filtered by HTF trend direction. elder_alexander_trading_for_a_living Sec31."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi_overbought_oversold_re_entry_trend_filtered",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h-4h",
    "indicators": "rsi,ema50 (HTF bias via htf arg)",
    "long": "RSI crosses back above 30 (was below) AND weekly trend up (htf bias +1)",
    "short": "RSI crosses back below 70 (was above) AND weekly trend down (htf bias -1)",
    "desc": "Elder RSI re-entry: buy pullback cross-back above 30 in uptrend; sell rally cross-back below 70 in downtrend",
    "source": "book: elder_alexander_trading_for_a_living, Sec31",
}

OB = 70.0
OS = 30.0


def signal(ind, pos, htf=None):
    """RSI cross-back through 30/70 gated on HTF trend bias."""
    if pos < 1:
        return None
    rs = ind["rsi"][pos]
    rs1 = ind["rsi"][pos - 1]
    if nan(rs, rs1):
        return None
    # Determine HTF trend
    if htf is not None:
        bias = htf["bias"][pos] if not nan(htf["bias"][pos]) else 0
    else:
        # Fallback: close vs ema50
        c = ind["close"][pos]
        e = ind["ema50"][pos]
        if nan(c, e):
            return None
        bias = 1 if c > e else -1
    if bias > 0 and rs1 < OS and rs >= OS:
        return "long"
    if bias < 0 and rs1 > OB and rs <= OB:
        return "short"
    return None
