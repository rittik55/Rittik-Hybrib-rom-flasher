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

    # Fix x86 fastboot binary with Termux arm fastboot if exists
    bin_linux_dir = os.path.join(target_dir, "bin", "linux")
    if os.path.exists(bin_linux_dir):
        system_fastboot = subprocess.getoutput("which fastboot").strip()
        if system_fastboot and os.path.exists(system_fastboot):
            target_bin = os.path.join(bin_linux_dir, "fastboot")
            os.system(f"rm -f '{target_bin}'")
            os.system(f"ln -sf '{system_fastboot}' '{target_bin}'")

    print("\nEnsure target phone is connected in Fastboot mode...\n")
    check_mode()

    print(f"\n\033[92mExecuting {script_name} from {target_dir}...\033[0m\n")
    os.system(f"cd '{target_dir}' && env PATH=\"$PREFIX/bin:$PATH\" bash '{script_name}'")
    exit()

def find_best_rom_directory():
    # 1. First priority: Default extracted folder
    default_dir = "/sdcard/Download/hybrid-fastboot-rom"
    if os.path.isdir(default_dir):
        return default_dir

    # 2. Look for any directory having images/ folder or .img files
    for root, dirs, files in os.walk("/sdcard"):
        if "/Android" in root or "/." in root:
            continue
        if "images" in dirs or any(f.endswith(".img") for f in files):
            return root

    return None

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
    
    # Check scripts inside extracted folder
    all_files = os.listdir(RF)
    sh_files = [f for f in all_files if f.endswith(".sh") and "lock" not in f.lower()]
    if sh_files:
        sh_files.sort()
        print("\n\033[93m--- Available Flashing Scripts (.sh) ---\033[0m")
        for idx, f in enumerate(sh_files, start=1):
            print(f" \033[92m{idx}\033[0m - {translate_file_name(f)}")
        
        while True:
            try:
                ch = int(input("\nEnter your \033[92mchoice\033[0m: "))
                if 1 <= ch <= len(sh_files):
                    execute_script(RF, sh_files[ch - 1])
                print("\nInvalid choice!")
            except ValueError:
                print("\nInvalid input!")
    else:
        print("\n\033[91mNo .sh scripts found inside extracted folder!\033[0m\n")
        exit()

# ----------------- Main Scan & Selector -----------------

valid_extensions = (".tgz", ".tar.gz", ".zip", ".7z", ".rar")
ignored_keywords = ["module", "ksun", "magisk", "susfs", "kernel"]

items_list = []

print("\n\033[93mScanning storage for ROM archives and .sh scripts...\033[0m")

for root, dirs, files in os.walk("/sdcard"):
    if "/Android" in root or "/." in root:
        continue

    if any(kw in root.lower() for kw in ignored_keywords):
        continue

    for f in files:
        f_lower = f.lower()

        # 1. ROM Archives
        if f_lower.endswith(valid_extensions):
            if not any(kw in f_lower for kw in ignored_keywords):
                full_path = os.path.join(root, f)
                items_list.append({"name": f, "path": full_path, "type": "archive"})

        # 2. Standalone .sh scripts found anywhere
        elif f_lower.endswith(".sh") and "lock" not in f_lower:
            full_path = os.path.join(root, f)
            items_list.append({"name": f, "path": full_path, "type": "script"})

# Also show extracted ROM folder if it exists
RF_DIR = "/sdcard/Download/hybrid-fastboot-rom"
if os.path.isdir(RF_DIR) and any(f.endswith(".sh") for f in os.listdir(RF_DIR)):
    items_list.append({"name": "hybrid-fastboot-rom", "path": RF_DIR, "type": "folder"})

if items_list:
    # Deduplicate
    seen = set()
    unique_items = []
    for item in items_list:
        if item["path"] not in seen:
            seen.add(item["path"])
            unique_items.append(item)

    print(f"\nFound {len(unique_items)} Item(s):")
    for i, item in enumerate(unique_items, start=1):
        if item["type"] == "script":
            print(f" \033[92m{i}\033[0m - [Custom Script] {item['name']}  \033[90m({item['path']})\033[0m")
        elif item["type"] == "archive":
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

    # Action 1: ROM Archive selected -> Decompress & Flash
    if selected["type"] == "archive":
        decompress_and_flash_rom(selected["path"])

    # Action 2: Standalone .sh script selected
    elif selected["type"] == "script":
        script_full_path = selected["path"]
        script_name = selected["name"]
        rom_dir = find_best_rom_directory()

        if rom_dir:
            # If the script is outside the ROM folder, copy it inside
            if os.path.abspath(os.path.dirname(script_full_path)) != os.path.abspath(rom_dir):
                target_script = os.path.join(rom_dir, script_name)
                shutil.copy2(script_full_path, target_script)
                print(f"\n\033[92mCopied {script_name} to ROM directory: {rom_dir}\033[0m")
            execute_script(rom_dir, script_name)
        else:
            # If no ROM folder detected, execute from its current location
            execute_script(os.path.dirname(script_full_path), script_name)

    # Action 3: Already extracted ROM folder selected
    elif selected["type"] == "folder":
        all_files = os.listdir(selected["path"])
        sh_files = [f for f in all_files if f.endswith(".sh") and "lock" not in f.lower()]
        sh_files.sort()
        print("\n\033[93m--- Available Flashing Scripts (.sh) ---\033[0m")
        for idx, f in enumerate(sh_files, start=1):
            print(f" \033[92m{idx}\033[0m - {translate_file_name(f)}")
        
        while True:
            try:
                ch = int(input("\nEnter your \033[92mchoice\033[0m: "))
                if 1 <= ch <= len(sh_files):
                    execute_script(selected["path"], sh_files[ch - 1])
                print("\nInvalid choice!")
            except ValueError:
                print("\nInvalid input!")

else:
    print("\n\033[91mNo ROM archives or .sh scripts found in storage!\033[0m\n")
    
