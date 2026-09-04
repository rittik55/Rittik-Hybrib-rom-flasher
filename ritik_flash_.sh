#!/data/data/com.termux/files/usr/bin/sh
cd "$(dirname "$0")" || exit 1

if command -v termux-fastboot >/dev/null 2>&1; then
    fastboot="termux-fastboot"
elif command -v fastboot >/dev/null 2>&1; then
    fastboot="fastboot"
elif [ -f "./bin/linux/fastboot" ]; then
    fastboot="./bin/linux/fastboot"
else
    fastboot="fastboot"
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

echo "[!] You are going to wipe your data and internal storage."
echo "[!] It will delete all your files and photos stored on internal storage."
printf "Do you agree? (Y/N) "
read -r choice
[ "$choice" != "y" ] && [ "$choice" != "Y" ] && exit 0

echo "##################################################################"
echo "Please wait. The device will reboot when installation is finished."
echo "##################################################################"

$fastboot set_active a
$fastboot flash apusys_ab images/apusys.img
$fastboot flash audio_dsp_ab images/audio_dsp.img
$fastboot flash ccu_ab images/ccu.img
$fastboot flash connsys_bt_ab images/connsys_bt.img
$fastboot flash connsys_gnss_ab images/connsys_gnss.img
$fastboot flash connsys_wifi_ab images/connsys_wifi.img
$fastboot flash dpm_ab images/dpm.img
$fastboot flash dtbo_ab images/dtbo.img
$fastboot flash gpueb_ab images/gpueb.img
$fastboot flash gz_ab images/gz.img
$fastboot flash lk_ab images/lk.img
$fastboot flash logo_ab images/logo.img
$fastboot flash mcf_ota_ab images/mcf_ota.img
$fastboot flash mcupm_ab images/mcupm.img
$fastboot flash modem_ab images/modem.img
$fastboot flash mvpu_algo_ab images/mvpu_algo.img
$fastboot flash pi_img_ab images/pi_img.img
$fastboot flash scp_ab images/scp.img
$fastboot flash spmfw_ab images/spmfw.img
$fastboot flash sspm_ab images/sspm.img
$fastboot flash tee_ab images/tee.img
$fastboot flash vbmeta_ab images/vbmeta.img
$fastboot flash vbmeta_system_ab images/vbmeta_system.img
$fastboot flash vbmeta_vendor_ab images/vbmeta_vendor.img
$fastboot flash vcp_ab images/vcp.img
$fastboot flash boot_ab images/boot.img
$fastboot flash init_boot_ab images/init_boot.img
$fastboot flash vendor_boot_ab images/vendor_boot.img
$fastboot flash super images/super.img
$fastboot erase metadata
$fastboot erase frp
$fastboot erase expdb
$fastboot erase userdata
$fastboot oem cdms
$fastboot reboot
