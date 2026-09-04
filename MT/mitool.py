#!/usr/bin/env python3
import os
import sys
import tty
import time
import termios
import subprocess
import threading

VERSION = "5.0.0-ULTRA"

# Styling & Palette
ORANGE_BG = "\033[48;5;208m\033[38;5;16m\033[1m"  # Inverted selection
ORANGE    = "\033[38;5;208m"
CYAN      = "\033[38;5;51m"
GREEN     = "\033[38;5;48m"
RED       = "\033[38;5;196m"
GRAY      = "\033[38;5;240m"
BOLD      = "\033[1m"
RESET     = "\033[0m"

MENU_ITEMS = [
    ("⚡ Flash Fastboot / Hybrid ROM", "$PREFIX/bin/miflashf"),
    ("📦 Partition Flasher (boot/init_boot)", "fastboot flash"),
    ("🔄 Reboot to Fastboot / Bootloader", "fastboot reboot bootloader 2>/dev/null || adb reboot bootloader"),
    ("🚀 Reboot to System", "fastboot reboot 2>/dev/null || adb reboot"),
    ("💥 Wipe Userdata (Factory Reset)", "fastboot -w"),
    ("🌐 Check for Tool Updates", "update"),
    ("🚪 Exit Terminal", "exit")
]

def get_char():
    """Captures direct keystrokes without needing to press Enter."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == '\x1b':
            ch2 = sys.stdin.read(1)
            ch3 = sys.stdin.read(1)
            return ch + ch2 + ch3
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def get_device_badge():
    try:
        fb = subprocess.run(["fastboot", "devices"], capture_output=True, text=True, timeout=0.5)
        if fb.stdout.strip():
            dev = fb.stdout.strip().split()[0][:8]
            return f"{ORANGE}[FASTBOOT: {dev}]{RESET}"
        adb = subprocess.run(["adb", "devices"], capture_output=True, text=True, timeout=0.5)
        lines = [l for l in adb.stdout.strip().split('\n')[1:] if l.strip()]
        if lines:
            dev = lines[0].split()[0][:8]
            return f"{GREEN}[ADB: {dev}]{RESET}"
    except:
        pass
    return f"{RED}[DISCONNECTED]{RESET}"

def print_banner():
    badge = get_device_badge()
    # Cyber ASCII Art Logo
    logo = f"""{ORANGE}
    ██████╗ ██╗████████╗██╗██╗  ██╗
    ██╔══██╗██║╚══██╔══╝██║██║ ██╔╝
    ██████╔╝██║   ██║   ██║█████╔╝ 
    ██╔══██╗██║   ██║   ██║██╔═██╗ 
    ██║  ██║██║   ██║   ██║██║  ██╗
    ╚═╝  ╚═╝╚═╝   ╚═╝   ╚═╝╚═╝  ╚═╝{RESET}"""
    print(logo)
    print(f"    {GRAY}ENGINE v{VERSION}{RESET}  │  {badge}")
    print(f"    {GRAY}{'─' * 42}{RESET}\n")

def draw_menu(selected_idx):
    # Move cursor up or clear
    sys.stdout.write("\033[H\033[J")  # Clean ANSI Clear
    print_banner()

    print(f"    {GRAY}Navigate: [↑/↓] Arrows  │  Select: [ENTER]{RESET}\n")
    for idx, (label, _) in enumerate(MENU_ITEMS):
        if idx == selected_idx:
            # Highlight selected row
            print(f"    {ORANGE}❯{RESET} {ORANGE_BG} {label:<38} {RESET}")
        else:
            print(f"      {BOLD}{label:<40}{RESET}")
    print(f"\n    {GRAY}{'─' * 42}{RESET}")

def run_command(cmd, title):
    sys.stdout.write("\033[H\033[J")
    print(f"\n  {GREEN}▶ Executing:{RESET} {BOLD}{title}{RESET}")
    print(f"  {GRAY}$ {cmd}{RESET}\n")
    print(f"  {ORANGE}{'─' * 50}{RESET}\n")
    
    subprocess.run(cmd, shell=True)
    
    print(f"\n  {ORANGE}{'─' * 50}{RESET}")
    input(f"\n  {GRAY}Press [ENTER] to return to console...{RESET}")

def main():
    selected_idx = 0
    while True:
        draw_menu(selected_idx)
        key = get_char()

        # Arrow Up
        if key in ['\x1b[A', 'k']:
            selected_idx = (selected_idx - 1) % len(MENU_ITEMS)
        # Arrow Down
        elif key in ['\x1b[B', 'j']:
            selected_idx = (selected_idx + 1) % len(MENU_ITEMS)
        # Enter Key
        elif key in ['\r', '\n']:
            label, cmd = MENU_ITEMS[selected_idx]
            
            if cmd == "exit":
                sys.stdout.write("\033[H\033[J")
                print(f"\n  {ORANGE}Ritik Tool closed.{RESET}\n")
                break
            elif cmd == "update":
                run_command("curl -sL https://raw.githubusercontent.com/username/repo/main/ritiktool.py -o $0 && echo 'Done'", "Update Core")
            else:
                run_command(cmd, label)
        # Ctrl+C or 'q'
        elif key in ['\x03', 'q']:
            sys.stdout.write("\033[H\033[J")
            break

if __name__ == "__main__":
    main()
    
