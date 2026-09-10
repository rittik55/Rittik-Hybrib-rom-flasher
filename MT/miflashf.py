#!/usr/bin/python

import os
import sys
import time
import shutil
import subprocess
import urllib.request

# --- Tool Version Configuration ---
CURRENT_VERSION = "2.0.0"

# Exact GitHub Raw URLs for rittik55
VERSION_URL = "https://raw.githubusercontent.com/rittik55/Rittik-Hybrib-rom-flasher/main/MT/version.txt"
SCRIPT_URL = "https://raw.githubusercontent.com/rittik55/Rittik-Hybrib-rom-flasher/main/MT/miflashf.py"

# --- 100% Offline Embedded Custom Scripts (For Duchamp Only) ---
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

def enforce_mandatory_update():
    print("\n\033[93m[*] Checking for security & script updates...\033[0m")
    
    latest_version = None
    try:
        req = urllib.request.Request(VERSION_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            latest_version = response.read().decode('utf-8').strip()
    except Exception:
        print("\n\033[91m==================================================")
        print("  [!] ERROR: Internet Connection Required!")
        print("  Running outdated tools poses bricking risks.")
        print("  Please connect to the internet and run again.")
        print("==================================================\033[0m\n")
        sys.exit(1)

    if latest_version and latest_version != CURRENT_VERSION:
        print("\n\033[91m==================================================")
        print(f"  [!] CRITICAL UPDATE AVAILABLE! (v{latest_version})")
        print(f"  Your current version (v{CURRENT_VERSION}) is DEPRECATED.")
        print("  You must update the tool to continue!")
        print("==================================================\033[0m\n")

        while True:
            choice = input("Do you want to update now? (Y/N): ").strip().lower()
            if choice == 'y':
                print("\n\033[92m[*] Downloading latest update from GitHub...\033[0m")
                script_path = os.path.realpath(__file__)
                
                cmd = f"curl -sL '{SCRIPT_URL}' -o '{script_path}' && chmod +x '{script_path}'"
                res = os.system(cmd)
                
                if res == 0:
                    print(f"\n\033[92m✔ Tool successfully updated to v{latest_version}!\033[0m")
                    print("\033[93mRestarting tool now...\033[0m\n")
                    time.sleep(1)
                    os.execv(sys.executable, ['python'] + sys.argv)
                else:
                    print("\n\033[91m[-] Update failed. Please check your connection.\033[0m\n")
                    sys.exit(1)
            elif choice == 'n':
                print("\n\033[91m[-] Update rejected. Exiting to prevent errors.\033[0m\n")
                sys.exit(0)
            else:
                print("Please enter Y or N.")
    else:
        print(f"\033[92m✔ Tool is up-to-date (v{CURRENT_VERSION})\033[0m\n")

def find_working_rom_dir(base_dir):
    for root, dirs, files in os.walk(base_dir):
        if "img" in dirs or "images" in dirs or "flash_all.sh" in files:
            return root
    return base_dir

def check_mode():
    spinner = "|/-\\"
    message = "\r Waiting for Fastboot / ADB device... "
    while True:
        for char in spinner:
            try:
                fb_out = subprocess.check_output(
                    ['fastboot', 'devices'], 
                    stderr=subprocess.STDOUT
                ).decode('utf-8', errors='ignore').strip()
            except Exception:
                fb_out = ""

            if fb_out and "fastboot" in fb_out.lower():
                if "no permission" in fb_out.lower():
                    sys.stdout.write(message + char + '\r')
                    sys.stdout.flush()
                    time.sleep(0.2)
                    continue

                sys.stdout.write('\r\033[K')
                sys.stdout.flush()
                print("\n\033[92mDevice connected in Fastboot mode!\033[0m\n")
                return

            try:
                adb_out = subprocess.check_output(
                    ['adb', 'devices'], 
                    stderr=subprocess.STDOUT
                ).decode('utf-8', errors='ignore').strip()
            except Exception:
                adb_out = ""

            lines = [l for l in adb_out.split('\n')[1:] if l.strip()]
            for line in lines:
                if "\tdevice" in line:
                    sys.stdout.write('\r\033[K')
                    sys.stdout.flush()
                    print("\n\033[93mDevice detected in ADB mode! Rebooting to Fastboot...\033[0m")
                    os.system("adb reboot bootloader >/dev/null 2>&1")
                    time.sleep(3)
                    break
                elif "\tunauthorized" in line:
                    sys.stdout.write("\r Please allow USB Debugging prompt on phone screen! " + char + '\r')
                    sys.stdout.flush()
                    time.sleep(0.2)
                    break
            else:
                sys.stdout.write(message + char + '\r')
                sys.stdout.flush()
                time.sleep(0.2)

def format_script_name(file_name):
    name_lower = file_name.lower()
    if name_lower == "flash_all_lock.sh":
        return "Flash all \033[91mwith lock bootloader\033[0m"
    elif name_lower == "flash_all.sh":
        return "\033[92mFlash all without locking bootloader\033[0m"
    else:
        return file_name

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

    print("\nEnsure target phone is connected...\n")
    check_mode()

    print(f"\n\033[92mExecuting {script_name}...\033[0m\n")
    os.system(f"cd '{target_dir}' && env PATH=\"$PREFIX/bin:$PATH\" bash '{script_name}'")
    sys.exit(0)

def setup_duchamp_scripts_if_needed(target_dir, original_path=""):
    if os.path.exists(f"{target_dir}/flash_all.sh") or os.path.exists(f"{target_dir}/flash_all_lock.sh"):
        return

    check_str = (target_dir + " " + original_path).lower()
    if "duchamp" in check_str:
        if os.path.isdir(os.path.join(target_dir, "img")):
            script_path = os.path.join(target_dir, "Rittik_xpower.sh")
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(RITTIK_XPOWER_CODE)
            os.system(f"chmod +x '{script_path}'")
        elif os.path.isdir(os.path.join(target_dir, "images")):
            script_path = os.path.join(target_dir, "ritik_flash_.sh")
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(RITIK_FLASH_CODE)
            os.system(f"chmod +x '{script_path}'")

def show_flashing_scripts_menu(rom_dir, original_path=""):
    actual_dir = find_working_rom_dir(rom_dir)
    setup_duchamp_scripts_if_needed(actual_dir, original_path)

    all_sh = [f for f in os.listdir(actual_dir) if f.endswith(".sh")]
    all_sh.sort()

    if not all_sh:
        print("\n\033[91m[!] No flashing script (.sh) found in this ROM!\033[0m")
        print(f"\033[93mTarget Folder:\033[0m {actual_dir}")
        print("\033[96mPlease copy your device's flashing script (.sh) into the folder above and rerun the tool.\033[0m\n")
        sys.exit(1)

    print("\n\033[93m--- Available Flashing Scripts (.sh) ---\033[0m")
    for index, file in enumerate(all_sh, start=1):
        print(f" \033[92m{index}\033[0m - {format_script_name(file)}")

    while True:
        choice = input("\nEnter your \033[92mchoice\033[0m: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(all_sh):
            execute_script(actual_dir, all_sh[int(choice) - 1])
        else:
            print("\nInvalid choice! Please select a valid number.")

def decompress_and_flash_rom(archive_file):
    RF = "/sdcard/Download/hybrid-fastboot-rom"
    
    if os.path.exists(RF):
        print("\n\033[93mRemoving previous extracted ROM files...\033[0m")
        shutil.rmtree(RF, ignore_errors=True)

    os.makedirs(RF, exist_ok=True)

    print("\nDecompressing archive, please wait...\n")
    archive_lower = archive_file.lower()

    if archive_lower.endswith((".tgz", ".tar.gz")):
        file_size = os.path.getsize(archive_file)
        cmd = f"pv -s {file_size} '{archive_file}' | tar --strip-components=1 -xz -C '{RF}/' > /dev/null 2>&1"
    elif archive_lower.endswith((".zip", ".7z", ".rar")):
        cmd = f"7z x -y '{archive_file}' -o'{RF}/' -bsp1 -bso0 -bse0"
    else:
        print("\nUnsupported format!\n")
        sys.exit(1)

    return_code = os.system(cmd)
    if return_code != 0:
        print(f"\n\033[91mError during extraction (Exit Code: {return_code})\033[0m\n")
        sys.exit(1)

    print("\n\033[92m✔ Decompression completed successfully!\033[0m\n")

    show_flashing_scripts_menu(RF, archive_file)

# ----------------- Main Scan & Selector -----------------

enforce_mandatory_update()

valid_extensions = (".tgz", ".tar.gz", ".zip", ".7z", ".rar")
ignored_keywords = ["module", "ksun", "magisk", "susfs", "kernel"]

main_items = []

print("\033[93mScanning storage for ROM archives and folders...\033[0m")

for root, dirs, files in os.walk("/sdcard"):
    if "/Android" in root or "/." in root:
        continue
    if any(kw in root.lower() for kw in ignored_keywords):
        continue

    for f in files:
        f_lower = f.lower()
        if f_lower.endswith(valid_extensions):
            if not any(kw in f_lower for kw in ignored_keywords):
                main_items.append({"path": os.path.join(root, f), "type": "archive"})

RF_DIR = "/sdcard/Download/hybrid-fastboot-rom"
if os.path.isdir(RF_DIR):
    main_items.append({"path": RF_DIR, "type": "folder"})

if main_items:
    seen = set()
    unique_items = []
    for item in main_items:
        if item["path"] not in seen:
            seen.add(item["path"])
            unique_items.append(item)

    print(f"\nFound {len(unique_items)} ROM item(s):")
    for i, item in enumerate(unique_items, start=1):
        print(f" \033[92m{i}\033[0m - {item['path']}")

    while True:
        try:
            choice = int(input("\nEnter your \033[92mchoice\033[0m: "))
            if 1 <= choice <= len(unique_items):
                break
            print("\nInvalid choice!")
        except ValueError:
            print("\nInvalid input!")

    selected = unique_items[choice - 1]

    if selected["type"] == "archive":
        decompress_and_flash_rom(selected["path"])
    elif selected["type"] == "folder":
        show_flashing_scripts_menu(selected["path"], selected["path"])

else:
    print("\n\033[91mNo ROM archives or folders found in storage!\033[0m\n")
    
