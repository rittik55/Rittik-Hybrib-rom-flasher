#!/usr/bin/env python3

import subprocess
import sys
import os

version = "2.0.0"

ORANGE = "\033[38;5;208m"
BLUE = "\033[38;5;75m"
DIM = "\033[2m"
BOLD = "\033[1m"
RED = "\033[1;31m"
GREEN = "\033[1;32m"
RESET = "\033[0m"

TOOLS = {
    "1": ("Flash Fastboot / Hybrid ROM", "$PREFIX/bin/miflashf")
}

width = 48

print()
print(f"{BLUE}●{RESET} {BOLD}RitikTool CLI{RESET} {DIM}(duchamp core v{version}){RESET}")
print(f"{DIM}{'─' * width}{RESET}")

for key, (desc, _) in TOOLS.items():
    print(f" {GREEN}{key}.{RESET} {desc}")
print(f" {DIM}q.{RESET} {DIM}Quit{RESET}")

print(f"{DIM}{'─' * width}{RESET}")

try:
    choice = input(f"{ORANGE}Select option » {RESET}").strip().lower()
except (KeyboardInterrupt, EOFError):
    print(f"\n{DIM}Aborted.{RESET}\n")
    sys.exit(0)

if choice in ['q', 'quit', 'exit']:
    sys.exit(0)

if choice in TOOLS:
    desc, cmd = TOOLS[choice]
    print(f"\n{DIM}Executing: {cmd}{RESET}\n")
    subprocess.run(cmd, shell=True)
else:
    print(f"\n{RED}Error:{RESET} Unknown command '{choice}'\n")
    sys.exit(1)
    
