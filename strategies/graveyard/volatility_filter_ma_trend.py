#!/usr/bin/env python3
"""volatility_filter_ma_trend -- Volatility Filter on Moving-Average Trend System: SMA(50) rising/falling as trend signal, gated by absolute close-to-close change within a mean +/- SD band. Kaufman Ch.20.

Price/OHLC only. No volume.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "volatility_filter_ma_trend",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "sma50, abschg, atr, atr_pct, close",
    "long": "SMA50 rising AND abschg (absolute close change) is above its low-vol floor (> 0) but not spiking",
    "short": "SMA50 falling AND abschg is in the normal volatility band",
    "desc": "MA trend + volatility activity filter: enter trend only when absolute daily change is in the normal activity band (above low floor, below shock ceiling)",
    "source": "trading_systems_and_methods_kaufman -- Ch.20 Volatility Filters / Constructing a Volatility Filter",
}

# The spec filters: enter if change > low_limit (vavg - vsd) AND change < high_limit (vavg + 2*vsd).
# Proxy: use atr_pct as a normalised activity measure; enter when it exceeds 0 (always true) but
# below 3*atr_pct (shock ceiling). Simpler codeable form: require abschg > 0 and < 3*atr to avoid
# quiet or shock bars. abschg = |close - close[1]| precomputed.
_SHOCK_MULT = 3.0


def signal(ind, pos, htf=None):
    """SMA trend with volatility-activity gate: skip quiet and shock bars."""
    if pos < 1:
        return None
    s50 = ind["sma50"][pos]
    s50_1 = ind["sma50"][pos - 1]
    chg = ind["abschg"][pos]
    a = ind["atr"][pos]
    if nan(s50, s50_1, chg, a):
        return None
    # Volatility gate: change must be positive (some activity) but below shock threshold
    in_band = 0 < chg < _SHOCK_MULT * a
    if not in_band:
        return None
    if s50 > s50_1:
        return "long"
    if s50 < s50_1:
        return "short"
    return None
