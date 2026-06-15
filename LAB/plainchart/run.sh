#!/usr/bin/env bash
# Launch the FOREX plain chart dashboard.
# FOREX port convention: base 9500, +10 per service (9500/9510/9520 ...), chosen far from
# sister-lab (91xx) and BINARYOPTION (84xx/92xx). Bind = Tailscale interface ONLY (127.0.0.1).
# Defaults (port 9500, host 127.0.0.1) live in app.py; pass --port/--host to override.
exec /home/user/global-venv/bin/python3 "$(cd "$(dirname "$0")" && pwd)/app.py" "$@"
