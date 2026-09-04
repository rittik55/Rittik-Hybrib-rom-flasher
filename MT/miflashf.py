#!/usr/bin/python

import os
import sys
import time
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
        return f"{file_name} (\033[91mFirst Install / Clean Flash - Wipes Data\033[0m)"
    elif "update" in name_lower:
        return f"{file_name} (\033[92mUpdate ROM / Dirty Flash - Keeps Data\033[0m)"
    elif "flash_all_except" in name_lower:
        return f"{file_name} (\033[92mFlash All - Keeps Data\033[0m)"
    elif "flash_all" in name_lower or name_lower in ["flash.sh", "install.sh"]:
        return f"{file_name} (\033[92mFull Flash / Clean Flash\033[0m)"
    else:
        return f"\033[93m{file_name}\033[0m (Custom Script)"

def flash_selected_result(selected_result):
    while True:
        try:
            all_files = os.listdir(selected_result)
            found_files = [
                f for f in all_files 
                if f.endswith(".sh") and "lock" not in f.lower()
            ]
        except Exception as e:
            print(f"\nError reading directory: {e}")
            exit()

        if found_files:
            found_files.sort()
            print("\n\033[93m--- Available Flashing Scripts (.sh) ---\033[0m")
            for index, file in enumerate(found_files, start=1):
                translated_name = translate_file_name(file)
                print(f" \033[92m{index}\033[0m - {translated_name}")

            choice = input("\nEnter your \033[92mchoice\033[0m: ").strip()

            if not choice.isdigit():
                print("\nInvalid input! Please enter a valid number.\n")
                continue

            choice = int(choice)

            if 1 <= choice <= len(found_files):
                selected_file = found_files[choice - 1]
                file_path = os.path.join(selected_result, selected_file)

                # Fix Windows CRLF line endings
                os.system(f"sed -i -e 's/\\r$//' '{file_path}' 2>/dev/null")
                os.system(f"chmod +x '{file_path}'")

                # Replace x86 PC fastboot with system fastboot if present
                bin_linux_dir = os.path.join(selected_result, "bin", "linux")
                if os.path.exists(bin_linux_dir):
                    system_fastboot = subprocess.getoutput("which fastboot").strip()
                    if system_fastboot and os.path.exists(system_fastboot):
                        target_bin = os.path.join(bin_linux_dir, "fastboot")
                        os.system(f"rm -f '{target_bin}'")
                        os.system(f"ln -sf '{system_fastboot}' '{target_bin}'")

                print("\nEnsure target phone is connected in Fastboot mode...\n")
                check_mode()

                print(f"\n\033[92mExecuting {selected_file}...\033[0m\n")
                os.system(f"cd '{selected_result}' && env PATH=\"$PREFIX/bin:$PATH\" bash '{selected_file}'")
                exit()
            else:
                print(f"\nInvalid choice! Please select between 1 and {len(found_files)}.\n")
        else:
            print("\n\033[91mNo executable .sh flashing script found in this folder!\033[0m\n")
            exit()

def decompress_and_flash_rom(archive_file):
    RF = "/sdcard/Download/hybrid-fastboot-rom"
    if not os.path.exists(RF):
        os.makedirs(RF)

    print(f"\n\033[92mExtracting ROM archive, please wait...\033[0m\n")
    
    if archive_file.endswith((".tgz", ".tar.gz")):
        cmd = f"pv -bpe '{archive_file}' | tar --strip-components=1 -xzf- -C '{RF}/'"
    elif archive_file.endswith(".zip"):
        cmd = f"unzip -o '{archive_file}' -d '{RF}/'"
    else:
        print("\nUnsupported format!\n")
        exit()

    return_code = os.system(cmd)
    if return_code != 0:
        print(f"\nError during extraction (Exit Code: {return_code})\n")
        exit()

    flash_selected_result(RF)

# ----------------- Main Scan & Selector -----------------

valid_extensions = (".tgz", ".tar.gz", ".zip")
result_paths = []

print("\n\033[93mScanning storage for ROM archives and folders...\033[0m")
for root, dirs, files in os.walk("/sdcard"):
    if "Android" in root:
        continue

    # Find archives
    for f in files:
        if f.endswith(valid_extensions):
            result_paths.append(os.path.join(root, f))

    # Find folders containing any .sh script
    for dir_name in dirs:
        dir_path = os.path.join(root, dir_name)
        try:
            dir_files = os.listdir(dir_path)
            if any(f.endswith(".sh") for f in dir_files):
                result_paths.append(dir_path)
        except PermissionError:
            continue

if result_paths:
    result_paths = list(dict.fromkeys(result_paths))
    
    print(f"\nFound {len(result_paths)} ROM item(s):")
    for i, result in enumerate(result_paths, start=1):
        print(f" \033[92m{i}\033[0m - {result}")

    while True:
        try:
            selected_index = int(input("\nEnter your \033[92mchoice\033[0m: "))
            if 1 <= selected_index <= len(result_paths):
                break
            else:
                print("\nInvalid choice!")
        except ValueError:
            print("\nInvalid input!")

    selected_result = result_paths[selected_index - 1]

    if any(selected_result.endswith(ext) for ext in valid_extensions):
        decompress_and_flash_rom(selected_result)
    elif os.path.isdir(selected_result):
        flash_selected_result(selected_result)

else:
    print("\n\033[91mNo ROM files (.zip, .tgz) or unzipped folders found in /sdcard!\033[0m\n")
