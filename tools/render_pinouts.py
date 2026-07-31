#!/usr/bin/env python3
"""Rendert die Pinout-Grafiken der Boards im Bestand mit boardgen.

boardgen erwartet ein Basisverzeichnis, das sowohl die eigenen Board-, Template-
und Shape-Definitionen als auch presets/roles/flash enthaelt. Statt die
mitgelieferten Dateien ins Repo zu kopieren, wird das Basisverzeichnis hier zur
Laufzeit zusammengesetzt: eigene Definitionen aus tools/boardgen/, der Rest per
Symlink aus dem installierten Paket.

    pip install boardgen
    python3 tools/render_pinouts.py

Ergebnis: tools/out/<board>.svg
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
OWN = HERE / "boardgen"
OUT = HERE / "out"

BOARDS = [
    "esp01s", "d1_mini",
    "esp32_devkitc", "cyd_2432s024r",
    "xiao_esp32c3",
    "xiao_esp32s3", "xiao_s3_sense", "esp32s3_devkitc1", "freenove_s3_cam",
]


def bundled_res() -> Path:
    try:
        import boardgen
    except ImportError:
        sys.exit("boardgen fehlt — 'pip install boardgen' ausfuehren.")
    res = Path(boardgen.__file__).parent / "res"
    if not res.is_dir():
        sys.exit(f"Ressourcen von boardgen nicht gefunden: {res}")
    return res


def build_base(tmp: Path, res: Path) -> Path:
    """Eigene Definitionen und mitgelieferte Ressourcen zusammenfuehren."""
    base = tmp / "base"
    base.mkdir()

    # presets/roles/flash muessen im Basisverzeichnis liegen
    for name in ("presets.json", "roles.json", "flash.json"):
        shutil.copy(res / name, base / name)

    # eigene Rollen und Presets ueber die mitgelieferten legen
    for name in ("roles.json", "presets.json"):
        own = OWN / name
        if not own.is_file():
            continue
        merged = json.loads((base / name).read_text(encoding="utf-8"))
        for key, value in json.loads(own.read_text(encoding="utf-8")).items():
            merged.setdefault(key, {}).update(value)
        (base / name).write_text(json.dumps(merged, indent=2), encoding="utf-8")

    # eigene Definitionen zuerst, mitgelieferte als Ergaenzung darunter
    for kind in ("boards", "templates", "shapes"):
        target = base / kind
        target.mkdir()
        for src_dir in (res / kind, OWN / kind):
            if not src_dir.is_dir():
                continue
            for f in src_dir.glob("*.json"):
                shutil.copy(f, target / f.name)
    return base


def main() -> int:
    res = bundled_res()
    OUT.mkdir(exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        base = build_base(Path(tmp), res)
        cmd = [
            "boardgen", "--base", str(base),
            "draw", *BOARDS,
            "-o", str(OUT), "-w", "3000", "-h", "1500", "--no-canvas",
        ]
        print("$", " ".join(cmd))
        r = subprocess.run(cmd, capture_output=True, text=True)
        sys.stdout.write(r.stdout)
        if r.returncode:
            sys.stderr.write(r.stderr)
            return r.returncode

    for svg in sorted(OUT.glob("*.svg")):
        print(f"  {svg.name:28} {svg.stat().st_size:>8} Bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
