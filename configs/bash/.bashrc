# ~/.bashrc - Cyberdeck Fallout Theme

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

# History behavior
HISTCONTROL=ignoreboth
HISTSIZE=5000
HISTFILESIZE=10000
shopt -s histappend
shopt -s checkwinsize

# Color support
if [ -x /usr/bin/dircolors ]; then
    eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    alias grep='grep --color=auto'
fi

# Useful aliases
alias ll='ls -lah'
alias la='ls -A'
alias l='ls -CF'
alias cls='clear'
alias ports='ss -tulpn'
alias weather='curl wttr.in'
alias update='sudo apt update && sudo apt upgrade -y'

# Homelab shortcuts
alias blacklodge='ssh root@192.168.199.101'
alias whitelodge='ssh root@192.168.199.100'
alias owl='ssh root@192.168.199.204'

# Cyberdeck status helper
cyberdeck_status() {
    echo "========================================"
    echo " VAULT-TEC FIELD TERMINAL"
    echo "========================================"
    echo " Hostname : $(hostname)"
    echo " User     : $(whoami)"
    echo " Kernel   : $(uname -r)"
    echo " Uptime   : $(uptime -p 2>/dev/null)"
    echo " IP       : $(hostname -I 2>/dev/null | awk '{print $1}')"
    echo " Repo     : ~/projects/cyberdeck-pi"
    echo "========================================"
}

# Network check helper
cyberdeck_net() {
    if ping -c 1 -W 1 8.8.8.8 >/dev/null 2>&1; then
        echo "[ONLINE] External network reachable"
    else
        echo "[OFFLINE] Wasteland mode engaged"
    fi
}

# Show banner once per shell
if [ -z "$CYBERDECK_BANNER_SHOWN" ]; then
    export CYBERDECK_BANNER_SHOWN=1
    echo
    echo "========================================"
    echo " VAULT-TEC FIELD TERMINAL v0.2"
    echo " STATUS: OPERATIONAL"
    echo "========================================"
    cyberdeck_net
    echo
fi

# Prompt
# PS1='\[\e[1;32m\][VAULT@\h \W]\$\[\e[0m\] '
PS1='\e[1;32m[VAULT@\h \W]\$\e[0m '
