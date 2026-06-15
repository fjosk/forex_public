#!/usr/bin/env python3
"""oscillator_retracement_entry_trend_pullback_to_extreme -- In a trend, wait for an oscillator
(RSI) pullback to extreme, then enter when price reclaims the prior fractal swing level.

Source: trade_your_way_to_financial_freedom_mabroke_blogsp, Ch.8.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "oscillator_retracement_entry_trend_pullback_to_extreme",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h-4h",
    "indicators": "rsi, sma50, close, frac_up_px, frac_dn_px",
    "long": "Uptrend (close > sma50): RSI dipped below 35 within last 5 bars; close now reclaims recent fractal high (frac_up_px)",
    "short": "Downtrend (close < sma50): RSI spiked above 65 within last 5 bars; close now breaks below recent fractal low (frac_dn_px)",
    "desc": "Trend pullback to oscillator extreme then reclaim of prior swing level: tight-stop with-trend re-entry",
    "source": "trade_your_way_to_financial_freedom_mabroke_blogsp Ch.8",
}

_LOOK = 5   # bars to look back for the oscillator extreme
_OB = 65    # overbought threshold
_OS = 35    # oversold threshold


def signal(ind, pos, htf=None):
    """With-trend re-entry: RSI extreme within lookback + price reclaims fractal swing."""
    if pos < _LOOK:
        return None
    c = ind["close"][pos]
    s50 = ind["sma50"][pos]
    frac_hi = ind["frac_up_px"][pos]
    frac_lo = ind["frac_dn_px"][pos]
    if nan(c, s50, frac_hi, frac_lo):
        return None

    # long: uptrend + recent RSI oversold + price reclaims fractal high
    if c > s50:
        rsi_dipped = any(
            not nan(ind["rsi"][pos - k]) and ind["rsi"][pos - k] < _OS
            for k in range(1, _LOOK + 1)
        )
        if rsi_dipped and c >= frac_hi and frac_hi > 0:
            return "long"

    # short: downtrend + recent RSI overbought + price breaks below fractal low
    if c < s50:
        rsi_spiked = any(
            not nan(ind["rsi"][pos - k]) and ind["rsi"][pos - k] > _OB
            for k in range(1, _LOOK + 1)
        )
        if rsi_spiked and c <= frac_lo and frac_lo > 0:
            return "short"

    return None
