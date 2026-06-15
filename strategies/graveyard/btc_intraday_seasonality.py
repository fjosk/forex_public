#!/usr/bin/env python3
"""btc_intraday_seasonality -- Bitcoin overnight intraday-seasonality long (21:00-23:00 UTC window).. Ported from sister-lab catalog (https://quantpedia.com/strategies/intraday-seasonality-in-bitcoin).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "btc_intraday_seasonality", "cadences": ['day'], "exit": {'sl_atr': 3.0, 'tp_atr': 6.0, 'trail': False, 'time_stop_h': 2, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "seasonality", "tf": "1h (UTC)", "indicators": "UTC hour-of-day, SMA200 direction",
    "long": "Enter long at 21:00 UTC when SMA200 trend up; clock/time-stop exit", "short": "(long-only effect; no short)", "desc": "Bitcoin overnight intraday-seasonality long (21:00-23:00 UTC window).", "source": "sister-lab catalog: https://quantpedia.com/strategies/intraday-seasonality-in-bitcoin",
}


def signal(I, i, htf):
    # Long-only UTC overnight effect (Quantpedia): enter 21:00 UTC, regime-gated by
    # the 200-bar SMA-direction proxy. Exit is the engine time stop (~2 bars at 1h).
    hour, trend = I["hour_utc"][i], I["sma200_dir"][i]
    if _nan(hour, trend):
        return None
    if hour == 21.0 and trend > 0:
        return "long"
    return None
