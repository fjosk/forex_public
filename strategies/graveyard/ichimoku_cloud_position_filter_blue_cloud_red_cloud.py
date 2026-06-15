#!/usr/bin/env python3
"""ichimoku_cloud_position_filter_blue_cloud_red_cloud -- Ichimoku cloud color filter: long in blue cloud (SpanA > SpanB), avoid/short red cloud. buku_panduan."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "ichimoku_cloud_position_filter_blue_cloud_red_cloud",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "ich_a, ich_b, close",
    "long": "Cloud is bullish (SpanA > SpanB) and price enters or is above the cloud",
    "short": "Cloud is bearish (SpanA < SpanB) and price is below the cloud",
    "desc": "Ichimoku cloud position filter: blue cloud = long bias, red cloud = short/avoid",
    "source": "book:buku_panduan Sec 10.6 p.57",
}


def signal(ind, pos, htf=None):
    """Ichimoku Blue/Red Cloud position filter."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    span_a = ind["ich_a"][pos]
    span_b = ind["ich_b"][pos]
    if nan(c, span_a, span_b):
        return None
    cloud_top = max(span_a, span_b)
    cloud_bot = min(span_a, span_b)
    bullish_cloud = span_a > span_b
    bearish_cloud = span_a < span_b
    # Long: blue cloud and price at or above cloud bottom (inside or above)
    if bullish_cloud and c >= cloud_bot:
        return "long"
    # Short: red cloud and price at or below cloud top (inside or below)
    if bearish_cloud and c <= cloud_top:
        return "short"
    return None
