#!/usr/bin/env python3
"""wave_clock_angle_trend_filter -- Raghee Wave 34-EMA clock-angle trend direction. thirty_days_of_forex_trading_trades_tactics_and_te.

The Wave = EMA of close (34-period; proxied with EMA21 as closest available).
Clock angle via slope: EMA21 rising (12-2 o'clock) -> uptrend long; EMA21 falling (4-6) -> downtrend short.
Slope measured over 5 bars, normalised by ATR.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "wave_clock_angle_trend_filter",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ema21,atr",
    "long": "EMA21 slope positive (ATR-normalised) for at least 5 bars -> 12-to-2 o'clock Wave",
    "short": "EMA21 slope negative -> 4-to-6 o'clock Wave",
    "desc": "Raghee Wave clock-angle: EMA21 slope direction as trend regime classifier generating signals",
    "source": "thirty_days_of_forex_trading_trades_tactics_and_te chunk2 Days 16-30",
}


def signal(ind, pos, htf=None):
    """Wave clock-angle: fire on slope sign-change over 5-bar window."""
    if pos < 6:
        return None
    e   = ind["ema21"][pos]
    e5  = ind["ema21"][pos - 5]
    e6  = ind["ema21"][pos - 6]
    a   = ind["atr"][pos]
    if nan(e, e5, e6, a) or a == 0:
        return None
    slope_now  = (e  - e5) / a
    slope_prev = (e5 - e6) / a   # one-bar-earlier slope sign
    threshold  = 0.05            # ATR-normalised slope threshold for 12-2 / 4-6
    in_up_now  = slope_now  >  threshold
    in_dn_now  = slope_now  < -threshold
    in_up_prev = slope_prev >  threshold
    in_dn_prev = slope_prev < -threshold
    # Fire on new entry into the uptrend / downtrend bucket
    if in_up_now and not in_up_prev:
        return "long"
    if in_dn_now and not in_dn_prev:
        return "short"
    return None
