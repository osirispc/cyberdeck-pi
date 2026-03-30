cyberdeck_status() {
    echo "========================================"
    echo " VAULT-TEC FIELD TERMINAL"
    echo "========================================"
    echo " Hostname : $(hostname)"
    echo " Uptime   : $(uptime -p 2>/dev/null)"
    echo " CPU Load : $(uptime | awk -F'load average:' '{print $2}')"
    echo " Memory   : $(free -h | awk '/Mem:/ {print $3 "/" $2}')"
    echo " Disk     : $(df -h / | awk 'NR==2 {print $3 "/" $2}')"
    echo " IP       : $(hostname -I | awk '{print $1}')"
    echo "========================================"
}
