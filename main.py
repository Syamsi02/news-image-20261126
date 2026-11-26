#!/usr/bin/env python3
"""news-image-20261126: sum up Thursday 26 November 2026 world news in one image.

Pure standard library (zlib + struct). Renders a 1024x1024 PNG with five
real stories reported on 26 November 2026, drawn as labelled scenes:
  1. Houthis claim a strike on Saudi Arabia's Ras Tanura oil refinery
  2. Tankers hit mines in the Strait of Hormuz
  3. Pakistan's first astronaut joins China's space station mission
  4. Israel strikes a Hamas official in Gaza; ceasefire under strain
  5. BepiColombo reaches Mercury orbit after an eight-year journey

Run:  python3 -P -s main.py
Writes entry.png to $MAKEFUN_OUTPUT_DIR, else /output, else ./out.
Deterministic: same bytes on every run.
Text is drawn with the built-in 5x7 bitmap font below; no font files needed.
"""

import math
import os
import struct
import zlib

W = 1024
H = 1024

# ---------------------------------------------------------------- palette ---
NAVY = (13, 27, 48)
NAVY2 = (18, 38, 66)
GOLD = (232, 184, 72)
WHITE = (245, 246, 248)
LIGHT = (205, 216, 230)
DARK = (8, 16, 30)
SKY = (38, 68, 110)
SEA = (16, 84, 120)
SEA2 = (10, 60, 92)
ORANGE = (240, 120, 32)
FLAME = (250, 190, 60)
RED = (198, 52, 44)
GREY = (120, 128, 140)
SAND = (214, 186, 138)
GREEN = (46, 160, 90)
PANEL = (24, 46, 78)

# ------------------------------------------------------------- 5x7 font -----
# Each glyph: 7 rows of 5 pixels, "1" = ink. Uppercase + digits + punctuation.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
}


def char_width(scale):
    return 6 * scale


def text_width(text, scale):
    if not text:
        return 0
    return len(text) * char_width(scale) - scale


def wrap_text(text, max_width, scale):
    """Split text into lines that fit max_width pixels."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split(" ")
        line = ""
        for word in words:
            trial = word if not line else line + " " + word
            if text_width(trial, scale) <= max_width or not line:
                line = trial
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


# -------------------------------------------------------------- canvas ------
class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)
        self.rect(0, 0, w, h, bg)

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i] = color[0]
            self.px[i + 1] = color[1]
            self.px[i + 2] = color[2]

    def rect(self, x, y, w, h, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.px[i] = color[0]
                self.px[i + 1] = color[1]
                self.px[i + 2] = color[2]

    def circle(self, cx, cy, r, color):
        for dy in range(-r, r + 1):
            dx = int(math.sqrt(max(0, r * r - dy * dy)))
            self.rect(cx - dx, cy + dy, 2 * dx + 1, 1, color)

    def ring(self, cx, cy, r, thick, color):
        for dy in range(-r, r + 1):
            dx = int(math.sqrt(max(0, r * r - dy * dy)))
            self.rect(cx - dx, cy + dy, 2 * dx + 1, 1, color)
        inner = r - thick
        for dy in range(-inner, inner + 1):
            dx = int(math.sqrt(max(0, inner * inner - dy * dy)))
            self.rect(cx - dx, cy + dy, 2 * dx + 1, 1, NAVY)

    def triangle(self, x1, y1, x2, y2, x3, y3, color):
        ymin = max(0, min(y1, y2, y3))
        ymax = min(self.h - 1, max(y1, y2, y3))
        for y in range(ymin, ymax + 1):
            xs = []
            for (ax, ay), (bx, by) in (((x1, y1), (x2, y2)),
                                       ((x2, y2), (x3, y3)),
                                       ((x3, y3), (x1, y1))):
                if ay == by:
                    continue
                if min(ay, by) <= y < max(ay, by):
                    xs.append(ax + (y - ay) * (bx - ax) / (by - ay))
            if len(xs) >= 2:
                self.rect(int(min(xs)), y, int(max(xs)) - int(min(xs)) + 1, 1, color)

    def line(self, x1, y1, x2, y2, color):
        steps = max(abs(x2 - x1), abs(y2 - y1), 1)
        for s in range(steps + 1):
            t = s / steps
            self.set(int(x1 + (x2 - x1) * t), int(y1 + (y2 - y1) * t), color)

    def text(self, x, y, s, color, scale=2):
        cx = x
        for ch in s.upper():
            glyph = FONT.get(ch, FONT[" "])
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits[col] == "1":
                        self.rect(cx + col * scale, y + row * scale,
                                  scale, scale, color)
            cx += char_width(scale)

    def text_block(self, x, y, s, color, scale, max_width, leading=None):
        if leading is None:
            leading = 9 * scale
        yy = y
        for line in wrap_text(s, max_width, scale):
            self.text(x, yy, line, color, scale)
            yy += leading
        return yy

    def stars(self, x, y, w, h, count, seed):
        n = 0
        v = seed
        while n < count:
            v = (v * 1103515245 + 12345) % 2147483648
            sx = x + v % w
            v = (v * 1103515245 + 12345) % 2147483648
            sy = y + v % h
            v = (v * 1103515245 + 12345) % 2147483648
            r = 1 + v % 2
            self.circle(sx, sy, r, WHITE if v % 3 else GOLD)
            n += 1


# -------------------------------------------------------------- scenes ------
def flame(c, x, y, s):
    c.triangle(x, y, x - 12 * s // 4, y + 26 * s // 4,
               x + 12 * s // 4, y + 26 * s // 4, ORANGE)
    c.triangle(x, y - 6, x - 6 * s // 4, y + 16 * s // 4,
               x + 6 * s // 4, y + 16 * s // 4, FLAME)
    c.circle(x, y + 20 * s // 4, 5 * s // 4, FLAME)


def refinery_scene(c, x, y, w, h):
    """Hero: Ras Tanura refinery at dusk, flames and smoke."""
    c.rect(x, y, w, h, SKY)
    c.rect(x, y + h - 46, w, 46, SEA2)
    c.circle(x + w - 90, y + 52, 34, FLAME)          # low sun
    c.circle(x + w - 90, y + 52, 26, (250, 210, 110))
    for i, tx in enumerate((70, 210, 360, 520)):
        tw = 46
        th = 120 + (i % 2) * 30
        bx = x + tx
        by = y + h - 46 - th
        c.rect(bx, by, tw, th, DARK)
        c.rect(bx + 8, by - 26, 10, 26, DARK)        # stack
        c.rect(bx + 28, by - 18, 8, 18, DARK)
        for wy in range(by + 12, by + th - 8, 22):
            c.rect(bx + 6, wy, tw - 12, 5, GOLD)
    # storage tanks: plain drums with a gold roof band, fully inside the scene
    for tx in (620, 740, 860):
        c.rect(x + tx, y + h - 46 - 62, 96, 62, NAVY2)
        c.rect(x + tx, y + h - 46 - 62, 96, 8, GOLD)
        c.rect(x + tx + 10, y + h - 46 - 46, 76, 4, GOLD)
    flame(c, x + 170, y + h - 46 - 118, 4)
    flame(c, x + 430, y + h - 46 - 138, 4)
    flame(c, x + 660, y + h - 46 - 96, 3)
    # smoke puffs
    for sx, sy, sr in ((180, 60, 16), (210, 44, 20), (440, 46, 18),
                       (470, 30, 22), (660, 78, 14)):
        c.circle(x + sx, y + sy, sr, (90, 96, 108))
    # tanker on the water
    c.rect(x + 40, y + h - 30, 220, 16, DARK)
    c.rect(x + 150, y + h - 44, 40, 14, DARK)
    c.line(x + 60, y + h - 14, x + 240, y + h - 14, GOLD)


def hormuz_scene(c, x, y, w, h):
    """Tanker at sea with naval mines."""
    c.rect(x, y, w, h, SEA)
    c.rect(x, y, w, 60, (120, 170, 205))
    c.circle(x + w - 70, y + 34, 22, FLAME)
    for wy in (70, 92, 114):
        c.line(x + 10, y + wy, x + w - 10, y + wy, SEA2)
    # tanker, kept inside the 132px scene: hull y+88..y+118
    c.rect(x + 60, y + 88, 300, 30, DARK)
    c.rect(x + 300, y + 62, 60, 26, DARK)
    c.rect(x + 312, y + 48, 12, 14, RED)
    for cx in (110, 180, 250, 320):
        c.rect(x + cx, y + 62, 34, 26, RED)
    # mines: spiked spheres
    for mx, my in ((430, 96), (452, 66)):
        c.circle(x + mx, y + my, 12, DARK)
        for ang in range(0, 360, 45):
            ex = int(mx + 19 * math.cos(math.radians(ang)))
            ey = int(my + 19 * math.sin(math.radians(ang)))
            c.line(x + mx, y + my, x + ex, y + ey, DARK)
        c.circle(x + mx, y + my, 4, GOLD)
    c.circle(x + 468, y + 116, 14, ORANGE)
    c.circle(x + 468, y + 116, 8, FLAME)


def space_scene(c, x, y, w, h):
    """Rocket climbing to a ringed station above Earth."""
    c.rect(x, y, w, h, DARK)
    c.stars(x, y, w, h, 46, 1234567)
    # Small Earth disc, fully inside the scene (a big arc would spill
    # into the neighbouring panels).
    c.circle(x + 62, y + 100, 22, SEA)
    c.circle(x + 54, y + 94, 8, GREEN)
    c.circle(x + 70, y + 106, 6, GREEN)
    # station ring
    c.ring(x + 400, y + 78, 52, 10, GOLD)
    c.rect(x + 352, y + 70, 96, 16, WHITE)
    c.rect(x + 388, y + 46, 24, 64, LIGHT)
    # rocket
    rx, ry = x + 250, y + 130
    c.triangle(rx, ry - 34, rx - 16, ry + 6, rx + 16, ry + 6, WHITE)
    c.rect(rx - 16, ry + 6, 32, 44, WHITE)
    c.rect(rx - 16, ry + 6, 32, 10, RED)
    c.triangle(rx - 16, ry + 50, rx - 30, ry + 62, rx - 16, ry + 44, RED)
    c.triangle(rx + 16, ry + 50, rx + 30, ry + 62, rx + 16, ry + 44, RED)
    flame(c, rx, ry + 58, 3)
    c.circle(x + 60, y + 60, 18, (200, 205, 215))


def gaza_scene(c, x, y, w, h):
    """City skyline under a smoke-filled sky, warning flag."""
    c.rect(x, y, w, h, (64, 52, 44))
    c.circle(x + w - 66, y + 36, 24, (235, 200, 150))
    # Buildings stand on the bottom edge of the 132px scene, heights 40..68.
    for bx, bw, bh in ((20, 70, 52), (110, 56, 68), (186, 80, 44),
                       (286, 60, 60), (366, 76, 48), (452, 38, 36)):
        c.rect(x + bx, y + h - bh, bw, bh, DARK)
        for wy in range(y + h - bh + 10, y + h - 8, 18):
            for wx in range(x + bx + 8, x + bx + bw - 10, 18):
                c.rect(wx, wy, 7, 9, GOLD)
    for sx, sy, sr in ((140, 30, 16), (180, 20, 18), (330, 36, 14),
                       (370, 24, 16)):
        c.circle(x + sx, y + sy, sr, (110, 104, 96))
    c.rect(x + 30, y + 42, 8, 90, WHITE)
    c.triangle(x + 38, y + 42, x + 100, y + 54, x + 38, y + 66, RED)


def mercury_scene(c, x, y, w, h):
    """BepiColombo arriving at cratered Mercury, Sun blazing."""
    c.rect(x, y, w, h, DARK)
    c.stars(x, y, w, h, 40, 987654)
    c.circle(x + 70, y + 44, 30, FLAME)
    c.circle(x + 70, y + 44, 20, (250, 220, 120))
    # Mercury
    mx, my, mr = x + 330, y + 120, 74
    c.circle(mx, my, mr, (168, 152, 132))
    c.circle(mx, my, mr - 12, (150, 134, 114))
    for cx, cy, cr in ((300, 96, 12), (352, 140, 16), (308, 158, 9),
                       (372, 92, 8), (336, 108, 6)):
        c.circle(x + cx, y + cy, cr, (120, 106, 88))
    # probe with solar panels
    px, py = x + 130, y + 120
    c.rect(px - 52, py - 6, 34, 12, (60, 90, 200))
    c.rect(px + 18, py - 6, 34, 12, (60, 90, 200))
    c.rect(px - 18, py - 12, 36, 24, WHITE)
    c.rect(px - 18, py - 12, 36, 6, GOLD)
    c.line(px + 18, py, px + 130, py - 30, GOLD)
    c.line(px + 18, py, px + 150, py + 40, GOLD)


# -------------------------------------------------------------- compose -----
def build():
    c = Canvas(W, H, NAVY)

    # Header
    c.rect(0, 0, W, 104, DARK)
    c.rect(0, 100, W, 4, GOLD)
    c.text(28, 18, "WORLD NEWS", GOLD, 5)
    c.text(28, 62, "THURSDAY 26 NOVEMBER 2026", WHITE, 2)
    c.text(1024 - 28 - text_width("5 STORIES - ONE DAY", 2), 62,
           "5 STORIES - ONE DAY", LIGHT, 2)

    # Hero panel: Ras Tanura
    hx, hy, hw, hh = 16, 116, 992, 300
    refinery_scene(c, hx, hy, hw, 190)
    c.rect(hx, hy + 190, hw, hh - 190, NAVY2)
    c.rect(hx, hy + 190, hw, 3, GOLD)
    c.text(hx + 20, hy + 204, "1  OIL UNDER FIRE", GOLD, 2)
    c.text_block(hx + 20, hy + 230,
                 "HOUTHIS CLAIM STRIKE ON SAUDI REFINERY",
                 WHITE, 3, hw - 40)
    c.text(hx + 20, hy + 268,
           "RAS TANURA - 4 DRONES DOWNED, BRENT OIL JUMPS",
           LIGHT, 2)

    # 2x2 grid
    gy = 432
    gw, gh = 490, 258
    gx = (16, 518)
    panels = [
        (hormuz_scene, "2  SEA LANES AT RISK",
         "TANKERS HIT MINES IN STRAIT OF HORMUZ",
         "SHIPS TARGETED - OIL ROUTE IN DOUBT"),
        (space_scene, "3  NEW CREW IN ORBIT",
         "PAKISTAN ASTRONAUT JOINS CHINA SPACE STATION",
         "FIRST FOREIGN FLIER TO TIANGONG"),
        (gaza_scene, "4  CEASEFIRE UNDER STRAIN",
         "ISRAEL STRIKES HAMAS OFFICIAL IN GAZA",
         "TRUCE TALKS SHAKEN AS STRIKES RESUME"),
        (mercury_scene, "5  EIGHT YEARS ON THE ROAD",
         "BEPICOLOMBO REACHES MERCURY ORBIT",
         "EUROPE-JAPAN PROBE ENDS 8-YEAR TRIP"),
    ]
    for row in range(2):
        for col in range(2):
            idx = row * 2 + col
            scene, kicker, headline, sub = panels[idx]
            px, py = gx[col], gy + row * (gh + 12)
            scene(c, px, py, gw, 132)
            c.rect(px, py + 132, gw, gh - 132, PANEL)
            c.rect(px, py + 132, gw, 3, GOLD)
            c.text(px + 16, py + 144, kicker, GOLD, 2)
            c.text_block(px + 16, py + 168, headline, WHITE, 2, gw - 32)
            c.text(px + 16, py + 226, sub, LIGHT, 2)

    # Footer
    c.rect(0, 984, W, 40, DARK)
    c.rect(0, 984, W, 3, GOLD)
    c.text(28, 998, "AS REPORTED ON 26 NOVEMBER 2026 - REUTERS / AP / BBC",
           LIGHT, 2)
    return c


# ------------------------------------------------------------------ png ------
def encode_png(c):
    raw = bytearray()
    for y in range(c.h):
        raw.append(0)
        start = y * c.w * 3
        raw.extend(c.px[start:start + c.w * 3])

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        out += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", c.w, c.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


def output_path():
    out = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    if os.path.isdir(out):
        return os.path.join(out, "entry.png")
    os.makedirs("out", exist_ok=True)
    return os.path.join("out", "entry.png")


def main():
    data = encode_png(build())
    path = output_path()
    with open(path, "wb") as f:
        f.write(data)


if __name__ == "__main__":
    main()
