#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$HOME/projects/cyberdeck-pi"

echo "==> Cyberdeck bootstrap starting"

if [ ! -d "$REPO_DIR" ]; then
  echo "ERROR: Repo not found at $REPO_DIR"
  exit 1
fi

echo "==> Repairing package state if needed"
sudo dpkg --configure -a || true
sudo apt -f install -y || true

echo "==> Running base install"
"$REPO_DIR/scripts/base-install.sh"

echo "==> Applying saved configs"
"$REPO_DIR/scripts/apply-configs.sh"

echo "==> Ensuring workspace exists"
mkdir -p "$HOME/projects"

echo "==> Trying to set Alacritty as default terminal"
if command -v alacritty >/dev/null 2>&1; then
  ALACRITTY_PATH="$(command -v alacritty)"
  if update-alternatives --list x-terminal-emulator >/dev/null 2>&1; then
    echo "Available terminal alternatives:"
    update-alternatives --list x-terminal-emulator || true
    echo
    echo "If Alacritty is not already default, run:"
    echo "  sudo update-alternatives --config x-terminal-emulator"
  fi
else
  echo "Alacritty not found yet; skipping terminal default hint"
fi

echo
echo "==> Bootstrap complete"
echo "Recommended next steps:"
echo "  1. Close and reopen Alacritty"
echo "  2. Reload tmux with: tmux source-file ~/.tmux.conf"
echo "  3. Reboot if this is a fresh build: sudo reboot"
