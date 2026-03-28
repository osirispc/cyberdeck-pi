#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$HOME/projects/cyberdeck-pi"

echo "==> Applying cyberdeck configs from repo"

mkdir -p "$HOME/.config/alacritty"
mkdir -p "$HOME/.config"

backup_file() {
  local target="$1"
  if [ -f "$target" ]; then
    cp "$target" "${target}.bak.$(date +%Y%m%d-%H%M%S)"
  fi
}

echo "==> Backing up existing tmux config if present"
backup_file "$HOME/.tmux.conf"

echo "==> Backing up existing alacritty config if present"
backup_file "$HOME/.config/alacritty/alacritty.toml"

echo "==> Applying tmux config"
cp "$REPO_DIR/configs/tmux/.tmux.conf" "$HOME/.tmux.conf"

echo "==> Applying alacritty config"
cp "$REPO_DIR/configs/alacritty/alacritty.toml" "$HOME/.config/alacritty/alacritty.toml"

echo "==> Configs applied successfully"
echo "Next:"
echo "  1. restart Alacritty"
echo "  2. run: tmux source-file ~/.tmux.conf"
