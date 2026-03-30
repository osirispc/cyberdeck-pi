# Vault Cyberdeck Layer

# Only run in interactive shells
case $- in
    *i*) ;;
      *) return;;
esac

# Prevent double-loading
if [ -n "$VAULT_LOADED" ]; then
  return
fi
export VAULT_LOADED=1

# Prompt (safe for all terminals)
case "$(hostname)" in
  theblacklodge)
    COLOR="31" ;;  # red
  thewhitelodge)
    COLOR="36" ;;  # cyan
  pacard-sawmill)
    COLOR="32" ;;  # green
  *)
    COLOR="32" ;;
esac

PS1="\e[1;${COLOR}m[VAULT@\h \W]\$\e[0m "

# Helpers
cyberdeck_net() {
  if ping -c 1 -W 1 8.8.8.8 >/dev/null 2>&1; then
    echo "[ONLINE]"
  else
    echo "[OFFLINE - WASTELAND MODE]"
  fi
}

# Banner (only once per session)
if [ -z "$VAULT_BANNER" ]; then
  export VAULT_BANNER=1
  echo
  echo "========================================"
  echo " VAULT-TEC FIELD TERMINAL"
  echo "========================================"
  cyberdeck_net
  echo
fi

# Auto-start or attach tmux for interactive sessions
if command -v tmux >/dev/null 2>&1; then
  if [ -z "$TMUX" ]; then
    SESSION="vault"

    if tmux has-session -t "$SESSION" 2>/dev/null; then
      exec tmux attach -t "$SESSION"
    else
      exec tmux new-session -s "$SESSION"
    fi
  fi
fi