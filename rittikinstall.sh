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

if ! cmd package list packages --user 0 com.termux.api < /dev/null 2>/dev/null | grep -q 'com.termux.api'; then
    echo
    echo 'com.termux.api app is not installed'
    echo 'Please install it first'
    echo
    exit 1
fi

arch=$(dpkg --print-architecture)

if [[ "$arch" != "aarch64" && "$arch" != "arm" ]]; then
    echo "Rittik Tool does not support architecture $arch"
    exit 1
fi

run_step "Updating System & Fixing Broken Packages" \
"yes | apt --fix-broken install && yes | apt update && yes | apt upgrade"

run_step "Installing Python3" \
"yes | pkg install python3"

run_step "Installing libusb" \
"yes | pkg install libusb"

run_step "Installing pv & p7zip (For 7z, RAR, ZIP, TGZ Extraction)" \
"yes | pkg install pv p7zip"

run_step "Installing termux-adb" \
"curl -fsS https://raw.githubusercontent.com/nohajc/termux-adb/master/install.sh | bash"

run_step "symlink termux-adb/termux-fastboot — adb/fastboot" \
"ln -sf "$PREFIX/bin/termux-fastboot" "$PREFIX/bin/fastboot" && ln -sf "$PREFIX/bin/termux-adb" "$PREFIX/bin/adb""

run_step "Installing colorama" \
"pip install -U colorama"

run_step "Installing fcetool" \
"pip install -U fcetool"

REPO_URL="https://raw.githubusercontent.com/rittik55/Rittik-Hybrib-rom-flasher/main/RR"

run_step "download rittiktool launcher" \
"curl -fsS "${REPO_URL}/mitool.py" -o "$PREFIX/bin/rittiktool" && chmod +x "$PREFIX/bin/rittiktool""

run_step "download miflashf.py (Flashing Tool)" \
"curl -fsS "${REPO_URL}/miflashf.py" -o "$PREFIX/bin/miflashf" && chmod +x "$PREFIX/bin/miflashf""

run_step "download mifcetool.py" \
"curl -fsS "${REPO_URL}/mifcetool.py" -o "$PREFIX/bin/mifcetool" && chmod +x "$PREFIX/bin/mifcetool""

run_step "download miasst.py" \
"curl -fsS "${REPO_URL}/miasst.py" -o "$PREFIX/bin/miasst" && chmod +x "$PREFIX/bin/miasst""

run_step "download miasst_termux" \
"curl -fsS -L -o $PREFIX/bin/miasst_termux \
"$(curl -fsS 'https://api.github.com/repos/MiForge/MiAssistantTool/releases/latest' \
| grep 'browser_download_url.*miasst_termux_'${arch} | cut -d '"' -f 4)" \
&& chmod +x $PREFIX/bin/miasst_termux"

echo -e "${G}✔ Installation completed successfully${N}\n"
echo -e "Run command: ${G}ritiktool${N}"
echo ""

