# World News in One Image - 24 November 2026
#
# A program that draws one newspaper-style image summing up the world news
# of Tuesday 24 November 2026. Everything is drawn procedurally with the
# Python standard library only: a small bitmap font, simple shapes, and a
# hand-rolled PNG encoder. No network, no files read, no randomness, so
# every run writes the exact same bytes.
#
# The six stories were checked against news reported on 24 November 2026:
#   1. World Chess Championship, Game 1: Gukesh vs Sindarov, Geneva.
#   2. Crimea Platform summit: European leaders gather in Stockholm.
#   3. US lists Venezuela's Cartel de los Soles as a terrorist group.
#   4. India-Nepal: Saryu-Kamala Express flagged off, Ayodhya to Janakpur.
#   5. Lisbon: unions rally outside parliament on budget-vote day.
#   6. Markets: India's Sensex falls 1,484 points to 82,435.

import os
import struct
import zlib

W = 1024
H = 1024

NAVY = (16, 28, 52)
PAPER = (250, 247, 240)
WHITE = (255, 255, 255)
INK = (24, 24, 24)
GREY = (110, 110, 110)
BORDER = (205, 205, 205)
GOLD = (212, 175, 55)
RED = (178, 34, 34)
BLUE = (0, 91, 172)
TEAL = (0, 128, 96)
GREEN = (0, 102, 51)
LIGHT_BLUE = (135, 206, 235)
DARK = (40, 40, 40)

# ---------------------------------------------------------------- font
# A 5x7 bitmap font. Each glyph is 7 rows of 5 characters; '#' is on.
FONT = {
    'A': [" ### ", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    'B': ["#### ", "#   #", "#   #", "#### ", "#   #", "#   #", "#### "],
    'C': [" ### ", "#   #", "#    ", "#    ", "#    ", "#   #", " ### "],
    'D': ["#### ", "#   #", "#   #", "#   #", "#   #", "#   #", "#### "],
    'E': ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#####"],
    'F': ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#    "],
    'G': [" ### ", "#   #", "#    ", "#  ##", "#   #", "#   #", " ### "],
    'H': ["#   #", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    'I': [" ### ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "],
    'J': ["  ###", "   # ", "   # ", "   # ", "   # ", "#  # ", " #   "],
    'K': ["#   #", "#  # ", "# #  ", "##   ", "# #  ", "#  # ", "#   #"],
    'L': ["#    ", "#    ", "#    ", "#    ", "#    ", "#    ", "#####"],
    'M': ["#   #", "## ##", "# # #", "# # #", "#   #", "#   #", "#   #"],
    'N': ["#   #", "##  #", "# # #", "#  ##", "#   #", "#   #", "#   #"],
    'O': [" ### ", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    'P': ["#### ", "#   #", "#   #", "#### ", "#    ", "#    ", "#    "],
    'Q': [" ### ", "#   #", "#   #", "#   #", "# # #", "#  # ", " ## #"],
    'R': ["#### ", "#   #", "#   #", "#### ", "# #  ", "#  # ", "#   #"],
    'S': [" ####", "#    ", "#    ", " ### ", "    #", "    #", "#### "],
    'T': ["#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "],
    'U': ["#   #", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    'V': ["#   #", "#   #", "#   #", "#   #", "#   #", " # # ", "  #  "],
    'W': ["#   #", "#   #", "#   #", "# # #", "# # #", "## ##", "#   #"],
    'X': ["#   #", "#   #", " # # ", "  #  ", " # # ", "#   #", "#   #"],
    'Y': ["#   #", "#   #", " # # ", "  #  ", "  #  ", "  #  ", "  #  "],
    'Z': ["#####", "    #", "   # ", "  #  ", " #   ", "#    ", "#####"],
    '0': [" ### ", "#   #", "#  ##", "# # #", "##  #", "#   #", " ### "],
    '1': ["  #  ", " ##  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "],
    '2': [" ### ", "#   #", "    #", "  ## ", " #   ", "#    ", "#####"],
    '3': ["#### ", "    #", "    #", " ### ", "    #", "    #", "#### "],
    '4': ["   # ", "  ## ", " # # ", "#  # ", "#####", "   # ", "   # "],
    '5': ["#####", "#    ", "#### ", "    #", "    #", "#   #", " ### "],
    '6': [" ### ", "#    ", "#    ", "#### ", "#   #", "#   #", " ### "],
    '7': ["#####", "    #", "   # ", "  #  ", " #   ", " #   ", " #   "],
    '8': [" ### ", "#   #", "#   #", " ### ", "#   #", "#   #", " ### "],
    '9': [" ### ", "#   #", "#   #", " ####", "    #", "    #", " ### "],
    ' ': ["     ", "     ", "     ", "     ", "     ", "     ", "     "],
    '-': ["     ", "     ", "     ", "#####", "     ", "     ", "     "],
    '.': ["     ", "     ", "     ", "     ", "     ", " ##  ", " ##  "],
    ',': ["     ", "     ", "     ", "     ", " ##  ", "  #  ", " #   "],
    "'": ["  #  ", "  #  ", " #   ", "     ", "     ", "     ", "     "],
    ':': ["     ", " ##  ", " ##  ", "     ", " ##  ", " ##  ", "     "],
    '!': ["  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "     ", "  #  "],
    '?': [" ### ", "#   #", "    #", "  ## ", "  #  ", "     ", "  #  "],
    '(': ["   # ", "  #  ", " #   ", " #   ", " #   ", "  #  ", "   # "],
    ')': [" #   ", "  #  ", "   # ", "   # ", "   # ", "  #  ", " #   "],
    '/': ["    #", "   # ", "   # ", "  #  ", " #   ", " #   ", "#    "],
    '&': [" ##  ", "#  # ", "# #  ", " #   ", "# # #", "#  # ", " ## #"],
    '%': ["##  #", "## # ", "   # ", "  #  ", " #   ", "# ## ", "#  ##"],
    '+': ["     ", "  #  ", "  #  ", "#####", "  #  ", "  #  ", "     "],
    '$': ["  #  ", " ####", "# #  ", " ### ", "  # #", "#### ", "  #  "],
    '"': [" # # ", " # # ", "     ", "     ", "     ", "     ", "     "],
    ';': ["     ", " ##  ", " ##  ", "     ", " ##  ", "  #  ", " #   "],
    '=': ["     ", "     ", "#####", "     ", "#####", "     ", "     "],
}


def glyph(ch):
    # The font holds capitals only; render lowercase as capitals so every
    # letter is legible instead of falling back to '?'.
    return FONT.get(ch.upper(), FONT['?'])


def text_width(text, scale):
    return len(text) * 6 * scale - scale


def wrap_text(text, scale, max_w):
    words = text.split(' ')
    lines = []
    cur = ''
    for word in words:
        trial = word if not cur else cur + ' ' + word
        if text_width(trial, scale) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i] = color[0]
            self.px[i + 1] = color[1]
            self.px[i + 2] = color[2]

    def rect(self, x, y, w, h, color):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, color)

    def circle(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy) <= r * r:
                    self.set(xx, yy, color)

    def ring(self, cx, cy, r, t, color):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d2 = (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy)
                if (r - t) * (r - t) <= d2 <= r * r:
                    self.set(xx, yy, color)

    def line(self, x0, y0, x1, y1, color, thick=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        x, y = x0, y0
        while True:
            for a in range(-(thick // 2), thick // 2 + 1):
                for b in range(-(thick // 2), thick // 2 + 1):
                    self.set(x + a, y + b, color)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy

    def triangle(self, x0, y0, x1, y1, x2, y2, color):
        ys = sorted([y0, y1, y2])
        for yy in range(ys[0], ys[2] + 1):
            xs = []
            for (ax, ay, bx, by) in ((x0, y0, x1, y1), (x1, y1, x2, y2), (x2, y2, x0, y0)):
                if ay == by:
                    continue
                if min(ay, by) <= yy <= max(ay, by):
                    t = (yy - ay) / (by - ay)
                    xs.append(ax + t * (bx - ax))
            if len(xs) >= 2:
                xa, xb = int(min(xs)), int(max(xs))
                for xx in range(xa, xb + 1):
                    self.set(xx, yy, color)

    def text(self, x, y, s, scale, color):
        for ci, ch in enumerate(s):
            g = glyph(ch)
            ox = x + ci * 6 * scale
            for row in range(7):
                for col in range(5):
                    if g[row][col] == '#':
                        self.rect(ox + col * scale, y + row * scale, scale, scale, color)

    def text_center(self, cx, y, s, scale, color):
        self.text(cx - text_width(s, scale) // 2, y, s, scale, color)

    def paragraph(self, x, y, s, scale, color, max_w, leading):
        lines = wrap_text(s, scale, max_w)
        for i, ln in enumerate(lines):
            self.text(x, y + i * leading, ln, scale, color)
        return len(lines) * leading


# ---------------------------------------------------------------- icons
def icon_chess(cv, x, y):
    # Checkerboard with a king piece in the middle.
    cell = 14
    for r in range(8):
        for c in range(8):
            col = WHITE if (r + c) % 2 == 0 else DARK
            cv.rect(x + c * cell, y + r * cell, cell, cell, col)
    # border
    cv.rect(x, y, 112, 3, NAVY)
    cv.rect(x, y + 109, 112, 3, NAVY)
    cv.rect(x, y, 3, 112, NAVY)
    cv.rect(x + 109, y, 3, 112, NAVY)
    cx, cy = x + 56, y + 56
    cv.circle(cx, cy, 26, GOLD)
    cv.ring(cx, cy, 26, 3, NAVY)
    cv.circle(cx, cy - 8, 7, NAVY)
    cv.rect(cx - 12, cy + 2, 24, 5, NAVY)
    cv.rect(cx - 15, cy + 10, 30, 5, NAVY)


def icon_flag(cv, x, y):
    # Blue over yellow flag with a white dove-ish diamond.
    cv.rect(x, y + 8, 112, 48, BLUE)
    cv.rect(x, y + 56, 112, 48, GOLD)
    cv.rect(x, y + 8, 112, 3, NAVY)
    cv.rect(x, y + 101, 112, 3, NAVY)
    cv.rect(x, y + 8, 3, 96, NAVY)
    cv.rect(x + 109, y + 8, 3, 96, NAVY)
    cx, cy = x + 56, y + 56
    cv.rect(cx - 16, cy - 4, 32, 8, WHITE)
    cv.rect(cx - 4, cy - 16, 8, 32, WHITE)


def icon_warning(cv, x, y):
    # Yellow warning triangle with a black exclamation mark.
    cv.triangle(x + 56, y + 6, x + 106, y + 100, x + 6, y + 100, GOLD)
    cv.triangle(x + 56, y + 18, x + 96, y + 92, x + 16, y + 92, (255, 210, 40))
    cv.rect(x + 52, y + 38, 8, 34, DARK)
    cv.rect(x + 52, y + 80, 8, 8, DARK)


def icon_train(cv, x, y):
    # Front of a train on rails.
    cv.rect(x + 16, y + 18, 80, 62, TEAL)
    cv.rect(x + 16, y + 18, 80, 8, NAVY)
    cv.rect(x + 26, y + 34, 24, 20, LIGHT_BLUE)
    cv.rect(x + 62, y + 34, 24, 20, LIGHT_BLUE)
    cv.circle(x + 32, y + 66, 6, GOLD)
    cv.circle(x + 80, y + 66, 6, GOLD)
    cv.circle(x + 32, y + 88, 10, DARK)
    cv.circle(x + 80, y + 88, 10, DARK)
    cv.circle(x + 32, y + 88, 4, GREY)
    cv.circle(x + 80, y + 88, 4, GREY)
    cv.rect(x + 4, y + 104, 104, 4, DARK)
    cv.rect(x + 4, y + 96, 104, 3, DARK)


def icon_crowd(cv, x, y):
    # A crowd of heads with two placards.
    heads = [(18, 78), (42, 66), (66, 78), (90, 66), (30, 96), (58, 92), (84, 96)]
    cols = [RED, BLUE, TEAL, GOLD, GREEN, NAVY, (150, 60, 120)]
    for (hx, hy), col in zip(heads, cols):
        cv.circle(x + hx, y + hy, 9, col)
        cv.rect(x + hx - 9, y + hy + 9, 18, 14, col)
    cv.rect(x + 22, y + 8, 3, 34, DARK)
    cv.rect(x + 12, y + 8, 26, 16, RED)
    cv.rect(x + 78, y + 4, 3, 34, DARK)
    cv.rect(x + 66, y + 4, 26, 16, BLUE)


def icon_chart(cv, x, y):
    # Axes with a falling red line and bars.
    cv.rect(x + 10, y + 10, 4, 92, DARK)
    cv.rect(x + 10, y + 98, 92, 4, DARK)
    bars = [(22, 30, 12, 62), (40, 44, 12, 48), (58, 56, 12, 36), (76, 70, 12, 22)]
    for bx, by, bw, bh in bars:
        cv.rect(x + bx, y + by, bw, bh, (190, 190, 190))
    cv.line(x + 16, y + 22, x + 36, y + 38, RED, 4)
    cv.line(x + 36, y + 38, x + 58, y + 52, RED, 4)
    cv.line(x + 58, y + 52, x + 80, y + 68, RED, 4)
    cv.line(x + 80, y + 68, x + 100, y + 88, RED, 4)
    cv.triangle(x + 100, y + 88, x + 92, y + 84, x + 96, y + 96, RED)


ICONS = [icon_chess, icon_flag, icon_warning, icon_train, icon_crowd, icon_chart]

STORIES = [
    ("CHESS", BLUE, "GAME 1 BEGINS IN GENEVA",
     "Gukesh, 20, defends the world title against Sindarov, 20 - the youngest championship match ever."),
    ("UKRAINE", NAVY, "EUROPE GATHERS IN STOCKHOLM",
     "Leaders meet for the fourth Crimea Platform summit as Ukraine presses for a dignified peace."),
    ("VENEZUELA", RED, "US NAMES CARTEL A TERROR GROUP",
     "Washington lists Venezuela's Cartel de los Soles as a foreign terrorist organisation."),
    ("INDIA - NEPAL", TEAL, "NEW TRAIN LINKS INDIA AND NEPAL",
     "Modi and Shah flag off the Saryu-Kamala Express from Ayodhya to Janakpur."),
    ("PORTUGAL", GREEN, "LISBON RALLIES ON BUDGET DAY",
     "Unions march outside parliament as MPs vote on the budget amid cost-of-living anger."),
    ("MARKETS", RED, "SENSEX SLIDES 1,484 POINTS",
     "Indian shares fall 1.77% to 82,435 as markets slide."),
]


# ---------------------------------------------------------------- png
def chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def encode_png(w, h, px):
    raw = bytearray()
    for yy in range(h):
        raw.append(0)
        raw += px[yy * w * 3:(yy + 1) * w * 3]
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        + chunk(b"IEND", b"")
    )


# ---------------------------------------------------------------- build
def build():
    cv = Canvas(W, H, PAPER)

    # Header band.
    cv.rect(0, 0, W, 148, NAVY)
    cv.text_center(W // 2, 22, "WORLD NEWS", 7, WHITE)
    cv.rect(212, 84, 600, 4, GOLD)
    cv.text_center(W // 2, 102, "TUESDAY 24 NOVEMBER 2026", 4, WHITE)

    # Story panels: 2 columns x 3 rows.
    pw, ph = 488, 264
    for i, (tag, color, headline, caption) in enumerate(STORIES):
        col = i % 2
        row = i // 2
        px = 16 + col * (pw + 16)
        py = 164 + row * (ph + 16)
        cv.rect(px, py, pw, ph, WHITE)
        cv.rect(px, py, pw, 2, BORDER)
        cv.rect(px, py + ph - 2, pw, 2, BORDER)
        cv.rect(px, py, 2, ph, BORDER)
        cv.rect(px + pw - 2, py, 2, ph, BORDER)
        cv.rect(px, py, pw, 36, color)
        cv.text(px + 14, py + 10, tag, 2, WHITE)
        ICONS[i](cv, px + 16, py + 56)
        tx = px + 152
        cv.paragraph(tx, py + 56, headline, 3, INK, pw - 152 - 14, 27)
        cv.paragraph(tx, py + 128, caption, 2, (60, 60, 60), pw - 152 - 14, 22)

    # Footer line.
    cv.text_center(W // 2, 992, "DRAWN FROM REPORTS OF 24 NOVEMBER 2026", 2, GREY)

    return encode_png(W, H, cv.px)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    data = build()
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    print("wrote %s (%d bytes)" % (path, len(data)))


if __name__ == "__main__":
    main()
