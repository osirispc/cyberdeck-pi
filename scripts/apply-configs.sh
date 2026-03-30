#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="${HOME}/projects/cyberdeck-pi"

echo "==> Applying cyberdeck configs from: ${REPO_DIR}"

if [ ! -d "${REPO_DIR}" ]; then
    echo "ERROR: Repo not found at ${REPO_DIR}"
    exit 1
fi

mkdir -p "${HOME}/.config/alacritty"
mkdir -p "${HOME}/.config/tmux"
mkdir -p "${HOME}/.config/cyberdeck"

# Backup existing tmux config
if [ -f "${HOME}/.tmux.conf" ]; then
    cp "${HOME}/.tmux.conf" "${HOME}/.tmux.conf.bak.$(date +%F-%H%M%S)"
    echo "Backed up existing ~/.tmux.conf"
fi

# Backup existing bash config
if [ -f "${HOME}/.bashrc" ]; then
    cp "${HOME}/.bashrc" "${HOME}/.bashrc.bak.$(date +%F-%H%M%S)"
    echo "Backed up existing ~/.bashrc"
fi

# Backup existing alacritty config if present
if [ -f "${HOME}/.config/alacritty/alacritty.toml" ]; then
    cp "${HOME}/.config/alacritty/alacritty.toml" \
       "${HOME}/.config/alacritty/alacritty.toml.bak.$(date +%F-%H%M%S)"
    echo "Backed up existing alacritty config"
fi

# Apply tmux config
if [ -f "${REPO_DIR}/configs/tmux/.tmux.conf" ]; then
    cp "${REPO_DIR}/configs/tmux/.tmux.conf" "${HOME}/.tmux.conf"
    echo "Applied tmux config"
fi

# Apply bash config
if [ -f "${REPO_DIR}/configs/bash/.bashrc" ]; then
    cp "${REPO_DIR}/configs/bash/.bashrc" "${HOME}/.bashrc"
    echo "Applied bash config"
fi

# Apply alacritty config directory if present
if [ -d "${REPO_DIR}/configs/alacritty" ]; then
    cp -r "${REPO_DIR}/configs/alacritty/"* "${HOME}/.config/alacritty/" 2>/dev/null || true
    echo "Applied alacritty config"
fi

echo "==> Config apply complete"
echo "Open a new shell or run: source ~/.bashrc"
echo "Reload tmux with: tmux source-file ~/.tmux.conf"
