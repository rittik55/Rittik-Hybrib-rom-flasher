#!/usr/bin/env python3

import os
import re
import shutil
import subprocess
import sys

VERSION = "2.1.0"
AUTHOR = "Ritik"

# Color Palette (ANSI 256 / Standard)
ORANGE = "\033[38;5;208m"
CYAN = "\033[38;5;45m"
GREEN = "\033[1;32m"
RED = "\033[1;31m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

# Registered Operations: "Key": ("Display Title", "Description", "Command")
TOOLS = {
    "1": (
        "Flash Fastboot / Hybrid ROM",
        "Flash official fastboot or hybrid firmware packages",
        "$PREFIX/bin/miflashf"
    ),
}

def get_terminal_width():
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80

def strip_ansi(text: str) -> str:
    """Accurately removes ANSI escape sequences for alignment calculations."""
    ansi_regex = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_regex.sub('', text)

def center_text(text: str, width: int = None) -> str:
    if width is None:
        width = get_terminal_width()
    visible_length = len(strip_ansi(text))
    pad = max(0, (width - visible_length) // 2)
    return (' ' * pad) + text

def render_banner():
    width = min(get_terminal_width(), 60)
    inner_width = width - 4

    app_name = f"RITIK TOOL"
    sub_text = f"v{VERSION} | By {AUTHOR}"

    top_border = f"{ORANGE}╭{'─' * (width - 2)}╮{RESET}"
    bottom_border = f"{ORANGE}╰{'─' * (width - 2)}╯{RESET}"
    side_border = f"{ORANGE}│{RESET}"

    # Header Box
    print(center_text(top_border, width))
    
    title_line = f"{BOLD}{ORANGE}{app_name}{RESET}"
    title_pad = max(0, inner_width - len(strip_ansi(title_line)))
    print(center_text(f"{side_border} {' ' * (title_pad // 2)}{title_line}{' ' * (title_pad - title_pad // 2)} {side_border}", width))

    sub_line = f"{DIM}{sub_text}{RESET}"
    sub_pad = max(0, inner_width - len(strip_ansi(sub_line)))
    print(center_text(f"{side_border} {' ' * (sub_pad // 2)}{sub_line}{' ' * (sub_pad - sub_pad // 2)} {side_border}", width))

    print(center_text(bottom_border, width))
    print()

def render_menu():
    print(f"{BOLD} AVAILABLE MODULES{RESET}")
    print(f"{DIM}{'─' * min(get_terminal_width(), 60)}{RESET}\n")

    for key, (title, desc, _) in TOOLS.items():
        print(f"  {ORANGE}{BOLD}[{key}]{RESET} {BOLD}{title}{RESET}")
        print(f"      {DIM}↳ {desc}{RESET}\n")

    print(f"  {RED}{BOLD}[q]{RESET} {DIM}Quit / Exit Console{RESET}\n")
    print(f"{DIM}{'─' * min(get_terminal_width(), 60)}{RESET}")

def run_module(choice: str):
    title, _, cmd = TOOLS[choice]
    expanded_cmd = os.path.expandvars(cmd)

    # Basic binary check if executable exists
    binary_name = expanded_cmd.split()[0]
    if not shutil.which(binary_name) and not os.path.exists(binary_name):
        print(f"\n{RED}✗ Dependency Error:{RESET} '{binary_name}' command not found.")
        print(f"{DIM}Ensure the package or binary is properly installed in your PATH.{RESET}\n")
        return

    print(f"\n{GREEN}▶ Launching:{RESET} {BOLD}{title}{RESET}")
    print(f"{DIM}Running command: {expanded_cmd}{RESET}\n")
    print(f"{DIM}{'═' * min(get_terminal_width(), 60)}{RESET}\n")

    try:
        subprocess.run(expanded_cmd, shell=True)
    except Exception as err:
        print(f"\n{RED}Execution Failed:{RESET} {err}")
    finally:
        print(f"\n{DIM}{'═' * min(get_terminal_width(), 60)}{RESET}")
        input(f"\n{DIM}Press [Enter] to return to menu...{RESET}")

def main():
    # Direct CLI argument support (e.g., ./tool.py 1)
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in TOOLS:
            run_module(arg)
            sys.exit(0)
        elif arg in ['q', 'quit', 'exit']:
            sys.exit(0)
        else:
            print(f"{RED}Invalid argument:{RESET} {arg}")
            sys.exit(1)

    # Interactive Loop
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        render_banner()
        render_menu()

        try:
            choice = input(f"{ORANGE}{BOLD}ritik-tool{RESET} {BOLD}❯{RESET} ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{DIM}Session closed by user.{RESET}\n")
            sys.exit(0)

        if choice in ['q', 'quit', 'exit']:
            print(f"\n{DIM}Exiting session. Good day!{RESET}\n")
            break
        elif choice in TOOLS:
            run_module(choice)
        else:
            if choice != "":
                print(f"\n{RED}Unknown option '{choice}'. Please select a valid key.{RESET}")
                input(f"{DIM}Press [Enter] to retry...{RESET}")

if __name__ == "__main__":
    main()
    
