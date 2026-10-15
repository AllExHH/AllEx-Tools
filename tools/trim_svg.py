#!/usr/bin/env python3
"""Schneidet die viewBox der gerenderten SVGs auf den tatsaechlichen Inhalt zu.

boardgen zeichnet immer auf eine feste Leinwand; der Inhalt sitzt mittig darin
und laesst je nach Board viel Leerraum. Die echte Ausdehnung liefert nur eine
Layout-Engine, deshalb wird sie hier per getBBox() in Headless-Chromium
gemessen und als neue viewBox zurueckgeschrieben.

    python3 tools/trim_svg.py assets/pinouts/*.svg
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
MARGIN = 8.0        # Nutzereinheiten Luft rundum


def bbox(svg_text: str) -> dict | None:
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp, "m.html")
        page.write_text(
            "<body>" + svg_text.split("?>", 1)[-1] +
            "<script>const b=document.querySelector('svg').getBBox();"
            "document.title=JSON.stringify({x:b.x,y:b.y,w:b.width,h:b.height});</script>",
            encoding="utf-8")
        r = subprocess.run(
            [CHROME, "--headless", "--no-sandbox", "--disable-gpu",
             "--virtual-time-budget=4000", "--dump-dom", page.as_uri()],
            capture_output=True, text=True, timeout=120)
    m = re.search(r"<title>(\{.*?\})</title>", r.stdout)
    return json.loads(m.group(1)) if m else None


def trim(path: Path) -> str:
    s = path.read_text(encoding="utf-8")
    b = bbox(s)
    if not b or b["w"] <= 0:
        return f"{path.name}: Messung fehlgeschlagen, unveraendert"
    x, y = b["x"] - MARGIN, b["y"] - MARGIN
    w, h = b["w"] + 2 * MARGIN, b["h"] + 2 * MARGIN
    s = re.sub(r'viewBox="[^"]*"', f'viewBox="{x:.1f},{y:.1f},{w:.1f},{h:.1f}"', s, count=1)
    s = re.sub(r'\sheight="[\d.]+"', f' height="{h:.0f}"', s, count=1)
    s = re.sub(r'\swidth="[\d.]+"', f' width="{w:.0f}"', s, count=1)
    path.write_text(s, encoding="utf-8")
    return f"{path.name:32} {w:.0f} x {h:.0f}  (Seitenverhaeltnis {w/h:.2f})"


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        print(trim(Path(arg)))
