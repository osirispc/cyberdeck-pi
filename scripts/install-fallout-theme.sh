#!/usr/bin/env bash
set -euo pipefail

echo "==> Installing Fallout theme support packages"

sudo apt update
sudo apt install -y tmux neovim htop btop figlet lolcat fonts-firacode

echo "==> Fallout theme support packages installed"
