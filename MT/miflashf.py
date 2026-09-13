#!/usr/bin/python

import os
import sys
import time
import shutil
import subprocess

# --- Modern UI Styles & 256-Colors ---
ORANGE = "\033[38;5;208m"
CYAN   = "\033[38;5;51m"
GREEN  = "\033[38;5;48m"
RED    = "\033[38;5;196m"
GRAY   = "\033[38;5;242m"
YELLOW = "\033[38;5;220m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

# --- 100% Offline Embedded Custom Scripts (For Duchamp) ---
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

def format_size(size_bytes):
    if size_bytes >= 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
    elif size_bytes >= 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    return f"{size_bytes} B"

def flatten_extracted_folder(target_dir):
    while True:
        items = os.listdir(target_dir)
        if len(items) == 1 and os.path.isdir(os.path.join(target_dir, items[0])):
            nested = os.path.join(target_dir, items[0])
            for item in os.listdir(nested):
                shutil.move(os.path.join(nested, item), target_dir)
            os.rmdir(nested)
            continue
        break

def find_working_rom_dir(base_dir):
    flatten_extracted_folder(base_dir)
    for root, dirs, files in os.walk(base_dir):
        if "img" in dirs or "images" in dirs or any(f.endswith(".sh") for f in files):
            return root
    return base_dir

def check_mode():
    spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    idx = 0
    message = f" {CYAN}⚡{RESET} {GRAY}Waiting for Fastboot / ADB device...{RESET} "
    while True:
        char = spinner[idx % len(spinner)]
        idx += 1
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
                time.sleep(0.1)
                continue

            sys.stdout.write('\r\033[K')
            sys.stdout.flush()
            print(f"\n {GREEN}✔ Device connected in Fastboot mode!{RESET}\n")
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
                print(f"\n {YELLOW}⚡ Device detected in ADB mode! Rebooting to Fastboot...{RESET}")
                os.system("adb reboot bootloader >/dev/null 2>&1")
                time.sleep(3)
                break
            elif "\tunauthorized" in line:
                sys.stdout.write(f"\r {RED}! Please allow USB Debugging prompt on phone screen!{RESET} " + char + '\r')
                sys.stdout.flush()
                time.sleep(0.1)
                break
        else:
            sys.stdout.write(message + char + '\r')
            sys.stdout.flush()
            time.sleep(0.1)

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

    print(f"\n {GRAY}Ensure target phone is connected via OTG...{RESET}")
    check_mode()

    print(f" {GREEN}▶ Executing script:{RESET} {BOLD}{script_name}{RESET}\n")
    print(f"{GRAY}{'─' * 50}{RESET}\n")
    os.system(f"cd '{target_dir}' && env PATH=\"$PREFIX/bin:$PATH\" bash '{script_name}'")
    sys.exit(0)

def setup_duchamp_scripts_if_needed(target_dir, original_path=""):
    # अगर पहले से कोई टर्मक्स फ्लैश स्क्रिप्ट मौजूद है, तो जबरन ओवरराइट नहीं करेगा
    existing = [f for f in os.listdir(target_dir) if f.endswith(".sh") and not f.lower().startswith(("linux_", "macos_", "mac_"))]
    if existing:
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
                f.write(RITIK_FLASH_CODE)
            os.system(f"chmod +x '{script_path}'")

def get_valid_scripts(target_dir):
    # केवल वही स्क्रिप्ट दिखाएगा जो Termux में चलने लायक हैं (PC वाली को फ़िल्टर करेगा)
    return [
        f for f in os.listdir(target_dir)
        if f.endswith(".sh") and not f.lower().startswith(("linux_", "macos_", "mac_"))
    ]

def show_flashing_scripts_menu(rom_dir, original_path=""):
    actual_dir = find_working_rom_dir(rom_dir)
    setup_duchamp_scripts_if_needed(actual_dir, original_path)

    while True:
        display_scripts = get_valid_scripts(actual_dir)
        display_scripts.sort()

        if display_scripts:
            break

        # अगर कोई भी .sh स्क्रिप्ट नहीं मिली तो क्रैश नहीं होगा, बल्कि लाइव वेट करेगा
        print(f"\n{RED}╭─ [!] No Flashing Script Found In ROM ─────────────╮{RESET}")
        print(f"{RED}│{RESET}  {YELLOW}इस ROM में कोई भी Termux (.sh) स्क्रिप्ट नहीं मिली।{RESET}")
        print(f"{RED}├───────────────────────────────────────────────────┤{RESET}")
        print(f"{RED}│{RESET}  {BOLD}ROM फ़ोल्डर का पाथ (Target Path):{RESET}")
        print(f"{RED}│{RESET}  {CYAN}{actual_dir}{RESET}")
        print(f"{RED}├───────────────────────────────────────────────────┤{RESET}")
        print(f"{RED}│{RESET}  {GREEN}आप क्या कर सकते हैं:{RESET}")
        print(f"{RED}│{RESET}  अपनी कस्टम स्क्रिप्ट (जैसे: Termux_CleanFlash.sh)")
        print(f"{RED}│{RESET}  सीधे ऊपर दिए गए फ़ोल्डर में पेस्ट कर दें।")
        print(f"{RED}╰───────────────────────────────────────────────────╯")
        
        input(f"\n {BOLD}{YELLOW}फ़ाइल पेस्ट करने के बाद [Enter] दबाएँ (या Cancel के लिए Ctrl+C)...{RESET}")

    print(f"\n{ORANGE}╭─ Available Flashing Scripts{RESET}")
    for index, file in enumerate(display_scripts, start=1):
        print(f"{ORANGE}│{RESET}  [{GREEN}{index}{RESET}] {file}")
    print(f"{ORANGE}╰────────────────────────────{RESET}")

    while True:
        try:
            choice = input(f"\n {BOLD}{CYAN}select script ❯{RESET} ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(display_scripts):
                execute_script(actual_dir, display_scripts[int(choice) - 1])
            else:
                print(f" {RED}Invalid choice! Enter a number between 1 and {len(display_scripts)}{RESET}")
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n {GRAY}Flashing cancelled.{RESET}\n")
            sys.exit(0)

def decompress_and_flash_rom(archive_file):
    RF = "/sdcard/Download/hybrid-fastboot-rom"
    
    if os.path.exists(RF):
        print(f"\n {GRAY}Clearing previous temporary extracted files...{RESET}")
        shutil.rmtree(RF, ignore_errors=True)

    os.makedirs(RF, exist_ok=True)

    print(f"\n {CYAN}⚡ Decompressing archive, please wait...{RESET}\n")
    archive_lower = archive_file.lower()

    if archive_lower.endswith((".tgz", ".tar.gz")):
        file_size = os.path.getsize(archive_file)
        cmd = f"pv -s {file_size} '{archive_file}' | tar --strip-components=1 -xz -C '{RF}/' > /dev/null 2>&1"
    elif archive_lower.endswith((".zip", ".7z", ".rar")):
        cmd = f"7z x -y '{archive_file}' -o'{RF}/' -bsp1 -bso0 -bse0"
    else:
        print(f"\n {RED}Unsupported archive format!{RESET}\n")
        sys.exit(1)

    return_code = os.system(cmd)
    if return_code != 0:
        print(f"\n {RED}✖ Error during decompression (Code: {return_code}){RESET}\n")
        sys.exit(1)

    flatten_extracted_folder(RF)
    print(f"\n {GREEN}✔ Decompression completed successfully!{RESET}")

    show_flashing_scripts_menu(RF, archive_file)

# ----------------- Main Scan & Selector -----------------

valid_extensions = (".tgz", ".tar.gz", ".zip", ".7z", ".rar")
ignored_keywords = ["module", "ksun", "magisk", "susfs", "kernel"]

main_items = []

print(f"\n {GRAY}Scanning storage for ROM archives and folders...{RESET}")

for root, dirs, files in os.walk("/sdcard"):
    if "/Android" in root or "/." in root:
        continue
    if any(kw in root.lower() for kw in ignored_keywords):
        continue

    for f in files:
        f_lower = f.lower()
        if f_lower.endswith(valid_extensions):
            if not any(kw in f_lower for kw in ignored_keywords):
                full_p = os.path.join(root, f)
                main_items.append({"path": full_p, "type": "archive", "name": f, "size": os.path.getsize(full_p)})

RF_DIR = "/sdcard/Download/hybrid-fastboot-rom"
if os.path.isdir(RF_DIR):
    main_items.append({"path": RF_DIR, "type": "folder", "name": "hybrid-fastboot-rom", "size": 0})

if main_items:
    seen = set()
    unique_items = []
    for item in main_items:
        if item["path"] not in seen:
            seen.add(item["path"])
            unique_items.append(item)

    print(f"\n{CYAN}╭─ Detected ROMs ({len(unique_items)}){RESET}")
    for i, item in enumerate(unique_items, start=1):
        if item["type"] == "archive":
            size_str = format_size(item["size"])
            ext = item["name"].split('.')[-1].upper()
            badge = f"{YELLOW}[{ext} • {size_str}]{RESET}"
            print(f"{CYAN}│{RESET}  {ORANGE}[{i}]{RESET} {item['name']} {badge}")
            print(f"{CYAN}│{RESET}      {GRAY}↳ {item['path']}{RESET}")
        else:
            badge = f"{GREEN}[EXTRACTED FOLDER]{RESET}"
            print(f"{CYAN}│{RESET}  {ORANGE}[{i}]{RESET} {item['name']} {badge}")
            print(f"{CYAN}│{RESET}      {GRAY}↳ {item['path']}{RESET}")
    print(f"{CYAN}╰─────────────────────────────────────────{RESET}")

    while True:
        try:
            choice = input(f"\n {BOLD}{CYAN}select ROM ❯{RESET} ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(unique_items):
                selected = unique_items[int(choice) - 1]
                break
            print(f" {RED}Invalid choice! Enter a number between 1 and {len(unique_items)}{RESET}")
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n {GRAY}Aborted.{RESET}\n")
            sys.exit(0)

    if selected["type"] == "archive":
        decompress_and_flash_rom(selected["path"])
    elif selected["type"] == "folder":
        show_flashing_scripts_menu(selected["path"], selected["path"])

else:
    print(f"\n {RED}✖ No ROM archives or extracted folders found in storage!{RESET}\n")
