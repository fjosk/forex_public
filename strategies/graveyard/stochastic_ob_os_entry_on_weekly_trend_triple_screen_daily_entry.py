#!/usr/bin/env python3
"""stochastic_ob_os_entry_on_weekly_trend_triple_screen_daily_entry -- Triple-Screen: HTF trend up + daily stoch < 20 = long entry; HTF trend down + daily stoch > 80 = short entry. Elder.

tier1 multi-timeframe. Price/OHLC only.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "stochastic_ob_os_entry_on_weekly_trend_triple_screen_daily_entry",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "stoch_k, ema50",
    "long": "Trend (EMA50) up AND stoch_k < 20 (oversold dip in uptrend)",
    "short": "Trend (EMA50) down AND stoch_k > 80 (overbought rally in downtrend)",
    "desc": "Elder Triple-Screen stochastic entry: trend-filtered stochastic OB/OS zone entry",
    "source": "Elder, Trading for a Living, Sec 30 Stochastic OB/OS rules + Triple Screen, p.160-161",
}


def signal(ind, pos, htf=None):
    """Stochastic extreme entry gated by EMA50 trend direction."""
    if pos < 1:
        return None
    sk = ind["stoch_k"][pos]
    e = ind["ema50"][pos]
    e1 = ind["ema50"][pos - 1]
    if nan(sk, e, e1):
        return None
    trend_up = e > e1
    trend_dn = e < e1
    if trend_up and sk < 20:
        return "long"
    if trend_dn and sk > 80:
        return "short"
    return None
