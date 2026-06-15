#!/usr/bin/env python3
"""
Shared helpers + exit presets for the modular FX strategy library.

Every strategy module under strategies/<lifecycle>/<ID>.py imports what it needs from here so the
modules stay small and self-contained while the NaN-guard and the ATR-exit archetypes are defined
ONCE. PURE: no I/O, no state.
"""

__all__ = ["nan", "_nan", "_xup", "_xdn",
           "TREND", "TREND_FLIP", "REVERT", "BREAK", "B1_EXIT", "QQE_EXIT", "ALL_CLASSES"]


def nan(*xs):
    """True if any value is None or NaN (NaN != NaN). The standard signal-guard for missing
    indicator warm-up bars."""
    for x in xs:
        if x is None or x != x:
            return True
    return False


# Book-extracted modules (tier2, ingested from sister-lab/LAB/backtest/catalog_books.py) call the
# helpers under these EXACT names, so they are provided verbatim -- the function bodies are imported
# zero-edit (renaming 110 bodies would be pure transcription risk). _nan is the same guard as nan.
_nan = nan


def _xup(a, a1, b, b1):
    """a crosses ABOVE b between bar i-1 and i."""
    return a > b and a1 <= b1


def _xdn(a, a1, b, b1):
    """a crosses BELOW b between bar i-1 and i."""
    return a < b and a1 >= b1


# ATR-exit archetypes (mirror sister-lab/LAB/backtest/catalog.py so behaviour ports cleanly). The engine
# NEVER overrides a strategy's exit; it merges the module's exit dict over engine.DEFAULT_EXIT.
#   sl_atr / tp_atr        stop + target distance in ATR multiples
#   trail / chand_mult     chandelier trailing stop (after trail_activate_r R of profit)
#   time_stop_h            hard time stop in hours; exit_opposite flips on an opposing signal
TREND = {"sl_atr": 2.0, "tp_atr": 4.0, "trail": True, "chand_mult": 3.0,
         "trail_activate_r": 1.0, "time_stop_h": 48, "exit_opposite": False}
TREND_FLIP = {"sl_atr": 2.0, "tp_atr": 4.0, "trail": True, "chand_mult": 3.0,
              "trail_activate_r": 1.0, "time_stop_h": 48, "exit_opposite": True}   # trend + flip on opposite signal
REVERT = {"sl_atr": 1.5, "tp_atr": 2.0, "trail": True, "chand_mult": 3.0,
          "trail_activate_r": 1.0, "time_stop_h": 24, "exit_opposite": False}
BREAK = {"sl_atr": 2.0, "tp_atr": 4.0, "trail": True, "chand_mult": 3.0,
         "trail_activate_r": 1.0, "time_stop_h": 36, "exit_opposite": False}
B1_EXIT = {**REVERT}                       # B1's tuned exit (sl 1.5, tp 2.0, 24h) == REVERT archetype
QQE_EXIT = {**TREND, "tp_atr": 3.0}        # QQE's tuned exit (sl 2.0, tp 3.0, 48h)

# Asset-class scope tag (documentation only -- the engine picks the real Ostium spread per traded
# PAIR via shared/instruments.cost_class, so this does not gate which pairs run).
ALL_CLASSES = ["major", "cross", "commodity", "exotic"]
