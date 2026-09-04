#!/usr/bin/env python3

import os
import subprocess
import sys

VERSION = "5.3.0"

ORANGE = "\033[38;5;208m"
GREEN  = "\033[38;5;48m"
RED    = "\033[38;5;196m"
GRAY   = "\033[38;5;242m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

MENU = {
    "1": ("Flash Fastboot / Hybrid ROM", "$PREFIX/bin/miflashf"),
    "2": ("Reboot to Bootloader / Fastboot", "fastboot reboot bootloader 2>/dev/null || adb reboot bootloader"),
    "3": ("Reboot to System", "fastboot reboot 2>/dev/null || adb reboot"),
    "4": ("Wipe Userdata (Factory Reset)", "fastboot -w"),
}

def get_status():
    try:
        fb = subprocess.run(["fastboot", "devices"], capture_output=True, text=True, timeout=0.6)
        if fb.stdout.strip():
            dev = fb.stdout.strip().split()[0][:8]
            return f"{GREEN}● Fastboot [{dev}]{RESET}"

        adb = subprocess.run(["adb", "devices"], capture_output=True, text=True, timeout=0.6)
        lines = [l for l in adb.stdout.strip().split('\n')[1:] if l.strip()]
        if lines:
            dev = lines[0].split()[0][:8]
            return f"{GREEN}● ADB [{dev}]{RESET}"
    except Exception:
        pass
    return f"{RED}○ Disconnected{RESET}"

def render_screen():
    status = get_status()
    print("\n" + f"{ORANGE}{BOLD}  RITIK TOOL{RESET} {GRAY}v{VERSION}{RESET}  │  {status}")
    print(f"{GRAY}  {'─' * 42}{RESET}\n")

    for key, (name, _) in MENU.items():
        print(f"  {ORANGE}{BOLD}[{key}]{RESET}  {name}")

    print(f"\n  {RED}{BOLD}[0]{RESET}  Exit")
    print(f"{GRAY}  {'─' * 42}{RESET}\n")

def execute(choice):
    name, cmd = MENU[choice]
    expanded_cmd = os.path.expandvars(cmd)

    print(f"\n{GRAY}Running: {expanded_cmd}{RESET}\n")
    try:
        subprocess.run(expanded_cmd, shell=True)
    except Exception as e:
        print(f"{RED}Error:{RESET} {e}")
    finally:
        input(f"\n{GRAY}Press Enter to continue...{RESET}")

def main():
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        render_screen()

        try:
            choice = input(f"  {BOLD}Select option:{RESET} ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n")
            sys.exit(0)

        if choice in ['0', 'q', 'exit']:
            print(f"\n{GRAY}Exiting...{RESET}\n")
            break
        elif choice in MENU:
            execute(choice)

if __name__ == "__main__":
    main()
    
