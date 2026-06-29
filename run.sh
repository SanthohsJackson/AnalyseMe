#!/usr/bin/env bash
# Launch the Analyse Me UI using the project's own venv,
# regardless of what `python3` resolves to in the current shell.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PY="$SCRIPT_DIR/.venv/bin/python"

if [[ ! -x "$VENV_PY" ]]; then
    echo "[run.sh] No venv found at $SCRIPT_DIR/.venv"
    echo "[run.sh] Creating it with Python 3.11..."
    python3.11 -m venv "$SCRIPT_DIR/.venv"
    "$VENV_PY" -m pip install --upgrade pip >/dev/null
    "$VENV_PY" -m pip install -r "$SCRIPT_DIR/requirements.txt"
fi

# Default to the startup menu (analyse vs chat); pass through any args
# (e.g. `./run.sh analyse`, `./run.sh chat --provider openai`)
exec "$VENV_PY" "$SCRIPT_DIR/main.py" "${@:-menu}"
