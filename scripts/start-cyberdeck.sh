#!/bin/bash

SESSION="cyberdeck"

tmux kill-session -t $SESSION 2>/dev/null

tmux new-session -d -s $SESSION -n main

# Pane 1 — System Stats
tmux send-keys -t $SESSION "htop" C-m

# Split horizontally
tmux split-window -h -t $SESSION

# Pane 2 — Sync Log
tmux send-keys -t $SESSION "tail -f ~/cyberdeck/sync.log" C-m

# Split bottom left
tmux split-window -v -t $SESSION:0.0

# Pane 3 — Docker Containers
tmux send-keys -t $SESSION "watch docker ps" C-m

# Split bottom right
tmux split-window -v -t $SESSION:0.1

# Pane 4 — Network + IP
tmux send-keys -t $SESSION "watch -n 2 hostname -I" C-m

# Layout
tmux select-layout tiled

tmux attach-session -t $SESSION
