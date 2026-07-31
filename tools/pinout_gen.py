#!/usr/bin/env python3
"""Erzeugt Pinout-Grafiken im Seeed-Stil als eigenständiges SVG.

Datenmodell je Board: Zeilen aus farbcodierten Chips, links und rechts
neben einer Platinendarstellung. Chips sind in Leserichtung angegeben,
die innerste Spalte führt jeweils die Leitung zum Pad.
"""

# Funktionsklassen — mittlere Sättigung, damit weiße Schrift auf hellem
# wie dunklem Seitenhintergrund lesbar bleibt.
CAT = {
    'power':  '#c0392b',
    'gnd':    '#33393d',
    'system': '#78868f',
    'gpio':   '#4f9243',
    'adc':    '#cf8524',
    'name':   '#7a5843',
    'spi':    '#8e56a8',
    'uart':   '#158b7c',
    'i2c':    '#2b8fc4',
    'periph': '#1a5468',
    'strap':  '#b8452f',
}

LEGEND = [
    ('power',  'POWER'),   ('gnd', 'GND'),      ('system', 'SYSTEM'),
    ('gpio',   'GPIO'),    ('adc', 'ADC'),      ('name',   'PIN NAME'),
    ('spi',    'SPI'),     ('uart', 'UART'),    ('i2c',    'I2C'),
    ('periph', 'ONBOARD'), ('strap', 'STRAPPING'),
]

CH, GAP, PAD_X, FS = 22, 7, 8, 11.0
PITCH = CH + GAP


def w(text):
    """Chipbreite aus der Textlänge; Monospace-Näherung."""
    return max(38, round(len(text) * 6.35 + 2 * PAD_X))


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def cols(rows, align='left'):
    """Spaltenbreiten je Seite: breitester Chip je Spaltenindex.

    align='right' bildet die nach innen buendige Anordnung der linken Seite ab —
    Chip j einer kurzen Zeile landet dort in Spalte n-len(row)+j. Messung und
    Platzierung muessen dieselbe Zuordnung verwenden, sonst ueberlappen Chips,
    die breiter sind als ihre Spalte.
    """
    n = max((len(r) for r in rows), default=0)
    width = [0] * n
    for r in rows:
        off = (n - len(r)) if align == 'right' else 0
        for j, (_, text) in enumerate(r):
            width[off + j] = max(width[off + j], w(text))
    return width


def chip(x, y, text, cat):
    return (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w(text):.0f}" height="{CH}" rx="3" '
            f'fill="{CAT[cat]}"/>'
            f'<text x="{x + w(text) / 2:.0f}" y="{y + CH / 2 + 3.9:.0f}" text-anchor="middle" '
            f'fill="#fff" font-size="{FS}" font-family="var(--font-display)" '
            f'font-weight="600">{esc(text)}</text>')


def render(title, subtitle, left, right, note=None, board_w=170):
    """left/right: Listen von Zeilen, jede Zeile eine Liste von (cat, text)."""
    lc, rc = cols(left, 'right'), cols(right)
    lead = 26
    lw = sum(lc) + GAP * max(0, len(lc) - 1) + lead
    rw = sum(rc) + GAP * max(0, len(rc) - 1) + lead
    rows = max(len(left), len(right))

    m_top, m_side = 46, 12
    body_h = rows * PITCH + 24
    legend_h = 58
    W = m_side * 2 + lw + board_w + rw
    # Kopf- und Fusszeile duerfen nicht ueber den viewBox-Rand laufen
    W = max(W, m_side * 2 + len(title) * 8.6, m_side * 2 + len(subtitle or '') * 6.4)
    if note:
        W = max(W, m_side * 2 + len(note) * 6.4)
    H = m_top + body_h + legend_h + (26 if note else 0)

    bx = m_side + lw
    by = m_top

    o = [f'<svg viewBox="0 0 {W:.0f} {H:.0f}" role="img" '
         f'aria-label="Pinout {esc(title)}" xmlns="http://www.w3.org/2000/svg">']

    # Titel
    o.append(f'<text x="{m_side}" y="20" font-size="14" font-weight="700" '
             f'font-family="var(--font-display)" fill="var(--ink)">{esc(title)}</text>')
    if subtitle:
        o.append(f'<text x="{m_side}" y="36" font-size="10.5" '
                 f'font-family="var(--font-display)" fill="var(--ink-3)">{esc(subtitle)}</text>')

    # Platine
    o.append(f'<rect x="{bx}" y="{by}" width="{board_w}" height="{body_h}" rx="9" '
             f'fill="#1b2124" stroke="#2f383c"/>')

    def pads_and_rows(side_rows, colw, side):
        out = []
        for i, row in enumerate(side_rows):
            cy = by + 12 + i * PITCH
            py = cy + CH / 2
            px = bx + (7 if side == 'L' else board_w - 7)
            out.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="4.6" fill="#c9922f"/>')
            out.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="2.1" fill="#1b2124"/>')

            if side == 'L':
                # Zeilen sind nach innen buendig: kurze Zeilen stehen an der
                # Platine, nicht am aeusseren Rand. Fehlende Spalten vorn ueber-
                # springen, damit der letzte Chip immer in der innersten liegt.
                skip = len(colw) - len(row)
                x = m_side + sum(colw[:skip]) + GAP * skip
                inner = x
                for j, (cat, text) in enumerate(row):
                    cw = colw[skip + j]
                    cx = x + cw - w(text)          # rechtsbündig in der Spalte
                    out.append(chip(cx, cy, text, cat))
                    inner = cx + w(text)
                    x += cw + GAP
                out.append(f'<line x1="{inner:.0f}" y1="{py:.0f}" x2="{px - 6:.0f}" y2="{py:.0f}" '
                           f'stroke="var(--rule)" stroke-width="1"/>')
            else:
                x = bx + board_w + lead
                first = x
                for j, (cat, text) in enumerate(row):
                    out.append(chip(x, cy, text, cat))
                    if j == 0:
                        first = x
                    x += colw[j] + GAP
                out.append(f'<line x1="{px + 6:.0f}" y1="{py:.0f}" x2="{first:.0f}" y2="{py:.0f}" '
                           f'stroke="var(--rule)" stroke-width="1"/>')
        return out

    o += pads_and_rows(left, lc, 'L')
    o += pads_and_rows(right, rc, 'R')

    # Beschriftung auf der Platine
    o.append(f'<text x="{bx + board_w / 2:.0f}" y="{by + body_h / 2:.0f}" text-anchor="middle" '
             f'fill="#8b979b" font-size="10.5" font-family="var(--font-display)" '
             f'font-weight="600">{esc(title.split(" · ")[0])}</text>')

    # Legende: nur die tatsächlich verwendeten Klassen
    used, seen = [], set()
    for row in left + right:
        for cat, _ in row:
            if cat not in seen:
                seen.add(cat)
                used.append(cat)
    ly = m_top + body_h + 20
    lx = m_side
    for cat in [c for c, _ in LEGEND if c in seen]:
        label = dict((c, l) for c, l in LEGEND)[cat]
        o.append(chip(lx, ly, label, cat))
        lx += w(label) + GAP

    if note:
        o.append(f'<text x="{m_side}" y="{ly + CH + 20:.0f}" font-size="10.5" '
                 f'font-family="var(--font-display)" fill="var(--ink-3)">{esc(note)}</text>')

    o.append('</svg>')
    return '\n'.join(o)
