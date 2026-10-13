#!/bin/bash
set -euo pipefail

project_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
if [[ ${1:-} == --help ]]; then
    cat "$project_dir/BUILD.md"
    exit 0
fi
[[ $# == 0 ]] || { echo 'Usage: ./build.sh [--help]' >&2; exit 2; }
[[ $EUID == 0 ]] || { echo 'Run sudo ./build.sh on a Debian 13 amd64 builder.' >&2; exit 1; }
. /etc/os-release
[[ ${ID:-} == debian && ${VERSION_CODENAME:-} == trixie ]] || {
    echo 'This recipe requires a Debian 13 (trixie) build host or VM.' >&2; exit 1;
}
[[ $(dpkg --print-architecture) == amd64 ]] || { echo 'An amd64 builder is required.' >&2; exit 1; }
for program in lb debootstrap xorriso mksquashfs; do
    command -v "$program" >/dev/null || { echo "Missing $program. Read BUILD.md." >&2; exit 1; }
done
# Always use a new directory. No cleanup or disk-writing commands are automatic.
mkdir -p "$project_dir/work"
build_dir=$(mktemp -d "$project_dir/work/build-XXXXXXXX")
cp -a "$project_dir/auto" "$project_dir/config" "$build_dir/"
cd "$build_dir"
printf 'Building in %s\n' "$build_dir"
lb config 2>&1 | tee configure.log
lb build 2>&1 | tee build.log
shopt -s nullglob
images=( *.iso )
(( ${#images[@]} == 1 )) || { echo 'Expected exactly one ISO; inspect build.log.' >&2; exit 1; }
sha256sum "${images[0]}" > SHA256SUMS
printf '\nISO: %s/%s\nChecksum: %s/SHA256SUMS\n' "$build_dir" "${images[0]}" "$build_dir"
