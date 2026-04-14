#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
pip install -e . >/dev/null

export TWENTY20_FOCUS_SECONDS=30
export TWENTY20_BREAK_SECONDS=20

exec twenty20-beeper
