#!/usr/bin/env python3
"""Erzeugt die boardgen-Templates und Board-Dateien der Boards im Bestand.

Acht der zehn Boards teilen sich wenige Grundformen — ein langes Devkit mit
Stiftleisten an beiden Laengsseiten, ein XIAO im Scheckkartenformat mit
Castellated-Pads, dazu zwei Sonderfaelle (ESP-01S, CYD). Deshalb entstehen die
Templates hier parametrisch statt als handgepflegtes JSON: eine Korrektur an der
Grundform wirkt auf alle Boards derselben Familie.

Ausgenommen ist xiao-esp32s3 — dieses Template ist handabgestimmt und
abgenommen, es wird von hier nicht angefasst.

    python3 tools/make_boards.py     # schreibt tools/boardgen/{templates,boards}
    python3 tools/render_pinouts.py  # rendert daraus die SVGs
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TPL = HERE / "boardgen" / "templates"
BRD = HERE / "boardgen" / "boards"
SILK = "${SILK_COLOR}"
RASTER = 2.54
HAIR = 0.14


# ── Zeichenprimitive ──────────────────────────────────────────────────────
def rect(x, y, w, h, **kw):
    d = {"type": "rect", "pos": f"{x:.2f},{y:.2f}", "size": f"{w:.2f},{h:.2f}"}
    d.update(kw)
    return d


def circle(x, y, d, **kw):
    o = {"type": "circle", "pos": f"{x:.2f},{y:.2f}", "d": d}
    o.update(kw)
    return o


def text(x, y, s, size=0.8, color=SILK):
    return {"type": "text", "pos": f"{x:.2f},{y:.2f}", "text": s,
            "font_size": size, "fill": {"color": color}}


def pcb(w, h, r=1.2):
    return rect(0, 0, w, h, rx=r, ry=r, preset="${MASK_PRESET}")


def usb_c(x, y, w=8.8, h=3.4):
    return [rect(x, y, w, h, rx=0.5, ry=0.5,
                 fill={"lgrad": ["0,0", "#E8E8E8", "0,1", "#9A9A9A"]}),
            rect(x + 1.25, y + 1.0, w - 2.5, h - 1.9, rx=0.7, ry=0.7,
                 fill={"color": "#4A4A4A"})]


def usb_micro(x, y, w=7.5, h=2.6):
    return [rect(x, y, w, h, rx=0.3, ry=0.3,
                 fill={"lgrad": ["0,0", "#DCDCDC", "0,1", "#8E8E8E"]}),
            rect(x + 1.1, y + 0.8, w - 2.2, h - 1.5,
                 fill={"color": "#4A4A4A"})]


def shield(x, y, w, h, label=None, sub=None):
    """HF-Abschirmblech mit optionalem Typenschild."""
    out = [rect(x, y, w, h, preset="shield")]
    if label:
        out.append(rect(x + 0.7, y + h * 0.18, w - 1.4, h * 0.5, rx=0.3, ry=0.3,
                        fill={"color": "#FBFBFB"}))
        out.append(text(x + w / 2, y + h * 0.42, label, min(1.0, w / 12), "#222222"))
        if sub:
            out.append(text(x + w / 2, y + h * 0.60, sub, min(0.7, w / 18), "#555555"))
    return out


def button(x, y, d=2.6):
    return [circle(x, y, d, fill={"lgrad": ["0,0", "#E0E0E0", "0,1", "#9C9C9C"]}),
            circle(x, y, d * 0.45, fill={"color": "#2B2B2B"})]


def pin_rows(w, pad_y, n, kind="r_header_vert"):
    return [
        {"id": "left", "name": kind, "repeat": n, "pos": f"0,{pad_y:.2f}",
         "vars": {"PINDIR": "left"}},
        {"id": "right", "name": kind, "repeat": n, "pos": f"{w:.2f},{pad_y:.2f}",
         "vars": {"PINDIR": "right"}},
    ]


def pads_for(name, left, right, side="front"):
    """Pad-Namen auf die Anker der beiden Pinreihen abbilden."""
    m = {}
    for i, p in enumerate(left, 1):
        if p:
            m[p] = f"{name}.{side}.left.pin{i}"
    for i, p in enumerate(right, 1):
        if p:
            m[p] = f"{name}.{side}.right.pin{i}"
    return m


# ── Grundform: langes Devkit mit Stiftleisten ─────────────────────────────
def devkit(name, title, w, h, left, right, *, module=None, module_sub=None,
           usb="micro", usb_at="bottom", buttons=(), extras_front=(),
           back=None, pad_inset=None, silk=None):
    n = max(len(left), len(right))
    pad_y = pad_inset if pad_inset is not None else (h - (n - 1) * RASTER) / 2

    front = [pcb(w, h)]
    if usb:
        cw = 8.8 if usb == "c" else 7.5
        cx = (w - cw) / 2
        cy = -0.9 if usb_at == "top" else h - 2.5
        front += (usb_c(cx, cy) if usb == "c" else usb_micro(cx, cy))
    if module:
        mw = min(w - 5.0, 18.0)
        front += shield((w - mw) / 2, pad_y - 1.5, mw, mw * 0.62, module, module_sub)
    for bx, by in buttons:
        front += button(bx, by)
    front += list(extras_front)
    front += [text(w / 2, h - 4.2, silk or title.split("·")[0].strip(), 0.9)]
    front += pin_rows(w, pad_y, n)

    t = {
        "name": name, "title": title, "width": w, "height": h,
        "vars": {"RASTER": RASTER, "MASK_HOLE": "#101010"},
        "front": front,
        "back": back or [],
        "pads": pads_for(name, left, right),
        "test_pads": {},
    }
    return t


# ── Grundform: XIAO ──────────────────────────────────────────────────────
def xiao(name, title, left, right, *, module_label, module_sub,
         antenna="ufl", back=None, test_pads=None):
    W, H, PAD_Y = 17.5, 21.0, 4.7
    front = [pcb(W, H)]
    front += usb_c(4.35, -0.9)
    front += [circle(2.5, 2.0, 1.5, preset="copper2"), text(2.5, 3.9, "R", 1.1),
              circle(15.0, 2.0, 1.5, preset="copper2"), text(15.0, 3.9, "B", 1.1)]
    front += shield(2.6, 4.6, 12.3, 10.4, module_label, module_sub)
    if antenna == "ufl":
        front += [circle(3.9, 17.4, 2.6,
                         fill={"lgrad": ["0,0", "#D8D8D8", "0,1", "#8C8C8C"]}),
                  circle(3.9, 17.4, 1.0, fill={"color": "#3A3A3A"})]
    else:                                   # Keramikantenne
        front += [rect(2.6, 16.2, 3.4, 2.4, rx=0.2, ry=0.2,
                       fill={"color": "#2C4E8A"})]
    front += [rect(7.2, 16.1, 7.6, 2.6, rx=0.2, ry=0.2, fill={"color": "#1C1C1C"}),
              rect(7.6, 16.6, 6.8, 1.6, fill={"color": "#3E3E3E"})]
    front += [
        {"id": "left", "name": "r_pins_vert", "repeat": 7, "pos": f"0,{PAD_Y}",
         "vars": {"PINDIR": "left"}},
        {"id": "right", "name": "r_pins_vert", "repeat": 7, "pos": f"{W},{PAD_Y}",
         "vars": {"PINDIR": "right"}},
    ]
    return {
        "name": name, "title": title, "width": W, "height": H,
        "vars": {"PINTYPE_VERT": "pin_vert_cast_hole", "RASTER": RASTER, "PAD_Y": PAD_Y},
        "front": front,
        "back": back or [],
        "pads": pads_for(name, left, right),
        "test_pads": test_pads or {},
    }


def xiao_back(name, pad_left, pad_right, silk_title, clusters, bat=None):
    """Rueckseite eines XIAO: gespiegelter Siebdruck, mittige Testpads mit
    Haarlinien nach aussen, Callouts haengen an unsichtbaren Randankern."""
    W, H, PAD_Y = 17.5, 21.0, 4.7
    COLL, COLR = 6.6, 10.9
    rows = [6.30, 8.84, 11.38, 13.92][:len(clusters[0])]

    back = [pcb(W, H), text(W / 2, 2.30, "Unterseite - gespiegelt", 0.85)]
    for i, nm in enumerate(pad_left):
        back.append(text(2.30, PAD_Y + i * RASTER + 0.30, nm, 0.8))
    for i, nm in enumerate(pad_right):
        back.append(text(14.40, PAD_Y + i * RASTER + 0.30, nm, 0.8))

    for y in rows:
        back.append(rect(0, y - HAIR / 2, COLL, HAIR, fill={"color": "#6E6A5F"}))
        back.append(rect(COLR, y - HAIR / 2, W - COLR, HAIR, fill={"color": "#6E6A5F"}))
    for y, nl, nr in zip(rows, clusters[0], clusters[1]):
        back += [circle(COLL, y, 0.9, preset="copper1"), text(COLL + 1.5, y + 0.28, nl, 0.7),
                 circle(COLR, y, 0.9, preset="copper1"), text(COLR + 1.5, y + 0.28, nr, 0.7)]

    tp = {}
    for i, y in enumerate(rows, 1):
        back.append({"id": f"al{i}", "name": "anchor_edge", "pos": f"0,{y:.2f}",
                     "vars": {"PINDIR": "left"}})
        back.append({"id": f"ar{i}", "name": "anchor_edge", "pos": f"{W},{y:.2f}",
                     "vars": {"PINDIR": "right"}})
    if bat:
        bm, bp = 16.46, 19.00
        back += [
            rect(11.5, bm - HAIR / 2, W - 11.5, HAIR, fill={"color": "#6E6A5F"}),
            rect(12.9 - HAIR / 2, bm, HAIR, bp - bm, fill={"color": "#6E6A5F"}),
            rect(12.9, bp - HAIR / 2, W - 12.9, HAIR, fill={"color": "#6E6A5F"}),
            circle(11.5, bm, 0.9, preset="copper1"),
            circle(12.9, bm, 0.9, preset="copper1"),
            text(12.2, bm + 1.30, "BAT", 0.7),
            {"id": "abm", "name": "anchor_edge", "pos": f"{W},{bm}", "vars": {"PINDIR": "right"}},
            {"id": "abp", "name": "anchor_edge", "pos": f"{W},{bp}", "vars": {"PINDIR": "right"}},
        ]
        tp[bat[0]] = f"{name}.back.abm.a"
        tp[bat[1]] = f"{name}.back.abp.a"
    back += [text(5.6, 18.6, silk_title[0], 0.85), text(5.6, 19.8, silk_title[1], 0.85)]

    for i, nm in enumerate(clusters[0], 1):
        tp[nm] = f"{name}.back.al{i}.a"
    for i, nm in enumerate(clusters[1], 1):
        tp[nm] = f"{name}.back.ar{i}.a"
    return back, tp


def write(kind, name, data):
    path = (TPL if kind == "template" else BRD) / f"{name}.json"
    path.write_text(json.dumps(data, indent="\t", ensure_ascii=False) + "\n",
                    encoding="utf-8")
    return path


def board(variant, name, vendor, url, tpl, pinout, *, flash, ram=327680,
          mcu="esp32", family="esp32", fcpu="240000000L", scale=26, symbol=None):
    return {
        "build": {"f_cpu": fcpu, "family": family, "mcu": mcu, "variant": variant},
        "name": name, "url": url, "vendor": vendor,
        "upload": {"flash_size": flash, "maximum_size": int(flash * 0.4),
                   "maximum_ram_size": ram},
        "pcb": {"symbol": symbol or variant.upper(), "templates": tpl,
                "scale": scale, "pinout": pinout},
    }
