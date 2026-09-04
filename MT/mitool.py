#!/usr/bin/env python3

import os
import re
import shutil
import subprocess
import sys
import urllib.request

CURRENT_VERSION = "2.2.0"
AUTHOR = "Ritik"
GITHUB_RAW_URL = "https://raw.githubusercontent.com/username/repo/main/ritiktool.py"

# ANSI Terminal Color Palette
ACCENT = "\033[38;5;208m"   # Bright Orange
CYAN   = "\033[38;5;51m"    # Cyan
GREEN  = "\033[38;5;48m"    # Mint Green
RED    = "\033[38;5;196m"   # Red
YELLOW = "\033[38;5;220m"   # Yellow
MUTED  = "\033[38;5;242m"   # Dim Gray
BOLD   = "\033[1m"
RESET  = "\033[0m"

TOOLS = {
    "1": (
        "Flash Fastboot / Hybrid ROM",
        "Automated installer for official Fastboot/Hybrid packages",
        "$PREFIX/bin/miflashf"
    ),
    "2": (
        "Reboot to Bootloader",
        "Trigger bootloader mode via Fastboot or ADB",
        "fastboot devices && fastboot reboot bootloader 2>/dev/null || adb reboot bootloader"
    ),
    "3": (
        "List Fastboot Devices",
        "Scan USB bus for devices in fastboot mode",
        "fastboot devices"
    )
}

def get_width():
    try:
        return min(os.get_terminal_size().columns, 65)
    except OSError:
        return 65

def strip_ansi(text: str) -> str:
    return re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', text)

def check_device_state():
    state = f"{RED}● Disconnected{RESET}"
    try:
        fb = subprocess.run(["fastboot", "devices"], capture_output=True, text=True, timeout=1)
        if fb.stdout.strip():
            dev_id = fb.stdout.strip().split()[0]
            return f"{YELLOW}⚡ Fastboot [{dev_id[:8]}]{RESET}"

        adb = subprocess.run(["adb", "devices"], capture_output=True, text=True, timeout=1)
        lines = [line for line in adb.stdout.strip().split('\n')[1:] if line.strip()]
        if lines:
            dev_id = lines[0].split()[0]
            return f"{GREEN}● ADB [{dev_id[:8]}]{RESET}"
    except Exception:
        pass
    return state

def render_banner():
    w = get_width()
    inner = w - 4
    
    dev_status = check_device_state()

    print(f"\n{ACCENT}╭{'─' * (w - 2)}╮{RESET}")
    title = f"{BOLD}{ACCENT}⚡ R I T I K   T O O L ⚡{RESET}"
    t_pad = max(0, inner - len(strip_ansi(title)))
    print(f"{ACCENT}│{RESET} {' ' * (t_pad // 2)}{title}{' ' * (t_pad - t_pad // 2)} {ACCENT}│{RESET}")

    sub = f"{MUTED}v{CURRENT_VERSION} │ Developed by {AUTHOR}{RESET}"
    s_pad = max(0, inner - len(strip_ansi(sub)))
    print(f"{ACCENT}│{RESET} {' ' * (s_pad // 2)}{sub}{' ' * (s_pad - s_pad // 2)} {ACCENT}│{RESET}")
    print(f"{ACCENT}╰{'─' * (w - 2)}╯{RESET}")

    print(f" {MUTED}Device:{RESET} {dev_status}  {MUTED}│  Shell:{RESET} {CYAN}Termux{RESET}")
    print(f"{MUTED}{'━' * w}{RESET}\n")

def render_menu():
    w = get_width()
    for key, (title, desc, _) in TOOLS.items():
        print(f"  {ACCENT}{BOLD}[{key}]{RESET} {BOLD}{title}{RESET}")
        print(f"      {MUTED}↳ {desc}{RESET}\n")

    print(f"{MUTED}{'─' * w}{RESET}")
    print(f"  {CYAN}{BOLD}[u]{RESET} {BOLD}Check Updates{RESET}        {RED}{BOLD}[q]{RESET} {MUTED}Quit{RESET}")
    print(f"{MUTED}{'─' * w}{RESET}\n")

def trigger_update():
    print(f"\n{ACCENT}► Fetching latest version from repository...{RESET}")
    script_path = os.path.realpath(__file__)
    tmp_path = script_path + ".tmp"
    
    try:
        urllib.request.urlretrieve(GITHUB_RAW_URL, tmp_path)
        os.replace(tmp_path, script_path)
        os.chmod(script_path, 0o755)
        print(f"{GREEN}✓ Update applied successfully!{RESET}")
        print(f"{CYAN}► Reloading script...{RESET}")
        os.execv(sys.executable, [sys.executable, script_path])
    except Exception as err:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        print(f"{RED}✗ Update failed:{RESET} {err}")
        input(f"\n{MUTED}Press [Enter] to return...{RESET}")

def execute_operation(key: str):
    title, _, cmd = TOOLS[key]
    expanded_cmd = os.path.expandvars(cmd)
    
    bin_name = expanded_cmd.split()[0]
    if not shutil.which(bin_name) and not os.path.exists(bin_name):
        print(f"\n{RED}✗ Error:{RESET} Command '{bin_name}' not found.")
        print(f"{MUTED}Ensure required packages (e.g. android-tools) are installed.{RESET}\n")
        input(f"{MUTED}Press [Enter] to return...{RESET}")
        return

    print(f"\n{GREEN}▶ Executing:{RESET} {BOLD}{title}{RESET}")
    print(f"{MUTED}$ {expanded_cmd}{RESET}\n")
    print(f"{ACCENT}{'─' * get_width()}{RESET}\n")

    try:
        subprocess.run(expanded_cmd, shell=True)
    except Exception as e:
        print(f"\n{RED}✗ Runtime error:{RESET} {e}")
    finally:
        print(f"\n{ACCENT}{'─' * get_width()}{RESET}")
        input(f"\n{MUTED}Press [Enter] to return to menu...{RESET}")

def main():
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        render_banner()
        render_menu()

        try:
            choice = input(f"{ACCENT}ritik{RESET}{BOLD}@{RESET}{CYAN}termux{RESET} {BOLD}❯{RESET} ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{MUTED}Process terminated.{RESET}\n")
            sys.exit(0)

        if choice in ['q', 'exit']:
            print(f"\n{MUTED}Exiting session.{RESET}\n")
            break
        elif choice == 'u':
            trigger_update()
        elif choice in TOOLS:
            execute_operation(choice)
        else:
            if choice:
                print(f"\n{RED}Invalid selection: '{choice}'{RESET}")
                input(f"{MUTED}Press [Enter] to retry...{RESET}")

if __name__ == "__main__":
    main()
    
