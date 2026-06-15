#!/usr/bin/env python3
"""supply_demand_zone_swing -- Supply/demand zone swing using fractal proxies with reversal candle. web:purefinancialacademy.com."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "supply_demand_zone_swing",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "frac_dn_px, frac_dn_bar_high, frac_up_px, frac_up_bar_low, close, open, low, high",
    "long": "price returns to fractal demand zone (frac_dn_px to frac_dn_bar_high) with bullish candle",
    "short": "price returns to fractal supply zone (frac_up_bar_low to frac_up_px) with bearish candle",
    "desc": "Supply/demand zone reversal using fractal proxies with bullish/bearish candle confirmation",
    "source": "web:https://www.purefinancialacademy.com/blog/swing-trading-strategy-with-supply-demand-zones-pfa",
}


def signal(ind, pos, htf=None):
    """Return to fractal demand/supply zone with candle confirmation."""
    fdn_px = ind["frac_dn_px"][pos]
    fdn_bh = ind["frac_dn_bar_high"][pos]
    fup_px = ind["frac_up_px"][pos]
    fup_bl = ind["frac_up_bar_low"][pos]
    c, o = ind["close"][pos], ind["open"][pos]
    if nan(fdn_px, fdn_bh, fup_px, fup_bl, c, o):
        return None
    # Demand zone: frac_dn_px (low) to frac_dn_bar_high (high of fractal bar)
    in_demand = fdn_px <= c <= fdn_bh if fdn_bh > fdn_px else False
    bull_candle = c > o
    if in_demand and bull_candle:
        return "long"
    # Supply zone: frac_up_bar_low (low of fractal bar) to frac_up_px (high)
    in_supply = fup_bl <= c <= fup_px if fup_px > fup_bl else False
    bear_candle = c < o
    if in_supply and bear_candle:
        return "short"
    return None
