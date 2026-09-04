#!/data/data/com.termux/files/usr/bin/bash

set -e

R='\033[0;31m'
G='\033[0;32m'
I='\033[0;90m' 
N='\033[0m'

run_step() {
    local msg="$1"
    local cmd="$2"

    echo -e "${I}[..]${N} $msg..."

    if eval "$cmd" > /dev/null 2>&1; then
        echo -e "     └─> ${G}[SUCCESS]${N}\n"
    else
        echo -e "     └─> ${R}[FAILED]${N}"
        echo -e "${R}Error occurred during: $msg${N}\n"
        exit 1
    fi
}

echo

if [ ! -d "$HOME/storage" ]; then
    echo -e "\nGrant permission: termux-setup-storage\nThen rerun the command.\n"
    exit 1
fi

arch=$(dpkg --print-architecture)

if [[ "$arch" != "aarch64" && "$arch" != "arm" ]]; then
    echo "RitikTool does not support architecture $arch"
    exit 1
fi

run_step "Updating System & Fixing Broken Packages" \
"yes | apt --fix-broken install && yes | apt update && yes | apt upgrade"

run_step "Installing Python3" \
"yes | pkg install python3"

run_step "Installing libusb" \
"yes | pkg install libusb"

run_step "Installing pv" \
"yes | pkg install pv"

run_step "Installing Archive Tools (7z, rar, zip, tar)" \
"yes | pkg install p7zip unrar unzip tar"

run_step "Installing termux-adb" \
"curl -fsS https://raw.githubusercontent.com/nohajc/termux-adb/master/install.sh | bash"

run_step "symlink termux-adb/termux-fastboot — adb/fastboot" \
'ln -sf "$PREFIX/bin/termux-fastboot" "$PREFIX/bin/fastboot" && ln -sf "$PREFIX/bin/termux-adb" "$PREFIX/bin/adb"'

run_step "Installing colorama" \
"pip install -U colorama"

run_step "download mitool.py" \
'curl -fsS "https://raw.githubusercontent.com/rittik55/Rittik-Hybrib-rom-flasher/main/mitool.py" -o "$PREFIX/bin/mitool" && chmod +x "$PREFIX/bin/mitool"'

run_step "download miflashf.py" \
'curl -fsS "https://raw.githubusercontent.com/rittik55/Rittik-Hybrib-rom-flasher/main/miflashf.py" -o "$PREFIX/bin/miflashf" && chmod +x "$PREFIX/bin/miflashf"'

echo -e "${G}✔ Installation completed successfully${N}\n"

echo -e "Run command: ${G}mitool${N}"
echo ""
