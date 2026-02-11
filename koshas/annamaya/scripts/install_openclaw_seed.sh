#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

python3 -m pip install --user --quiet rich >/dev/null 2>&1 || true

mkdir -p "$HOME/.local/bin"
ln -sf "$SCRIPT_DIR/openclaw_seed.py" "$HOME/.local/bin/openclaw-seed"
chmod +x "$SCRIPT_DIR/openclaw_seed.py" "$HOME/.local/bin/openclaw-seed"

echo "Installed: $HOME/.local/bin/openclaw-seed"
echo "If needed, add this to your shell PATH:"
echo "  export PATH=\"$HOME/.local/bin:\$PATH\""
