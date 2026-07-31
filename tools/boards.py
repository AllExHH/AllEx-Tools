#!/usr/bin/env python3
"""Pin-Daten der acht Boards im Bestand. Zeilen in physischer Reihenfolge."""

from pinout_gen import render

BOARDS = {}

# ── ESP-01 / ESP-01S ──────────────────────────────────────────────────────
# Nummerierung wie im Eagle-Schaltplan des eigenen Shields (JP2).
BOARDS['esp01'] = dict(
    title='ESP-01S · ESP8266EX',
    subtitle='2x4-Header · Nummerierung wie JP2 im eigenen Shield',
    board_w=150,
    note='Nur GPIO0 und GPIO2 nutzbar — genau die zwei Leitungen, die APA102 braucht.',
    left=[
        [('name', 'Pin 1'), ('uart', 'TXD'), ('gpio', 'GPIO1')],
        [('name', 'Pin 3'), ('system', 'CH_PD / EN'), ('power', 'an 3V3')],
        [('name', 'Pin 5'), ('system', 'RST'), ('power', 'an 3V3')],
        [('name', 'Pin 7'), ('power', 'VCC 3V3'), ('power', 'REG1117')],
    ],
    right=[
        [('name', 'Pin 2'), ('gnd', 'GND')],
        [('name', 'Pin 4'), ('gpio', 'GPIO2'), ('strap', 'Strapping'), ('periph', 'LED_out 2')],
        [('name', 'Pin 6'), ('gpio', 'GPIO0'), ('strap', 'Strapping'), ('periph', 'LED_out 3')],
        [('name', 'Pin 8'), ('uart', 'RXD'), ('gpio', 'GPIO3')],
    ],
)

# ── Wemos D1 mini ─────────────────────────────────────────────────────────
BOARDS['d1mini'] = dict(
    title='Wemos D1 mini · ESP8266EX',
    subtitle='4 MB Flash · micro-USB',
    board_w=160,
    note='LED-Ausgang bevorzugt auf D1 oder D2 — D3, D4 und D8 sind Strapping-Pins.',
    left=[
        [('uart', 'TX'), ('gpio', 'GPIO1')],
        [('uart', 'RX'), ('gpio', 'GPIO3')],
        [('name', 'D1'), ('gpio', 'GPIO5'), ('i2c', 'SCL')],
        [('name', 'D2'), ('gpio', 'GPIO4'), ('i2c', 'SDA')],
        [('name', 'D3'), ('gpio', 'GPIO0'), ('strap', 'Strapping')],
        [('name', 'D4'), ('gpio', 'GPIO2'), ('periph', 'Onboard-LED')],
        [('gnd', 'GND')],
        [('power', '5V')],
    ],
    right=[
        [('system', 'RST')],
        [('name', 'A0'), ('adc', 'ADC0')],
        [('name', 'D0'), ('gpio', 'GPIO16'), ('system', 'Wakeup')],
        [('name', 'D5'), ('gpio', 'GPIO14'), ('spi', 'SCK')],
        [('name', 'D6'), ('gpio', 'GPIO12'), ('spi', 'MISO')],
        [('name', 'D7'), ('gpio', 'GPIO13'), ('spi', 'MOSI')],
        [('name', 'D8'), ('gpio', 'GPIO15'), ('strap', 'Strapping')],
        [('power', '3V3')],
    ],
)

# ── ESP32 DevKitC (38-polig) ──────────────────────────────────────────────
BOARDS['devkit'] = dict(
    title='ESP32 DevKitC · WROOM-32',
    subtitle='38-polig · 4 MB Flash · 2x 240 MHz',
    board_w=170,
    note='GPIO6-11 sind der interne Flash und dürfen nicht beschaltet werden.',
    left=[
        [('power', '3V3')],
        [('system', 'EN')],
        [('name', 'VP'), ('gpio', 'GPIO36'), ('adc', 'ADC1'), ('system', 'nur Eingang')],
        [('name', 'VN'), ('gpio', 'GPIO39'), ('adc', 'ADC1'), ('system', 'nur Eingang')],
        [('gpio', 'GPIO34'), ('adc', 'ADC1'), ('system', 'nur Eingang')],
        [('gpio', 'GPIO35'), ('adc', 'ADC1'), ('system', 'nur Eingang')],
        [('gpio', 'GPIO32'), ('adc', 'ADC1')],
        [('gpio', 'GPIO33'), ('adc', 'ADC1')],
        [('gpio', 'GPIO25'), ('adc', 'ADC2')],
        [('gpio', 'GPIO26'), ('adc', 'ADC2')],
        [('gpio', 'GPIO27'), ('adc', 'ADC2')],
        [('gpio', 'GPIO14'), ('adc', 'ADC2')],
        [('gpio', 'GPIO12'), ('strap', 'MTDI — LOW halten!')],
        [('gnd', 'GND')],
        [('gpio', 'GPIO13'), ('adc', 'ADC2')],
        [('periph', 'SD2'), ('gpio', 'GPIO9'), ('system', 'Flash — tabu')],
        [('periph', 'SD3'), ('gpio', 'GPIO10'), ('system', 'Flash — tabu')],
        [('periph', 'CMD'), ('gpio', 'GPIO11'), ('system', 'Flash — tabu')],
        [('power', '5V')],
    ],
    right=[
        [('gnd', 'GND')],
        [('gpio', 'GPIO23'), ('spi', 'MOSI')],
        [('gpio', 'GPIO22'), ('i2c', 'SCL')],
        [('uart', 'TX0'), ('gpio', 'GPIO1')],
        [('uart', 'RX0'), ('gpio', 'GPIO3')],
        [('gpio', 'GPIO21'), ('i2c', 'SDA')],
        [('gnd', 'GND')],
        [('gpio', 'GPIO19'), ('spi', 'MISO')],
        [('gpio', 'GPIO18'), ('spi', 'SCK')],
        [('gpio', 'GPIO5'), ('spi', 'CS'), ('strap', 'Strapping')],
        [('gpio', 'GPIO17')],
        [('gpio', 'GPIO16')],
        [('gpio', 'GPIO4'), ('adc', 'ADC2')],
        [('gpio', 'GPIO0'), ('strap', 'Boot')],
        [('gpio', 'GPIO2'), ('strap', 'Strapping')],
        [('gpio', 'GPIO15'), ('strap', 'Strapping')],
        [('periph', 'SD1'), ('gpio', 'GPIO8'), ('system', 'Flash — tabu')],
        [('periph', 'SD0'), ('gpio', 'GPIO7'), ('system', 'Flash — tabu')],
        [('periph', 'CLK'), ('gpio', 'GPIO6'), ('system', 'Flash — tabu')],
    ],
)

# ── Seeed XIAO ESP32-C3 ───────────────────────────────────────────────────
BOARDS['xiaoc3'] = dict(
    title='XIAO ESP32-C3',
    subtitle='4 MB · USB-C · dunkelblaue Chips = Belegung durch den IR-Mate-Aufsatz',
    board_w=150,
    note='GPIO9 ist Boot-Pin und zugleich die Reset-Taste des IR-Mate-Aufsatzes.',
    left=[
        [('name', 'D0'), ('gpio', 'GPIO2'), ('adc', 'A0')],
        [('name', 'D1'), ('gpio', 'GPIO3'), ('adc', 'A1'), ('periph', 'IR-Sender')],
        [('name', 'D2'), ('gpio', 'GPIO4'), ('adc', 'A2'), ('periph', 'IR-Empfang')],
        [('name', 'D3'), ('gpio', 'GPIO5'), ('adc', 'A3'), ('periph', 'Touch')],
        [('name', 'D4'), ('gpio', 'GPIO6'), ('i2c', 'SDA'), ('periph', 'Vibration')],
        [('name', 'D5'), ('gpio', 'GPIO7'), ('i2c', 'SCL'), ('periph', 'WS2812')],
        [('name', 'D6'), ('gpio', 'GPIO21'), ('uart', 'TX')],
    ],
    right=[
        [('power', '5V')],
        [('gnd', 'GND')],
        [('power', '3V3')],
        [('name', 'D10'), ('gpio', 'GPIO10'), ('spi', 'MOSI')],
        [('name', 'D9'), ('gpio', 'GPIO9'), ('spi', 'MISO'), ('strap', 'Boot / Reset')],
        [('name', 'D8'), ('gpio', 'GPIO8'), ('spi', 'SCK'), ('strap', 'Strapping')],
        [('name', 'D7'), ('gpio', 'GPIO20'), ('uart', 'RX')],
    ],
)

# ── ESP32-S3-DevKitC-1 N16R8 ──────────────────────────────────────────────
BOARDS['s3devkit'] = dict(
    title='ESP32-S3-DevKitC-1 · N16R8',
    subtitle='16 MB Flash + 8 MB Oktal-PSRAM · zwei USB-Buchsen',
    board_w=175,
    note='Bei N16R8 sind GPIO33-37 vom PSRAM belegt, obwohl der Aufdruck sie frei zeigt.',
    left=[
        [('power', '3V3')],
        [('power', '3V3')],
        [('system', 'RST')],
        [('gpio', 'GPIO4'), ('adc', 'ADC1')],
        [('gpio', 'GPIO5'), ('adc', 'ADC1')],
        [('gpio', 'GPIO6'), ('adc', 'ADC1')],
        [('gpio', 'GPIO7'), ('adc', 'ADC1')],
        [('gpio', 'GPIO15'), ('adc', 'ADC2')],
        [('gpio', 'GPIO16'), ('adc', 'ADC2')],
        [('gpio', 'GPIO17'), ('adc', 'ADC2')],
        [('gpio', 'GPIO18'), ('adc', 'ADC2')],
        [('gpio', 'GPIO8'), ('i2c', 'SDA')],
        [('gpio', 'GPIO3'), ('strap', 'Strapping')],
        [('gpio', 'GPIO46'), ('strap', 'Strapping')],
        [('gpio', 'GPIO9'), ('i2c', 'SCL')],
        [('gpio', 'GPIO10'), ('spi', 'CS')],
        [('gpio', 'GPIO11'), ('spi', 'MOSI')],
        [('gpio', 'GPIO12'), ('spi', 'SCK')],
        [('gpio', 'GPIO13'), ('spi', 'MISO')],
        [('gpio', 'GPIO14')],
        [('power', '5V')],
        [('gnd', 'GND')],
    ],
    right=[
        [('gnd', 'GND')],
        [('uart', 'TX'), ('gpio', 'GPIO43')],
        [('uart', 'RX'), ('gpio', 'GPIO44')],
        [('gpio', 'GPIO1'), ('adc', 'ADC1')],
        [('gpio', 'GPIO2'), ('adc', 'ADC1')],
        [('gpio', 'GPIO42')],
        [('gpio', 'GPIO41')],
        [('gpio', 'GPIO40')],
        [('gpio', 'GPIO39')],
        [('gpio', 'GPIO38')],
        [('gpio', 'GPIO37'), ('system', 'PSRAM belegt')],
        [('gpio', 'GPIO36'), ('system', 'PSRAM belegt')],
        [('gpio', 'GPIO35'), ('system', 'PSRAM belegt')],
        [('gpio', 'GPIO0'), ('strap', 'Boot')],
        [('gpio', 'GPIO45'), ('strap', 'Strapping')],
        [('gpio', 'GPIO48'), ('periph', 'WS2812')],
        [('gpio', 'GPIO47')],
        [('gpio', 'GPIO21')],
        [('gpio', 'GPIO20'), ('periph', 'USB D+')],
        [('gpio', 'GPIO19'), ('periph', 'USB D-')],
        [('gnd', 'GND')],
        [('gnd', 'GND')],
    ],
)

# ── Freenove ESP32-S3-WROOM CAM ───────────────────────────────────────────
# Reihenfolge und Belegung aus ESP32S3_Pinout.png im eigenen Repo.
BOARDS['freenove'] = dict(
    title='Freenove ESP32-S3-WROOM CAM',
    subtitle='8 MB Flash + 8 MB PSRAM · OV2640 · Belegung laut ESP32S3_Pinout.png',
    board_w=175,
    note='Die Kamera belegt 14 GPIOs fest — frei bleiben im Wesentlichen 21, 47 und 45.',
    left=[
        [('power', '3V3')],
        [('system', 'RST')],
        [('gpio', 'GPIO4'), ('periph', 'CAM_SIOD')],
        [('gpio', 'GPIO5'), ('periph', 'CAM_SIOC')],
        [('gpio', 'GPIO6'), ('periph', 'CAM_VSYNC')],
        [('gpio', 'GPIO7'), ('periph', 'CAM_HREF')],
        [('gpio', 'GPIO15'), ('periph', 'CAM_XCLK')],
        [('gpio', 'GPIO16'), ('periph', 'CAM_Y9')],
        [('gpio', 'GPIO17'), ('periph', 'CAM_Y8')],
        [('gpio', 'GPIO18'), ('periph', 'CAM_Y7')],
        [('gpio', 'GPIO8'), ('periph', 'CAM_Y4')],
        [('gpio', 'GPIO3'), ('strap', 'JTAG EN')],
        [('gpio', 'GPIO46'), ('system', 'LOG')],
        [('gpio', 'GPIO9'), ('periph', 'CAM_Y3')],
        [('gpio', 'GPIO10'), ('periph', 'CAM_Y5')],
        [('gpio', 'GPIO11'), ('periph', 'CAM_Y2')],
        [('gpio', 'GPIO12'), ('periph', 'CAM_Y6')],
        [('gpio', 'GPIO13'), ('periph', 'CAM_PCLK')],
        [('gpio', 'GPIO14')],
        [('power', '5V')],
    ],
    right=[
        [('gpio', 'GPIO43'), ('uart', 'U0TXD')],
        [('gpio', 'GPIO44'), ('uart', 'U0RXD')],
        [('gpio', 'GPIO1'), ('adc', 'ADC1')],
        [('gpio', 'GPIO2'), ('periph', 'LED ON')],
        [('gpio', 'GPIO42')],
        [('gpio', 'GPIO41')],
        [('gpio', 'GPIO40'), ('periph', 'SD_DATA')],
        [('gpio', 'GPIO39'), ('periph', 'SD_CLK')],
        [('gpio', 'GPIO38'), ('periph', 'SD_CMD')],
        [('gpio', 'GPIO37'), ('system', 'PSRAM belegt')],
        [('gpio', 'GPIO36'), ('system', 'PSRAM belegt')],
        [('gpio', 'GPIO35'), ('system', 'PSRAM belegt')],
        [('gpio', 'GPIO0'), ('strap', 'Boot')],
        [('gpio', 'GPIO45'), ('strap', 'Strapping')],
        [('gpio', 'GPIO48'), ('periph', 'WS2812')],
        [('gpio', 'GPIO47')],
        [('gpio', 'GPIO21')],
        [('gpio', 'GPIO20'), ('periph', 'USB D+')],
        [('gpio', 'GPIO19'), ('periph', 'USB D-')],
        [('gnd', 'GND')],
    ],
)

# ── CYD ESP32-2432S024R ───────────────────────────────────────────────────
# Kein Stiftleisten-Board: Belegung ist fest verdrahtet, Quelle ist der
# Schaltplan V1.0 im eigenen Repo. Links Onboard-Peripherie, rechts frei.
BOARDS['cyd'] = dict(
    title='CYD ESP32-2432S024R',
    subtitle='resistiv · fest verdrahtete Peripherie laut Schaltplan V1.0',
    board_w=190,
    note='Touch und Display teilen sich einen SPI-Bus — unterschieden nur durch CS.',
    left=[
        [('periph', 'TFT SCK'), ('gpio', 'GPIO14')],
        [('periph', 'TFT MOSI'), ('gpio', 'GPIO13')],
        [('periph', 'TFT MISO'), ('gpio', 'GPIO12')],
        [('periph', 'TFT DC'), ('gpio', 'GPIO2')],
        [('periph', 'TFT CS'), ('gpio', 'GPIO15')],
        [('periph', 'Backlight'), ('gpio', 'GPIO27')],
        [('periph', 'Touch CS'), ('gpio', 'GPIO33')],
        [('periph', 'Touch IRQ'), ('gpio', 'GPIO36')],
        [('periph', 'Audio'), ('gpio', 'GPIO26')],
    ],
    right=[
        [('periph', 'SD CLK'), ('gpio', 'GPIO18')],
        [('periph', 'SD MISO'), ('gpio', 'GPIO19')],
        [('periph', 'SD MOSI'), ('gpio', 'GPIO23')],
        [('periph', 'SD CS'), ('gpio', 'GPIO5')],
        [('periph', 'RGB rot'), ('gpio', 'GPIO4')],
        [('periph', 'RGB grün'), ('gpio', 'GPIO16')],
        [('periph', 'RGB blau'), ('gpio', 'GPIO17')],
        [('periph', 'LDR'), ('gpio', 'GPIO34'), ('adc', 'ADC1')],
        [('system', 'frei auf P3'), ('gpio', 'GPIO21 / 22 / 35')],
    ],
)

# ── 01Space ESP32-C3 0.42 Zoll ────────────────────────────────────────────
# Physische Pad-Reihenfolge nicht belegt — daher Funktionskarte statt
# Positionsangabe. Nur gesicherte Belegungen.
BOARDS['c3lcd'] = dict(
    title='01Space ESP32-C3 0.42"',
    subtitle='Funktionskarte — physische Pad-Reihenfolge nicht belegt',
    board_w=160,
    note='OLED ist ein 72x40-Ausschnitt aus einem 128x64-Controller: Versatz x=30, y=12.',
    left=[
        [('periph', 'OLED SDA'), ('gpio', 'GPIO5'), ('i2c', 'I2C')],
        [('periph', 'OLED SCL'), ('gpio', 'GPIO6'), ('i2c', 'I2C')],
        [('periph', 'WS2812'), ('gpio', 'GPIO2 oder 8')],
        [('strap', 'Boot'), ('gpio', 'GPIO9')],
    ],
    right=[
        [('power', '5V')],
        [('power', '3V3')],
        [('gnd', 'GND')],
        [('gpio', 'GPIO0-10, 20, 21'), ('system', 'herausgeführt')],
    ],
)


# ── Seeed XIAO ESP32-S3 ───────────────────────────────────────────────────
# Belegung abgelesen aus den beiden Seeed-Pinout-Grafiken (Ober- und
# Unterseite). Achtung: NICHT identisch mit dem XIAO ESP32-C3.
BOARDS['xiaos3'] = dict(
    title='XIAO ESP32-S3',
    subtitle='8 MB Flash + 8 MB PSRAM · USB-C · alle D-Pads sind ADC1, Touch und RTC',
    board_w=150,
    note='Andere GPIO-Nummern als der XIAO C3 — gleiche Pads, verschobene Zuordnung.',
    left=[
        [('name', 'D0'), ('gpio', 'GPIO1'), ('adc', 'A0')],
        [('name', 'D1'), ('gpio', 'GPIO2'), ('adc', 'A1')],
        [('name', 'D2'), ('gpio', 'GPIO3'), ('adc', 'A2')],
        [('name', 'D3'), ('gpio', 'GPIO4'), ('adc', 'A3')],
        [('name', 'D4'), ('gpio', 'GPIO5'), ('adc', 'A4'), ('i2c', 'SDA')],
        [('name', 'D5'), ('gpio', 'GPIO6'), ('adc', 'A5'), ('i2c', 'SCL')],
        [('name', 'D6'), ('gpio', 'GPIO43'), ('uart', 'TX')],
    ],
    right=[
        [('power', '5V / VBUS')],
        [('gnd', 'GND')],
        [('power', '3V3-OUT')],
        [('name', 'D10'), ('gpio', 'GPIO9'), ('adc', 'A10'), ('spi', 'MOSI')],
        [('name', 'D9'), ('gpio', 'GPIO8'), ('adc', 'A9'), ('spi', 'MISO')],
        [('name', 'D8'), ('gpio', 'GPIO7'), ('adc', 'A8'), ('spi', 'SCK')],
        [('name', 'D7'), ('gpio', 'GPIO44'), ('uart', 'RX')],
    ],
)

# ── XIAO ESP32-S3 Sense — Aufsatzplatine ──────────────────────────────────
# Kamera, Mikrofon und microSD des Sense-Aufsatzes. Werte aus der Seeed-
# Dokumentation, nicht aus einem eigenen Repo belegt.
BOARDS['xiaos3sense'] = dict(
    title='XIAO ESP32-S3 Sense · Aufsatz',
    subtitle='OV2640 + PDM-Mikrofon + microSD · Belegung laut Seeed-Dokumentation',
    board_w=175,
    note='Der Aufsatz belegt GPIOs, die am nackten S3 gar nicht herausgefuehrt sind.',
    left=[
        [('periph', 'CAM XCLK'), ('gpio', 'GPIO10')],
        [('periph', 'CAM SIOD'), ('gpio', 'GPIO40')],
        [('periph', 'CAM SIOC'), ('gpio', 'GPIO39')],
        [('periph', 'CAM VSYNC'), ('gpio', 'GPIO38')],
        [('periph', 'CAM HREF'), ('gpio', 'GPIO47')],
        [('periph', 'CAM PCLK'), ('gpio', 'GPIO13')],
        [('periph', 'CAM Y9'), ('gpio', 'GPIO48')],
        [('periph', 'CAM Y8'), ('gpio', 'GPIO11')],
        [('periph', 'CAM Y7'), ('gpio', 'GPIO12')],
    ],
    right=[
        [('periph', 'CAM Y6'), ('gpio', 'GPIO14')],
        [('periph', 'CAM Y5'), ('gpio', 'GPIO16')],
        [('periph', 'CAM Y4'), ('gpio', 'GPIO18')],
        [('periph', 'CAM Y3'), ('gpio', 'GPIO17')],
        [('periph', 'CAM Y2'), ('gpio', 'GPIO15')],
        [('periph', 'Mikrofon CLK'), ('gpio', 'GPIO42')],
        [('periph', 'Mikrofon DATA'), ('gpio', 'GPIO41')],
        [('periph', 'microSD CS'), ('gpio', 'GPIO21')],
        [('system', 'SD nutzt SPI'), ('spi', 'D8 / D9 / D10')],
    ],
)


if __name__ == '__main__':
    import json, sys
    out = {k: render(**v) for k, v in BOARDS.items()}
    json.dump(out, open('pinouts.json', 'w'))
    print(f'{len(out)} Grafiken erzeugt: ' + ', '.join(out))
    for k, v in out.items():
        print(f'  {k:10} {len(v):>6} Bytes')
