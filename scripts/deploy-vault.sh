#!/usr/bin/env bash

TARGET="$1"

if [ -z "$TARGET" ]; then
  echo "Usage: ./deploy-vault.sh user@host"
  exit 1
fi

echo "Deploying Vault layer to $TARGET..."

scp configs/bash/vault.sh "$TARGET:~/vault.sh"

ssh "$TARGET" << 'EOF'

# Ensure bashrc loads vault layer safely
if ! grep -q "vault.sh" ~/.bashrc; then
  echo "" >> ~/.bashrc
  echo "# Load Vault Cyberdeck layer" >> ~/.bashrc
  echo "[ -f ~/vault.sh ] && source ~/vault.sh" >> ~/.bashrc
fi

echo "Vault layer installed."

EOF
