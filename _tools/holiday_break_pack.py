"""BodhiCubs monthly pack: Holiday Break Brain Games (built 2026-11-06).
Run: python3 _tools/holiday_break_pack.py <out_dir>
"""
import itertools, math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reportlab.pdfgen import canvas
from printables_lib import *
from printables_lib import _start, _count

OUT = sys.argv[1] if len(sys.argv) > 1 else "out/"
PDF = "BodhiCubs_Holiday_Break_Brain_Games_Ages4-9.pdf"
COLOR["purple"] = (0.45, 0.3, 0.75); BW["purple"] = (1, 1, 1)

# ---------- theme icons (unit box -0.5..0.5); no snow, so they suit both hemispheres ----------
def ic_bulb(c, x, y, s, P):
    _start(c, x, y, s, P)
    fill(c, P["gold"]); c.circle(0, 0.1, 0.32, 1, 1)
    fill(c, P["grey"] if not P["bw"] else P["white"]); c.roundRect(-0.14, -0.42, 0.28, 0.2, 0.04, 1, 1)
    c.line(-0.14, -0.32, 0.14, -0.32)
    c.setLineWidth(0.03); c.line(-0.08, -0.2, -0.05, 0.08); c.line(0.08, -0.2, 0.05, 0.08); c.line(-0.05, 0.08, 0.05, 0.08)
    c.restoreState()

def ic_dice(c, x, y, s, P):
    _start(c, x, y, s, P)
    fill(c, P["red"] if not P["bw"] else P["white"]); c.roundRect(-0.4, -0.4, 0.8, 0.8, 0.12, 1, 1)
    fill(c, P["white"] if not P["bw"] else P["ink"])
    for a, b in [(-0.2, 0.2), (0.2, 0.2), (0, 0), (-0.2, -0.2), (0.2, -0.2)]: c.circle(a, b, 0.07, 1, 0)
    c.restoreState()

def ic_rocket(c, x, y, s, P):
    _start(c, x, y, s, P)
    fill(c, P["red"]); poly(c, [(-0.15, -0.2), (-0.34, -0.42), (-0.15, -0.36)]); poly(c, [(0.15, -0.2), (0.34, -0.42), (0.15, -0.36)])
    fill(c, P["orange"]); poly(c, [(-0.1, -0.36), (0.1, -0.36), (0, -0.5)])
    fill(c, P["white"])
    p = c.beginPath(); p.moveTo(-0.17, -0.36); p.lineTo(0.17, -0.36); p.curveTo(0.24, -0.02, 0.16, 0.26, 0, 0.48)
    p.curveTo(-0.16, 0.26, -0.24, -0.02, -0.17, -0.36); p.close(); c.drawPath(p, 1, 1)
    fill(c, P["blue"]); c.circle(0, 0.08, 0.09, 1, 1)
    c.restoreState()

def ic_kite(c, x, y, s, P):
    _start(c, x, y, s, P)
    c.setLineWidth(0.03); p = c.beginPath(); p.moveTo(0, -0.22); p.curveTo(0.14, -0.3, -0.14, -0.38, 0.05, -0.5); c.drawPath(p, 1, 0)
    c.setLineWidth(0.035); fill(c, P["blue"]); poly(c, [(0, 0.48), (0.3, 0.1), (0, -0.24), (-0.3, 0.1)])
    fill(c, P["gold"]); poly(c, [(0, 0.48), (0.3, 0.1), (0, 0.1)]); poly(c, [(0, -0.24), (-0.3, 0.1), (0, 0.1)])
    c.restoreState()

def ic_book(c, x, y, s, P):
    _start(c, x, y, s, P)
    fill(c, P["green"]); poly(c, [(-0.44, -0.3), (0, -0.38), (0, 0.32), (-0.44, 0.38)]); poly(c, [(0.44, -0.3), (0, -0.38), (0, 0.32), (0.44, 0.38)])
    c.setLineWidth(0.025); stroke(c, P["white"] if not P["bw"] else P["ink"])
    for k in (0.16, 0.0, -0.14):
        c.line(-0.34, k + 0.03, -0.1, k); c.line(0.1, k, 0.34, k + 0.03)
    c.restoreState()

def ic_pencil(c, x, y, s, P):
    _start(c, x, y, s, P)
    c.rotate(0)
    fill(c, P["gold"]); c.rect(-0.11, -0.2, 0.22, 0.52, 1, 1)
    fill(c, P["red"]); c.roundRect(-0.11, 0.32, 0.22, 0.14, 0.04, 1, 1)
    fill(c, P["light"]); poly(c, [(-0.11, -0.2), (0.11, -0.2), (0, -0.46)])
    fill(c, P["ink"]); poly(c, [(-0.04, -0.37), (0.04, -0.37), (0, -0.46)])
    c.restoreState()

def ic_apple(c, x, y, s, P):
    _start(c, x, y, s, P)
    fill(c, P["red"]); p = c.beginPath(); p.moveTo(0, 0.22)
    p.curveTo(0.2, 0.36, 0.44, 0.22, 0.4, -0.06); p.curveTo(0.36, -0.34, 0.14, -0.5, 0, -0.38)
    p.curveTo(-0.14, -0.5, -0.36, -0.34, -0.4, -0.06); p.curveTo(-0.44, 0.22, -0.2, 0.36, 0, 0.22); p.close(); c.drawPath(p, 1, 1)
    c.line(0, 0.22, 0.03, 0.4)
    fill(c, P["green"]); c.ellipse(0.05, 0.3, 0.3, 0.44, 1, 1)
    c.restoreState()

def ic_fish(c, x, y, s, P):
    _start(c, x, y, s, P)
    fill(c, P["orange"]); poly(c, [(-0.22, 0), (-0.48, 0.22), (-0.48, -0.22)])
    fill(c, P["blue"]); c.ellipse(-0.32, -0.24, 0.46, 0.24, 1, 1)
    fill(c, P["white"]); c.circle(0.24, 0.06, 0.07, 1, 1)
    fill(c, P["ink"]); c.circle(0.25, 0.06, 0.025, 1, 0)
    c.restoreState()

def ic_key(c, x, y, s, P):
    _start(c, x, y, s, P)
    fill(c, P["gold"]); c.rect(-0.1, -0.05, 0.56, 0.1, 1, 1)
    c.rect(0.3, -0.2, 0.07, 0.15, 1, 1); c.rect(0.16, -0.17, 0.07, 0.12, 1, 1)
    c.circle(-0.26, 0, 0.2, 1, 1)
    fill(c, P["white"]); c.circle(-0.26, 0, 0.08, 1, 1)
    c.restoreState()

def ic_ball(c, x, y, s, P):
    _start(c, x, y, s, P)
    fill(c, P["white"]); c.circle(0, 0, 0.43, 1, 1)
    fill(c, P["red"]); 
    for a in (90, 210, 330):
        px, py = 0.25 * math.cos(math.radians(a)), 0.25 * math.sin(math.radians(a))
        c.circle(px, py, 0.11, 1, 1)
    c.restoreState()

def ic_sun(c, x, y, s, P):
    _start(c, x, y, s, P)
    c.setLineWidth(0.055); stroke(c, P["orange"] if not P["bw"] else P["ink"])
    for i in range(10):
        a = math.radians(i * 36); c.line(0.3 * math.cos(a), 0.3 * math.sin(a), 0.47 * math.cos(a), 0.47 * math.sin(a))
    c.setLineWidth(0.035); stroke(c, P["ink"]); fill(c, P["gold"]); c.circle(0, 0, 0.24, 1, 1)
    c.restoreState()

ICONS.update(bulb=ic_bulb, dice=ic_dice, rocket=ic_rocket, kite=ic_kite, book=ic_book, pencil=ic_pencil,
             apple=ic_apple, fish=ic_fish, key=ic_key, ball=ic_ball, sun=ic_sun)

def turned(c, name, x, y, s, P, how):
    c.saveState(); c.translate(x, y)
    if how == "flip": c.scale(-1, 1)
    elif how == "down": c.rotate(180)
    icon(c, name, 0, 0, s, P); c.restoreState()

# ---------- frame / helpers ----------
def frame(c, P, title, sub=None, name=True):
    stroke(c, P["ink"]); c.setLineWidth(1.5)
    fill(c, P["band"]); c.roundRect(36, H - 112, W - 72, 76, 18, stroke=1 if P["bw"] else 0, fill=1)
    sz = fit(title, "PB", 26, W - 200)
    text(c, W / 2, H - 72 if sub else H - 82, title, "PB", sz, P["bandtxt"])
    if sub: text(c, W / 2, H - 96, sub, "PM", 11.5, P["bandtxt"])
    icon(c, "bulb", 72, H - 74, 40, P); icon(c, "dice", W - 72, H - 74, 36, P)
    if name:
        text(c, 40, H - 140, "Name: ______________________________", "PM", 11, P["ink"], "l")
        text(c, W - 40, H - 140, "Date: ______________", "PM", 11, P["ink"], "r")
    text(c, W / 2, 22, "© BodhiCubs  •  Personal & classroom use  •  bodhicubs.com", "PR", 8, P["grey"])

def box(c, P, x, y, w, h, r=14, f="white"):
    stroke(c, P["ink"]); c.setLineWidth(1.5); fill(c, P[f]); c.roundRect(x, y, w, h, r, 1, 1)

# ---------- cover / info ----------
ACTIVITIES = 11
def cover(c):
    P = COLOR
    fill(c, P["light"]); c.rect(0, 0, W, H, 0, 1)
    stroke(c, P["red"]); c.setLineWidth(10); c.roundRect(20, 20, W - 40, H - 40, 26, 1, 0)
    stroke(c, P["green"]); c.setLineWidth(3); c.roundRect(34, 34, W - 68, H - 68, 20, 1, 0)
    fill(c, P["green"]); c.roundRect(W / 2 - 80, H - 98, 160, 34, 17, 0, 1)
    text(c, W / 2, H - 87, "BodhiCubs", "PB", 16, P["white"])
    icon(c, "bulb", 90, H - 82, 60, P); icon(c, "dice", W - 90, H - 82, 50, P)
    y = H - 175
    for i, ln in enumerate(["Holiday Break", "Brain Games"]):
        sz = fit(ln, "PB", 52, W - 160)
        text(c, W / 2, y, ln, "PB", sz, P["red"] if i == 0 else P["dkgreen"]); y -= sz * 1.1
    fill(c, P["gold"]); c.roundRect(W / 2 - 170, y - 10, 340, 38, 19, 0, 1)
    text(c, W / 2, y + 2, f"Ages 4–9  •  {ACTIVITIES} Screen-Free Activities", "PB", 16, P["ink"])
    y -= 70
    for i, n in enumerate(["rocket", "kite", "book", "star", "ball"]): icon(c, n, W / 2 + (i - 2) * 92, y, 74, P)
    y -= 62
    inside = ["Logic puzzles, number pyramids, secret codes", "Picture sudoku, word search and a maze",
              "Memory game, odd one out, what comes next", "Drawing challenges + brain bingo",
              "12 cut-out family game cards", "Black & white version + answer key"]
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
        ("How to use this pack", ["Pick one page a day during any school break, a rainy afternoon or a long journey.",
                                  "Younger kids (4–5): odd one out, patterns, the maze, drawing challenges and the game cards with a helper.",
                                  "Older kids (6–9): logic puzzles, number pyramids, secret codes, sudoku and word search."]),
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
    for i, n in enumerate(["star", "kite", "bulb", "rocket", "dice"]): icon(c, n, W / 2 + (i - 2) * 80, 80, 56, P)

def divider(c, title, sub, lines, P):
    frame(c, P, title, sub, name=False)
    for i, ln in enumerate(lines): instr(c, P, H / 2 + 40 - i * 30, ln, 15)
    for i, n in enumerate(["kite", "rocket", "bulb", "dice"]): icon(c, n, W / 2 + (i - 1.5) * 100, H / 2 - 110, 70, P)

# ---------- logic grids ----------
LOGIC = [
    dict(title="Puzzle 1: Who has which toy?", names=["Mia", "Leo", "Asha"], items=["kite", "ball", "book"],
         clues=["Leo does not have the kite.", "Leo does not have the ball.", "Asha does not have the ball."],
         rules=[lambda a: a["Leo"] != "kite", lambda a: a["Leo"] != "ball", lambda a: a["Asha"] != "ball"]),
    dict(title="Puzzle 2: Whose picture is whose?", names=["Sam", "Zoe", "Ravi", "Lena"], items=["apple", "fish", "dice", "rocket"],
         clues=["Zoe's picture can fly to space.", "Ravi's picture cannot swim and you cannot eat it.", "Sam's picture cannot swim."],
         rules=[lambda a: a["Zoe"] == "rocket", lambda a: a["Ravi"] not in ("fish", "apple"), lambda a: a["Sam"] != "fish"]),
]
def solve_logic(p):
    sols = []
    for perm in itertools.permutations(p["items"]):
        a = dict(zip(p["names"], perm))
        if all(r(a) for r in p["rules"]): sols.append(a)
    return sols

def p_logic(c, P):
    frame(c, P, "Logic Detective", "Use the clues to work it out!")
    instr(c, P, TOP - 16, "Read each clue. Put X for \"no\" and a circle for \"yes\" in the grid.", 12)
    y = TOP - 42
    for p in LOGIC:
        n = len(p["names"]); bh = 262 if n == 4 else 216
        box(c, P, 44, y - bh, W - 88, bh, 16, "soft")
        text(c, 62, y - 26, p["title"], "PB", 14, P["acc"], "l")
        yy = y - 54
        for i, cl in enumerate(p["clues"]):
            k = wrap(c, 62, yy, f"{i + 1}.  {cl}", "PM", 12, 220, P["ink"], 16, "l"); yy -= 16 * k + 8
        cs = 44; gx = W - 56 - cs * n; gy = y - bh + 14
        stroke(c, P["ink"]); c.setLineWidth(1.2)
        for r in range(n):
            text(c, gx - 8, gy + (n - r - 1) * cs + cs / 2 - 4, p["names"][r], "PB", 12, P["ink"], "r")
            for q in range(n):
                fill(c, P["white"]); c.rect(gx + q * cs, gy + (n - r - 1) * cs, cs, cs, 1, 1)
        for q, it in enumerate(p["items"]): icon(c, it, gx + q * cs + cs / 2, gy + n * cs + 18, 32, P)
        y -= bh + 12

# ---------- number pyramids ----------
PYR = [([3, 2, 4], {(0, 0), (1, 0), (1, 1)}), ([5, 1, 2], {(0, 0), (1, 1)}), ([2, 6, 3], {(0, 0), (1, 0), (2, 1)}),
       ([1, 2, 3, 1], {(0, 0), (1, 0), (2, 0), (2, 2)}), ([2, 1, 2, 3], {(0, 0), (1, 1), (2, 1), (3, 2)}), ([3, 2, 1, 4], {(1, 0), (2, 1), (2, 2), (3, 0)})]
def pyr_rows(base):
    rows = [base]
    while len(rows[0]) > 1: rows.insert(0, [a + b for a, b in zip(rows[0], rows[0][1:])])
    return rows
def pyr_solve(rows, hide):
    """Fill by the brick rule only: proves each puzzle can be solved with one answer."""
    g = [[None if (r, i) in hide else v for i, v in enumerate(row)] for r, row in enumerate(rows)]
    changed = True
    while changed:
        changed = False
        for r in range(len(g) - 1):
            for i in range(len(g[r])):
                t, a, b = g[r][i], g[r + 1][i], g[r + 1][i + 1]
                if t is None and None not in (a, b): g[r][i] = a + b; changed = True
                elif a is None and None not in (t, b): g[r + 1][i] = t - b; changed = True
                elif b is None and None not in (t, a): g[r + 1][i + 1] = t - a; changed = True
    return g

def p_pyramids(c, P):
    frame(c, P, "Number Pyramids", "Add and take away")
    instr(c, P, TOP - 16, "Each brick is the sum of the two bricks under it. Fill in the empty bricks!", 12)
    for i, (base, hide) in enumerate(PYR):
        rows = pyr_rows(base); bw, bh = 56, 34
        cx = W / 2 + (-132 if i % 2 == 0 else 132); ytop = TOP - 60 - (i // 2) * 186
        text(c, cx - 112, ytop + 2, f"{i + 1}.", "PB", 14, P["acc"], "l")
        for r, row in enumerate(rows):
            for k, v in enumerate(row):
                x = cx + (k - len(row) / 2) * bw; y = ytop - (r + 1) * bh
                stroke(c, P["ink"]); c.setLineWidth(1.4); fill(c, P["white"] if (r, k) in hide else P["soft"]); c.rect(x, y, bw, bh, 1, 1)
                if (r, k) not in hide: text(c, x + bw / 2, y + 11, str(v), "PB", 15, P["ink"])

# ---------- odd one out + patterns ----------
ODD = [("rocket", 3, "down"), ("pencil", 1, "down"), ("fish", 4, "flip"), ("key", 2, "flip")]
PATS = [(["sun", "apple", "sun", "apple", "sun"], "apple"), (["kite", "kite", "ball", "kite", "kite"], "ball"),
        (["star", "dice", "book", "star", "dice"], "book")]
NUMS = [([2, 4, 6, 8], 10, "2, 4, 6, 8, ___"), ([5, 10, 15, 20], 25, "5, 10, 15, 20, ___"), ([20, 18, 16, 14], 12, "20, 18, 16, 14, ___")]
def p_odd(c, P):
    frame(c, P, "Odd One Out & What Comes Next", "Look closely!")
    text(c, 50, TOP - 18, "A.  One picture is turned the other way. Circle it!", "PB", 13, P["acc"], "l")
    for i, (n, odd, how) in enumerate(ODD):
        y = TOP - 62 - i * 64
        for k in range(5):
            x = 110 + k * 88
            if k == odd: turned(c, n, x, y, 52, P, how)
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

# ---------- sudoku ----------
SYMS = ["bulb", "dice", "rocket", "star"]
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

# ---------- memory ----------
TRAY = [["star", "kite", "apple", "key"], ["ball", "star", "fish", "book"], ["apple", "pencil", "star", "sun"]]
MEM_Q = [("Was there a rocket?", "No"), ("Was there a kite?", "Yes"), ("How many stars?", "3"),
         ("How many apples?", "2"), ("What was in the top left corner?", "A star"), ("What was in the bottom right corner?", "A sun")]
def p_memory(c, P):
    frame(c, P, "Super Memory Game", "Train your brain")
    instr(c, P, TOP - 16, "Look at the pictures for 30 seconds. Then fold the page on the dotted line", 12)
    instr(c, P, TOP - 32, "(or ask a helper to cover them) and answer the questions.", 12)
    cs = 88; gx = (W - 4 * cs) / 2; gy = TOP - 52 - 3 * cs
    box(c, P, gx - 8, gy - 8, 4 * cs + 16, 3 * cs + 16, 16, "soft")
    for r, row in enumerate(TRAY):
        for k, n in enumerate(row): icon(c, n, gx + (k + .5) * cs, gy + (2.5 - r) * cs, 64, P)
    fy = gy - 24
    c.saveState(); stroke(c, P["ink"]); c.setLineWidth(1); c.setDash(5, 4); c.line(40, fy, W - 40, fy); c.restoreState()
    text(c, W / 2, fy + 4, "fold here", "PR", 9, P["grey"])
    for i, (q, _) in enumerate(MEM_Q):
        y = fy - 34 - i * 38
        text(c, 60, y, f"{i + 1}.  {q}", "PM", 13, P["ink"], "l")
        stroke(c, P["ink"]); c.setLineWidth(0.9); c.line(370, y - 2, W - 60, y - 2)

# ---------- maze ----------
def mk_maze(seed):
    m = make_maze(10, 12, seed)
    def page(c, P):
        frame(c, P, "Rocket Maze", "Find the way")
        instr(c, P, TOP - 18, "Fly the rocket to the star. Do not cross any lines!")
        draw_maze(c, P, m, 70, 96, W - 140, TOP - 196, icons=("rocket", "star"))
    def mini(c, P, x, y, s): draw_maze(c, P, m, x, y, s, s, answers=True, icons=None, lw=1.1)
    return page, mini, m

# ---------- word search ----------
WORDS = ["BRAIN", "CLUES", "FAMILY", "FOCUS", "GAMES", "LOGIC", "MAZE", "MEMORY", "PUZZLE", "RIDDLE", "SMART", "THINK"]
def mk_ws(seed):
    g, placed = make_wordsearch(WORDS, 12, [(0, 1), (1, 0), (1, 1)], seed)
    def page(c, P):
        frame(c, P, "Brain Word Search", "12 x 12  •  across, down, diagonal")
        instr(c, P, TOP - 18, "Find and circle each word. Check it off the list!")
        size = 372; x = (W - size) / 2; y = TOP - 48 - size
        draw_wordsearch(c, P, g, placed, x, y, size)
        for i, w in enumerate(WORDS):
            col, row = divmod(i, 4); xx = 90 + col * 160; yy = y - 40 - row * 22
            stroke(c, P["ink"]); c.setLineWidth(1.2); fill(c, P["white"]); c.rect(xx, yy - 2, 12, 12, 1, 1)
            text(c, xx + 20, yy, w, "PM", 12.5, P["ink"], "l")
    def mini(c, P, x, y, s): draw_wordsearch(c, P, g, placed, x, y, s, answers=True)
    return page, mini, g, placed

# ---------- secret code ----------
MESSAGES = ["YOU ARE SMART", "KEEP ON TRYING", "BRAINS LOVE FUN", "PLAY WITH FAMILY"]
def encode(m): return [None if ch == " " else ord(ch) - 64 for ch in m]
def decode(nums): return "".join(" " if n is None else chr(n + 64) for n in nums)
def p_code(c, P):
    frame(c, P, "Secret Code Messages", "Be a code breaker")
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

# ---------- drawing ----------
def starter(c, P, kind, cx, cy):
    stroke(c, P["ink"]); c.setLineWidth(2.2); c.setLineCap(1)
    if kind == "circle": c.circle(cx, cy, 24, 1, 0)
    elif kind == "zigzag":
        p = c.beginPath(); p.moveTo(cx - 36, cy - 8)
        for i in range(1, 6): p.lineTo(cx - 36 + i * 14, cy + (10 if i % 2 else -8))
        c.drawPath(p, 1, 0)
    elif kind == "dots":
        fill(c, P["ink"]); c.circle(cx - 18, cy, 4, 1, 0); c.circle(cx + 18, cy, 4, 1, 0)
def p_draw(c, P):
    frame(c, P, "Drawing Challenges", "Use your imagination!")
    cards = [("Turn this circle into something funny.", "circle"), ("A new animal: half fish, half cat!", None),
             ("Turn this zigzag into a picture.", "zigzag"), ("A robot that helps at home.", None),
             ("Turn these 2 dots into a face or a creature.", "dots"), ("Your own invention for a long journey.", None)]
    w, h = 255, 180
    for i, (t, st) in enumerate(cards):
        col, row = i % 2, i // 2; x = 44 + col * (w + 14); y = TOP - 16 - (row + 1) * (h + 14)
        box(c, P, x, y, w, h)
        text(c, x + w / 2, y + h - 22, t, "PB", fit(t, "PB", 11.5, w - 20), P["acc"])
        if st: starter(c, P, st, x + w / 2, y + (h - 30) / 2)

# ---------- bingo ----------
BINGO = ["Tell a riddle", "Build a tower of 10 things", "Count back from 20", "Draw with your other hand",
         "Stand on one foot for 20 seconds", "Teach someone a game", "Invent a secret handshake", "Read a story out loud",
         "Make up a joke", "Fold a paper plane", "Spell your name backwards", "Find 5 round things",
         "Make a shadow animal", "Hum a song for others to guess", "Name 5 animals fast", "Solve one puzzle in this pack"]
def p_bingo(c, P):
    frame(c, P, "Brain Bingo Challenge", "Screen-free fun")
    instr(c, P, TOP - 18, "Do a challenge, then color the square. Can you get 4 in a row?")
    cs = 126; x0 = (W - 4 * cs) / 2; ytop = TOP - 34
    for i, t in enumerate(BINGO):
        col, row = i % 4, i // 4; x = x0 + col * cs; y = ytop - (row + 1) * cs
        stroke(c, P["ink"]); c.setLineWidth(1.5); fill(c, P["white"]); c.rect(x, y, cs, cs, 1, 1)
        icon(c, ["star", "bulb", "kite", "dice"][(row + col) % 4], x + cs / 2, y + cs - 30, 36, P)
        wrap(c, x + cs / 2, y + cs - 66, t, "PM", 11, cs - 16, P["ink"], 14)

# ---------- family game cards ----------
GAMES = [("Story Chain", "Each person adds one sentence to a silly story."),
         ("20 Questions", "Think of a thing. Others ask yes or no questions to guess it."),
         ("Rhyme Time", "Say a word. Take turns saying words that rhyme with it."),
         ("Alphabet Trip", "\"I packed an apple.\" Next: A + something with B. Keep going!"),
         ("Copy My Clap", "Clap a pattern. Others copy it. Make it longer each time."),
         ("Category Race", "Pick a topic, like fruits. Take turns naming one. No repeats!"),
         ("What's Missing?", "Put 6 things on a table. Look, close eyes, take one away. Guess!"),
         ("Would You Rather", "Ask a funny \"would you rather\" question. Everyone says why."),
         ("Statues", "Dance around. When the music stops, freeze like a statue!"),
         ("Two True, One Not", "Say 3 things about you. Others guess which one is not true."),
         ("Mirror Moves", "Face a partner and copy every move, slowly, like a mirror."),
         ("Guess the Sound", "Close your eyes. A helper makes a sound with an object. Guess it!")]
def p_cards(c, P):
    frame(c, P, "Family Game Cards", "Cut out, pick one, play!", name=False)
    w, h = 170, 150; x0 = (W - 3 * w) / 2; ytop = H - 124
    c.saveState(); stroke(c, P["grey"]); c.setLineWidth(1); c.setDash(4, 4)
    for i in range(4): c.line(x0 + i * w, ytop, x0 + i * w, ytop - 4 * h)
    for i in range(5): c.line(x0, ytop - i * h, x0 + 3 * w, ytop - i * h)
    c.restoreState()
    for i, (t, d) in enumerate(GAMES):
        col, row = i % 3, i // 3; x = x0 + col * w; y = ytop - (row + 1) * h
        icon(c, ["dice", "star", "bulb", "kite"][i % 4], x + w / 2, y + h - 28, 34, P)
        text(c, x + w / 2, y + h - 66, t, "PB", fit(t, "PB", 13, w - 20), P["acc"])
        wrap(c, x + w / 2, y + h - 86, d, "PR", 10.5, w - 22, P["ink"], 13.5)

# ---------- answers ----------
def p_answers_text(c, P):
    frame(c, P, "Answer Key", "Logic, numbers, patterns, code, memory", name=False)
    left = [("Logic Detective", [f"Puzzle {i + 1}: " + ", ".join(f"{k}: {v}" for k, v in solve_logic(p)[0].items()) for i, p in enumerate(LOGIC)]),
            ("Number Pyramids", [f"{i + 1}.  " + "  |  ".join(" ".join(str(v) for v in row) for row in pyr_rows(b)) for i, (b, _) in enumerate(PYR)])]
    right = [("Odd One Out", [f"Row {i + 1}: picture {o + 1}" for i, (_, o, _h) in enumerate(ODD)]),
             ("What Comes Next", [f"{i + 1}.  {a}" for i, (_, a) in enumerate(PATS)] + [f"{i + 4}.  {a}" for i, (_, a, _s) in enumerate(NUMS)]),
             ("Secret Code", [f"{i + 1}.  {m}" for i, m in enumerate(MESSAGES)]),
             ("Super Memory Game", [f"{i + 1}.  {a}" for i, (_, a) in enumerate(MEM_Q)])]
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
        for i, (t, m) in enumerate([("Word Search", ws_mini), ("Rocket Maze", maze_mini)]):
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
    for p in LOGIC:
        sols = solve_logic(p); assert len(sols) == 1, (p["title"], sols); print(p["title"], sols[0])
    for base, hide in PYR:
        rows = pyr_rows(base); assert pyr_solve(rows, hide) == rows, base
        assert max(max(r) for r in rows) <= 20
    for m in MESSAGES: assert decode(encode(m)) == m
    assert PATS[0][1] == "apple" and PATS[1][0][:3] == PATS[1][0][3:] + [PATS[1][1]] and PATS[2][0][:2] == PATS[2][0][3:]
    flat = sum(TRAY, []); assert flat.count("star") == 3 and flat.count("apple") == 2 and "rocket" not in flat and "kite" in flat
    assert TRAY[0][0] == "star" and TRAY[2][3] == "sun"
    for seq, ans, _ in NUMS: assert seq[1] - seq[0] == seq[3] - seq[2] == ans - seq[3]
    print("verify OK")

def run():
    os.makedirs(OUT, exist_ok=True)
    ws, ws_mini, g, placed = mk_ws(3101)
    mz, mz_mini, maze = mk_maze(3102)
    sd, sd_mini, puz = mk_sudoku([3103, 3104, 3105, 3106], 8)
    verify((g, placed), maze, puz)
    pages = [p_logic, p_pyramids, p_odd, sd, p_memory, mz, ws, p_code, p_draw, p_bingo, p_cards]
    assert len(pages) == ACTIVITIES
    c = canvas.Canvas(os.path.join(OUT, PDF), pagesize=letter)
    c.setTitle("Holiday Break Brain Games for Kids – Free Printable Pack"); c.setAuthor("BodhiCubs")
    cover(c); c.showPage(); thanks(c); c.showPage()
    for p in pages: p(c, COLOR); c.showPage()
    divider(c, "Black & White Version", "Printer-friendly", [f"The same {ACTIVITIES} pages in black & white.", "Kids can color them in too!"], BW); c.showPage()
    for p in pages: p(c, BW); c.showPage()
    divider(c, "Answer Key", "For grown-ups", ["Answers for the puzzles, numbers,", "code and memory pages."], COLOR); c.showPage()
    p_answers_text(c, COLOR); c.showPage()
    answer_puzzles(ws_mini, mz_mini)(c, COLOR); c.showPage()
    answer_sudoku(sd_mini, len(puz))(c, COLOR); c.showPage()
    c.save(); print("saved", os.path.join(OUT, PDF))

if __name__ == "__main__":
    run()
