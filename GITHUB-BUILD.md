# Build Mita Lite without installing Linux locally

This repository includes a GitHub Actions workflow that builds the ISO in a temporary Linux machine on GitHub.

## Use it

1. Create or update the GitHub repository with the Mita Lite source, including the hidden `.github` folder.
2. Push changes to the `main` branch, or open the repository's **Actions** tab and run **Build Mita Lite ISO** manually.
3. Wait for the build to finish.
4. Download the artifact named **mita-lite-0.2-iso**, or use the `v0.2` GitHub Release asset.

The artifact contains the generated `.iso`, `SHA256SUMS` when available, and build logs when available. Successful builds also replace the `v0.2` release ISO with the newest build.

## Notes

- The build runs in a Debian 13 (`trixie`) privileged container because the supplied `build.sh` explicitly requires Debian 13 and `live-build` needs chroot/mount operations.
- GitHub-hosted runners have finite disk space. If the build runs out of space, use a Linux VM/cloud VM with at least 40 GiB free as described in `BUILD.md`.
- Release builds use workflow concurrency so an older in-progress build cannot overwrite a newer `v0.2` release asset.
