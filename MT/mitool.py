#!/usr/bin/env python3

import subprocess
import sys
import os
import shutil
import time
import urllib.request

version = "2.0.1"

# Colors & Formatting
CYAN = "\033[38;5;51m"
PURPLE = "\033[38;5;141m"
ORANGE = "\033[38;5;208m"
GREEN = "\033[38;5;48m"
RED = "\033[38;5;196m"
GRAY = "\033[38;5;242m"
YELLOW = "\033[38;5;220m"
BOLD = "\033[1m"
RESET = "\033[0m"

# --- URLs for Auto-Update ---
VERSION_URL = "https://raw.githubusercontent.com/rittik55/Rittik-Hybrib-rom-flasher/main/version.txt"
BASE_RAW_MT = "https://raw.githubusercontent.com/rittik55/Rittik-Hybrib-rom-flasher/main/MT/"

def check_and_apply_update():
    try:
        req = urllib.request.Request(VERSION_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as resp:
            remote_ver = resp.read().decode('utf-8').strip()

        if remote_ver and remote_ver != version:
            print("\033[H\033[J")
            print(f"{RED}╭───────────────────────────────────────────────────╮{RESET}")
            print(f"{RED}│{RESET}  {BOLD}{YELLOW}⚡ NEW UPDATE DETECTED! [{version} ➔ {remote_ver}]{RESET}")
            print(f"{RED}│{RESET}  {CYAN}Updating tool files, please wait...{RESET}")
            print(f"{RED}╰───────────────────────────────────────────────────╯{RESET}\n")

            prefix_bin = os.path.expandvars("$PREFIX/bin")
            ritiktool_path = os.path.join(prefix_bin, "ritiktool")
            miflashf_path = os.path.join(prefix_bin, "miflashf")

            # Download updated files directly from GitHub into $PREFIX/bin
            urllib.request.urlretrieve(BASE_RAW_MT + "mitool.py", ritiktool_path)
            os.chmod(ritiktool_path, 0o755)

            urllib.request.urlretrieve(BASE_RAW_MT + "miflashf.py", miflashf_path)
            os.chmod(miflashf_path, 0o755)

            print(f"{GREEN}✔ Successfully updated to v{remote_ver}!{RESET}")
            print(f"{GRAY}Restarting tool...{RESET}\n")
            time.sleep(1)

            # Restart tool with new updated code
            os.execv(sys.executable, [sys.executable, ritiktool_path])
    except Exception:
        pass

# Check for updates before rendering menu
check_and_apply_update()

TOOLS = {
    "1": ("Flash Fastboot / Hybrid ROM", "$PREFIX/bin/miflashf")
}

try:
    term_width = os.get_terminal_size().columns
except:
    term_width = 80

box_width = min(term_width - 2, 54)

def get_quick_status():
    has_fb = shutil.which("fastboot") or shutil.which("termux-fastboot")
    return f"{GREEN}READY{RESET}" if has_fb else f"{RED}MISSING FASTBOOT{RESET}"

print()
print(f"{PURPLE}╭{'─' * (box_width - 2)}╮{RESET}")
print(f"{PURPLE}│{RESET}  {BOLD}{CYAN}⚡ RITIK TOOL{RESET} {GRAY}v{version}{RESET}" + " " * (box_width - len(f"  ⚡ RITIK TOOL v{version}") - 3) + f"{PURPLE}│{RESET}")
print(f"{PURPLE}│{RESET}  {GRAY}Status: {get_quick_status()}{RESET}" + " " * (box_width - 24) + f"{PURPLE}│{RESET}")
print(f"{PURPLE}├{'─' * (box_width - 2)}┤{RESET}")

print(f"{PURPLE}│{RESET}  {BOLD}MAIN MENU{RESET}" + " " * (box_width - 13) + f"{PURPLE}│{RESET}")
for key, (desc, _) in TOOLS.items():
    line = f"  {ORANGE}[{key}]{RESET} {desc}"
    pad = box_width - len(f"  [{key}] {desc}") - 2
    print(f"{PURPLE}│{RESET}{line}" + " " * max(0, pad) + f"{PURPLE}│{RESET}")

q_line = f"  {GRAY}[q] Exit Console{RESET}"
pad_q = box_width - len("  [q] Exit Console") - 2
print(f"{PURPLE}│{RESET}{q_line}" + " " * max(0, pad_q) + f"{PURPLE}│{RESET}")
print(f"{PURPLE}╰{'─' * (box_width - 2)}╯{RESET}\n")

if len(sys.argv) > 1:
    choice = sys.argv[1].lower()
else:
    try:
        choice = input(f" {BOLD}{CYAN}ritik@termux{RESET}{GRAY}:{RESET}{ORANGE}~${RESET} ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{GRAY}Operation aborted.{RESET}\n")
        sys.exit(0)

if choice in ['q', 'quit', 'exit']:
    print(f"{GRAY}Closing launcher...{RESET}\n")
    sys.exit(0)

if choice in TOOLS:
    desc, cmd = TOOLS[choice]
    print(f"\n{GRAY}↳ Launching {desc}...{RESET}\n")
    subprocess.run(cmd, shell=True)
else:
    print(f"\n{RED}✖ Invalid selection:{RESET} '{choice}'\n")
    sys.exit(1)
    
