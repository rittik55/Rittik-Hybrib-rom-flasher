#!/usr/bin/env python3

import subprocess
import sys
import os
import time

version = "2.1.3"

ORANGE = "\033[38;5;208m"
DIM = "\033[2m"
BOLD = "\033[1m"
RED = "\033[1;31m"
GREEN = "\033[1;32m"
RESET = "\033[0m"

try:
    term_width = os.get_terminal_size().columns
except:
    term_width = 80

def get_center(text):
    clean = text.replace(ORANGE, '').replace(RESET, '').replace(DIM, '').replace(BOLD, '').replace(GREEN, '').replace(RED, '')
    pad = max(0, (term_width - len(clean)) // 2)
    return ' ' * pad + text

def check_sideload_device():
    dots = [".  ", ".. ", "..."]
    base_msg = f"{ORANGE}[*] Waiting for target device in ADB Sideload mode{RESET}"
    idx = 0
    while True:
        try:
            output = subprocess.check_output(['adb', 'devices'], stderr=subprocess.STDOUT).decode('utf-8', errors='ignore').strip()
        except Exception:
            output = ""

        if output and "sideload" in output.lower():
            sys.stdout.write('\r\033[K')
            sys.stdout.flush()
            print(f"\n{GREEN}✔ Target Device connected in Sideload mode!{RESET}\n")
            return

        sys.stdout.write(f"\r{base_msg}{dots[idx % 3]}")
        sys.stdout.flush()
        idx += 1
        time.sleep(0.6)

def run_adb_sideload_launcher():
    print(f"\n{ORANGE}Scanning storage for Recovery ROM (.zip) files...{RESET}")
    ignored_keywords = ["module", "ksun", "magisk", "susfs", "kernel", "magic"]
    zip_files = []

    for root, dirs, files in os.walk("/sdcard"):
        if "/Android" in root or "/." in root:
            continue
        for f in files:
            if f.lower().endswith(".zip"):
                if not any(kw in f.lower() for kw in ignored_keywords):
                    full_path = os.path.join(root, f)
                    try:
                        if os.path.getsize(full_path) > 500 * 1024 * 1024:
                            zip_files.append(full_path)
                    except OSError:
                        pass

    if not zip_files:
        print(f"\n{RED}✗ No valid Recovery ROM files found (>500MB) in storage!{RESET}\n")
        sys.exit(1)

    zip_files = list(set(zip_files))
    print(f"\n{GREEN}Found {len(zip_files)} Recovery ROM(s):{RESET}")
    for i, file_path in enumerate(zip_files, start=1):
        file_size_gb = os.path.getsize(file_path) / (1024 * 1024 * 1024)
        print(f"  {DIM}▸{RESET} [{ORANGE}{i}{RESET}] {os.path.basename(file_path)} {DIM}({file_size_gb:.2f} GB){RESET}")

    while True:
        try:
            choice = input(f"\n{BOLD}►{RESET} Select ROM number: ").strip()
            idx = int(choice)
            if 1 <= idx <= len(zip_files):
                selected_zip = zip_files[idx - 1]
                break
            print(f"{RED}Invalid number!{RESET}")
        except (ValueError, KeyboardInterrupt):
            print(f"\n{RED}Cancelled.{RESET}\n")
            sys.exit(0)

    print(f"\n{BOLD}Selected ROM:{RESET} {GREEN}{os.path.basename(selected_zip)}{RESET}")
    print(f"{DIM}1. Put Target phone in Recovery -> Advanced -> ADB Sideload{RESET}")
    print(f"{DIM}2. Connect with OTG Cable{RESET}\n")

    check_sideload_device()

    print(f"{GREEN}Executing: adb sideload '{os.path.basename(selected_zip)}'...{RESET}\n")
    print(f"{DIM}{'─' * min(term_width, 70)}{RESET}\n")
    subprocess.run(f"adb sideload '{selected_zip}'", shell=True)
    print(f"\n{GREEN}✔ Process finished successfully!{RESET}\n")
    sys.exit(0)

TOOLS = {
    "1": ("Flash Fastboot / Hybrid ROM", "$PREFIX/bin/miflashf"),
    "2": ("Flash Recovery ROM (ADB Sideload)", "CUSTOM_SIDELOAD")
}

print("\n")
print(get_center(f"{DIM}{'═' * min(term_width, 70)}{RESET}"))

title = f"RitikTool v{version}"
box_width = len(title) + 4
print(get_center(f"┏{'━' * (box_width - 2)}┓"))
print(get_center(f"┃  {ORANGE}RitikTool{RESET} {DIM}v{version}{RESET}  ┃"))
print(get_center(f"┗{'━' * (box_width - 2)}┛"))

print(get_center(f"{DIM}Developed by Ritik{RESET}"))
print(get_center(f"{DIM}{'═' * min(term_width, 70)}{RESET}"))
print()

print(f"{BOLD}Available Operations:{RESET}\n")
for key, (desc, _) in TOOLS.items():
    print(f"  {DIM}▸{RESET} [{ORANGE}{key}{RESET}] {desc}")
print(f"\n  {DIM}▸{RESET} [{ORANGE}q{RESET}] Quit\n")

if len(sys.argv) > 1:
    choice = sys.argv[1].lower()
    print(f"{ORANGE}►{RESET} Selected: {ORANGE}{choice}{RESET}\n")
else:
    try:
        choice = input(f"{BOLD}►{RESET} Enter choice: ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        print(f"\n\n{ORANGE}Cancelled{RESET}")
        sys.exit(0)

if choice in ['q', 'quit', 'exit']:
    print(f"{ORANGE}Exiting...{RESET}\n")
    sys.exit(0)

if choice in TOOLS:
    desc, cmd = TOOLS[choice]
    if cmd == "CUSTOM_SIDELOAD":
        run_adb_sideload_launcher()
    else:
        print(f"\n{ORANGE}►{RESET} Executing: {DIM}{cmd}{RESET}\n")
        print(f"{DIM}{'─' * min(term_width, 70)}{RESET}\n")
        subprocess.run(cmd, shell=True)
else:
    print(f"{RED}✗ Invalid:{RESET} '{choice}'")
    print(f"{DIM}Select 1, 2 or 'q' to quit{RESET}\n")
    sys.exit(1)
    
