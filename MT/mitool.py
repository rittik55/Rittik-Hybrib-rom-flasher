#!/usr/bin/env python3
# ==============================================================================
#  RITIK ENGINE PRO - ULTRA FASTBOOT & HYBRID FLASHING WORKSTATION
#  Architecture : Pure Python 3.8+ (Zero Third-Party Dependencies)
#  Target Shell : Android Termux / Linux AArch64 & x86_64
# ==============================================================================

import os
import re
import sys
import time
import glob
import shutil
import zipfile
import threading
import subprocess
import urllib.request

VERSION = "4.0.0-PRO"
AUTHOR = "Ritik"
REPO_RAW = "https://raw.githubusercontent.com/username/repo/main/ritiktool.py"

# ANSI 256 Ultra Stream Palette
HEX_ORANGE = "\033[38;5;208m"
HEX_CYAN   = "\033[38;5;45m"
HEX_GREEN  = "\033[38;5;48m"
HEX_RED    = "\033[38;5;196m"
HEX_YELLOW = "\033[38;5;220m"
HEX_PURPLE = "\033[38;5;141m"
HEX_MUTED  = "\033[38;5;240m"
BOLD       = "\033[1m"
RESET      = "\033[0m"

# Global Hardware State Object
DEVICE_STATE = {
    "status": "DISCONNECTED",
    "mode": "NONE",
    "serial": "N/A",
    "product": "N/A",
    "unlocked": "N/A",
    "slot": "N/A",
    "arb": "N/A"
}
WATCHDOG_ACTIVE = True

def strip_ansi(text: str) -> str:
    return re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', text)

def get_terminal_width():
    try:
        return min(os.get_terminal_size().columns, 75)
    except OSError:
        return 75

class TerminalSpinner:
    def __init__(self, message="Processing..."):
        self.message = message
        self.running = False
        self.thread = None
        self.chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    def _spin(self):
        idx = 0
        while self.running:
            sys.stdout.write(f"\r  {HEX_ORANGE}{self.chars[idx % len(self.chars)]}{RESET} {self.message}")
            sys.stdout.flush()
            idx += 1
            time.sleep(0.08)
        sys.stdout.write("\r" + " " * (len(self.message) + 10) + "\r")
        sys.stdout.flush()

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._spin, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

def hardware_watchdog():
    """Asynchronous background worker polling USB endpoints every 1.5s"""
    global DEVICE_STATE
    while WATCHDOG_ACTIVE:
        try:
            # Check Fastboot Bus
            fb = subprocess.run(["fastboot", "devices"], capture_output=True, text=True, timeout=1)
            if fb.stdout.strip():
                serial = fb.stdout.strip().split()[0]
                DEVICE_STATE["status"] = "CONNECTED"
                DEVICE_STATE["mode"] = "FASTBOOT"
                DEVICE_STATE["serial"] = serial

                # Batch query properties
                props = subprocess.run(
                    ["fastboot", "getvar", "all"],
                    capture_output=True, text=True, timeout=1.5
                )
                output = props.stderr + props.stdout
                
                prod = re.search(r'product:\s*(\S+)', output)
                unlock = re.search(r'unlocked:\s*(\S+)', output)
                slot = re.search(r'current-slot:\s*(\S+)', output)
                arb = re.search(r'anti:\s*(\S+)', output)

                DEVICE_STATE["product"] = prod.group(1) if prod else "Generic"
                DEVICE_STATE["unlocked"] = unlock.group(1).lower() in ['yes', 'true', '1'] if unlock else False
                DEVICE_STATE["slot"] = slot.group(1).replace("_", "") if slot else "N/A"
                DEVICE_STATE["arb"] = arb.group(1) if arb else "Safe/None"
                time.sleep(1.5)
                continue

            # Check ADB Bus
            adb = subprocess.run(["adb", "devices"], capture_output=True, text=True, timeout=1)
            lines = [l for l in adb.stdout.strip().split('\n')[1:] if l.strip()]
            if lines:
                serial = lines[0].split()[0]
                DEVICE_STATE["status"] = "CONNECTED"
                DEVICE_STATE["mode"] = "ADB"
                DEVICE_STATE["serial"] = serial
                DEVICE_STATE["product"] = "Active System"
                DEVICE_STATE["unlocked"] = "N/A"
                DEVICE_STATE["slot"] = "N/A"
                DEVICE_STATE["arb"] = "N/A"
                time.sleep(1.5)
                continue

            # Reset state if nothing found
            DEVICE_STATE["status"] = "DISCONNECTED"
            DEVICE_STATE["mode"] = "NONE"
            DEVICE_STATE["serial"] = "N/A"
            DEVICE_STATE["product"] = "N/A"
            DEVICE_STATE["unlocked"] = "N/A"
            DEVICE_STATE["slot"] = "N/A"
            DEVICE_STATE["arb"] = "N/A"

        except Exception:
            pass
        time.sleep(1.5)

def render_dashboard():
    w = get_terminal_width()
    inner = w - 4

    print(f"\n{HEX_ORANGE}╭{'─' * (w - 2)}╮{RESET}")
    hdr = f"{BOLD}{HEX_ORANGE}R I T I K   E N G I N E   P R O{RESET}"
    h_pad = max(0, inner - len(strip_ansi(hdr)))
    print(f"{HEX_ORANGE}│{RESET} {' ' * (h_pad // 2)}{hdr}{' ' * (h_pad - h_pad // 2)} {HEX_ORANGE}│{RESET}")
    
    sub = f"{HEX_MUTED}Release v{VERSION}  |  Kernel Bus Engine{RESET}"
    s_pad = max(0, inner - len(strip_ansi(sub)))
    print(f"{HEX_ORANGE}│{RESET} {' ' * (s_pad // 2)}{sub}{' ' * (s_pad - s_pad // 2)} {HEX_ORANGE}│{RESET}")
    print(f"{HEX_ORANGE}╰{'─' * (w - 2)}╯{RESET}")

    # Telemetry HUD
    st = DEVICE_STATE["status"]
    st_color = HEX_GREEN if st == "CONNECTED" else HEX_RED
    mode_color = HEX_YELLOW if DEVICE_STATE["mode"] == "FASTBOOT" else HEX_CYAN

    print(f" {BOLD}SYSTEM TELEMETRY HUD{RESET}")
    print(f"  Link: {st_color}{st}{RESET}  [{mode_color}{DEVICE_STATE['mode']}{RESET}]  Target: {HEX_CYAN}{DEVICE_STATE['product']}{RESET}")
    
    if DEVICE_STATE["mode"] == "FASTBOOT":
        unlocked_str = f"{HEX_GREEN}UNLOCKED{RESET}" if DEVICE_STATE["unlocked"] else f"{HEX_RED}LOCKED{RESET}"
        print(f"  Serial: {HEX_MUTED}{DEVICE_STATE['serial'][:12]}{RESET} │ Bootloader: {unlocked_str} │ Slot: {HEX_YELLOW}_{DEVICE_STATE['slot']}{RESET} │ ARB: {HEX_PURPLE}{DEVICE_STATE['arb']}{RESET}")
    print(f"{HEX_MUTED}{'━' * w}{RESET}\n")

def scan_storage_files(extensions, base_dir="~/storage/shared/Download"):
    path = os.path.expanduser(base_dir)
    found = []
    for ext in extensions:
        found.extend(glob.glob(os.path.join(path, f"*.{ext}")))
    return sorted(found)

def interactive_partition_flasher():
    partitions = ["boot", "init_boot", "vendor_boot", "recovery", "dtbo", "vbmeta", "super"]
    print(f"\n{BOLD}Target Partition Select:{RESET}")
    for idx, p in enumerate(partitions, 1):
        print(f"  {HEX_ORANGE}[{idx}]{RESET} {p}")
    
    p_in = input(f"\n{BOLD}Select partition [1-{len(partitions)}]: {RESET}").strip()
    try:
        part = partitions[int(p_in) - 1]
    except Exception:
        print(f"{HEX_RED}Aborted: Invalid target index.{RESET}")
        return

    files = scan_storage_files(["img"])
    if not files:
        print(f"{HEX_RED}No .img files found in ~/storage/shared/Download{RESET}")
        return

    print(f"\n{BOLD}Detected Image Artifacts:{RESET}")
    for idx, f in enumerate(files, 1):
        mb = os.path.getsize(f) / (1024 * 1024)
        print(f"  {HEX_ORANGE}[{idx}]{RESET} {os.path.basename(f)} {HEX_MUTED}({mb:.1f} MB){RESET}")

    f_in = input(f"\n{BOLD}Select artifact [1-{len(files)}]: {RESET}").strip()
    try:
        selected_img = files[int(f_in) - 1]
    except Exception:
        print(f"{HEX_RED}Aborted.{RESET}")
        return

    # Slot Targeting Options
    slot_arg = ""
    if DEVICE_STATE["slot"] != "N/A":
        print(f"\n{BOLD}Slot Distribution:{RESET}")
        print(f"  {HEX_ORANGE}[1]{RESET} Active Slot Only (_{DEVICE_STATE['slot']})")
        print(f"  {HEX_ORANGE}[2]{RESET} Both Slots (Slot A + B via --slot=all)")
        s_in = input(f"Selection [1/2]: ").strip()
        if s_in == "2":
            slot_arg = "--slot=all"

    # Execution Stream
    cmd = f"fastboot flash {part} {slot_arg} \"{selected_img}\""
    print(f"\n{HEX_YELLOW}Pipeline Ready:{RESET} {cmd}")
    if input(f"{BOLD}Execute flash pipeline? [y/N]: {RESET}").lower() == 'y':
        spinner = TerminalSpinner("Transmitting payload via USB transport...")
        spinner.start()
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        spinner.stop()
        print(f"\n{res.stdout}{res.stderr}")
        if res.returncode == 0:
            print(f"{HEX_GREEN}✓ Partition {part} updated successfully.{RESET}")
        else:
            print(f"{HEX_RED}✗ Transport failure. Return code: {res.returncode}{RESET}")

def zip_stream_extractor():
    """Extracts specific partition images directly from ZIP packages in Downloads"""
    zips = scan_storage_files(["zip"])
    if not zips:
        print(f"{HEX_RED}No .zip packages found in Downloads.{RESET}")
        return

    print(f"\n{BOLD}Available Archives:{RESET}")
    for idx, z in enumerate(zips, 1):
        mb = os.path.getsize(z) / (1024 * 1024)
        print(f"  {HEX_ORANGE}[{idx}]{RESET} {os.path.basename(z)} {HEX_MUTED}({mb:.1f} MB){RESET}")

    z_in = input(f"\nSelect archive index: ").strip()
    try:
        target_zip = zips[int(z_in) - 1]
    except Exception:
        return

    spinner = TerminalSpinner("Indexing archive structure...")
    spinner.start()
    try:
        with zipfile.ZipFile(target_zip, 'r') as archive:
            img_members = [m for m in archive.namelist() if m.endswith('.img')]
            spinner.stop()

            if not img_members:
                print(f"{HEX_RED}No .img elements found inside archive.{RESET}")
                return

            print(f"\n{BOLD}Extractable Artifacts inside ZIP:{RESET}")
            for idx, item in enumerate(img_members, 1):
                print(f"  {HEX_ORANGE}[{idx}]{RESET} {item}")

            m_in = input(f"\nSelect image to extract & ready: ").strip()
            selected_member = img_members[int(m_in) - 1]

            out_dir = os.path.expanduser("~/storage/shared/Download")
            spinner = TerminalSpinner(f"Streaming {selected_member} to disk...")
            spinner.start()
            extracted_path = archive.extract(selected_member, path=out_dir)
            spinner.stop()
            print(f"{HEX_GREEN}✓ Extracted successfully to:{RESET} {extracted_path}")

    except Exception as e:
        spinner.stop()
        print(f"{HEX_RED}Archive parsing error:{RESET} {e}")

def active_reboot_manager():
    print(f"\n{BOLD}Bus Power & Mode Switch:{RESET}")
    print(f"  {HEX_ORANGE}[1]{RESET} System Reboot")
    print(f"  {HEX_ORANGE}[2]{RESET} Fastboot / Bootloader")
    print(f"  {HEX_ORANGE}[3]{RESET} Fastbootd (Dynamic Partitions Userspace)")
    print(f"  {HEX_ORANGE}[4]{RESET} Stock/Custom Recovery")
    print(f"  {HEX_ORANGE}[5]{RESET} Emergency Download Mode (EDL)")

    r_in = input(f"\nSelect reboot mode: ").strip()
    matrix = {
        "1": "fastboot reboot 2>/dev/null || adb reboot",
        "2": "fastboot reboot bootloader 2>/dev/null || adb reboot bootloader",
        "3": "fastboot reboot fastboot",
        "4": "fastboot reboot recovery 2>/dev/null || adb reboot recovery",
        "5": "fastboot oem edl 2>/dev/null || adb reboot edl"
    }

    if r_in in matrix:
        cmd = matrix[r_in]
        print(f"\n{HEX_YELLOW}Triggering:{RESET} {cmd}")
        subprocess.run(cmd, shell=True)

def atomic_self_update():
    print(f"\n{HEX_ORANGE}► Contacting upstream deployment node...{RESET}")
    this_script = os.path.realpath(__file__)
    tmp_stage = this_script + ".stage"
    try:
        urllib.request.urlretrieve(REPO_RAW, tmp_stage)
        os.replace(tmp_stage, this_script)
        os.chmod(this_script, 0o755)
        print(f"{HEX_GREEN}✓ Engine core updated to edge build.{RESET}")
        print(f"{HEX_CYAN}► Hot-reloading process context...{RESET}")
        global WATCHDOG_ACTIVE
        WATCHDOG_ACTIVE = False
        os.execv(sys.executable, [sys.executable, this_script])
    except Exception as err:
        if os.path.exists(tmp_stage):
            os.remove(tmp_stage)
        print(f"{HEX_RED}Update pipeline broken:{RESET} {err}")

def main():
    # Spawn the background USB Watchdog Engine
    wd_thread = threading.Thread(target=hardware_watchdog, daemon=True)
    wd_thread.start()

    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        render_dashboard()

        print(f" {BOLD}EXECUTION SUITE{RESET}")
        print(f"  {HEX_ORANGE}[1]{RESET} Native MiFlashf Launcher        {HEX_MUTED}(Fastboot/Hybrid firmware){RESET}")
        print(f"  {HEX_ORANGE}[2]{RESET} Partition Flasher & A/B Router  {HEX_MUTED}(boot, vendor, init_boot){RESET}")
        print(f"  {HEX_ORANGE}[3]{RESET} ZIP Artifact Stream Extractor   {HEX_MUTED}(Pull images directly from ZIP){RESET}")
        print(f"  {HEX_ORANGE}[4]{RESET} Target Mode & Bus Switcher      {HEX_MUTED}(System, Recovery, Fastbootd, EDL){RESET}")
        print(f"  {HEX_ORANGE}[5]{RESET} Hard Userdata Wipe              {HEX_MUTED}(fastboot -w / Format all partitions){RESET}")
        print(f"\n {BOLD}INTERNAL UTILITIES{RESET}")
        print(f"  {HEX_CYAN}[u]{RESET} Trigger Atomic Edge Update      {HEX_RED}[q]{RESET} Detach CLI Session")
        print(f"{HEX_MUTED}{'─' * get_terminal_width()}{RESET}")

        try:
            cmd_prompt = f"{HEX_ORANGE}ritik-core{RESET}{BOLD}❯{RESET} "
            choice = input(cmd_prompt).strip().lower()
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{HEX_MUTED}Shutting down thread pools...{RESET}")
            break

        if choice in ['q', 'exit']:
            break
        elif choice == 'u':
            atomic_self_update()
            input(f"\n{HEX_MUTED}Press [Enter]...{RESET}")
        elif choice == '1':
            print(f"\n{HEX_GREEN}► Launching miflashf binary...{RESET}\n")
            subprocess.run("$PREFIX/bin/miflashf", shell=True)
            input(f"\n{HEX_MUTED}Press [Enter] to return...{RESET}")
        elif choice == '2':
            interactive_partition_flasher()
            input(f"\n{HEX_MUTED}Press [Enter] to return...{RESET}")
        elif choice == '3':
            zip_stream_extractor()
            input(f"\n{HEX_MUTED}Press [Enter] to return...{RESET}")
        elif choice == '4':
            active_reboot_manager()
            input(f"\n{HEX_MUTED}Press [Enter] to return...{RESET}")
        elif choice == '5':
            print(f"\n{HEX_RED}{BOLD}[WARNING] ALL DATA ON INTERNAL STORAGE WILL BE PERMANENTLY ERASED!{RESET}")
            if input(f"Type 'ERASE' to continue: ").strip() == "ERASE":
                subprocess.run("fastboot -w", shell=True)
            else:
                print(f"{HEX_CYAN}Wipe sequence aborted.{RESET}")
            input(f"\n{HEX_MUTED}Press [Enter] to return...{RESET}")

    global WATCHDOG_ACTIVE
    WATCHDOG_ACTIVE = False
    sys.exit(0)

if __name__ == "__main__":
    main()
        
