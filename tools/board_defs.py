#!/usr/bin/env python3
"""Board- und Template-Definitionen. Ausfuehren erzeugt die JSON-Dateien.

Die Pin-Belegungen stammen aus den in der Referenz genannten Quellen:
ESP-01S aus dem eigenen Eagle-Schaltplan, XIAO IR Mate aus dem eigenen README,
CYD aus Schaltplan V1.0 des eigenen Repos, Freenove aus ESP32S3_Pinout.png,
XIAO S3 aus den Seeed-Pinout-Grafiken. Der Rest aus der Chipdokumentation.
"""

from make_boards import (HAIR, RASTER, board, circle, devkit, pcb, pin_rows,
                         rect, shield, text, write, xiao, xiao_back)

SILK = "${SILK_COLOR}"


def gpio(n, **extra):
    d = {"GPIO": f"IO{n}"}
    d.update(extra)
    return d


# ══════════════════════════════════════════════════════════════════════════
# XIAO ESP32-C3
# ══════════════════════════════════════════════════════════════════════════
C3_LEFT = ["D0", "D1", "D2", "D3", "D4", "D5", "D6"]
C3_RIGHT = ["5V", "GND", "3V3", "D10", "D9", "D8", "D7"]

back, tp = xiao_back(
    "xiao-esp32c3", C3_RIGHT, C3_LEFT, ("seeed studio", "XIAO ESP32C3"),
    (["MTDO", "GND_T", "MTCK", "USB_DP"], ["MTDI", "EN", "MTMS", "USB_DM"]),
    bat=("BAT-", "BAT+"))
t = xiao("xiao-esp32c3", "Seeed XIAO ESP32-C3 (21 x 17.5 mm)", C3_LEFT, C3_RIGHT,
         module_label="seeed studio", module_sub="XIAO ESP32-C3",
         antenna="ceramic", back=back, test_pads=tp)
write("template", "xiao-esp32c3", t)

C3_PINS = {
    "D0": {"PHYSICAL": "D0", **gpio(2, ADC=0)},
    "D1": {"PHYSICAL": "D1", **gpio(3, ADC=1), "DVP": "IR TX"},
    "D2": {"PHYSICAL": "D2", **gpio(4, ADC=2), "DVP": "IR RX"},
    "D3": {"PHYSICAL": "D3", **gpio(5, ADC=3), "DVP": "Touch"},
    "D4": {"PHYSICAL": "D4", **gpio(6), "I2C": "SDA", "DVP": "Vibration"},
    "D5": {"PHYSICAL": "D5", **gpio(7), "I2C": "SCL", "DVP": "WS2812"},
    "D6": {"PHYSICAL": "D6", **gpio(21), "UART": "TX"},
    "D7": {"PHYSICAL": "D7", **gpio(20), "UART": "RX"},
    "D8": {"PHYSICAL": "D8", **gpio(8), "SPI": "SCK", "CTRL": "Strap"},
    "D9": {"PHYSICAL": "D9", **gpio(9), "SPI": "MISO", "CTRL": "Boot"},
    "D10": {"PHYSICAL": "D10", **gpio(10), "SPI": "MOSI"},
    "5V": {"PWR": "VBUS"}, "3V3": {"PWR": "3V3"}, "GND": {"GND": None},
    "MTDO": {"JTAG": "MTDO"}, "MTDI": {"JTAG": "MTDI"},
    "MTCK": {"JTAG": "MTCK"}, "MTMS": {"JTAG": "MTMS"},
    "USB_DP": {"USB": "D+"}, "USB_DM": {"USB": "D-"},
    "EN": {"CTRL": "EN"}, "GND_T": {"GND": None},
    "BAT+": {"PWR": "BAT+"}, "BAT-": {"PWR": "BAT-"},
}
write("board", "xiao_esp32c3", board(
    "xiao_esp32c3", "Seeed XIAO ESP32-C3", "Seeed Studio",
    "https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/",
    ["pcb-black", "xiao-esp32c3"], C3_PINS,
    flash=4194304, mcu="esp32c3", family="esp32c3", fcpu="160000000L",
    symbol="XIAO-C3"))


# ══════════════════════════════════════════════════════════════════════════
# XIAO ESP32-S3 Sense — Aufsatzplatine mit Kamera, Mikrofon und microSD
# ══════════════════════════════════════════════════════════════════════════
W, H = 17.5, 21.0
front = [pcb(W, H)]
front += [rect(2.4, 1.6, 12.7, 9.4, rx=0.4, ry=0.4, fill={"color": "#22262B"}),
          rect(3.2, 2.4, 11.1, 7.8, rx=0.3, ry=0.3, fill={"color": "#33393F"}),
          text(8.75, 6.8, "OV2640", 0.95, "#C9D2D8")]
front += [rect(1.9, 12.4, 13.7, 5.4, rx=0.3, ry=0.3,
               fill={"lgrad": ["0,0", "#D2D2D2", "0,1", "#8F8F8F"]}),
          rect(2.6, 13.1, 12.3, 4.0, rx=0.2, ry=0.2, fill={"color": "#6E6E6E"}),
          text(8.75, 15.6, "microSD", 0.8, "#F2F2F2")]
front += [rect(4.9, 18.7, 7.6, 1.8, rx=0.2, ry=0.2, fill={"color": "#1C1C1C"}),
          text(8.75, 11.6, "PDM-Mikrofon", 0.7)]
front += [{"id": "al", "name": "anchor_edge", "pos": f"0,{3.4 + i * 2.54:.2f}",
           "vars": {"PINDIR": "left"}, "repeat": 1} for i in range(0)]

ROWS_L = [3.2, 5.74, 8.28, 10.82, 13.36]
ROWS_R = [3.2, 5.74, 8.28, 10.82, 13.36, 15.90, 18.44]
sense_tp = {}
for i, y in enumerate(ROWS_L, 1):
    front.append({"id": f"sl{i}", "name": "anchor_edge", "pos": f"0,{y:.2f}",
                  "vars": {"PINDIR": "left"}})
for i, y in enumerate(ROWS_R, 1):
    front.append({"id": f"sr{i}", "name": "anchor_edge", "pos": f"{W},{y:.2f}",
                  "vars": {"PINDIR": "right"}})
SENSE_L = ["XCLK", "SIOD", "SIOC", "VSYNC", "HREF"]
SENSE_R = ["PCLK", "CAM_Y9", "CAM_Y8", "CAM_Y7", "MIC_CLK", "MIC_DAT", "SD_CS"]
for i, n in enumerate(SENSE_L, 1):
    sense_tp[n] = f"xiao-s3-sense.front.sl{i}.a"
for i, n in enumerate(SENSE_R, 1):
    sense_tp[n] = f"xiao-s3-sense.front.sr{i}.a"

sense_back = [pcb(W, H), text(W / 2, 2.4, "Unterseite", 0.9),
              rect(4.9, 4.0, 7.6, 2.4, rx=0.2, ry=0.2, fill={"color": "#1C1C1C"}),
              text(8.75, 7.6, "B2B zum XIAO", 0.8),
              text(8.75, 18.6, "seeed studio", 0.85),
              text(8.75, 19.8, "XIAO Sense", 0.85),
              {"id": "b1", "name": "anchor_edge", "pos": f"0,11.0",
               "vars": {"PINDIR": "left"}}]
sense_tp["SD_BUS"] = "xiao-s3-sense.back.b1.a"

write("template", "xiao-s3-sense", {
    "name": "xiao-s3-sense", "title": "XIAO ESP32-S3 Sense (Aufsatz)",
    "width": W, "height": H,
    "vars": {"RASTER": RASTER, "MASK_HOLE": "#101010"},
    "front": front, "back": sense_back, "pads": {}, "test_pads": sense_tp,
})

SENSE_PINS = {
    "XCLK": {"DVP": "XCLK", **gpio(10)}, "SIOD": {"DVP": "SIOD", **gpio(40)},
    "SIOC": {"DVP": "SIOC", **gpio(39)}, "VSYNC": {"DVP": "VSYNC", **gpio(38)},
    "HREF": {"DVP": "HREF", **gpio(47)}, "PCLK": {"DVP": "PCLK", **gpio(13)},
    "CAM_Y9": {"DVP": "Y9", **gpio(48)}, "CAM_Y8": {"DVP": "Y8", **gpio(11)},
    "CAM_Y7": {"DVP": "Y7", **gpio(12)},
    "MIC_CLK": {"PHYSICAL": "MIC", "I2S": "CLK", **gpio(42)},
    "MIC_DAT": {"PHYSICAL": "MIC", "I2S": "DAT", **gpio(41)},
    "SD_CS": {"SD": "CS", **gpio(21)},
    "SD_BUS": {"SPI": "D8/9/10"},
}
write("board", "xiao_s3_sense", board(
    "xiao_s3_sense", "Seeed XIAO ESP32-S3 Sense", "Seeed Studio",
    "https://wiki.seeedstudio.com/xiao_esp32s3_sense_filesystem/",
    ["pcb-black", "xiao-s3-sense"], SENSE_PINS,
    flash=8388608, mcu="esp32s3", family="esp32s3", symbol="SENSE"))


# ══════════════════════════════════════════════════════════════════════════
# Wemos D1 mini
# ══════════════════════════════════════════════════════════════════════════
D1_L = ["RST", "A0", "D0", "D5", "D6", "D7", "D8", "3V3"]
D1_R = ["TX", "RX", "D1", "D2", "D3", "D4", "GND", "5V"]
t = devkit("d1-mini", "Wemos D1 mini (34.2 x 25.6 mm)", 25.6, 34.2, D1_L, D1_R,
           module="ESP-12F", module_sub="4 MB", usb="micro", usb_at="bottom",
           silk="D1 mini")
write("template", "d1-mini", t)

D1_PINS = {
    "RST": {"CTRL": "RST"}, "3V3": {"PWR": "3V3"}, "5V": {"PWR": "5V"},
    "GND": {"GND": None},
    "A0": {"PHYSICAL": "A0", "ADC": 0},
    "D0": {"PHYSICAL": "D0", **gpio(16), "CTRL": "Wake"},
    "D1": {"PHYSICAL": "D1", **gpio(5), "I2C": "SCL"},
    "D2": {"PHYSICAL": "D2", **gpio(4), "I2C": "SDA"},
    "D3": {"PHYSICAL": "D3", **gpio(0), "CTRL": "Strap"},
    "D4": {"PHYSICAL": "D4", **gpio(2), "CTRL": "LED"},
    "D5": {"PHYSICAL": "D5", **gpio(14), "SPI": "SCK"},
    "D6": {"PHYSICAL": "D6", **gpio(12), "SPI": "MISO"},
    "D7": {"PHYSICAL": "D7", **gpio(13), "SPI": "MOSI"},
    "D8": {"PHYSICAL": "D8", **gpio(15), "CTRL": "Strap"},
    "TX": {"UART": "TX", **gpio(1)}, "RX": {"UART": "RX", **gpio(3)},
}
write("board", "d1_mini", board(
    "d1_mini", "Wemos D1 mini", "Wemos", "https://www.wemos.cc/en/latest/d1/d1_mini.html",
    ["pcb-black", "d1-mini"], D1_PINS,
    flash=4194304, mcu="esp8266", family="esp8266", fcpu="80000000L",
    ram=81920, scale=22, symbol="D1MINI"))


# ══════════════════════════════════════════════════════════════════════════
# ESP32 DevKitC (38-polig)
# ══════════════════════════════════════════════════════════════════════════
DK_L = ["3V3", "EN", "VP", "VN", "IO34", "IO35", "IO32", "IO33", "IO25", "IO26",
        "IO27", "IO14", "IO12", "GND1", "IO13", "SD2", "SD3", "CMD", "5V"]
DK_R = ["GND2", "IO23", "IO22", "TX0", "RX0", "IO21", "GND3", "IO19", "IO18",
        "IO5", "IO17", "IO16", "IO4", "IO0", "IO2", "IO15", "SD1", "SD0", "CLK"]
t = devkit("esp32-devkitc", "ESP32 DevKitC / WROOM-32 (28.2 x 53 mm)", 28.2, 53.0,
           DK_L, DK_R, module="ESP32-WROOM", module_sub="4 MB",
           usb="micro", usb_at="bottom",
           buttons=((4.0, 48.5), (24.2, 48.5)), silk="ESP32 DevKitC")
write("template", "esp32-devkitc", t)

DK_PINS = {
    "3V3": {"PWR": "3V3"}, "5V": {"PWR": "5V"}, "EN": {"CTRL": "EN"},
    "GND1": {"GND": None}, "GND2": {"GND": None}, "GND3": {"GND": None},
    "VP": {"PHYSICAL": "VP", **gpio(36), "ADC": 1},
    "VN": {"PHYSICAL": "VN", **gpio(39), "ADC": 1},
    "IO34": {**gpio(34), "ADC": 1}, "IO35": {**gpio(35), "ADC": 1},
    "IO32": {**gpio(32), "ADC": 1}, "IO33": {**gpio(33), "ADC": 1},
    "IO25": {**gpio(25), "ADC": 2}, "IO26": {**gpio(26), "ADC": 2},
    "IO27": {**gpio(27), "ADC": 2}, "IO14": {**gpio(14), "ADC": 2},
    "IO12": {**gpio(12), "CTRL": "MTDI"}, "IO13": {**gpio(13), "ADC": 2},
    "IO23": {**gpio(23), "SPI": "MOSI"}, "IO22": {**gpio(22), "I2C": "SCL"},
    "IO21": {**gpio(21), "I2C": "SDA"}, "IO19": {**gpio(19), "SPI": "MISO"},
    "IO18": {**gpio(18), "SPI": "SCK"}, "IO5": {**gpio(5), "SPI": "CS"},
    "IO17": gpio(17), "IO16": gpio(16), "IO4": {**gpio(4), "ADC": 2},
    "IO0": {**gpio(0), "CTRL": "Boot"}, "IO2": {**gpio(2), "CTRL": "Strap"},
    "IO15": {**gpio(15), "CTRL": "Strap"},
    "TX0": {"UART": "TX0", **gpio(1)}, "RX0": {"UART": "RX0", **gpio(3)},
    "SD0": {"FLASH": "SD0"}, "SD1": {"FLASH": "SD1"}, "SD2": {"FLASH": "SD2"},
    "SD3": {"FLASH": "SD3"}, "CMD": {"FLASH": "CMD"}, "CLK": {"FLASH": "CLK"},
}
write("board", "esp32_devkitc", board(
    "esp32_devkitc", "ESP32 DevKitC / WROOM-32", "Espressif",
    "https://docs.espressif.com/projects/esp-idf/en/latest/esp32/hw-reference/esp32/get-started-devkitc.html",
    ["pcb-black", "esp32-devkitc"], DK_PINS,
    flash=4194304, scale=17, symbol="DEVKITC"))


# ══════════════════════════════════════════════════════════════════════════
# ESP32-S3-DevKitC-1 N16R8
# ══════════════════════════════════════════════════════════════════════════
S3_L = ["3V3a", "3V3b", "RST", "IO4", "IO5", "IO6", "IO7", "IO15", "IO16",
        "IO17", "IO18", "IO8", "IO3", "IO46", "IO9", "IO10", "IO11", "IO12",
        "IO13", "IO14", "5V", "GNDa"]
S3_R = ["GNDb", "TX", "RX", "IO1", "IO2", "IO42", "IO41", "IO40", "IO39",
        "IO38", "IO37", "IO36", "IO35", "IO0", "IO45", "IO48", "IO47", "IO21",
        "IO20", "IO19", "GNDc", "GNDd"]
t = devkit("esp32s3-devkitc1", "ESP32-S3-DevKitC-1 N16R8 (25.5 x 63 mm)",
           25.5, 63.0, S3_L, S3_R, module="ESP32-S3", module_sub="N16R8",
           usb="c", usb_at="bottom",
           buttons=((3.6, 58.0), (21.9, 58.0)), silk="S3-DevKitC-1")
write("template", "esp32s3-devkitc1", t)

S3_PINS = {
    "3V3a": {"PWR": "3V3"}, "3V3b": {"PWR": "3V3"}, "5V": {"PWR": "5V"},
    "GNDa": {"GND": None}, "GNDb": {"GND": None}, "GNDc": {"GND": None},
    "GNDd": {"GND": None}, "RST": {"CTRL": "RST"},
    "IO4": {**gpio(4), "ADC": 1}, "IO5": {**gpio(5), "ADC": 1},
    "IO6": {**gpio(6), "ADC": 1}, "IO7": {**gpio(7), "ADC": 1},
    "IO15": {**gpio(15), "ADC": 2}, "IO16": {**gpio(16), "ADC": 2},
    "IO17": {**gpio(17), "ADC": 2}, "IO18": {**gpio(18), "ADC": 2},
    "IO8": {**gpio(8), "I2C": "SDA"}, "IO9": {**gpio(9), "I2C": "SCL"},
    "IO3": {**gpio(3), "CTRL": "Strap"}, "IO46": {**gpio(46), "CTRL": "Strap"},
    "IO10": {**gpio(10), "SPI": "CS"}, "IO11": {**gpio(11), "SPI": "MOSI"},
    "IO12": {**gpio(12), "SPI": "SCK"}, "IO13": {**gpio(13), "SPI": "MISO"},
    "IO14": gpio(14), "IO1": {**gpio(1), "ADC": 1}, "IO2": {**gpio(2), "ADC": 1},
    "IO42": gpio(42), "IO41": gpio(41), "IO40": gpio(40), "IO39": gpio(39),
    "IO38": gpio(38),
    "IO37": {**gpio(37), "CTRL": "PSRAM"}, "IO36": {**gpio(36), "CTRL": "PSRAM"},
    "IO35": {**gpio(35), "CTRL": "PSRAM"},
    "IO0": {**gpio(0), "CTRL": "Boot"}, "IO45": {**gpio(45), "CTRL": "Strap"},
    "IO48": {**gpio(48), "SD": "WS2812"}, "IO47": gpio(47), "IO21": gpio(21),
    "IO20": {**gpio(20), "USB": "D+"}, "IO19": {**gpio(19), "USB": "D-"},
    "TX": {"UART": "TX", **gpio(43)}, "RX": {"UART": "RX", **gpio(44)},
}
write("board", "esp32s3_devkitc1", board(
    "esp32s3_devkitc1", "ESP32-S3-DevKitC-1 N16R8", "Espressif",
    "https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/hw-reference/esp32s3/user-guide-devkitc-1.html",
    ["pcb-black", "esp32s3-devkitc1"], S3_PINS,
    flash=16777216, mcu="esp32s3", family="esp32s3", scale=15, symbol="S3DEVKIT"))


# ══════════════════════════════════════════════════════════════════════════
# Freenove ESP32-S3-WROOM CAM
# ══════════════════════════════════════════════════════════════════════════
FN_L = ["3V3", "RST", "IO4", "IO5", "IO6", "IO7", "IO15", "IO16", "IO17",
        "IO18", "IO8", "IO3", "IO46", "IO9", "IO10", "IO11", "IO12", "IO13",
        "IO14", "5V"]
FN_R = ["IO43", "IO44", "IO1", "IO2", "IO42", "IO41", "IO40", "IO39", "IO38",
        "IO37", "IO36", "IO35", "IO0", "IO45", "IO48", "IO47", "IO21", "IO20",
        "IO19", "GND"]
fn_back = [pcb(25.0, 55.0), text(12.5, 3.0, "Unterseite", 0.95),
           rect(5.5, 6.0, 14.0, 12.0, rx=0.4, ry=0.4, fill={"color": "#2A2E33"}),
           text(12.5, 12.4, "Kamera-FPC", 0.85),
           rect(4.5, 22.0, 16.0, 6.0, rx=0.3, ry=0.3,
                fill={"lgrad": ["0,0", "#D2D2D2", "0,1", "#8F8F8F"]}),
           text(12.5, 25.4, "microSD", 0.85, "#333333"),
           text(12.5, 52.0, "FREENOVE ESP32-S3", 0.85),
           {"id": "f1", "name": "anchor_edge", "pos": "0,12.0", "vars": {"PINDIR": "left"}},
           {"id": "f2", "name": "anchor_edge", "pos": "25.0,25.0", "vars": {"PINDIR": "right"}}]
t = devkit("freenove-s3-cam", "Freenove ESP32-S3-WROOM CAM (ca. 25 x 55 mm)",
           25.0, 55.0, FN_L, FN_R, module="ESP32-S3", module_sub="8/8 MB",
           usb="c", usb_at="bottom", silk="Freenove S3", back=fn_back)
t["test_pads"] = {"CAM": "freenove-s3-cam.back.f1.a", "SD": "freenove-s3-cam.back.f2.a"}
write("template", "freenove-s3-cam", t)

FN_PINS = {
    "3V3": {"PWR": "3V3"}, "5V": {"PWR": "5V"}, "GND": {"GND": None},
    "RST": {"CTRL": "RST"},
    "IO4": {**gpio(4), "DVP": "SIOD"}, "IO5": {**gpio(5), "DVP": "SIOC"},
    "IO6": {**gpio(6), "DVP": "VSYNC"}, "IO7": {**gpio(7), "DVP": "HREF"},
    "IO15": {**gpio(15), "DVP": "XCLK"}, "IO16": {**gpio(16), "DVP": "Y9"},
    "IO17": {**gpio(17), "DVP": "Y8"}, "IO18": {**gpio(18), "DVP": "Y7"},
    "IO8": {**gpio(8), "DVP": "Y4"}, "IO9": {**gpio(9), "DVP": "Y3"},
    "IO10": {**gpio(10), "DVP": "Y5"}, "IO11": {**gpio(11), "DVP": "Y2"},
    "IO12": {**gpio(12), "DVP": "Y6"}, "IO13": {**gpio(13), "DVP": "PCLK"},
    "IO3": {**gpio(3), "CTRL": "JTAG"}, "IO46": {**gpio(46), "CTRL": "LOG"},
    "IO14": gpio(14), "IO1": {**gpio(1), "ADC": 1}, "IO2": {**gpio(2), "SD": "LED"},
    "IO42": gpio(42), "IO41": gpio(41),
    "IO40": {**gpio(40), "SD": "DATA"}, "IO39": {**gpio(39), "SD": "CLK"},
    "IO38": {**gpio(38), "SD": "CMD"},
    "IO37": {**gpio(37), "CTRL": "PSRAM"}, "IO36": {**gpio(36), "CTRL": "PSRAM"},
    "IO35": {**gpio(35), "CTRL": "PSRAM"},
    "IO0": {**gpio(0), "CTRL": "Boot"}, "IO45": {**gpio(45), "CTRL": "Strap"},
    "IO48": {**gpio(48), "SD": "WS2812"}, "IO47": gpio(47), "IO21": gpio(21),
    "IO20": {**gpio(20), "USB": "D+"}, "IO19": {**gpio(19), "USB": "D-"},
    "IO43": {"UART": "TX", **gpio(43)}, "IO44": {"UART": "RX", **gpio(44)},
    "CAM": {"DVP": "OV2640"}, "SD": {"SD": "microSD"},
}
write("board", "freenove_s3_cam", board(
    "freenove_s3_cam", "Freenove ESP32-S3-WROOM CAM", "Freenove",
    "https://github.com/Freenove/Freenove_ESP32_S3_WROOM_Board",
    ["pcb-black", "freenove-s3-cam"], FN_PINS,
    flash=8388608, mcu="esp32s3", family="esp32s3", scale=16, symbol="FREENOVE"))

print("Templates und Boards geschrieben.")


# ══════════════════════════════════════════════════════════════════════════
# ESP-01S — 2x4-Header an der Stirnseite
# ══════════════════════════════════════════════════════════════════════════
# boardgens eigenes Idiom fuer zweireihige Header (res/templates/esp01m-14.json):
# die eine Pinreihe wird in der Vorder-, die andere in der Rueckansicht
# beschriftet. Nummerierung wie JP2 im eigenen Eagle-Schaltplan.
W, H = 14.3, 24.8
PITCH, HX, HY = 2.54, 3.2, 22.2

def esp01_side(row_labels, title):
    s = [pcb(W, H, 0.8)]
    # PCB-Antenne als Maeander am oberen Ende
    s += [rect(2.0, 1.4, 10.3, 0.7, fill={"color": "#C9922F"}),
          rect(2.0, 1.4, 0.7, 3.2, fill={"color": "#C9922F"}),
          rect(4.6, 2.4, 0.7, 2.6, fill={"color": "#C9922F"}),
          rect(7.2, 1.4, 0.7, 3.2, fill={"color": "#C9922F"}),
          rect(9.8, 2.4, 0.7, 2.6, fill={"color": "#C9922F"}),
          rect(11.6, 1.4, 0.7, 3.2, fill={"color": "#C9922F"})]
    s += shield(2.3, 6.4, 9.7, 6.6, "ESP8266EX", "1 MB")
    s += [rect(3.0, 14.4, 8.3, 4.4, rx=0.3, ry=0.3, fill={"color": "#1E1E1E"}),
          text(7.15, 17.0, "ESP-01S", 0.85)]
    s += [text(7.15, 20.6, title, 0.75)]
    s += [{"id": "row", "name": "r_pins_horz", "repeat": 4,
           "pos": f"{HX},{HY}", "vars": {"PINDIR": "down"}}]
    s += [{"id": "pins", "name": "r_labels_horz", "repeat": 4,
           "pos": f"{HX},{HY + 1.4}", "vars": {"PINDIR": "down"}}]
    return s

ESP01_FRONT = ["P1", "P3", "P5", "P7"]     # TXD, CH_PD, RST, VCC
ESP01_BACK  = ["P2", "P4", "P6", "P8"]     # GND, GPIO2, GPIO0, RXD
t = {
    "name": "esp01s", "title": "ESP-01S (24.8 x 14.3 mm)",
    "width": W, "height": H,
    "vars": {"PINTYPE_HORZ": "header_pad", "RASTER": PITCH, "PINDIR": "down",
             "MASK_HOLE": "#101010"},
    "front": esp01_side(ESP01_FRONT, "Header-Reihe 1/3/5/7"),
    "back": esp01_side(ESP01_BACK, "Header-Reihe 2/4/6/8"),
    "pads": {n: f"esp01s.front.pins.label{i}.anchor" for i, n in enumerate(ESP01_FRONT, 1)},
    "test_pads": {n: f"esp01s.back.pins.label{i}.anchor" for i, n in enumerate(ESP01_BACK, 1)},
}
write("template", "esp01s", t)

# Der Faecher unter dem Header traegt hoechstens zwei Bloecke je Pin.
# Details wie "an 3V3" oder die LED_out-Verdrahtung stehen in der Tabelle.
ESP01_PINS = {
    "P1": {"PHYSICAL": "Pin 1", "UART": "TXD"},
    "P3": {"PHYSICAL": "Pin 3", "CTRL": "CH_PD"},
    "P5": {"PHYSICAL": "Pin 5", "CTRL": "RST"},
    "P7": {"PHYSICAL": "Pin 7", "PWR": "3V3"},
    "P2": {"PHYSICAL": "Pin 2", "GND": None},
    "P4": {"PHYSICAL": "Pin 4", **gpio(2)},
    "P6": {"PHYSICAL": "Pin 6", **gpio(0)},
    "P8": {"PHYSICAL": "Pin 8", "UART": "RXD"},
}
write("board", "esp01s", board(
    "esp01s", "ESP-01S", "Ai-Thinker", "https://www.espressif.com/en/products/socs/esp8266",
    ["pcb-black", "esp01s"], ESP01_PINS,
    flash=1048576, mcu="esp8266", family="esp8266", fcpu="80000000L",
    ram=81920, scale=30, symbol="ESP-01S"))


# ══════════════════════════════════════════════════════════════════════════
# CYD ESP32-2432S024R — gelbe Platine, Displayboard
# ══════════════════════════════════════════════════════════════════════════
# Maße aus 3-Structure_Diagram/Dimensions.png des eigenen Repos: 68 mm breit,
# R1,6-Ecken, Bohrungen 3,2 mm von den Kanten. Belegung aus Schaltplan V1.0.
CW, CH_ = 68.0, 43.0

def cyd_holes():
    return [circle(x, y, 3.2, fill={"color": "#B9962A"}) for x in (3.2, CW - 3.2)
            for y in (3.2, CH_ - 3.2)] + \
           [circle(x, y, 1.9, fill={"color": "#101010"}) for x in (3.2, CW - 3.2)
            for y in (3.2, CH_ - 3.2)]

cyd_front = [rect(0, 0, CW, CH_, rx=1.6, ry=1.6, preset="mask_yellow")]
cyd_front += cyd_holes()
cyd_front += [rect(8.5, 1.5, 51.0, 40.0, rx=0.5, ry=0.5, fill={"color": "#1A1A1A"}),
              rect(10.5, 3.5, 47.0, 36.0, fill={"color": "#0B1A2B"}),
              text(34.0, 22.0, "2,4\" ILI9341 240x320", 1.6, "#7FA8CC"),
              text(34.0, 25.6, "resistiver Touch XPT2046", 1.2, "#5E7E9B")]
cyd_front += [circle(63.5, 8.0, 2.4, fill={"color": "#E8E8E8"}),
              text(63.5, 12.2, "RGB", 1.0, "#3A3000")]
ROWS_C = [7.0, 11.5, 16.0, 20.5, 25.0, 29.5, 34.0, 38.5]
for i, y in enumerate(ROWS_C, 1):
    cyd_front.append({"id": f"cl{i}", "name": "anchor_edge", "pos": f"0,{y:.2f}",
                      "vars": {"PINDIR": "left"}})
CYD_L = ["TFT_SCK", "TFT_MOSI", "TFT_MISO", "TFT_DC", "TFT_CS", "TFT_BL",
         "TP_CS", "TP_IRQ"]

cyd_back = [rect(0, 0, CW, CH_, rx=1.6, ry=1.6, preset="mask_yellow")]
cyd_back += cyd_holes()
cyd_back += shield(24.0, 12.0, 20.0, 18.0, "ESP32-WROOM", "4 MB")
cyd_back += [rect(1.0, 17.0, 7.0, 9.0, rx=0.3, ry=0.3,
                  fill={"lgrad": ["0,0", "#D2D2D2", "0,1", "#8F8F8F"]}),
             text(4.5, 27.8, "microSD", 0.9, "#3A3000")]
cyd_back += [rect(30.0, 39.0, 8.0, 3.4, rx=0.3, ry=0.3,
                  fill={"lgrad": ["0,0", "#DCDCDC", "0,1", "#8E8E8E"]}),
             text(34.0, 37.4, "micro-USB", 0.9, "#3A3000")]
cyd_back += [rect(59.0, 8.0, 6.5, 5.0, rx=0.3, ry=0.3, fill={"color": "#2B2B2B"}),
             text(62.2, 15.0, "P3", 0.9, "#3A3000"),
             rect(59.0, 20.0, 6.5, 5.0, rx=0.3, ry=0.3, fill={"color": "#2B2B2B"}),
             text(62.2, 27.0, "CN1", 0.9, "#3A3000"),
             circle(12.0, 34.0, 2.0, fill={"color": "#5A4A1A"}),
             text(12.0, 37.6, "LDR", 0.9, "#3A3000"),
             circle(48.0, 34.0, 2.6, fill={"color": "#2B2B2B"}),
             text(48.0, 38.4, "Lautsprecher", 0.9, "#3A3000"),
             text(34.0, 3.2, "Unterseite", 1.1, "#3A3000")]
ROWS_CB = [8.0, 12.5, 17.0, 21.5, 26.0, 30.5, 35.0]
for i, y in enumerate(ROWS_CB, 1):
    cyd_back.append({"id": f"cr{i}", "name": "anchor_edge", "pos": f"{CW},{y:.2f}",
                     "vars": {"PINDIR": "right"}})
CYD_R = ["SD_CLK", "SD_MISO", "SD_MOSI", "SD_CS", "RGB_R", "LDR", "SPK"]

write("template", "cyd-2432s024r", {
    "name": "cyd-2432s024r", "title": "CYD ESP32-2432S024R (68 x 43 mm)",
    "width": CW, "height": CH_,
    "vars": {"RASTER": 3.4, "MASK_HOLE": "#101010"},
    "front": cyd_front, "back": cyd_back, "pads": {},
    "test_pads": {**{n: f"cyd-2432s024r.front.cl{i}.a" for i, n in enumerate(CYD_L, 1)},
                  **{n: f"cyd-2432s024r.back.cr{i}.a" for i, n in enumerate(CYD_R, 1)}},
})

CYD_PINS = {
    "TFT_SCK": {"SPI": "SCK", **gpio(14)}, "TFT_MOSI": {"SPI": "MOSI", **gpio(13)},
    "TFT_MISO": {"SPI": "MISO", **gpio(12)}, "TFT_DC": {"CTRL": "DC", **gpio(2)},
    "TFT_CS": {"SPI": "CS", **gpio(15)}, "TFT_BL": {"CTRL": "BL", **gpio(27)},
    "TP_CS": {"SPI": "TP CS", **gpio(33)}, "TP_IRQ": {"CTRL": "TP IRQ", **gpio(36)},
    "SD_CLK": {"SD": "CLK", **gpio(18)}, "SD_MISO": {"SD": "MISO", **gpio(19)},
    "SD_MOSI": {"SD": "MOSI", **gpio(23)}, "SD_CS": {"SD": "CS", **gpio(5)},
    "RGB_R": {"PHYSICAL": "RGB", "CTRL": "4/16/17"}, "LDR": {"ADC": 1, **gpio(34)},
    "SPK": {"I2S": "Audio", **gpio(26)},
}
write("board", "cyd_2432s024r", board(
    "cyd_2432s024r", "CYD ESP32-2432S024R", "Guition",
    "https://github.com/AllExHH/CYD_2.4inch_ESP32-2432S024",
    ["pcb-black", "cyd-2432s024r"], CYD_PINS,
    flash=4194304, scale=13, symbol="CYD"))
