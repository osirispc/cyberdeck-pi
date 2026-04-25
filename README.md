You’re right. Paste this whole thing into `README.md`.

Open it:

```bash
nano README.md
```

Delete everything in it, then paste this:

````markdown
# cyberdeck-pi

Portable Raspberry Pi cyberdeck workstation.

## Purpose

This repo stores the setup files, configs, scripts, and notes needed to rebuild the cyberdeck if the SD card fails, the Pi is upgraded, or the desktop configuration gets broken.

The goal is simple:

```text
Clone this repo.
Run the restore scripts.
Bring the cyberdeck back to life.
````

## Current Phase

Phase 1: Base workstation and desktop controls.

Current working setup:

* Raspberry Pi OS Desktop
* labwc desktop/window manager
* 4 virtual desktops/workspaces
* Corne-friendly workspace switching
* Cyberdeck shell helper command: `cyber`
* App launcher with `Super + Space`
* Portal/network helper commands
* VPN helper commands

## Desktop Workspace Map

The cyberdeck uses 4 labwc virtual desktops:

```text
Desktop 1 -> PORTAL
Desktop 2 -> TERMINAL
Desktop 3 -> CODE
Desktop 4 -> MEDIA
```

## Keyboard Controls

Main workspace switching:

```text
Super + A           -> switch to Desktop 1 / PORTAL
Super + S           -> switch to Desktop 2 / TERMINAL
Super + D           -> switch to Desktop 3 / CODE
Super + F           -> switch to Desktop 4 / MEDIA
```

Move the active window between workspaces:

```text
Super + Shift + A   -> move active window to PORTAL
Super + Shift + S   -> move active window to TERMINAL
Super + Shift + D   -> move active window to CODE
Super + Shift + F   -> move active window to MEDIA
```

Launcher:

```text
Super + Space       -> open app launcher
```

## Cyberdeck Helper Commands

The `cyber` shell function provides quick cyberdeck commands.

```bash
cyber help
cyber keys
cyber beacon
cyber client
cyber mode-offline
cyber mode-online
cyber mode-status
cyber signal
cyber vpn
cyber vpn-off
cyber vpn-status
```

### Command Notes

```text
cyber help        -> show full command menu
cyber keys        -> show keyboard shortcut reference
cyber beacon      -> turn hotspot/AP mode on and set portal offline
cyber client      -> return to Wi-Fi client mode and set portal online
cyber mode-offline -> set portal to field/offline links
cyber mode-online  -> set portal to home/online links
cyber mode-status  -> show current portal mode and link manifest
cyber signal      -> show wireless/AP status
cyber vpn         -> start OpenVPN tunnel
cyber vpn-off     -> stop OpenVPN tunnel
cyber vpn-status  -> show VPN state and public IP
```

## Repo Structure

```text
cyberdeck-pi/
├── configs/
│   ├── labwc/
│   │   └── rc.xml
│   └── shell/
│       └── cyber-function.sh
├── scripts/
│   └── install-cyberdeck-workspaces.sh
└── README.md
```

## Restore Workspace Config

From the repo root:

```bash
./scripts/install-cyberdeck-workspaces.sh
source ~/.bashrc
labwc --reconfigure
```

Then test:

```bash
cyber help
cyber keys
```

## Manual Config Locations

Live labwc config:

```bash
/home/osirisortiz/.config/labwc/rc.xml
```

Saved labwc config in repo:

```bash
configs/labwc/rc.xml
```

Live shell config:

```bash
/home/osirisortiz/.bashrc
```

Saved cyber helper function in repo:

```bash
configs/shell/cyber-function.sh
```

## Rebuild Philosophy

If the SD card dies, rebuild from this repo.

The cyberdeck should be able to return to its working field-terminal setup without guessing, hunting through old notes, or rebuilding from memory.

## Future Improvements

Planned additions:

* Auto-open browser on PORTAL desktop
* Auto-open terminal on TERMINAL desktop
* Auto-open code-server or dev tools on CODE desktop
* Auto-open Jellyfin/media tools on MEDIA desktop
* Add install script for required packages
* Add portal restore steps
* Add screenshots of the desktop layout
* Add full fresh-Pi rebuild guide

````
