# 0.2 — older-PC defaults

- Target older x86-64 PCs with 2 GiB RAM for the desktop and light/native games. This is a test target, not a measured minimum or game-compatibility promise.
- Turn off Xfce compositing and GTK animations; use one workspace.
- Keep the dark theme and wallpaper; use Adwaita plus its legacy icons instead of Papirus.
- Do not launch Game Hub at login. Size its scrollable window for smaller displays.
- Remove thumbnail generation, remote-filesystem backends, desktop portals and broad extra fonts from the explicit base list. Dependencies may still bring some components back.
- Make Bluetooth, Vulkan diagnostics/drivers, and GameMode optional. Keep network, sound and OpenGL support in the base.
- Install Steam/Lutris without optional recommended packages; keep necessary dependencies and 32-bit OpenGL libraries.
- Use the text-mode Debian live installer from the USB boot menu instead of bundling Calamares in the desktop.
- Explain the per-game WineD3D/OpenGL option for older DirectX 9–11 games. It does not guarantee compatibility or provide a DirectX 12 fallback.
- Keep compressed swap and bounded logs. Keep firmware coverage until the intended hardware is identified.

The revised ISO is not built or boot-tested. 32-bit-only CPUs remain outside this build's scope. Modern games, web pages and proprietary chat/game clients can exceed the intended hardware's capabilities even when the desktop itself runs well.
