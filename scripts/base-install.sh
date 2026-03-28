#!/usr/bin/env bash
set -euo pipefail

echo "==> Updating package lists"
sudo apt update

echo "==> Repairing any interrupted packages"
sudo dpkg --configure -a || true
sudo apt -f install -y || true

echo "==> Installing core workstation packages"
sudo apt install -y \
  git \
  curl \
  wget \
  tmux \
  htop \
  neovim \
  build-essential \
  lxterminal \
  alacritty \
  bluetooth \
  bluez \
  blueman \
  fonts-firacode

echo "==> Ensuring bluetooth service is enabled"
sudo systemctl enable bluetooth
sudo systemctl start bluetooth

echo "==> Creating project workspace"
mkdir -p "$HOME/projects"

echo "==> Base install complete"
echo "Next steps:"
echo "  1. reboot"
echo "  2. configure tmux"
echo "  3. configure alacritty"
echo "  4. set up SSH and GitHub workflow"
