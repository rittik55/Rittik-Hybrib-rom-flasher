#!/usr/bin/env python3

import os
import sys
import time
import shutil
import subprocess

VERSION = "7.0.0-PRO"

# Terminal Color Palette
ORANGE = "\033[38;5;208m"
GREEN  = "\033[38;5;48m"
RED    = "\033[38;5;196m"
YELLOW = "\033[38;5;220m"
GRAY   = "\033[38;5;242m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

# ==========================================================
# 100% ORIGINAL EMBEDDED SCRIPTS (UNTOUCHED)
# ==========================================================
RITTIK_XPOWER_CODE = r"""#!/data/data/com.termux/files/usr/bin/sh
# ==========================================================
# Flash Script for Fastboot ROM (Duchamp)
# Made by: Ritik
# ==========================================================

cd "$(dirname "$0")" || exit 1

if command -v termux-fastboot >/dev/null 2>&1; then
    fastboot="termux-fastboot"
elif command -v fastboot >/dev/null 2>&1; then
    fastboot="fastboot"
else
    echo "[-] Error: Fastboot not found!"
    echo "[!] Please install: pkg install termux-adb"
    exit 1
fi

echo "=================================================="
echo "----------------------------------------"
echo "                                        "
echo "  ___   _   _   ___  _____  _       "
echo " / _ \ | | | | / _ \|_   _|| |      "
echo "| | | || | | || | | | | |  | |      "
echo "| |_| || |_| || |_| | | |  | |___   "
echo " \__\_\\___/  \___/  |_|  |_____|  "
echo "                                        "
echo "         MADE BY RITIK                  "
echo "     ROM FLASH TOOL (duchamp)           "
echo "----------------------------------------"
echo "=================================================="

echo "[*] Waiting for device..."
device=$($fastboot getvar product 2>&1 | grep -F "product:" | tr -s " " | cut -d " " -f 2)
[ -z "$device" ] && device="unknown"

if [ "$device" != "duchamp" ]; then
    echo "[-] Error: Device mismatch!"
    echo "    Compatible devices: duchamp"
    echo "    Detected device: $device"
    exit 1
fi

echo "[!] WARNING: This install will delete all your applications, settings and files from internal storage."
printf "Do you agree? (Y/N) "
read -r choice
[ "$choice" != "y" ] && [ "$choice" != "Y" ] && exit 0

echo "###################################################"
echo "  Flashing started by Ritik's Script...            "
echo "  After install device will be rebooted.           "
echo "  Please wait and DO NOT disconnect your device.   "
echo "###################################################"

$fastboot set_active a
$fastboot flash apusys_a img/apusys.img
$fastboot flash apusys_b img/apusys.img
$fastboot flash audio_dsp_a img/audio_dsp.img
$fastboot flash audio_dsp_b img/audio_dsp.img
$fastboot flash boot_a img/boot.img
$fastboot flash boot_b img/boot.img
$fastboot flash ccu_a img/ccu.img
$fastboot flash ccu_b img/ccu.img
$fastboot flash connsys_bt_a img/connsys_bt.img
$fastboot flash connsys_bt_b img/connsys_bt.img
$fastboot flash connsys_gnss_a img/connsys_gnss.img
$fastboot flash connsys_gnss_b img/connsys_gnss.img
$fastboot flash connsys_wifi_a img/connsys_wifi.img
$fastboot flash connsys_wifi_b img/connsys_wifi.img
$fastboot flash dpm_a img/dpm.img
$fastboot flash dpm_b img/dpm.img
$fastboot flash dtbo_a img/dtbo.img
$fastboot flash dtbo_b img/dtbo.img
$fastboot flash gpueb_a img/gpueb.img
$fastboot flash gpueb_b img/gpueb.img
$fastboot flash gz_a img/gz.img
$fastboot flash gz_b img/gz.img
$fastboot flash init_boot_a img/init_boot.img
$fastboot flash init_boot_b img/init_boot.img
$fastboot flash lk_a img/lk.img
$fastboot flash lk_b img/lk.img
$fastboot flash logo_a img/logo.img
$fastboot flash logo_b img/logo.img
$fastboot flash mcf_ota_a img/mcf_ota.img
$fastboot flash mcf_ota_b img/mcf_ota.img
$fastboot flash mcupm_a img/mcupm.img
$fastboot flash mcupm_b img/mcupm.img
$fastboot flash modem_a img/modem.img
$fastboot flash modem_b img/modem.img
$fastboot flash mvpu_algo_a img/mvpu_algo.img
$fastboot flash mvpu_algo_b img/mvpu_algo.img
$fastboot flash pi_img_a img/pi_img.img
$fastboot flash pi_img_b img/pi_img.img
$fastboot flash preloader_a img/preloader_raw.img
$fastboot flash preloader_b img/preloader_raw.img
$fastboot flash scp_a img/scp.img
$fastboot flash scp_b img/scp.img
$fastboot flash spmfw_a img/spmfw.img
$fastboot flash spmfw_b img/spmfw.img
$fastboot flash sspm_a img/sspm.img
$fastboot flash sspm_b img/sspm.img
$fastboot flash tee_a img/tee.img
$fastboot flash tee_b img/tee.img
$fastboot flash vbmeta_a img/vbmeta.img
$fastboot flash vbmeta_b img/vbmeta.img
$fastboot flash vbmeta_system_a img/vbmeta_system.img
$fastboot flash vbmeta_system_b img/vbmeta_system.img
$fastboot flash vbmeta_vendor_a img/vbmeta_vendor.img
$fastboot flash vbmeta_vendor_b img/vbmeta_vendor.img
$fastboot flash vcp_a img/vcp.img
$fastboot flash vcp_b img/vcp.img
$fastboot flash vendor_boot_a img/vendor_boot.img
$fastboot flash vendor_boot_b img/vendor_boot.img
$fastboot flash super img/super.img
$fastboot erase metadata
$fastboot erase userdata
$fastboot erase expdb
$fastboot erase frp
$fastboot oem cdms
$fastboot reboot

echo ""
echo "[+] ROM Flashing Successfully Completed!"
echo "[+] Script executed by Ritik."
"""

RITIK_FLASH_CODE = r"""#!/data/data/com.termux/files/usr/bin/sh
cd "$(dirname "$0")" || exit 1

if command -v termux-fastboot >/dev/null 2>&1; then
    fastboot="termux-fastboot"
elif command -v fastboot >/dev/null 2>&1; then
    fastboot="fastboot"
elif [ -f "./bin/linux/fastboot" ]; then
    fastboot="./bin/linux/fastboot"
else
    fastboot="fastboot"
fi

echo "=================================================="
echo "----------------------------------------"
echo "                                        "
echo "  ___   _   _   ___  _____  _       "
echo " / _ \ | | | | / _ \|_   _|| |      "
echo "| | | || | | || | | | | |  | |      "
echo "| |_| || |_| || |_| | | |  | |___   "
echo " \__\_\\___/  \___/  |_|  |_____|  "
echo "                                        "
echo "         MADE BY RITIK                  "
echo "     ROM FLASH TOOL (duchamp)           "
echo "----------------------------------------"
echo "=================================================="

echo "[*] Waiting for device..."
device=$($fastboot getvar product 2>&1 | grep -F "product:" | tr -s " " | cut -d " " -f 2)
[ -z "$device" ] && device="unknown"

if [ "$device" != "duchamp" ]; then
    echo "[-] Error: Device mismatch!"
    echo "    Compatible devices: duchamp"
    echo "    Detected device: $device"
    exit 1
fi

echo "[!] You are going to wipe your data and internal storage."
echo "[!] It will delete all your files and photos stored on internal storage."
printf "Do you agree? (Y/N) "
read -r choice
[ "$choice" != "y" ] && [ "$choice" != "Y" ] && exit 0

echo "##################################################################"
echo "Please wait. The device will reboot when installation is finished."
echo "##################################################################"

$fastboot set_active a
$fastboot flash apusys_ab images/apusys.img
$fastboot flash audio_dsp_ab images/audio_dsp.img
$fastboot flash ccu_ab images/ccu.img
$fastboot flash connsys_bt_ab images/connsys_bt.img
$fastboot flash connsys_gnss_ab images/connsys_gnss.img
$fastboot flash connsys_wifi_ab images/connsys_wifi.img
$fastboot flash dpm_ab images/dpm.img
$fastboot flash dtbo_ab images/dtbo.img
$fastboot flash gpueb_ab images/gpueb.img
$fastboot flash gz_ab images/gz.img
$fastboot flash lk_ab images/lk.img
$fastboot flash logo_ab images/logo.img
$fastboot flash mcf_ota_ab images/mcf_ota.img
$fastboot flash mcupm_ab images/mcupm.img
$fastboot flash modem_ab images/modem.img
$fastboot flash mvpu_algo_ab images/mvpu_algo.img
$fastboot flash pi_img_ab images/pi_img.img
$fastboot flash scp_ab images/scp.img
$fastboot flash spmfw_ab images/spmfw.img
$fastboot flash sspm_ab images/sspm.img
$fastboot flash tee_ab images/tee.img
$fastboot flash vbmeta_ab images/vbmeta.img
$fastboot flash vbmeta_system_ab images/vbmeta_system.img
$fastboot flash vbmeta_vendor_ab images/vbmeta_vendor.img
$fastboot flash vcp_ab images/vcp.img
$fastboot flash boot_ab images/boot.img
$fastboot flash init_boot_ab images/init_boot.img
$fastboot flash vendor_boot_ab images/vendor_boot.img
$fastboot flash super images/super.img
$fastboot erase metadata
$fastboot erase frp
$fastboot erase expdb
$fastboot erase userdata
$fastboot oem cdms
$fastboot reboot
"""

def write_custom_scripts(target_dir):
    script1 = os.path.join(target_dir, "Rittik_xpower.sh")
    script2 = os.path.join(target_dir, "ritik_flash_.sh")

    with open(script1, "w", encoding="utf-8") as f:
        f.write(RITTIK_XPOWER_CODE)

    with open(script2, "w", encoding="utf-8") as f:
        f.write(RITIK_FLASH_CODE)

    os.system(f"chmod +x '{script1}' '{script2}'")

# --- FEATURE 2: OTG RECONNECT HANDLER ---
def wait_for_fastboot():
    spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    idx = 0
    was_disconnected = False

    while True:
        try:
            output = subprocess.check_output(
                ['fastboot', 'devices'], 
                stderr=subprocess.STDOUT
            ).decode('utf-8', errors='ignore').strip()
        except Exception:
            output = ""

        if output and "fastboot" in output.lower():
            if "no permission" not in output.lower():
                sys.stdout.write('\r' + ' ' * 60 + '\r')
                if was_disconnected:
                    print(f" {GREEN}✔ Connection Restored! Resuming...{RESET}\n")
                else:
                    print(f" {GREEN}✔ Target Device Detected in Fastboot Mode!{RESET}\n")
                return

        # If disconnected, prompt user to plug it back in
        was_disconnected = True
        char = spinner[idx % len(spinner)]
        sys.stdout.write(f"\r {YELLOW}{char}{RESET} {BOLD}Device not detected! Connect OTG in Fastboot...{RESET}")
        sys.stdout.flush()
        idx += 1
        time.sleep(0.08)

# --- FEATURE 3: LIVE DECOMPRESSION PROGRESS ---
def decompress_and_flash_rom(archive_file):
    RF = "/sdcard/Download/hybrid-fastboot-rom"
    
    if os.path.exists(RF):
        print(f"\n {GRAY}Cleaning old extracted ROM cache...{RESET}")
        shutil.rmtree(RF, ignore_errors=True)

    os.makedirs(RF, exist_ok=True)

    print(f"\n {ORANGE}► Decompressing ROM Archive (Live Stream)...{RESET}")
    archive_lower = archive_file.lower()

    # If tgz/tar.gz, use pv for a smooth visual progress bar
    if archive_lower.endswith((".tgz", ".tar.gz")):
        file_size = os.path.getsize(archive_file)
        if shutil.which("pv"):
            cmd = f"pv -s {file_size} '{archive_file}' | tar --strip-components=1 -xz -C '{RF}/'"
        else:
            cmd = f"tar --strip-components=1 -xvf '{archive_file}' -C '{RF}/'"
    elif archive_lower.endswith((".zip", ".7z", ".rar")):
        # 7z bsp1 prints progress percentage line by line
        cmd = f"7z x -y '{archive_file}' -o'{RF}/' -bsp1"
    else:
        print(f" {RED}Unsupported archive format!{RESET}")
        sys.exit(1)

    return_code = os.system(cmd)
    if return_code != 0:
        print(f"\n {RED}✖ Decompression failed (Exit Code: {return_code}){RESET}\n")
        sys.exit(1)

    print(f"\n {GREEN}✔ Extraction completed successfully!{RESET}\n")
    auto_detect_and_flash(RF)

# --- FEATURE 1: AUTO-DETECT ENGINE (SMART 1-CLICK) ---
def auto_detect_and_flash(rom_dir):
    # Ensure scripts exist in the folder
    has_stock_script = os.path.exists(f"{rom_dir}/flash_all.sh") or os.path.exists(f"{rom_dir}/flash_all_lock.sh")
    if not has_stock_script:
        write_custom_scripts(rom_dir)

    print(f" {BOLD}Scanning ROM Directory Structure...{RESET}")
    
    selected_script = None

    # Priority 1: Check if official stock script exists
    if os.path.exists(f"{rom_dir}/flash_all.sh"):
        selected_script = "flash_all.sh"
        print(f" {CYAN}↳ Official Stock Firmware Detected{RESET}")

    # Priority 2: Check for img/ directory -> Rittik_xpower.sh
    elif os.path.isdir(f"{rom_dir}/img"):
        selected_script = "Rittik_xpower.sh"
        print(f" {CYAN}↳ 'img/' folder detected -> Selected: Rittik_xpower.sh{RESET}")

    # Priority 3: Check for images/ directory -> ritik_flash_.sh
    elif os.path.isdir(f"{rom_dir}/images"):
        selected_script = "ritik_flash_.sh"
        print(f" {CYAN}↳ 'images/' folder detected -> Selected: ritik_flash_.sh{RESET}")

    # Fallback: Check which file exists
    elif os.path.exists(f"{rom_dir}/Rittik_xpower.sh"):
        selected_script = "Rittik_xpower.sh"
    elif os.path.exists(f"{rom_dir}/ritik_flash_.sh"):
        selected_script = "ritik_flash_.sh"

    if not selected_script:
        print(f"\n {RED}✖ Could not automatically determine flashing script.{RESET}")
        sys.exit(1)

    execute_script(rom_dir, selected_script)

def execute_script(target_dir, script_name):
    file_path = os.path.join(target_dir, script_name)
    os.system(f"sed -i -e 's/\\r$//' '{file_path}' 2>/dev/null")
    os.system(f"chmod +x '{file_path}'")

    bin_linux_dir = os.path.join(target_dir, "bin", "linux")
    if os.path.exists(bin_linux_dir):
        system_fastboot = subprocess.getoutput("which fastboot").strip()
        if system_fastboot and os.path.exists(system_fastboot):
            target_bin = os.path.join(bin_linux_dir, "fastboot")
            os.system(f"rm -f '{target_bin}'")
            os.system(f"ln -sf '{system_fastboot}' '{target_bin}'")

    # Wait for device with auto-reconnect protection
    wait_for_fastboot()

    print(f" {GREEN}▶ Auto-Launching: {BOLD}{script_name}{RESET}...\n")
    os.system(f"cd '{target_dir}' && env PATH=\"$PREFIX/bin:$PATH\" bash '{script_name}'")
    sys.exit(0)

def scan_rom_packages():
    valid_extensions = (".tgz", ".tar.gz", ".zip", ".7z", ".rar")
    ignored_keywords = ["module", "ksun", "magisk", "susfs", "kernel"]

    target_locations = ["/sdcard/Download", "/sdcard"]
    found_items = []

    for folder in target_locations:
        if not os.path.exists(folder):
            continue
        try:
            for item in os.listdir(folder):
                full_path = os.path.join(folder, item)
                if os.path.isfile(full_path) and item.lower().endswith(valid_extensions):
                    if not any(kw in item.lower() for kw in ignored_keywords):
                        found_items.append({"path": full_path, "type": "archive"})
        except PermissionError:
            pass

    RF_DIR = "/sdcard/Download/hybrid-fastboot-rom"
    if os.path.isdir(RF_DIR):
        found_items.append({"path": RF_DIR, "type": "folder"})

    return found_items

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    
    print(f"{ORANGE}{BOLD}")
    print("  ┌──────────────────────────────────────────────┐")
    print("  │         R I T I K   F L A S H E R            │")
    print(f"  │      {RESET}{GRAY}HYBRID ENGINE v{VERSION}  │  POCO X6 PRO{RESET}{ORANGE}{BOLD}      │")
    print("  └──────────────────────────────────────────────┘" + RESET)

    items = scan_rom_packages()

    if not items:
        print(f"\n {RED}✖ No ROM packages found in /sdcard/Download!{RESET}\n")
        sys.exit(1)

    print(f"\n {BOLD}Detected ROM Packages in Storage:{RESET}")
    print(f" {GRAY}{'─' * 45}{RESET}")
    for i, item in enumerate(items, start=1):
        name = os.path.basename(item["path"])
        if item["type"] == "folder":
            name += f" {YELLOW}[Extracted Folder]{RESET}"
        print(f"  {ORANGE}{BOLD}[{i}]{RESET} {name}")
    print(f" {GRAY}{'─' * 45}{RESET}")

    while True:
        choice = input(f"\n {BOLD}Select ROM index [1-{len(items)}]: {RESET}").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(items):
            selected = items[int(choice) - 1]
            break
        print(f" {RED}Invalid choice!{RESET}")

    if selected["type"] == "archive":
        decompress_and_flash_rom(selected["path"])
    elif selected["type"] == "folder":
        auto_detect_and_flash(selected["path"])

if __name__ == "__main__":
    main()
    
