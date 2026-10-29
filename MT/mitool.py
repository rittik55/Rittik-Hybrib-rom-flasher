#!/usr/bin/env python3

import subprocess
import sys
import os
import shutil
import time
import urllib.request

version = "2.0.0"

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

# --- GitHub URLs for Auto-Update ---
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

            repo_dir = os.path.expanduser("~/Rittik-Hybrib-rom-flasher")

            # 1. अगर git रिपॉजिटरी मौजूद है, तो git pull से सभी फाइल्स सिंक करो
            if os.path.exists(os.path.join(repo_dir, ".git")):
                subprocess.run(["git", "-C", repo_dir, "reset", "--hard", "HEAD"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.run(["git", "-C", repo_dir, "pull"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # 2. MT फोल्डर और $PREFIX/bin की फाइल्स को सीधे अपडेट करो
            current_dir = os.path.dirname(os.path.realpath(__file__))
            prefix_bin = os.path.expandvars("$PREFIX/bin")

            for script_name in ["mitool.py", "miflashf.py"]:
                target_local = os.path.join(current_dir, script_name)
                urllib.request.urlretrieve(BASE_RAW_MT + script_name, target_local)
                os.chmod(target_local, 0o755)

                # अगर $PREFIX/bin में बिना .py के शॉर्टकट हैं
                bin_short = os.path.join(prefix_bin, script_name.replace(".py", ""))
                if os.path.exists(bin_short):
                    shutil.copy2(target_local, bin_short)
                    os.chmod(bin_short, 0o755)

            print(f"{GREEN}✔ Successfully updated to v{remote_ver}!{RESET}")
            print(f"{GRAY}Restarting tool...{RESET}\n")
            time.sleep(1)

            # नए कोड के साथ टूल को तुरंत रीस्टार्ट करना
            os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception:
        # ऑफलाइन होने या एरर आने पर सामान्य रूप से टूल चलने देगा
        pass

# टूल मेन्यू लोड होने से पहले अपडेट चेक
check_and_apply_update()

TOOLS = {
    "1": ("Flash Fastboot / Hybrid ROM", "$PREFIX/bin/miflashf")
}

try:
    term_width = os.get_terminal_size().columns
except:
    term_width = 80

box_width = min(term_width - 2, 54)

# Fastboot/ADB quick status check
def get_quick_status():
    has_fb = shutil.which("fastboot") or shutil.which("termux-fastboot")
    return f"{GREEN}READY{RESET}" if has_fb else f"{RED}MISSING FASTBOOT{RESET}"

print()
# Header Box
print(f"{PURPLE}╭{'─' * (box_width - 2)}╮{RESET}")
print(f"{PURPLE}│{RESET}  {BOLD}{CYAN}⚡ RITIK TOOL{RESET} {GRAY}v{version}{RESET}" + " " * (box_width - len(f"  ⚡ RITIK TOOL v{version}") - 3) + f"{PURPLE}│{RESET}")
print(f"{PURPLE}│{RESET}  {GRAY}Status: {get_quick_status()}{RESET}" + " " * (box_width - 24) + f"{PURPLE}│{RESET}")
print(f"{PURPLE}├{'─' * (box_width - 2)}┤{RESET}")

# Body / Options
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
    
