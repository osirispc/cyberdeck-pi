#!/bin/bash

cd ~/projects/cyberdeck-pi/scanner/docker

docker compose down
docker compose up -d

echo "Scanner stack running..."
echo "Dashboard: http://localhost:5005"
echo "Radio:     http://localhost:8073"
