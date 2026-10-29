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

# --- Universal Header & Branding Template (100% Offline) ---
RITIK_TERMUX_HEADER = r"""#!/data/data/com.termux/files/usr/bin/sh
cd "$(dirname "$0")" || exit 1

if command -v termux-fastboot >/dev/null 2>&1; then
    fastboot="termux-fastboot"
elif command -v fastboot >/dev/null 2>&1; then
    fastboot="fastboot"
elif [ -f "./bin/linux/fastboot" ]; then
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
echo "        ROM FLASH TOOL                  "
echo "----------------------------------------"
echo "=================================================="

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

def auto_convert_pc_script_to_termux(src_path, dest_path):
    try:
        with open(src_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        body_lines = []
        start_capturing = False
        has_waiting_mark = any("waiting for device" in line.lower() for line in lines)

        for idx, line in enumerate(lines):
            line_clean = line.replace('\r', '')

            if any(bad in line_clean for bad in ["fastboot=bin/linux", "[ ! -f $fastboot ]", "[ ! -x $fastboot ]", "fastboot cannot be executed"]):
                continue

            if has_waiting_mark:
                if "waiting for device" in line_clean.lower():
                    start_capturing = True
                if start_capturing:
                    line_clean = line_clean.replace('./fastboot', '$fastboot')
                    line_clean = line_clean.replace('./linux/fastboot', '$fastboot')
                    line_clean = line_clean.replace('./bin/fastboot', '$fastboot')
                    line_clean = line_clean.replace('$PWD/fastboot', '$fastboot')
                    line_clean = line_clean.replace('fastboot.exe', '$fastboot')
                    body_lines.append(line_clean)
            else:
                if idx == 0 and line_clean.startswith("#!"):
                    continue
                line_clean = line_clean.replace('./fastboot', '$fastboot')
                line_clean = line_clean.replace('./linux/fastboot', '$fastboot')
                line_clean = line_clean.replace('./bin/fastboot', '$fastboot')
                line_clean = line_clean.replace('$PWD/fastboot', '$fastboot')
                line_clean = line_clean.replace('fastboot.exe', '$fastboot')
                body_lines.append(line_clean)

        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(RITIK_TERMUX_HEADER)
            f.writelines(body_lines)

        os.system(f"chmod +x '{dest_path}'")
        return True
    except Exception:
        return False

def scan_and_prepare_scripts(target_dir):
    for f in os.listdir(target_dir):
        f_lower = f.lower()

        # Ignore official ROM scripts (flash_all)
        if f_lower.startswith("flash_all"):
            continue

        # Handle custom ROM scripts (Checking content inside .sh)
        if f_lower.endswith(".sh") and not f.startswith("termux_"):
            src = os.path.join(target_dir, f)
            try:
                with open(src, 'r', encoding='utf-8', errors='ignore') as check_f:
                    content = check_f.read().lower()
            except Exception:
                content = ""

            # Check if it actually contains linux or bin/linux paths
            if "linux" in content or "bin/linux" in content:
                if "clean" in f_lower:
                    out_name = "termux_CleanFlash.sh"
                elif "dirty" in f_lower:
                    out_name = "termux_DirtyFlash.sh"
                else:
                    # Universal fallback for any custom named script
                    out_name = f"termux_{f}"

                dst = os.path.join(target_dir, out_name)
                auto_convert_pc_script_to_termux(src, dst)

def get_valid_scripts(target_dir):
    valid = []
    for f in os.listdir(target_dir):
        # Auto-generated custom ROM scripts
        if f.startswith("termux_") and f.endswith(".sh"):
            valid.append(f)
        # Official ROM original scripts
        elif f.lower().startswith("flash_all") and f.endswith(".sh"):
            valid.append(f)
    return valid

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

def show_flashing_scripts_menu(rom_dir, original_path=""):
    actual_dir = find_working_rom_dir(rom_dir)
    scan_and_prepare_scripts(actual_dir)

    while True:
        display_scripts = get_valid_scripts(actual_dir)
        display_scripts.sort()

        if display_scripts:
            break

        print(f"\n{RED}╭─ [!] No Flashing Script Found In ROM ─────────────╮{RESET}")
        print(f"{RED}│{RESET}  {YELLOW}No compatible flashing script detected.{RESET}")
        print(f"{RED}├───────────────────────────────────────────────────┤{RESET}")
        print(f"{RED}│{RESET}  {BOLD}Target Directory:{RESET}")
        print(f"{RED}│{RESET}  {CYAN}{actual_dir}{RESET}")
        print(f"{RED}├───────────────────────────────────────────────────┤{RESET}")
        print(f"{RED}│{RESET}  {GREEN}Action Required:{RESET}")
        print(f"{RED}│{RESET}  Paste your script (.sh) inside the target directory.")
        print(f"{RED}╰───────────────────────────────────────────────────╯")
        
        input(f"\n {BOLD}{YELLOW}Press [Enter] after pasting the file (or Ctrl+C to abort)...{RESET}")
        scan_and_prepare_scripts(actual_dir)

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
