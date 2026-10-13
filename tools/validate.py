#!/usr/bin/env python3
"""Offline source checks. Never mounts filesystems or installs software."""
import ast
import configparser
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "config/includes.chroot"
SKIP_DIRS = {".git", "work", "out"}


def main():
    count = 0
    for path in ROOT.rglob("*"):
        rel = path.relative_to(ROOT)
        if not path.is_file() or any(part in SKIP_DIRS for part in rel.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # Binary assets are valid source inputs but are not text-format checks.
            continue
        if text.startswith(("#!/bin/bash", "#!/bin/sh")):
            subprocess.run(["bash", "-n", str(path)], check=True)
            assert os.access(path, os.X_OK), f"Not executable: {path}"
            count += 1
        if text.startswith(("#!/usr/bin/python3", "#!/usr/bin/env python3")):
            ast.parse(text, filename=str(path))
            count += 1
        if path.suffix in (".xml", ".svg"):
            ET.parse(path)
            count += 1
        if path.suffix == ".desktop":
            parser = configparser.ConfigParser(interpolation=None)
            parser.read_string(text)
            entry = parser["Desktop Entry"]
            assert entry["Type"] == "Application"
            target = shlex.split(entry["Exec"])[0]
            if target.startswith("/usr/local/"):
                assert (OVERLAY / target.lstrip("/")).is_file(), target
            count += 1

    package_lines = (ROOT / "config/package-lists/desktop.list.chroot").read_text().splitlines()
    packages = [line.strip() for line in package_lines if line.strip() and not line.startswith("#")]
    assert len(packages) == len(set(packages)), "Duplicate packages"
    assert all(re.fullmatch(r"[a-z0-9][a-z0-9+.-]+", p) for p in packages)
    assert "mate-polkit" in packages and "xfce4-polkit" not in packages
    assert (OVERLAY / "usr/share/doc/mita-lite/guide.html").is_file()
    assert (OVERLAY / "usr/share/backgrounds/mita-lite/orbit.svg").is_file()

    # Exercise argument quoting/forwarding without invoking live-build.
    with tempfile.TemporaryDirectory(prefix="mita-check-") as tmp:
        temp = Path(tmp)
        fake_lb = temp / "lb"
        fake_lb.write_text(
            "#!/usr/bin/env python3\nimport json, os, sys\n"
            "with open(os.environ['MITA_CAPTURE'], 'w') as f: json.dump(sys.argv[1:], f)\n"
        )
        fake_lb.chmod(0o755)
        env = dict(os.environ, PATH=str(temp) + os.pathsep + os.environ["PATH"],
                   MITA_CAPTURE=str(temp / "args.json"))
        subprocess.run([str(ROOT / "auto/config"), "--iso-preparer", "Name with spaces"],
                       env=env, cwd=tmp, check=True)
        args = json.loads((temp / "args.json").read_text())
        assert args[:2] == ["config", "noauto"]
        assert args[args.index("--distribution") + 1] == "trixie"
        assert args[args.index("--archive-areas") + 1] == "main contrib non-free non-free-firmware"
        assert args[-2:] == ["--iso-preparer", "Name with spaces"]

    # Invalid commands must fail before sudo, APT or downloads can run.
    helper = str(OVERLAY / "usr/local/bin/mita-apps")
    for args in ([], ["unrecognized"], ["steam", "extra"]):
        result = subprocess.run([helper, *args], capture_output=True, text=True)
        assert result.returncode == 2, (args, result)
        assert "Usage:" in result.stdout
    result = subprocess.run([str(ROOT / "build.sh"), "--help"], capture_output=True, text=True)
    assert result.returncode == 0 and "Debian 13" in result.stdout
    if os.geteuid() == 0:
        result = subprocess.run([helper, "steam"], capture_output=True, text=True)
        assert result.returncode == 1 and "regular desktop user" in result.stderr

    print(f"PASS: {count} source-format checks; {len(packages)} package-name entries.")
    print("PASS: configuration wrapper quoting, local assets, CLI input and root guards.")
    print("NOT RUN: package resolution, GTK rendering, ISO build/boot/install, hardware or games.")


if __name__ == "__main__":
    main()
