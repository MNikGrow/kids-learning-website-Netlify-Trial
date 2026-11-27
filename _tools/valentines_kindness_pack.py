"""BodhiCubs monthly pack: Valentine's & Kindness Activities (built 2026-11-27).
Run: python3 _tools/valentines_kindness_pack.py <out_dir>
"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reportlab.pdfgen import canvas
from printables_lib import *
from printables_lib import _start, _count

OUT = sys.argv[1] if len(sys.argv) > 1 else "out/"
PDF = "BodhiCubs_Valentines_Kindness_Activities_Ages4-9.pdf"
COLOR["pink"] = (0.97, 0.62, 0.74); BW["pink"] = (1, 1, 1)
COLOR["purple"] = (0.55, 0.35, 0.78); BW["purple"] = (1, 1, 1)

# ---------- theme icons (unit box -0.5..0.5) ----------
def heart_path(c, k=1.0, dx=0, dy=0):
    p = c.beginPath()
    def P_(x, y): return (dx + x * k, dy + y * k)
    p.moveTo(*P_(0, -0.42))
    p.curveTo(*P_(-0.2, -0.24), *P_(-0.47, -0.06), *P_(-0.46, 0.15))
    p.curveTo(*P_(-0.45, 0.4), *P_(-0.12, 0.48), *P_(0, 0.26))
    p.curveTo(*P_(0.12, 0.48), *P_(0.45, 0.4), *P_(0.46, 0.15))
    p.curveTo(*P_(0.47, -0.06), *P_(0.2, -0.24), *P_(0, -0.42))
    p.close(); return p

def ic_heart(c, x, y, s, P):
    _start(c, x, y, s, P); fill(c, P["red"]); c.drawPath(heart_path(c), 1, 1); c.restoreState()

def ic_heart_open(c, x, y, s, P):  # outline heart for kids to color
    _start(c, x, y, s, P); c.setLineWidth(0.05); fill(c, P["white"]); c.drawPath(heart_path(c), 1, 1); c.restoreState()

def ic_flower(c, x, y, s, P):
    _start(c, x, y, s, P)
    c.setLineWidth(0.05); stroke(c, P["green"] if not P["bw"] else P["ink"]); c.line(0, -0.48, 0, 0.0)
    c.setLineWidth(0.035); stroke(c, P["ink"]); fill(c, P["green"]); c.ellipse(0.0, -0.32, 0.24, -0.2, 1, 1)
    fill(c, P["pink"])
    for i in range(5):
        a = math.radians(90 + i * 72); c.circle(0.17 * math.cos(a), 0.14 + 0.17 * math.sin(a), 0.13, 1, 1)
    fill(c, P["gold"]); c.circle(0, 0.14, 0.1, 1, 1)
    c.restoreState()

def ic_smile(c, x, y, s, P):
    _start(c, x, y, s, P)
    fill(c, P["gold"]); c.circle(0, 0, 0.44, 1, 1)
    fill(c, P["ink"]); c.circle(-0.15, 0.1, 0.055, 1, 0); c.circle(0.15, 0.1, 0.055, 1, 0)
    c.setLineWidth(0.05); p = c.beginPath(); p.arc(-0.24, -0.34, 0.24, 0.0, 200, 140); c.drawPath(p, 1, 0)
    c.restoreState()

def ic_envelope(c, x, y, s, P):
    _start(c, x, y, s, P)
    fill(c, P["light"] if not P["bw"] else P["white"]); c.rect(-0.45, -0.3, 0.9, 0.6, 1, 1)
    c.line(-0.45, 0.3, 0, -0.04); c.line(0.45, 0.3, 0, -0.04)
    c.restoreState()
    _start(c, x, y, s, P); fill(c, P["red"]); c.drawPath(heart_path(c, 0.3, 0, -0.06), 1, 1); c.restoreState()

def ic_balloon(c, x, y, s, P):
    _start(c, x, y, s, P)
    c.setLineWidth(0.025); p = c.beginPath(); p.moveTo(0, -0.18); p.curveTo(0.1, -0.28, -0.1, -0.38, 0.03, -0.5); c.drawPath(p, 1, 0)
    c.setLineWidth(0.035); fill(c, P["purple"]); c.ellipse(-0.27, -0.14, 0.27, 0.48, 1, 1)
    poly(c, [(0, -0.14), (-0.06, -0.21), (0.06, -0.21)])
    c.restoreState()

def ic_cupcake(c, x, y, s, P):
    _start(c, x, y, s, P)
    fill(c, P["blue"]); poly(c, [(-0.3, 0.0), (0.3, 0.0), (0.22, -0.44), (-0.22, -0.44)])
    for k in (-0.12, 0.0, 0.12): c.line(k * 1.4, 0.0, k, -0.44)
    fill(c, P["pink"])
    p = c.beginPath(); p.moveTo(-0.36, 0.0); p.curveTo(-0.46, 0.18, -0.3, 0.26, -0.2, 0.22)
    p.curveTo(-0.16, 0.4, 0.16, 0.4, 0.2, 0.22); p.curveTo(0.3, 0.26, 0.46, 0.18, 0.36, 0.0); p.close(); c.drawPath(p, 1, 1)
    fill(c, P["red"]); c.circle(0, 0.4, 0.07, 1, 1)
    c.restoreState()

ICONS.update(heart=ic_heart, heart_open=ic_heart_open, flower=ic_flower, smile=ic_smile, envelope=ic_envelope,
             balloon=ic_balloon, cupcake=ic_cupcake)

def turned(c, name, x, y, s, P):
    c.saveState(); c.translate(x, y); c.rotate(180); icon(c, name, 0, 0, s, P); c.restoreState()

# ---------- frame / helpers ----------
def frame(c, P, title, sub=None, name=True):
    stroke(c, P["ink"]); c.setLineWidth(1.5)
    fill(c, P["band"]); c.roundRect(36, H - 112, W - 72, 76, 18, stroke=1 if P["bw"] else 0, fill=1)
    sz = fit(title, "PB", 26, W - 200)
    text(c, W / 2, H - 72 if sub else H - 82, title, "PB", sz, P["bandtxt"])
    if sub: text(c, W / 2, H - 96, sub, "PM", 11.5, P["bandtxt"])
    hp = dict(P); hp["red"] = P["pink"] if not P["bw"] else P["white"]
    icon(c, "heart", 72, H - 74, 44, hp); icon(c, "envelope", W - 72, H - 74, 44, P)
    if name:
        text(c, 40, H - 140, "Name: ______________________________", "PM", 11, P["ink"], "l")
        text(c, W - 40, H - 140, "Date: ______________", "PM", 11, P["ink"], "r")
    text(c, W / 2, 22, "© BodhiCubs  •  Personal & classroom use  •  bodhicubs.com", "PR", 8, P["grey"])

def box(c, P, x, y, w, h, r=14, f="white"):
    stroke(c, P["ink"]); c.setLineWidth(1.5); fill(c, P[f]); c.roundRect(x, y, w, h, r, 1, 1)

def lines_(c, P, x0, x1, y):
    stroke(c, P["ink"]); c.setLineWidth(0.9); c.line(x0, y, x1, y)

# ---------- cover / info ----------
ACTIVITIES = 11
def cover(c):
    P = COLOR
    fill(c, P["light"]); c.rect(0, 0, W, H, 0, 1)
    stroke(c, P["red"]); c.setLineWidth(10); c.roundRect(20, 20, W - 40, H - 40, 26, 1, 0)
    stroke(c, P["pink"]); c.setLineWidth(3); c.roundRect(34, 34, W - 68, H - 68, 20, 1, 0)
    fill(c, P["green"]); c.roundRect(W / 2 - 80, H - 98, 160, 34, 17, 0, 1)
    text(c, W / 2, H - 87, "BodhiCubs", "PB", 16, P["white"])
    icon(c, "heart", 90, H - 82, 60, P); icon(c, "envelope", W - 90, H - 82, 58, P)
    y = H - 175
    for i, ln in enumerate(["Valentine's &", "Kindness Fun"]):
        sz = fit(ln, "PB", 52, W - 160)
        text(c, W / 2, y, ln, "PB", sz, P["red"] if i == 0 else P["dkgreen"]); y -= sz * 1.1
    fill(c, P["gold"]); c.roundRect(W / 2 - 170, y - 10, 340, 38, 19, 0, 1)
    text(c, W / 2, y + 2, f"Ages 4–9  •  {ACTIVITIES} Kind & Clever Activities", "PB", 15, P["ink"])
    y -= 70
    for i, n in enumerate(["flower", "balloon", "heart", "smile", "cupcake"]): icon(c, n, W / 2 + (i - 2) * 92, y, 74, P)
    y -= 62
    inside = ["14-day kindness challenge + kindness jar", "Count the hearts and heart math",
              "Word search, maze, picture sudoku", "Patterns, odd one out, secret messages",
              "My Friend & Me page + 6 cut-out friendship cards", "Black & white version + answer key"]
    bh = 46 + 25 * len(inside)
    box(c, P, 80, y - bh, W - 160, bh, 16)
    text(c, W / 2, y - 26, "What's inside", "PB", 16, P["dkgreen"])
    for i, it in enumerate(inside): text(c, 115, y - 52 - i * 25, "•  " + it, "PM", 12.5, P["ink"], "l")
    text(c, W / 2, 62, "Free printable  •  Color + Black & White  •  Answer Key", "PM", 12, P["ink"])

def thanks(c):
    P = COLOR; frame(c, P, "Hello, grown-ups!", "Read this before printing", name=False)
    lines = [
        ("Printing tips", ["Choose \"Fit to page\" in your print settings. The pages work on US Letter and A4 paper.",
                           "Low on color ink? The black & white version starts after the color pages.",
                           "Answers are at the very end."]),
        ("How to use this pack", ["Use it for Valentine's Day (14 February), a kindness week, or any day you want to talk about friendship.",
                                  "Younger kids (4–5): counting hearts, patterns, the maze, the kindness jar and the cards with a helper.",
                                  "Older kids (6–9): heart math, sudoku, word search, secret messages and the 14-day challenge."]),
        ("You may", ["Print as many copies as you need for your own family or classroom."]),
        ("Please don't", ["Sell or re-upload these files. Share the link bodhicubs.com/printables instead. Thank you!"]),
        ("More free fun", ["Play free science games, Brain Gym and puzzles at bodhicubs.com"]),
    ]
    y = TOP + 6
    for head, items in lines:
        text(c, 70, y, head, "PB", 17, P["acc"], "l"); y -= 26
        for it in items:
            n = wrap(c, 90, y, "•  " + it, "PR", 12.5, W - 170, P["ink"], 17, "l"); y -= 17 * n + 6
        y -= 12
    for i, n in enumerate(["flower", "heart", "smile", "balloon", "cupcake"]): icon(c, n, W / 2 + (i - 2) * 80, 74, 56, P)

def divider(c, title, sub, lines, P):
    frame(c, P, title, sub, name=False)
    for i, ln in enumerate(lines): instr(c, P, H / 2 + 40 - i * 30, ln, 15)
    for i, n in enumerate(["heart", "flower", "smile", "envelope"]): icon(c, n, W / 2 + (i - 1.5) * 100, H / 2 - 110, 70, P)

# ---------- 1. 14-day kindness challenge ----------
CHALLENGE = ["Smile at 5 people today", "Say thank you to a helper", "Share a toy or a snack", "Make a card for someone",
             "Help tidy up without being asked", "Say something nice to a friend", "Play with someone new",
             "Draw a picture for someone", "Help set the table or cook", "Write a kind note to yourself",
             "Talk to a grandparent or older friend", "Pick up 5 bits of litter (with a grown-up)",
             "Read a story to someone", "Say one kind thing about each person at home"]
def p_challenge(c, P):
    frame(c, P, "14-Day Kindness Challenge", "One kind act a day")
    instr(c, P, TOP - 16, "Do one kind thing each day. Then color the heart. Can you fill them all?", 12)
    cols, rows = 3, 5; gw = W - 80; cw = gw / cols; ch = 112; ytop = TOP - 34
    for i in range(15):
        col, row = i % cols, i // cols; x = 40 + col * cw; y = ytop - (row + 1) * ch
        box(c, P, x + 4, y + 4, cw - 8, ch - 8, 12, "soft" if i == 14 else "white")
        if i < 14:
            text(c, x + 16, y + ch - 28, f"Day {i + 1}", "PB", 13, P["acc"], "l")
            icon(c, "heart_open", x + cw - 30, y + ch - 30, 30, P)
            wrap(c, x + cw / 2, y + ch - 56, CHALLENGE[i], "PM", 11.5, cw - 28, P["ink"], 14.5)
        else:
            icon(c, "star", x + cw / 2, y + ch / 2 + 14, 46, P)
            text(c, x + cw / 2, y + 20, "I did it!", "PB", 16, P["acc"])

# ---------- 2. count the hearts ----------
COUNT = [({"heart": 6}, "heart", "How many hearts?"), ({"heart": 8, "flower": 3}, "heart", "How many hearts?"),
         ({"balloon": 5, "heart": 4}, "balloon", "How many balloons?"), ({"heart": 9, "smile": 3}, "smile", "How many smiley faces?"),
         ({"cupcake": 4, "flower": 7}, "flower", "How many flowers?"), ({"heart": 10, "star": 2}, "heart", "How many hearts?")]
def p_count(c, P):
    frame(c, P, "Count the Hearts", "Counting fun for little ones")
    instr(c, P, TOP - 16, "Count the pictures. Write the number in the box.", 13)
    w, h = 252, 178; rng = random.Random(4201)
    for i, (counts, ask, q) in enumerate(COUNT):
        col, row = i % 2, i // 2; x = 46 + col * (w + 16); y = TOP - 36 - (row + 1) * (h + 12)
        box(c, P, x, y, w, h, 14, "soft")
        text(c, x + 14, y + h - 22, f"{i + 1}.  {q}", "PB", 12, P["acc"], "l")
        for px, py, it in scatter(rng, counts, (x + 10, y + 10, x + w - 70, y + h - 30), 31): icon(c, it, px, py, 27, P)
        answer_box(c, P, x + w - 60, y + h / 2 - 30, 46, 40)

# ---------- 3. heart math ----------
PIC_SUMS = [(2, 3), (4, 1), (3, 3)]
SUMS = [("5 + 4 = ___", 9), ("8 + 6 = ___", 14), ("12 − 5 = ___", 7), ("15 − 7 = ___", 8),
        ("7 + ___ = 12", 5), ("___ − 3 = 9", 12), ("6 + 6 + 2 = ___", 14), ("10 + 4 = ___", 14)]
def sum_check():
    vals = [5 + 4, 8 + 6, 12 - 5, 15 - 7, 12 - 7, 9 + 3, 6 + 6 + 2, 10 + 4]
    return [v for v in vals]
def p_math(c, P):
    frame(c, P, "Heart Math", "Add and take away")
    text(c, 50, TOP - 18, "A.  Add the hearts. Write how many in all.", "PB", 13, P["acc"], "l")
    for i, (a, b) in enumerate(PIC_SUMS):
        y = TOP - 66 - i * 64; x = 80
        for k in range(a): icon(c, "heart", x + k * 40, y, 34, P)
        x += (a - 1) * 40 + 40; text(c, x, y - 9, "+", "PB", 26, P["ink"]); x += 40
        for k in range(b): icon(c, "heart", x + k * 40, y, 34, P)
        x += (b - 1) * 40 + 40; text(c, x, y - 9, "=", "PB", 26, P["ink"]); x += 24
        answer_box(c, P, x, y - 22, 52, 44)
    y0 = TOP - 66 - 3 * 64 + 8
    text(c, 50, y0, "B.  Heart sums. Write the missing number in each heart.", "PB", 13, P["acc"], "l")
    for i, (s, _) in enumerate(SUMS):
        col, row = i % 2, i // 2; x = 70 + col * 260; y = y0 - 50 - row * 62
        box(c, P, x - 14, y - 22, 236, 52, 12, "soft")
        pre, post = s.split("___"); xx = x + 4
        if pre: text(c, xx, y - 4, pre.strip(), "PB", 17, P["ink"], "l"); xx += pdfmetrics.stringWidth(pre.strip(), "PB", 17) + 8
        icon(c, "heart_open", xx + 18, y + 2, 38, P); xx += 44
        text(c, xx, y - 4, post.strip(), "PB", 17, P["ink"], "l")
    text(c, W / 2, 56, "Tip: use real buttons, beads or paper hearts to help you count.", "PR", 11, P["grey"])

# ---------- 4. patterns & odd one out ----------
ODD = [("heart", 3), ("balloon", 1), ("cupcake", 4), ("envelope", 2)]
PATS = [(["heart", "flower", "heart", "flower", "heart"], "flower"), (["smile", "smile", "balloon", "smile", "smile"], "balloon"),
        (["heart", "star", "cupcake", "heart", "star"], "cupcake")]
NUMS = [([2, 4, 6, 8], 10, "2, 4, 6, 8, ___"), ([1, 3, 5, 7], 9, "1, 3, 5, 7, ___"), ([14, 12, 10, 8], 6, "14, 12, 10, 8, ___")]
def p_odd(c, P):
    frame(c, P, "Odd One Out & What Comes Next", "Look closely!")
    text(c, 50, TOP - 18, "A.  One picture is upside down. Circle it!", "PB", 13, P["acc"], "l")
    for i, (n, odd) in enumerate(ODD):
        y = TOP - 62 - i * 64
        for k in range(5):
            x = 110 + k * 88
            if k == odd: turned(c, n, x, y, 52, P)
            else: icon(c, n, x, y, 52, P)
    y0 = TOP - 62 - 4 * 64 + 16
    text(c, 50, y0, "B.  What comes next? Draw it or write it in the box.", "PB", 13, P["acc"], "l")
    for i, (seq, ans) in enumerate(PATS):
        y = y0 - 44 - i * 56
        for k, n in enumerate(seq): icon(c, n, 110 + k * 66, y, 44, P)
        answer_box(c, P, 110 + 5 * 66 - 24, y - 24, 48, 48)
    y1 = y0 - 44 - 3 * 56 + 8
    for i, (_, _, s) in enumerate(NUMS):
        text(c, 56 + i * 180, y1 - 8, s, "PB", 13, P["ink"], "l")

# ---------- 5. sudoku ----------
SYMS = ["heart", "flower", "star", "smile"]
def mk_sudoku(seeds, givens=8):
    puz = [make_sudoku(s, givens) for s in seeds]
    def page(c, P):
        frame(c, P, "Picture Sudoku", "4 x 4 logic puzzles")
        instr(c, P, TOP - 18, "Draw the missing pictures. Each row, column and 2x2 box")
        instr(c, P, TOP - 36, "must have one of each:")
        for i, n in enumerate(SYMS): icon(c, n, W / 2 - 75 + i * 50, TOP - 66, 36, P)
        for i, (p, s) in enumerate(puz):
            col, row = i % 2, i // 2; size = 206
            x = 78 + col * (size + 50); y = TOP - 110 - (row + 1) * (size + 36) + 20
            text(c, x + size / 2, y + size + 8, f"Puzzle {i + 1}", "PB", 12, P["acc"])
            draw_sudoku(c, P, p, SYMS, x, y, size)
    def mini(c, P, i, x, y, s): draw_sudoku(c, P, puz[i][1], SYMS, x, y, s, lw=1.2)
    return page, mini, puz

# ---------- 6. maze ----------
def mk_maze(seed):
    m = make_maze(10, 12, seed)
    def page(c, P):
        frame(c, P, "Friendship Letter Maze", "Find the way")
        instr(c, P, TOP - 18, "Help the letter reach the heart. Do not cross any lines!")
        draw_maze(c, P, m, 70, 96, W - 140, TOP - 196, icons=("envelope", "heart"))
    def mini(c, P, x, y, s): draw_maze(c, P, m, x, y, s, s, answers=True, icons=None, lw=1.1)
    return page, mini, m

# ---------- 7. word search ----------
WORDS = ["KIND", "CARE", "SHARE", "HUG", "SMILE", "FRIEND", "HEART", "LOVE", "HELP", "THANKS", "GENTLE", "CARD"]
def mk_ws(seed):
    g, placed = make_wordsearch(WORDS, 12, [(0, 1), (1, 0), (1, 1)], seed)
    def page(c, P):
        frame(c, P, "Kindness Word Search", "12 x 12  •  across, down, diagonal")
        instr(c, P, TOP - 18, "Find and circle each word. Check it off the list!")
        size = 372; x = (W - size) / 2; y = TOP - 48 - size
        draw_wordsearch(c, P, g, placed, x, y, size)
        for i, w in enumerate(WORDS):
            col, row = divmod(i, 4); xx = 90 + col * 160; yy = y - 40 - row * 22
            stroke(c, P["ink"]); c.setLineWidth(1.2); fill(c, P["white"]); c.rect(xx, yy - 2, 12, 12, 1, 1)
            text(c, xx + 20, yy, w, "PM", 12.5, P["ink"], "l")
    def mini(c, P, x, y, s): draw_wordsearch(c, P, g, placed, x, y, s, answers=True)
    return page, mini, g, placed

# ---------- 8. secret code ----------
MESSAGES = ["BE KIND", "SHARE A SMILE", "YOU MAKE ME HAPPY", "KINDNESS IS COOL"]
def encode(m): return [None if ch == " " else ord(ch) - 64 for ch in m]
def decode(nums): return "".join(" " if n is None else chr(n + 64) for n in nums)
def p_code(c, P):
    frame(c, P, "Secret Kind Messages", "Be a code breaker")
    instr(c, P, TOP - 16, "Use the code key. Write the letter above each number to read the message.", 12)
    y = TOP - 42; cw = (W - 88) / 13
    box(c, P, 40, y - 86, W - 80, 88, 12, "soft")
    for i in range(26):
        col, row = i % 13, i // 13; x = 44 + col * cw; yy = y - 22 - row * 42
        text(c, x + cw / 2, yy, chr(65 + i), "PB", 13, P["acc"])
        text(c, x + cw / 2, yy - 15, str(i + 1), "PM", 11, P["ink"])
    y -= 110
    for k, m in enumerate(MESSAGES):
        nums = encode(m); bw = min(32, (W - 90) / len(nums)); x0 = (W - bw * len(nums)) / 2
        text(c, 46, y - 4, f"{k + 1}.", "PB", 14, P["acc"], "l")
        for j, n in enumerate(nums):
            if n is None: continue
            x = x0 + j * bw
            stroke(c, P["ink"]); c.setLineWidth(1.2); fill(c, P["white"]); c.rect(x + 2, y - 44, bw - 4, 34, 1, 1)
            text(c, x + bw / 2, y - 60, str(n), "PM", 11, P["ink"])
        y -= 96

# ---------- 9. kindness jar ----------
JAR_HEARTS = 20
def jar_hearts():
    pts = []
    for r, n in enumerate([4, 5, 4, 5, 2]):
        for k in range(n): pts.append(((k - (n - 1) / 2) * 62, r * 58))
    return pts
def p_jar(c, P):
    frame(c, P, "My Kindness Jar", "Fill it with kind acts")
    instr(c, P, TOP - 16, "Each time you do something kind, color one heart in the jar.", 12.5)
    cx = W / 2; jb = 210; jt = TOP - 70; jw = 360
    stroke(c, P["ink"]); c.setLineWidth(2.5); fill(c, P["soft"] if not P["bw"] else P["white"])
    c.roundRect(cx - jw / 2, jb, jw, jt - jb - 40, 40, 1, 1)
    fill(c, P["white"]); c.rect(cx - 120, jt - 44, 240, 30, 1, 1)
    fill(c, P["pink"]); c.roundRect(cx - 136, jt - 18, 272, 34, 10, 1, 1)
    text(c, cx, jt - 6, "KINDNESS", "PB", 15, P["ink"])
    for dx, dy in jar_hearts(): icon(c, "heart_open", cx + dx, jb + 40 + dy, 50, P)
    text(c, 60, 166, "The kindest thing I did:", "PB", 13, P["acc"], "l")
    for k in range(3): lines_(c, P, 60, W - 60, 134 - k * 30)

# ---------- 10. my friend & me ----------
def p_friend(c, P):
    frame(c, P, "My Friend & Me", "Draw and write")
    box(c, P, 60, TOP - 330, W - 120, 300, 16)
    text(c, W / 2, TOP - 54, "Draw you and your friend doing something fun together.", "PM", 12, P["grey"])
    prompts = ["My friend's name is", "We like to", "My friend is kind when", "I am a good friend because"]
    y = TOP - 370
    for p in prompts:
        text(c, 60, y, p, "PB", 13, P["acc"], "l")
        lines_(c, P, 60 + pdfmetrics.stringWidth(p, "PB", 13) + 10, W - 60, y - 2)
        lines_(c, P, 60, W - 60, y - 30); y -= 66

# ---------- 11. friendship cards ----------
CARDS = [("You make me smile!", "smile"), ("Thank you!", "flower"), ("You are a great friend", "heart"),
         ("You are so kind", "star"), ("Let's play together!", "balloon"), ("I'm glad you're you!", "cupcake")]
def p_cards(c, P):
    frame(c, P, "Friendship Cards", "Color, write, cut out and give!", name=False)
    w, h = 258, 200; x0 = (W - 2 * w) / 2; ytop = H - 128
    c.saveState(); stroke(c, P["grey"]); c.setLineWidth(1); c.setDash(4, 4)
    for i in range(3): c.line(x0 + i * w, ytop, x0 + i * w, ytop - 3 * h)
    for i in range(4): c.line(x0, ytop - i * h, x0 + 2 * w, ytop - i * h)
    c.restoreState()
    for i, (t, ic) in enumerate(CARDS):
        col, row = i % 2, i // 2; x = x0 + col * w; y = ytop - (row + 1) * h
        icon(c, ic, x + w / 2, y + h - 34, 44, P)
        text(c, x + w / 2, y + h - 76, t, "PB", fit(t, "PB", 15, w - 24), P["acc"])
        text(c, x + 18, y + 96, "To:", "PM", 11, P["ink"], "l"); lines_(c, P, x + 44, x + w - 18, y + 94)
        lines_(c, P, x + 18, x + w - 18, y + 70); lines_(c, P, x + 18, x + w - 18, y + 46)
        text(c, x + 18, y + 18, "From:", "PM", 11, P["ink"], "l"); lines_(c, P, x + 56, x + w - 18, y + 16)

# ---------- answers ----------
def count_answers(): return [counts[ask] for counts, ask, _ in COUNT]
def p_answers_text(c, P):
    frame(c, P, "Answer Key", "Counting, math, patterns, code", name=False)
    names = {"heart": "heart", "flower": "flower", "balloon": "balloon", "cupcake": "cupcake", "smile": "smiley face",
             "star": "star", "envelope": "envelope"}
    left = [("Count the Hearts", [f"{i + 1}.  {v}" for i, v in enumerate(count_answers())]),
            ("Heart Math – A", [f"{i + 1}.  {a} + {b} = {a + b}" for i, (a, b) in enumerate(PIC_SUMS)]),
            ("Heart Math – B", [f"{i + 1}.  {s.replace('___', '[' + str(v) + ']')}" for i, (s, v) in enumerate(SUMS)])]
    right = [("Odd One Out", [f"Row {i + 1}: picture {o + 1}" for i, (_, o) in enumerate(ODD)]),
             ("What Comes Next", [f"{i + 1}.  {names[a]}" for i, (_, a) in enumerate(PATS)] + [f"{i + 4}.  {a}" for i, (_, a, _s) in enumerate(NUMS)]),
             ("Secret Kind Messages", [f"{i + 1}.  {m}" for i, m in enumerate(MESSAGES)])]
    for x, blocks, mw in ((60, left, 240), (320, right, 240)):
        y = TOP + 8
        for head, lines in blocks:
            text(c, x, y, head, "PB", 12.5, P["acc"], "l"); y -= 19
            for ln in lines:
                n = wrap(c, x + 8, y, ln, "PR", 11, mw, P["ink"], 15, "l"); y -= 15 * n + 2
            y -= 12

def answer_puzzles(ws_mini, maze_mini):
    def page(c, P):
        frame(c, P, "Answer Key", "Word search & maze", name=False)
        s = 236
        for i, (t, m) in enumerate([("Kindness Word Search", ws_mini), ("Friendship Letter Maze", maze_mini)]):
            x = 56 + i * (s + 28); y = TOP - 280
            text(c, x + s / 2, y + s + 16, t, "PB", 12, P["acc"]); m(c, P, x, y, s)
    return page

def answer_sudoku(mini, n):
    def page(c, P):
        frame(c, P, "Answer Key", "Picture Sudoku", name=False)
        s = 200
        for i in range(n):
            col, row = i % 2, i // 2
            x = 90 + col * (s + 50); y = TOP - 50 - (row + 1) * (s + 50) + 20
            text(c, x + s / 2, y + s + 10, f"Puzzle {i + 1}", "PB", 12, P["acc"]); mini(c, P, i, x, y, s)
    return page

# ---------- verification ----------
def verify(ws, maze, puz):
    g, placed = ws
    for w, r, cc, dr, dc in placed:
        assert "".join(g[r + dr * i][cc + dc * i] for i in range(len(w))) == w, w
    assert sorted(p[0] for p in placed) == sorted(WORDS)
    path = maze["path"]; assert path[0] == (0, 0) and path[-1] == (maze["h"] - 1, maze["w"] - 1)
    D = {(-1, 0): "N", (1, 0): "S", (0, 1): "E", (0, -1): "W"}
    for a, b in zip(path, path[1:]): assert D[(b[0] - a[0], b[1] - a[1])] not in maze["walls"][a]
    for p, s in puz:
        assert _count(p[:], 3) == 1 and all(p[i] is None or p[i] == s[i] for i in range(16))
        for k in range(4): assert len({s[k * 4 + j] for j in range(4)}) == 4 and len({s[j * 4 + k] for j in range(4)}) == 4
    assert [v for _, v in SUMS] == sum_check(), ([v for _, v in SUMS], sum_check())
    # check each sum sentence by evaluating with the answer filled in
    for s, v in SUMS:
        lhs, rhs = s.replace("−", "-").replace("___", str(v)).split("=")
        assert eval(lhs) == int(rhs), s
    for m in MESSAGES: assert decode(encode(m)) == m
    for seq, ans in PATS:
        if seq[0] == seq[2] == seq[4]: assert ans == seq[1]
        elif seq[:2] == seq[3:]: assert ans == seq[2]
        else: assert seq[:3] == seq[3:] + [ans] or seq[:2] == seq[3:]
    for seq, ans, _ in NUMS: assert seq[1] - seq[0] == seq[3] - seq[2] == ans - seq[3]
    assert len(CHALLENGE) == 14 and len(jar_hearts()) == JAR_HEARTS
    print("verify OK")

def run():
    os.makedirs(OUT, exist_ok=True)
    ws, ws_mini, g, placed = mk_ws(4101)
    mz, mz_mini, maze = mk_maze(4102)
    sd, sd_mini, puz = mk_sudoku([4103, 4104, 4105, 4106], 8)
    verify((g, placed), maze, puz)
    pages = [p_challenge, p_count, p_math, p_odd, sd, mz, ws, p_code, p_jar, p_friend, p_cards]
    assert len(pages) == ACTIVITIES
    c = canvas.Canvas(os.path.join(OUT, PDF), pagesize=letter)
    c.setTitle("Valentine's & Kindness Activities for Kids – Free Printable Pack"); c.setAuthor("BodhiCubs")
    cover(c); c.showPage(); thanks(c); c.showPage()
    for p in pages: p(c, COLOR); c.showPage()
    divider(c, "Black & White Version", "Printer-friendly", [f"The same {ACTIVITIES} pages in black & white.", "Kids can color them in too!"], BW); c.showPage()
    for p in pages: p(c, BW); c.showPage()
    divider(c, "Answer Key", "For grown-ups", ["Answers for counting, math, patterns,", "code, word search, maze and sudoku."], COLOR); c.showPage()
    p_answers_text(c, COLOR); c.showPage()
    answer_puzzles(ws_mini, mz_mini)(c, COLOR); c.showPage()
    answer_sudoku(sd_mini, len(puz))(c, COLOR); c.showPage()
    c.save(); print("saved", os.path.join(OUT, PDF))

if __name__ == "__main__":
    run()
