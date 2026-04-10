#!/usr/bin/env bash
set -u

APP_DIR="/home/osirisortiz/projects/voight-kompff"
APP_MAIN="$APP_DIR/vk-test.py"
SPLASH_IMG="$APP_DIR/boot.png"
LOG_FILE="$APP_DIR/vk.log"

export DISPLAY="${DISPLAY:-:0}"
export XAUTHORITY="${XAUTHORITY:-/home/osirisortiz/.Xauthority}"

cd "$APP_DIR" || exit 1

{
  echo "==== $(date) ===="
  echo "PWD=$(pwd)"
  echo "DISPLAY=$DISPLAY"
  echo "XAUTHORITY=$XAUTHORITY"
  echo "APP_MAIN=$APP_MAIN"
  echo "SPLASH_IMG=$SPLASH_IMG"
} >> "$LOG_FILE"

SPLASH_PID=""

if [ -f "$SPLASH_IMG" ] && command -v feh >/dev/null 2>&1; then
    feh -F -Z "$SPLASH_IMG" >/dev/null 2>&1 &
    SPLASH_PID=$!
    sleep 2
    kill "$SPLASH_PID" >/dev/null 2>&1 || true
    wait "$SPLASH_PID" 2>/dev/null || true
fi

exec python3 "$APP_MAIN" >> "$LOG_FILE" 2>&1



