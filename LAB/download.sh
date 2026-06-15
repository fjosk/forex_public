#!/usr/bin/env bash
# Thin wrapper around download.py, kept so the FOREX lab is driven the same way as
# sister-lab/LAB (./download.sh). The real work is Python because HistData needs a token
# handshake the histdata package performs; a pure-bash curl (the sister-lab approach) cannot.
#
# All flags pass through to download.py; environment overrides (PAIRS, OUT_ROOT,
# FOREX_START_YEAR, FOREX_SLEEP) work too. Re-runnable: already-downloaded archives are
# skipped, so stop-and-resume costs nothing.
#
# Usage:
#   ./download.sh                     # all 13 HistData FX pairs, full history
#   ./download.sh --pairs eurusd      # one pair
#   PAIRS="eurusd usdjpy" ./download.sh
set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
PY=/home/user/global-venv/bin/python3

exec "$PY" "$HERE/download.py" "$@"
