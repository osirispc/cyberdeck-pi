# cyberdeck-pi

Portable Raspberry Pi 4 cyberdeck workstation.

## Goals

- Boot into a desktop environment with password login
- Work as a standalone local workstation
- Support browser-based access to GitHub, homelab tools, and documentation
- Be rebuildable from this repository onto a fresh SD card
- Expand later with:
  - external drive mounts
  - VPN
  - headless access
  - offline wiki
  - books/media services
  - local dashboards

## Current Phase

Phase 1: Base workstation

- Raspberry Pi OS Desktop
- Chromium browser
- Bluetooth mouse
- Git repo initialized
- Browser access working

## Planned Structure

- `scripts/` = install and setup scripts
- `configs/` = app and shell configs
- `docs/` = setup notes and rebuild instructions

## Rebuild Philosophy

If the SD card dies, rebuild from this repo.

