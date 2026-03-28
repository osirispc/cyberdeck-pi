# Cyberdeck Pi Setup

## Hardware

- Raspberry Pi 4
- 512 GB SD card
- 14-inch portable LCD
- external 2 TB drive
- battery packs kept charged
- Bluetooth keyboard and mouse

## Base Requirements

- boot straight to desktop
- password required on login
- auto-connect to home Wi-Fi
- browser available for GitHub and homelab access
- repo-based rebuild approach

## Current Build Status

Completed:
- Raspberry Pi OS Desktop flashed and booted
- browser opened and working
- Bluetooth mouse connected
- GitHub repository initialized on device

Next:
- install base packages
- configure terminal environment
- save configs into repo
- add rebuild scripts
- add SSH workflow
- expand into headless and offline services later

## First Rebuild Flow

1. Flash Raspberry Pi OS Desktop to SD card
2. Boot Pi and connect to Wi-Fi
3. Log in with password
4. Open browser and sign into GitHub
5. Clone this repo into `~/projects`
6. Run setup scripts from `scripts/`

