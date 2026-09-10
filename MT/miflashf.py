#!/usr/bin/python

import os
import sys
import time
import shutil
import subprocess

# --- 100% Offline Embedded Custom Scripts (Safe Flasher for Duchamp) ---
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

flash_partition() {
    img_file="$1"
    shift
    if [ -f "$img_file" ]; then
        for part in "$@"; do
            echo "[*] Flashing $part..."
            $fastboot flash "$part" "$img_file"
        done
    fi
}

$fastboot set_active a

flash_partition img/apusys.img apusys_a apusys_b
flash_partition img/audio_dsp.img audio_dsp_a audio_dsp_b
flash_partition img/boot.img boot_a boot_b
flash_partition img/ccu.img ccu_a ccu_b
flash_partition img/connsys_bt.img connsys_bt_a connsys_bt_b
flash_partition img/connsys_gnss.img connsys_gnss_a connsys_gnss_b
flash_partition img/connsys_wifi.img connsys_wifi_a connsys_wifi_b
flash_partition img/dpm.img dpm_a dpm_b
flash_partition img/dtbo.img dtbo_a dtbo_b
flash_partition img/gpueb.img gpueb_a gpueb_b
flash_partition img/gz.img gz_a gz_b
flash_partition img/init_boot.img init_boot_a init_boot_b
flash_partition img/lk.img lk_a lk_b
flash_partition img/logo.img logo_a logo_b
flash_partition img/mcf_ota.img mcf_ota_a mcf_ota_b
flash_partition img/mcupm.img mcupm_a mcupm_b
flash_partition img/modem.img modem_a modem_b
flash_partition img/mvpu_algo.img mvpu_algo_a mvpu_algo_b
flash_partition img/pi_img.img pi_img_a pi_img_b
flash_partition img/preloader_raw.img preloader_a preloader_b
flash_partition img/scp.img scp_a scp_b
flash_partition img/spmfw.img spmfw_a spmfw_b
flash_partition img/sspm.img sspm_a sspm_b
flash_partition img/tee.img tee_a tee_b
flash_partition img/vbmeta.img vbmeta_a vbmeta_b
flash_partition img/vbmeta_system.img vbmeta_system_a vbmeta_system_b
flash_partition img/vbmeta_vendor.img vbmeta_vendor_a vbmeta_vendor_b
flash_partition img/vcp.img vcp_a vcp_b
flash_partition img/vendor_boot.img vendor_boot_a vendor_boot_b

if [ -f img/super.img ]; then
    echo "[*] Flashing super partition (Chunked)..."
    $fastboot -S 256M flash super img/super.img
fi

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

flash_partition() {
    img_file="$1"
    part="$2"
    if [ -f "$img_file" ]; then
        echo "[*] Flashing $part..."
        $fastboot flash "$part" "$img_file"
    fi
}

$fastboot set_active a

flash_partition images/apusys.img apusys_ab
flash_partition images/audio_dsp.img audio_dsp_ab
flash_partition images/ccu.img ccu_ab
flash_partition images/connsys_bt.img connsys_bt_ab
flash_partition images/connsys_gnss.img connsys_gnss_ab
flash_partition images/connsys_wifi.img connsys_wifi_ab
flash_partition images/dpm.img dpm_ab
flash_partition images/dtbo.img dtbo_ab
flash_partition images/gpueb.img gpueb_ab
flash_partition images/gz.img gz_ab
flash_partition images/lk.img lk_ab
flash_partition images/logo.img logo_ab
flash_partition images/mcf_ota.img mcf_ota_ab
flash_partition images/mcupm.img mcupm_ab
flash_partition images/modem.img modem_ab
flash_partition images/mvpu_algo.img mvpu_algo_ab
flash_partition images/pi_img.img pi_img_ab
flash_partition images/scp.img scp_ab
flash_partition images/spmfw.img spmfw_ab
flash_partition images/sspm.img sspm_ab
flash_partition images/tee.img tee_ab
flash_partition images/vbmeta.img vbmeta_ab
flash_partition images/vbmeta_system.img vbmeta_system_ab
flash_partition images/vbmeta_vendor.img vbmeta_vendor_ab
flash_partition images/vcp.img vcp_ab
flash_partition images/boot.img boot_ab
flash_partition images/init_boot.img init_boot_ab
flash_partition images/vendor_boot.img vendor_boot_ab

if [ -f images/super.img ]; then
    echo "[*] Flashing super partition (Chunked)..."
    $fastboot -S 256M flash super images/super.img
fi

$fastboot erase metadata
$fastboot erase frp
$fastboot erase expdb
$fastboot erase userdata
$fastboot oem cdms
$fastboot reboot
"""

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
    elif name_lower == "flash_all_except_storage.sh":
        return "\033[93mFlash all except storage\033[0m"
    else:
        return f"\033[92m{file_name}\033[0m"

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
    if os.path.exists(os.path.join(target_dir, "flash_all.sh")) or os.path.exists(os.path.join(target_dir, "flash_all_lock.sh")):
        return

    check_str = (target_dir + " " + original_path).lower()
    is_duchamp = ("duchamp" in check_str or "wnl" in check_str or 
                  os.path.exists(os.path.join(target_dir, "img", "preloader_raw.img")) or
                  os.path.exists(os.path.join(target_dir, "images", "preloader_raw.img")) or
                  os.path.exists(os.path.join(target_dir, "img", "apusys.img")) or
                  os.path.exists(os.path.join(target_dir, "images", "apusys.img")))

    if is_duchamp:
        if os.path.isdir(os.path.join(target_dir, "img")):
            script_path = os.path.join(target_dir, "Rittik_xpower.sh")
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(RITTIK_XPOWER_CODE)
            os.system(f"chmod +x '{script_path}'")
        elif os.path.isdir(os.path.join(target_dir, "images")):
            script_path = os.path.join(target_dir, "ritik_flash_.sh")
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(RITTIK_FLASH_CODE)
            os.system(f"chmod +x '{script_path}'")

def show_flashing_scripts_menu(rom_dir, original_path=""):
    actual_dir = find_working_rom_dir(rom_dir)
    setup_duchamp_scripts_if_needed(actual_dir, original_path)

    allowed_scripts = ["Rittik_xpower.sh", "ritik_flash_.sh", "flash_all.sh", "flash_all_lock.sh", "flash_all_except_storage.sh"]

    filtered_scripts = [
        f for f in os.listdir(actual_dir)
        if f in allowed_scripts
    ]

    if filtered_scripts:
        display_scripts = filtered_scripts
    else:
        display_scripts = [
            f for f in os.listdir(actual_dir)
            if f.endswith(".sh") and not f.lower().startswith(("linux_", "macos_", "mac_"))
        ]

    display_scripts.sort()

    if not display_scripts:
        print("\n\033[91m[!] No valid Termux flashing script found!\033[0m")
        print(f"\033[93mTarget Folder:\033[0m {actual_dir}")
        print("\033[96mPlease copy your custom flashing script (.sh) into the above folder and rerun.\033[0m\n")
        sys.exit(1)

    print("\n\033[93m--- Available Flashing Scripts (.sh) ---\033[0m")
    for index, file in enumerate(display_scripts, start=1):
        print(f" \033[92m{index}\033[0m - {format_script_name(file)}")

    while True:
        choice = input("\nEnter your \033[92mchoice\033[0m: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(display_scripts):
            execute_script(actual_dir, display_scripts[int(choice) - 1])
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
        cmd = f"pv -s {file_size} '{archive_file}' | tar -xz -C '{RF}/' > /dev/null 2>&1"
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
