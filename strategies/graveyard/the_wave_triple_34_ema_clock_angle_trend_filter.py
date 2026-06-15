#!/usr/bin/env python3
"""wave_triple_34ema_trend_filter -- Triple 34-EMA clock-angle: slope of EMA21 on close, with sma_high21/sma_low21 channel. thirty_days_of_forex_trading_trades_tactics_and_te.

The Wave = three 34-EMAs on high/close/low. Proxied with EMA21(close) + sma_high21 / sma_low21.
Slope bucket: if EMA21 positive-sloped AND close above EMA21 -> uptrend; if negative AND below -> downtrend.
Standalone signal: fires on regime change (new uptrend or downtrend entry).
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "the_wave_triple_34_ema_clock_angle_trend_filter",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "close,ema21,sma_high21,sma_low21,atr",
    "long": "EMA21 rising AND close above sma_high21 (strong side) -> 12-to-2 Wave uptrend",
    "short": "EMA21 falling AND close below sma_low21 (weak side) -> 4-to-6 Wave downtrend",
    "desc": "Triple 34-EMA Wave (EMA21 proxy): slope + price-side-of-Wave determines trend regime",
    "source": "thirty_days_of_forex_trading_trades_tactics_and_te Introduction Four Keys key 2",
}


def signal(ind, pos, htf=None):
    """Triple Wave: EMA21 slope + close vs channel side -> trend regime signal."""
    if pos < 6:
        return None
    c    = ind["close"][pos]
    e    = ind["ema21"][pos]
    e5   = ind["ema21"][pos - 5]
    e6   = ind["ema21"][pos - 6]
    sh   = ind["sma_high21"][pos]
    sl   = ind["sma_low21"][pos]
    a    = ind["atr"][pos]
    if nan(c, e, e5, e6, sh, sl, a) or a == 0:
        return None
    slope_now  = (e  - e5) / a
    slope_prev = (e5 - e6) / a
    thr = 0.04
    up_now   = slope_now  >  thr and c > sh
    up_prev  = slope_prev >  thr
    dn_now   = slope_now  < -thr and c < sl
    dn_prev  = slope_prev < -thr
    if up_now and not up_prev:
        return "long"
    if dn_now and not dn_prev:
        return "short"
    return None
