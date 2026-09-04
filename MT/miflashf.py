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
            try:
                output = subprocess.check_output(
                    ['fastboot', 'devices'], 
                    stderr=subprocess.STDOUT
                ).decode('utf-8', errors='ignore').strip()
            except Exception:
                output = ""

            if output and "fastboot" in output.lower():
                if "no permission" in output.lower():
                    sys.stdout.write(message + char + '\r')
                    sys.stdout.flush()
                    time.sleep(0.2)
                    continue

                sys.stdout.write('\r\033[K')
                sys.stdout.flush()
                print("\n\033[92mDevice connected in Fastboot mode!\033[0m\n")
                return
            else:
                sys.stdout.write(message + char + '\r')
                sys.stdout.flush()
                time.sleep(0.2)

def translate_file_name(file_name):
    name_lower = file_name.lower()
    
    if "first_install" in name_lower or "format" in name_lower or "clean" in name_lower or "xpower" in name_lower:
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
    # सिर्फ आपकी दोनों स्क्रिप्ट्स ही लिस्ट में आएँगी
    allowed_scripts = ["Rittik_xpower.sh", "ritik_flash_.sh"]

    inside_scripts = [
        f for f in os.listdir(rom_dir) 
        if f in allowed_scripts
    ]

    inside_scripts.sort()

    if not inside_scripts:
        print("\n\033[91mNo custom flasher scripts found!\033[0m\n")
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
    
    if os.path.exists(RF):
        print(f"\n\033[93mRemoving previous extracted ROM files...\033[0m")
        shutil.rmtree(RF, ignore_errors=True)

    os.makedirs(RF, exist_ok=True)

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

    print("\033[93mAdding custom flasher scripts to ROM folder...\033[0m")
    os.system(f"curl -fsS 'https://raw.githubusercontent.com/rittik55/Rittik-Hybrib-rom-flasher/main/Rittik_xpower.sh' -o '{RF}/Rittik_xpower.sh' > /dev/null 2>&1")
    os.system(f"curl -fsS 'https://raw.githubusercontent.com/rittik55/Rittik-Hybrib-rom-flasher/main/ritik_flash_.sh' -o '{RF}/ritik_flash_.sh' > /dev/null 2>&1")

    show_flashing_scripts_menu(RF)

# ----------------- Main Scan & Selector -----------------

valid_extensions = (".tgz", ".tar.gz", ".zip", ".7z", ".rar")
ignored_keywords = ["module", "ksun", "magisk", "susfs", "kernel"]

main_items = []

print("\n\033[93mScanning storage for ROM archives and folders...\033[0m")

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
        show_flashing_scripts_menu(selected["path"])

else:
    print("\n\033[91mNo ROM archives or folders found in storage!\033[0m\n")
    
