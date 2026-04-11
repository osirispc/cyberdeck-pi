#!/usr/bin/env bash
set -u

APP_DIR="/home/osirisortiz/projects/voight-kompff"
APP_MAIN="$APP_DIR/voight_kompff.py"
SPLASH_IMG="$APP_DIR/boot.png"
LOG_FILE="$APP_DIR/vk.log"

export DISPLAY="${DISPLAY:-:0}"
export XAUTHORITY="${XAUTHORITY:-/home/osirisortiz/.Xauthority}"

cd "$APP_DIR" || exit 1

echo "==== $(date) ====" >> "$LOG_FILE"
echo "DISPLAY=$DISPLAY" >> "$LOG_FILE"
echo "XAUTHORITY=$XAUTHORITY" >> "$LOG_FILE"
echo "APP_MAIN=$APP_MAIN" >> "$LOG_FILE"

if [ -f "$SPLASH_IMG" ] && command -v feh >/dev/null 2>&1; then
    feh -x -Z -g 900x600+150+80 "$SPLASH_IMG" >/dev/null 2>&1 &
    SPLASH_PID=$!
    sleep 5
    kill "$SPLASH_PID" >/dev/null 2>&1 || true
fi

exec python3 "$APP_MAIN" >> "$LOG_FILE" 2>&1
