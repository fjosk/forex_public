"""Canonical FOREX-lab filesystem paths, derived from this file's location (no hardcoded
absolutes). Ported from sister-lab/LAB/backtest/paths.py and re-rooted at the FOREX lab. Import
these instead of re-hardcoding paths in engine/tools."""
from __future__ import annotations

from pathlib import Path

BACKTEST = Path(__file__).resolve().parent          # .../FOREX/LAB/backtest
LAB_ROOT = BACKTEST.parent                          # .../FOREX/LAB
FOREX_ROOT = LAB_ROOT.parent                        # .../FOREX

UNIFIED = LAB_ROOT / "parquet" / "unified"          # single source of truth: unified OHLCV
BTRES = BACKTEST / "BTRES"                           # sweep/gate/WFO/stress JSON outputs
REGISTRY = BACKTEST / "strategy_registry.json"
GAUNTLET = BACKTEST / "GAUNTLET.md"
# FOREX has NO funding-rate files (FX/commodity carry is modelled in costs.py holding_bps).
# Kept as a (non-existent) path so engine code that probes it degrades gracefully to "no funding".
FUNDING_DIR = LAB_ROOT / "data" / "_no_funding_for_forex"
