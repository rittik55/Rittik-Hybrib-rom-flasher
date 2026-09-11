#!/usr/bin/env python3

import subprocess
import sys
import os
import shutil

version = "2.0.0"

# Colors & Formatting
CYAN = "\033[38;5;51m"
PURPLE = "\033[38;5;141m"
ORANGE = "\033[38;5;208m"
GREEN = "\033[38;5;48m"
RED = "\033[38;5;196m"
GRAY = "\033[38;5;242m"
BOLD = "\033[1m"
RESET = "\033[0m"

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
    
