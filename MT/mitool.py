#!/usr/bin/env python3

import subprocess
import sys
import os

version = "2.0.0"

GOLD = "\033[38;5;220m"
ORANGE = "\033[38;5;208m"
DIM = "\033[38;5;240m"
BOLD = "\033[1m"
RED = "\033[38;5;196m"
GREEN = "\033[38;5;46m"
RESET = "\033[0m"

TOOLS = {
    "1": ("Flash Fastboot / Hybrid ROM", "$PREFIX/bin/miflashf")
}

BANNER = f"""
{GOLD} ___ _ _   _ _  _____           _ 
| _ (_) |_(_) | |_   _|__  ___ | |
|   / |  _| | / / | |/ _ \/ _ \| |
|_|_\_|\__|_|_\_\ |_|\___/\___/|_|{RESET} {DIM}v{version}{RESET}
"""

print(BANNER)
print(f" {DIM}Author: Ritik | Target: Poco X6 Pro (duchamp){RESET}")
print(f" {DIM}{'─' * 44}{RESET}")
print(f" {BOLD}ACTIONS:{RESET}\n")

for key, (desc, _) in TOOLS.items():
    print(f"   {ORANGE}⟨{key}⟩{RESET}  {desc}")
print(f"   {DIM}⟨q⟩  Exit{RESET}\n")

try:
    choice = input(f" {BOLD}{GREEN}❯{RESET} ").strip().lower()
except (KeyboardInterrupt, EOFError):
    print("\n")
    sys.exit(0)

if choice in ['q', 'quit', 'exit']:
    print(f"{DIM}Bye!{RESET}\n")
    sys.exit(0)

if choice in TOOLS:
    desc, cmd = TOOLS[choice]
    print(f"\n{DIM}Running {desc}...{RESET}\n")
    subprocess.run(cmd, shell=True)
else:
    print(f"\n{RED}Invalid choice!{RESET}\n")
    sys.exit(1)
    
