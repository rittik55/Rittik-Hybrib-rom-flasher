#!/usr/bin/python

import os
import sys
import time
import shutil
import subprocess

def check_mode():
    spinner = "|/-\\"
    message = "\r Device not connected in Fastboot! "
    while True:
        for char in spinner:
            process = subprocess.Popen(
                ['fastboot', 'devices'], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                encoding="utf-8", 
                errors="ignore"
            )
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                sys.stdout.write(message + char + '\r')
                sys.stdout.flush()
                time.sleep(0.1)
                continue

            if "No permission" in line:
                process.terminate()
                sys.stdout.write(message + char + '\r')
                sys.stdout.flush()
                time.sleep(0.1)
                continue

            sys.stdout.write('\r\033[K')
            sys.stdout.flush()
            print("\n\033[92mDevice connected in Fastboot mode!\033[0m\n")
            return

def translate_file_name(file_name):
    name_lower = file_name.lower()
    
    if "first_install" in name_lower or "format" in name_lower:
        return f"{file_name} (\033[91mClean Flash - Wipes Data\033[0m)"
    elif "update" in name_lower or "dirty" in name_lower:
        return f"{file_name} (\033[92mDirty Flash - Keeps Data\033[0m)"
    elif "flash_all_except" in name_lower:
        return f"{file_name} (\033[92mFlash All - Keeps Data\033[0m)"
    elif "flash_all" in name_lower or name_lower in ["flash.sh", "install.sh"]:
        return f"{file_name} (\033[92mFull Flash / Clean Flash\033[0m)"
    else:
        return f"\033[93m{file_name}\033[0m (Custom Script)"

def execute_script(target_dir, script_name):
    file_path = os.path.join(target_dir, script_name)
    os.system(f"sed -i -e 's/\\r$//' '{file_path}' 2>/dev/null")
    os.system(f"chmod +x '{file_path}'")

    # Fix x86 PC fastboot with system fastboot if needed
    bin_linux_dir = os.path.join(target_dir, "bin", "linux")
    if os.path.exists(bin_linux_dir):
        system_fastboot = subprocess.getoutput("which fastboot").strip()
        if system_fastboot and os.path.exists(system_fastboot):
            target_bin = os.path.join(bin_linux_dir, "fastboot")
            os.system(f"rm -f '{target_bin}'")
            os.system(f"ln -sf '{system_fastboot}' '{target_bin}'")

    print("\nEnsure target phone is connected in Fastboot mode...\n")
    check_mode()

    print(f"\n\033[92mExecuting {script_name}...\033[0m\n")
    os.system(f"cd '{target_dir}' && env PATH=\"$PREFIX/bin:$PATH\" bash '{script_name}'")
    exit()

def show_flashing_scripts_menu(rom_dir):
    ignored_keywords = ["module", "ksun", "magisk", "susfs", "kernel"]

    # 1. Collect all scripts inside the ROM folder
    inside_scripts = [
        f for f in os.listdir(rom_dir) 
        if f.endswith(".sh") and "lock" not in f.lower()
    ]

    # 2. Search for any external standalone scripts outside the ROM folder (e.g. in /sdcard/Download)
    external_scripts = {}
    for root, dirs, files in os.walk("/sdcard"):
        if "/Android" in root or "/." in root or os.path.abspath(root).startswith(os.path.abspath(rom_dir)):
            continue
        if any(kw in root.lower() for kw in ignored_keywords):
            continue

        for f in files:
            if f.endswith(".sh") and "lock" not in f.lower():
                external_scripts[f] = os.path.join(root, f)

    # Copy external scripts into the ROM folder so they can flash images
    for script_name, ext_path in external_scripts.items():
        dest = os.path.join(rom_dir, script_name)
        if not os.path.exists(dest):
            shutil.copy2(ext_path, dest)
        if script_name not in inside_scripts:
            inside_scripts.append(script_name)

    inside_scripts.sort()

    if not inside_scripts:
        print("\n\033[91mNo flashing scripts (.sh) found!\033[0m\n")
        exit()

    print("\n\033[93m--- Available Flashing Scripts (.sh) ---\033[0m")
    for index, file in enumerate(inside_scripts, start=1):
        print(f" \033[92m{index}\033[0m - {translate_file_name(file)}")

    while True:
        choice = input("\nEnter your \033[92mchoice\033[0m: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(inside_scripts):
            execute_script(rom_dir, inside_scripts[int(choice) - 1])
        else:
            print("\nInvalid choice! Please select a valid number.")

def decompress_and_flash_rom(archive_file):
    RF = "/sdcard/Download/hybrid-fastboot-rom"
    if not os.path.exists(RF):
        os.makedirs(RF)

    print(f"\n\033[92mDecompressing ROM archive, please wait...\033[0m\n")
    archive_lower = archive_file.lower()

    if archive_lower.endswith((".tgz", ".tar.gz")):
        file_size = os.path.getsize(archive_file)
        cmd = f"pv -s {file_size} -p -t -e -r -b '{archive_file}' | tar --strip-components=1 -xz -C '{RF}/' > /dev/null 2>&1"
    elif archive_lower.endswith((".zip", ".7z", ".rar")):
        cmd = f"7z x -y '{archive_file}' -o'{RF}/' -bsp1 -bso0 -bse0"
    else:
        print("\nUnsupported format!\n")
        exit()

    return_code = os.system(cmd)
    if return_code != 0:
        print(f"\n\033[91mError during extraction (Exit Code: {return_code})\033[0m\n")
        exit()

    print("\n\033[92m✔ Decompression completed successfully!\033[0m\n")
    show_flashing_scripts_menu(RF)

# ----------------- Main Scan & Selector -----------------

valid_extensions = (".tgz", ".tar.gz", ".zip", ".7z", ".rar")
ignored_keywords = ["module", "ksun", "magisk", "susfs", "kernel"]

main_items = []

print("\n\033[93mScanning storage for ROM archives and folders...\033[0m")

# 1. Scan ONLY for ROM archives (No .sh scripts in main menu)
for root, dirs, files in os.walk("/sdcard"):
    if "/Android" in root or "/." in root:
        continue
    if any(kw in root.lower() for kw in ignored_keywords):
        continue

    for f in files:
        f_lower = f.lower()
        if f_lower.endswith(valid_extensions):
            if not any(kw in f_lower for kw in ignored_keywords):
                main_items.append({"name": f, "path": os.path.join(root, f), "type": "archive"})

# 2. Add extracted ROM folder if it exists
RF_DIR = "/sdcard/Download/hybrid-fastboot-rom"
if os.path.isdir(RF_DIR):
    main_items.append({"name": "hybrid-fastboot-rom", "path": RF_DIR, "type": "folder"})

if main_items:
    # Deduplicate
    seen = set()
    unique_items = []
    for item in main_items:
        if item["path"] not in seen:
            seen.add(item["path"])
            unique_items.append(item)

    print(f"\nFound {len(unique_items)} ROM item(s):")
    for i, item in enumerate(unique_items, start=1):
        if item["type"] == "archive":
            print(f" \033[92m{i}\033[0m - [ROM Archive] {item['name']}")
        else:
            print(f" \033[92m{i}\033[0m - [Extracted ROM Folder] {item['path']}")

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
        show_flashing_scripts_menu(selected["path"])

else:
    print("\n\033[91mNo ROM archives or extracted ROM folders found in storage!\033[0m\n")
    
