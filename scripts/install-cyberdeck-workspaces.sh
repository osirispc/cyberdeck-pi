#!/usr/bin/env bash
set -euo pipefail

echo "[CYBERDECK] Installing workspace and keyboard configuration..."

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

LABWC_SRC="$REPO_DIR/configs/labwc/rc.xml"
CYBER_FUNC_SRC="$REPO_DIR/configs/shell/cyber-function.sh"

LABWC_DEST="$HOME/.config/labwc/rc.xml"
BASHRC="$HOME/.bashrc"

timestamp="$(date +%Y%m%d-%H%M%S)"

if [ ! -f "$LABWC_SRC" ]; then
  echo "[ERROR] Missing $LABWC_SRC"
  exit 1
fi

if [ ! -f "$CYBER_FUNC_SRC" ]; then
  echo "[ERROR] Missing $CYBER_FUNC_SRC"
  exit 1
fi

mkdir -p "$HOME/.config/labwc"

if [ -f "$LABWC_DEST" ]; then
  cp "$LABWC_DEST" "$LABWC_DEST.bak-$timestamp"
  echo "[CYBERDECK] Backed up labwc rc.xml"
fi

cp "$LABWC_SRC" "$LABWC_DEST"
echo "[CYBERDECK] Installed labwc rc.xml"

if [ -f "$BASHRC" ]; then
  cp "$BASHRC" "$BASHRC.bak-$timestamp"
  echo "[CYBERDECK] Backed up .bashrc"
else
  touch "$BASHRC"
fi

python3 <<PY
from pathlib import Path
import re

bashrc = Path("$BASHRC")
func = Path("$CYBER_FUNC_SRC").read_text()
text = bashrc.read_text()

text = re.sub(
    r'\\n?# Cyberdeck command helper\\n.*?\\n# End cyberdeck command helper\\n?',
    '\\n',
    text,
    flags=re.DOTALL
)

text = re.sub(
    r'\\n?cyber\\s*\\(\\)\\s*\\{.*?\\n\\}\\n?',
    '\\n',
    text,
    flags=re.DOTALL
)

wrapped = "\\n# Cyberdeck command helper\\n" + func.rstrip() + "\\n# End cyberdeck command helper\\n"
bashrc.write_text(text.rstrip() + wrapped + "\\n")
PY

echo "[CYBERDECK] Installed cyber shell function"
echo
echo "[CYBERDECK] Reload shell:"
echo "  source ~/.bashrc"
echo
echo "[CYBERDECK] Reload labwc:"
echo "  labwc --reconfigure"
echo
echo "[CYBERDECK] Test:"
echo "  cyber help"
echo "  cyber keys"
