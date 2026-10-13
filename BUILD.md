# Build a candidate ISO

Use a **Debian 13 (trixie) amd64 host or full virtual machine** with internet access. A plain Windows terminal, macOS terminal, or restricted container cannot run this build directly. Root access is needed for the chroot/mount steps. Use a VM if your main OS is different.

Allow approximately **40 GiB free build storage** and at least **4 GiB RAM** on the builder. These are conservative planning figures; the actual build depends on package versions and firmware selection. Keep build files on a Linux filesystem such as ext4.

## Commands

After extracting the source archive and entering its `mita-lite` directory:

```sh
sudo apt-get update
sudo apt-get install live-build debootstrap squashfs-tools xorriso isolinux syslinux-common grub-pc-bin grub-efi-amd64-bin mtools dosfstools python3
python3 tools/validate.py
chmod +x build.sh auto/config
sudo ./build.sh
```

The script creates a fresh `work/build-XXXXXXXX/` directory, runs `lb config` and `lb build`, and prints the resulting `.iso` path. `SHA256SUMS`, `configure.log` and `build.log` remain beside the image. Build time is not guaranteed. The command never writes an image to a physical disk.

If the build fails, preserve the logs and report the first relevant error. Builds are not automatically retried or cleaned. A failed `live-build` may leave mounts in its build directory; use `sudo lb clean --purge` **from that exact build directory** before considering removal. Never delete a build tree while it has mounted filesystems.

## Test before installing

Start with a disposable VM. On a builder with working KVM:

```sh
sudo apt-get install qemu-system-x86 qemu-utils ovmf
qemu-system-x86_64 -enable-kvm -m 4096 -smp 2 -boot d -cdrom /absolute/path/to/your-image.iso
```

Replace the example path with the ISO printed by the builder. This command has **no writable VM hard disk**; it is for a live-session smoke test only. Without KVM, omit `-enable-kvm` (much slower). The default QEMU graphics adapter is not a gaming benchmark and may not expose Vulkan.

Use your VM manager to create a new, empty **20 GiB or larger** virtual disk for an installation test. Test both legacy BIOS and UEFI, and repeat the installed-desktop test with **2 GiB RAM**. The builder itself still needs more memory and disk than the finished desktop. UEFI requires OVMF firmware in the VM settings. Do not attach your real physical disk to the test VM.

For physical testing, write the ISO to a spare USB drive with an image writer you already trust. Writing an image erases that USB drive, so verify the selected device. Try the live desktop and its network/audio/GPU support first. When ready, reboot from the USB and choose the text-mode **Install** entry in its boot menu. The Debian live installer is configured to copy the customized live system; no separate Calamares desktop installer is included. The installer performs the actual partitioning and asks for an account and password. Keep backups and review its final disk-operation summary.

The ISO recipe does not configure persistence. Apps installed during a normal live session disappear at reboot. Prefer installing the OS to a test disk before downloading large clients or games.

## What is not yet verified

Package dependency resolution, ISO generation, desktop appearance at runtime, live account setup, installation, post-install networking, GPU acceleration and game compatibility all require testing on Debian/hardware. The supplied local validator cannot establish these.

Before distributing an ISO, finish `TESTING.md`, review upstream redistribution/source obligations, and publish checksums and the exact package/build metadata alongside it.
