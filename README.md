# Mita Lite v0.3 (development)

Mita Lite is an unofficial Debian 13 (trixie) remix designed for older x86-64 laptops and desktops. This repository is the **development workspace** for v0.3; it does **not** yet contain a buildable ISO or finished v0.3 features.

## Planned improvements

- Mita desktop theme (Xfce wallpaper, icons, panel and login appearance)
- Performance mode with measured, reversible optimizations
- Graphical software center using Debian package tools
- Mita updater for Debian security updates and release notifications
- System information utility (CPU, RAM, storage and OS)
- Wi-Fi and NetworkManager configuration tools
- Intel and AMD x86-64 hardware compatibility checks and firmware guidance
- Recovery tools with safeguards and clear confirmation before changes

## Compatibility

The `amd64` architecture covers modern 64-bit **Intel and AMD** processors. A separate 32-bit build is not planned: Debian 13 does not provide a standard i386 kernel/installer. Firmware and graphics support must be validated on actual hardware.

## Development and testing

The existing [Mita Lite v0.2 project](https://github.com/RealZyynyu/mita-lite) is the starting reference. Before distributing a new ISO, port and review its build recipe, run static checks, build on Debian 13, boot-test with QEMU in BIOS and UEFI modes, and test installation on a disposable virtual disk. Never test installers on a disk containing important data without backups.

**Status:** roadmap only; features and ISO are not yet implemented or validated.
