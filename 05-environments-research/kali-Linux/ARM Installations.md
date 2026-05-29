 
 # 1. Verifying and Uncompressing the Image File
 
 ## Step-by-Step SHA256 Verification
 
 Downloaded files can occasionally corrupt during transit. To ensure your system boots properly and is secure, check the hash integrity before proceeding.
 
 * On Linux / macOS:Open your terminal, navigate to your Downloads folder, and run:

 ```bash
 sha256sum kali-linux-2026.1-raspberrypi-64.img.xz
```

* On Windows (PowerShell):

```powershell
powershellGet-FileHash .\kali-linux-2026.1-raspberrypi-64.img.xz -Algorithm SHA256
```

Compare the resulting alphanumeric string with the one provided next to the download link on the official site. They must match exactly.

## Extracting the Raw Image

The file extension ```.xz``` indicates high-ratio compression. You cannot flash this archive directly using standard CLI tools; it must be extracted first.

```bash
unxz kali-linux-2026.1-raspberrypi-64.img.xz
```

This leaves you with a large .img file ready for deployment.

# 2. Advanced Disk Flashing Protocol via Terminal

When using the dd utility on Unix-like platforms (Linux/macOS), choosing the wrong destination identifier will permanently erase your host computer's storage drive.

## Step A: Precise Drive Identification

Before plugging in your SD card or eMMC module, query your existing drives:
```bash
lsblk
```

Now insert your external storage device and run lsblk again. A new device name will appear (e.g., /dev/sdb or /dev/sdc). Note the root letter designation, **not the individual partition number** (use sdb, not sdb1).

## Step B: Execution of the Copy Command

Run the low-level copying command using optimized block boundaries:
```bash
sudo dd if=kali-linux-2026.1-raspberrypi-64.img of=/dev/sdb bs=4M status=progress conv=fsync
```
* **bs=4M**: Sets block sizes to 4 Megabytes to drastically speed up data throughput compared to the legacy 512k standard.
* **status=progress**: Forces the terminal to print real-time transmission rates and estimated completion time.
* **conv=fsync**: Forces physical data blocks to be fully committed to disk caches before finishing, eliminating the risk of data corruption upon safe removal.

# 3. Headless Network Discovery Strategy

If you do not have an HDMI monitor hooked up to your board, you must access the terminal over a secure shell (SSH) via a local network connection. Plug an Ethernet cable into the board and power it on.

### Network Reconnaissance using Nmap

To discover your device's dynamic IP address, scan your subnetwork using a host identification ping. First, determine your own local IP range via ip a (e.g., 192.168.1.50).

Scan the final block of that range (/24) using:
```bash
sudo nmap -sn 192.168.1.0/24
```

Look for an active host indicating a hardware identifier manufactured by your specific board creator (e.g., Raspberry Pi Trading, Pine64, etc.).

# 4. Initial Remote Access & Mandatory Security Hardening

Once you have identified the target network address (e.g., 192.168.1.145), start an encrypted transmission shell:

```bash
ssh kali@192.168.1.145
```

Input the factory-default security credential: kali.

## Securing the System (Critical)

Because default deployment images share identical system identity layouts, your device is vulnerable to exploitation if left on an open network with factory settings. Run these three adjustments immediately:

```bash
# 1. Update your primary user account password
passwd

# 2. Purge factory default host certificates to block impersonation attacks
sudo rm /etc/ssh/ssh_host_*

# 3. Force the SSH configuration module to re-evaluate and craft unique encryption keys
sudo dpkg-reconfigure openssh-server

# 4. Cycle the service to apply changes
sudo systemctl restart ssh
```
