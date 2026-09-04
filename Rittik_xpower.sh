#!/data/data/com.termux/files/usr/bin/sh
# ==========================================================
# Flash Script for Fastboot ROM (Duchamp)
# Made by: Ritik
# ==========================================================

cd "$(dirname "$0")" || exit 1

# Termux me termux-fastboot aur fastboot dono ko auto-detect karega
if command -v termux-fastboot >/dev/null 2>&1; then
    fastboot="termux-fastboot"
elif command -v fastboot >/dev/null 2>&1; then
    fastboot="fastboot"
else
    echo "[-] Error: Fastboot not found!"
    echo "[!] Please install: pkg install termux-adb"
    exit 1
fi

echo "=================================================="
echo "----------------------------------------"
echo "                                        "
echo "  ___   _   _   ___  _____  _       "
echo " / _ \ | | | | / _ \|_   _|| |      "
echo "| | | || | | || | | | | |  | |      "
echo "| |_| || |_| || |_| | | |  | |___   "
echo " \__\_\\___/  \___/  |_|  |_____|  "
echo "                                        "
echo "         MADE BY RITIK                  "
echo "     ROM FLASH TOOL (duchamp)           "
echo "----------------------------------------"
echo "=================================================="

echo "[*] Waiting for device..."
device=$($fastboot getvar product 2>&1 | grep -F "product:" | tr -s " " | cut -d " " -f 2)
[ -z "$device" ] && device="unknown"

if [ "$device" != "duchamp" ]; then
    echo "[-] Error: Device mismatch!"
    echo "    Compatible devices: duchamp"
    echo "    Detected device: $device"
    exit 1
fi

echo "[!] WARNING: This install will delete all your applications, settings and files from internal storage."
printf "Do you agree? (Y/N) "
read -r choice
[ "$choice" != "y" ] && [ "$choice" != "Y" ] && exit 0

echo "###################################################"
echo "  Flashing started by Ritik's Script...            "
echo "  After install device will be rebooted.           "
echo "  Please wait and DO NOT disconnect your device.   "
echo "###################################################"

$fastboot set_active a
$fastboot flash apusys_a img/apusys.img
$fastboot flash apusys_b img/apusys.img
$fastboot flash audio_dsp_a img/audio_dsp.img
$fastboot flash audio_dsp_b img/audio_dsp.img
$fastboot flash boot_a img/boot.img
$fastboot flash boot_b img/boot.img
$fastboot flash ccu_a img/ccu.img
$fastboot flash ccu_b img/ccu.img
$fastboot flash connsys_bt_a img/connsys_bt.img
$fastboot flash connsys_bt_b img/connsys_bt.img
$fastboot flash connsys_gnss_a img/connsys_gnss.img
$fastboot flash connsys_gnss_b img/connsys_gnss.img
$fastboot flash connsys_wifi_a img/connsys_wifi.img
$fastboot flash connsys_wifi_b img/connsys_wifi.img
$fastboot flash dpm_a img/dpm.img
$fastboot flash dpm_b img/dpm.img
$fastboot flash dtbo_a img/dtbo.img
$fastboot flash dtbo_b img/dtbo.img
$fastboot flash gpueb_a img/gpueb.img
$fastboot flash gpueb_b img/gpueb.img
$fastboot flash gz_a img/gz.img
$fastboot flash gz_b img/gz.img
$fastboot flash init_boot_a img/init_boot.img
$fastboot flash init_boot_b img/init_boot.img
$fastboot flash lk_a img/lk.img
$fastboot flash lk_b img/lk.img
$fastboot flash logo_a img/logo.img
$fastboot flash logo_b img/logo.img
$fastboot flash mcf_ota_a img/mcf_ota.img
$fastboot flash mcf_ota_b img/mcf_ota.img
$fastboot flash mcupm_a img/mcupm.img
$fastboot flash mcupm_b img/mcupm.img
$fastboot flash modem_a img/modem.img
$fastboot flash modem_b img/modem.img
$fastboot flash mvpu_algo_a img/mvpu_algo.img
$fastboot flash mvpu_algo_b img/mvpu_algo.img
$fastboot flash pi_img_a img/pi_img.img
$fastboot flash pi_img_b img/pi_img.img
$fastboot flash preloader_a img/preloader_raw.img
$fastboot flash preloader_b img/preloader_raw.img
$fastboot flash scp_a img/scp.img
$fastboot flash scp_b img/scp.img
$fastboot flash spmfw_a img/spmfw.img
$fastboot flash spmfw_b img/spmfw.img
$fastboot flash sspm_a img/sspm.img
$fastboot flash sspm_b img/sspm.img
$fastboot flash tee_a img/tee.img
$fastboot flash tee_b img/tee.img
$fastboot flash vbmeta_a img/vbmeta.img
$fastboot flash vbmeta_b img/vbmeta.img
$fastboot flash vbmeta_system_a img/vbmeta_system.img
$fastboot flash vbmeta_system_b img/vbmeta_system.img
$fastboot flash vbmeta_vendor_a img/vbmeta_vendor.img
$fastboot flash vbmeta_vendor_b img/vbmeta_vendor.img
$fastboot flash vcp_a img/vcp.img
$fastboot flash vcp_b img/vcp.img
$fastboot flash vendor_boot_a img/vendor_boot.img
$fastboot flash vendor_boot_b img/vendor_boot.img
$fastboot flash super img/super.img
$fastboot erase metadata
$fastboot erase userdata
$fastboot erase expdb
$fastboot erase frp
$fastboot oem cdms
$fastboot reboot

echo ""
echo "[+] ROM Flashing Successfully Completed!"
echo "[+] Script executed by Ritik."
