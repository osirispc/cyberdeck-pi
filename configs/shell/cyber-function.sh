cyber() {
  case "$1" in
    mode-offline)
      echo "offline" | sudo tee /srv/cyberdeck-portal/state/portal_mode >/dev/null
      echo "[CYBERDECK] Portal mode: FIELD SERVER"
      ;;

    mode-online)
      echo "online" | sudo tee /srv/cyberdeck-portal/state/portal_mode >/dev/null
      echo "[CYBERDECK] Portal mode: HOME NETWORK"
      ;;

    mode-status)
      echo "=== portal mode ==="
      cat /srv/cyberdeck-portal/state/portal_mode 2>/dev/null || echo "unknown"
      echo
      echo "=== portal links ==="
      curl -s http://127.0.0.1:8080/links.json | python3 -m json.tool | sed -n '1,60p'
      ;;

    beacon)
      echo "offline" | sudo tee /srv/cyberdeck-portal/state/portal_mode >/dev/null
      echo "[CYBERDECK] Portal mode: FIELD SERVER"
      echo "[CYBERDECK] Switching to ACCESS POINT mode..."
      sudo systemctl stop NetworkManager 2>/dev/null || true
      sudo systemctl stop wpa_supplicant 2>/dev/null || true
      sudo nmcli device set wlan0 managed no 2>/dev/null || true
      sudo ip addr flush dev wlan0
      sudo ip addr add 192.168.50.1/24 dev wlan0
      sudo ip link set wlan0 up
      sudo systemctl restart dnsmasq
      sudo systemctl restart hostapd
      echo "[CYBERDECK] Beacon is live. SSID: Cyberdeck"
      ;;
    client)
      echo "online" | sudo tee /srv/cyberdeck-portal/state/portal_mode >/dev/null
      echo "[CYBERDECK] Portal mode: HOME NETWORK"
      echo "[CYBERDECK] Switching to CLIENT mode..."
      sudo systemctl stop hostapd
      sudo systemctl stop dnsmasq
      sudo systemctl start NetworkManager
      sudo nmcli device set wlan0 managed yes
      sudo ip link set wlan0 down
      sudo ip link set wlan0 up
      echo "[CYBERDECK] Client mode restored."
      echo "[CYBERDECK] Use: nmcli dev wifi list"
      echo "[CYBERDECK] Then: nmcli dev wifi connect \"SSID\" password \"PASSWORD\""
      ;;
    signal)
      echo "=== iw dev wlan0 info ==="
      iw dev wlan0 info
      echo
      echo "=== wlan0 address ==="
      ip addr show wlan0
      echo
      echo "=== hostapd ==="
      systemctl status hostapd --no-pager 2>/dev/null | sed -n '1,8p'
      echo
      echo "=== dnsmasq ==="
      systemctl status dnsmasq --no-pager 2>/dev/null | sed -n '1,8p'
      ;;
    vpn)
      echo "[CYBERDECK] Starting OpenVPN..."
      sudo systemctl start openvpn-client@myvpn
      ;;
    vpn-off)
      echo "[CYBERDECK] Stopping OpenVPN..."
      sudo systemctl stop openvpn-client@myvpn
      ;;
    vpn-status)
      echo "=== OpenVPN instance ==="
      systemctl status openvpn-client@myvpn --no-pager | sed -n '1,12p'
      echo
      echo "=== tun0 ==="
      ip addr show tun0 2>/dev/null || echo "tun0 not up"
      echo
      echo "=== public ip ==="
      curl -4 -s ifconfig.me ; echo
      ;;
    keys)
      echo "Cyberdeck workspace keys:"
      echo "  Super + A           - switch to Desktop 1 / PORTAL"
      echo "  Super + S           - switch to Desktop 2 / TERMINAL"
      echo "  Super + D           - switch to Desktop 3 / CODE"
      echo "  Super + F           - switch to Desktop 4 / MEDIA"
      echo
      echo "Move active window:"
      echo "  Super + Shift + A   - move current window to PORTAL"
      echo "  Super + Shift + S   - move current window to TERMINAL"
      echo "  Super + Shift + D   - move current window to CODE"
      echo "  Super + Shift + F   - move current window to MEDIA"
      echo
      echo "Launcher:"
      echo "  Super + Space       - open app launcher"
      ;;
    help|"")
      echo "Cyberdeck commands:"
      echo "  cyber beacon       - turn hotspot/AP mode on and set portal offline"
      echo "  cyber client       - return to Wi-Fi client mode and set portal online"
      echo "  cyber mode-offline - set portal to field/offline links"
      echo "  cyber mode-online  - set portal to home/online links"
      echo "  cyber mode-status  - show current portal mode and link manifest"
      echo "  cyber signal       - show current wireless status"
      echo "  cyber vpn        - start OpenVPN tunnel"
      echo "  cyber vpn-off    - stop OpenVPN tunnel"
      echo "  cyber vpn-status - show VPN state and public IP"
      echo "  cyber help       - show this menu"
      echo "  cyber keys       - show workspace keyboard shortcuts"
      echo
      echo "Workspace keys:"
      echo "  Super + A           - switch to Desktop 1 / PORTAL"
      echo "  Super + S           - switch to Desktop 2 / TERMINAL"
      echo "  Super + D           - switch to Desktop 3 / CODE"
      echo "  Super + F           - switch to Desktop 4 / MEDIA"
      echo "  Super + Shift + A   - move current window to PORTAL"
      echo "  Super + Shift + S   - move current window to TERMINAL"
      echo "  Super + Shift + D   - move current window to CODE"
      echo "  Super + Shift + F   - move current window to MEDIA"
      echo "  Super + Space       - open app launcher"
      ;;
    *)
      echo "[CYBERDECK] Unknown command: $1"
      echo "Try: cyber help"
      ;;
  esac
}
