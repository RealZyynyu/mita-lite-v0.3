# Release acceptance checks

**Current result: source validation only. No ISO or boot test has been performed.**

## Source checks

Run `python3 tools/validate.py`. This checks shell/Python syntax, parses desktop configuration, tests the configuration wrapper with a mock `lb`, verifies local launcher targets, and checks invalid-input handling without installing anything. It does not simulate APT or Linux boot.

## Required before calling an ISO usable

| Check | Method | Current status |
| --- | --- | --- |
| Package resolution and ISO generation | Fresh Debian 13 build; keep logs and package manifests | Not run |
| BIOS and UEFI | Boot live session in both VM firmware modes | Not run |
| Desktop | Inspect theme, wallpaper, panel, text scaling, Hub and screen lock | Not run |
| Authentication | Open Synaptic; verify an authentication agent appears | Not run |
| Install | Run text-mode Install from the USB boot menu; install to an empty VM disk, eject ISO, reboot; verify custom desktop survived | Not run |
| Updates | Update Debian packages, reboot and open the desktop again | Not run |
| Core hardware | Wi-Fi, Ethernet, Bluetooth, audio input/output, suspend and resume | Not run |
| App setup | Install Steam, Discord, Lutris; test failed download and cancellation paths | Not run |
| GPU | `glxinfo -B`; ensure physical GPU, not llvmpipe. Test `vulkaninfo --summary` only after optional Vulkan setup on a supported GPU | Not run |
| Games | Native/older OpenGL game; optional WineD3D test on a non-Vulkan GPU; Proton/Vulkan on a compatible GPU | Not run |
| Drivers | Test AMD/Intel; choose/test NVIDIA separately for the actual card | Not run |
| Resource goals | Measure installed desktop with 2 GiB RAM, then test with 4 GiB; record package versions and actual disk use | Not run |
| Secure Boot | Boot and verify kernel/module chain on the intended machine | Not run |

For resource measurement, boot the **installed** OS, wait two minutes, close Hub/browser, then record:

```sh
free -h
swapon --show
zramctl
df -h /
sudo du -xsh /usr /var /home
systemctl --failed
systemctl --user --failed
```

Report available RAM as well as used RAM: Linux uses spare memory for cache. Record whether Steam/Discord are running. A live session's compressed filesystem and RAM overlay are not representative of installed disk/RAM use.

Also record CPU/GPU, RAM, SSD model, screen resolution, kernel (`uname -r`), installed packages (`dpkg-query -W`), and per-game Proton/version/settings. Idle RAM does not establish gaming performance; measure frame times in the actual game.
