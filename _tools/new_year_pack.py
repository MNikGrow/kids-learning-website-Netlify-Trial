"""BodhiCubs monthly pack: New Year Fun for Kids (built 2026-10-27).
Run: python3 _tools/new_year_pack.py <out_dir>
"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reportlab.pdfgen import canvas
from printables_lib import *
from printables_lib import _start, _count

OUT = sys.argv[1] if len(sys.argv) > 1 else "out/"
PDF = "BodhiCubs_New_Year_Fun_Pack_Ages4-9.pdf"
YEAR = "2027"
COLOR["purple"] = (0.45, 0.3, 0.75); BW["purple"] = (1, 1, 1)
COLOR["pink"] = (0.96, 0.45, 0.6); BW["pink"] = (1, 1, 1)

# ---------- New Year icons (unit box -0.5..0.5) ----------
def ic_firework(c, x, y, s, P):
    _start(c, x, y, s, P)
    cols = ["red", "gold", "blue", "green", "purple", "orange"]
    for i in range(12):
        a = math.radians(i * 30); ca, sa = math.cos(a), math.sin(a)
        c.setLineWidth(0.075 if not P["bw"] else 0.05)
        stroke(c, P["ink"] if P["bw"] else P[cols[i % 6]])
        c.line(0.12 * ca, 0.12 * sa, 0.38 * ca, 0.38 * sa)
        fill(c, P["ink"] if P["bw"] else P[cols[i % 6]])
        c.circle(0.45 * ca, 0.45 * sa, 0.04, 1, 0)
    fill(c, P["gold"]); stroke(c, P["ink"]); c.setLineWidth(0.035); c.circle(0, 0, 0.09, 1, 1)
    c.restoreState()

def ic_partyhat(c, x, y, s, P):
    _start(c, x, y, s, P)
    fill(c, P["purple"]); poly(c, [(-0.3, -0.42), (0.3, -0.42), (0, 0.3)])
    c.setLineWidth(0.06); stroke(c, P["gold"] if not P["bw"] else P["ink"])
    c.line(-0.2, -0.18, 0.2, -0.18); c.line(-0.1, 0.06, 0.1, 0.06)
    stroke(c, P["ink"]); c.setLineWidth(0.035)
    fill(c, P["gold"]); c.circle(0, 0.36, 0.09, 1, 1)
    fill(c, P["red"]); c.roundRect(-0.36, -0.48, 0.72, 0.1, 0.04, 1, 1)
    c.restoreState()

def ic_clock(c, x, y, s, P):
    _start(c, x, y, s, P)
    fill(c, P["gold"]); c.circle(0, 0, 0.46, 1, 1)
    fill(c, P["white"]); c.circle(0, 0, 0.36, 1, 1)
    c.setLineWidth(0.04)
    for i in range(12):
        a = math.radians(90 - i * 30); r1 = 0.28 if i % 3 else 0.24
        c.line(r1 * math.cos(a), r1 * math.sin(a), 0.33 * math.cos(a), 0.33 * math.sin(a))
    c.setLineWidth(0.06); c.line(0, 0, 0, 0.25); c.line(0, 0, -0.03, 0.17)
    fill(c, P["red"]); c.circle(0, 0, 0.05, 1, 1)
    c.restoreState()

def ic_balloon(c, x, y, s, P):
    _start(c, x, y, s, P)
    c.setLineWidth(0.03)
    p = c.beginPath(); p.moveTo(0, -0.2); p.curveTo(0.08, -0.3, -0.08, -0.38, 0.02, -0.5); c.drawPath(p, 1, 0)
    c.setLineWidth(0.035)
    fill(c, P["red"]); c.ellipse(-0.28, -0.18, 0.28, 0.48, 1, 1)
    poly(c, [(0, -0.17), (-0.06, -0.25), (0.06, -0.25)])
    fill(c, P["white"]); c.setLineWidth(0.0001); c.ellipse(-0.17, 0.2, -0.08, 0.36, 1, 0)
    c.restoreState()

def ic_heart(c, x, y, s, P):
    _start(c, x, y, s, P)
    fill(c, P["pink"])
    p = c.beginPath(); p.moveTo(0, -0.42)
    p.curveTo(-0.2, -0.24, -0.48, -0.06, -0.46, 0.14); p.curveTo(-0.44, 0.42, -0.08, 0.46, 0, 0.2)
    p.curveTo(0.08, 0.46, 0.44, 0.42, 0.46, 0.14); p.curveTo(0.48, -0.06, 0.2, -0.24, 0, -0.42)
    p.close(); c.drawPath(p, 1, 1)
    c.restoreState()

def ic_calendar(c, x, y, s, P):
    _start(c, x, y, s, P)
    fill(c, P["white"]); c.roundRect(-0.4, -0.42, 0.8, 0.76, 0.08, 1, 1)
    fill(c, P["red"]); c.roundRect(-0.4, 0.14, 0.8, 0.2, 0.06, 1, 1)
    fill(c, P["ink"]); c.roundRect(-0.25, 0.26, 0.07, 0.18, 0.03, 1, 0); c.roundRect(0.18, 0.26, 0.07, 0.18, 0.03, 1, 0)
    c.setFont("PB", 0.42); fill(c, P["ink"]); c.drawCentredString(0, -0.29, "1")
    c.restoreState()

ICONS.update(firework=ic_firework, partyhat=ic_partyhat, clock=ic_clock, balloon=ic_balloon,
             heart=ic_heart, calendar=ic_calendar)
NAMES.update(firework="firework", partyhat="party hat", clock="clock", balloon="balloon", heart="heart", calendar="calendar")
TYPES = ["firework", "partyhat", "clock", "balloon", "star", "heart", "calendar"]

# ---------- page frame (theme icons + required footer) ----------
def frame(c, P, title, sub=None, name=True):
    stroke(c, P["ink"]); c.setLineWidth(1.5)
    fill(c, P["band"]); c.roundRect(36, H - 112, W - 72, 76, 18, stroke=1 if P["bw"] else 0, fill=1)
    sz = fit(title, "PB", 26, W - 200)
    text(c, W / 2, H - 72 if sub else H - 82, title, "PB", sz, P["bandtxt"])
    if sub: text(c, W / 2, H - 96, sub, "PM", 11.5, P["bandtxt"])
    icon(c, "star", 70, H - 74, 34, P); icon(c, "firework", W - 70, H - 74, 38, P)
    if name:
        text(c, 40, H - 140, "Name: ______________________________", "PM", 11, P["ink"], "l")
        text(c, W - 40, H - 140, "Date: ______________", "PM", 11, P["ink"], "r")
    text(c, W / 2, 22, "© BodhiCubs  •  Personal & classroom use  •  bodhicubs.com", "PR", 8, P["grey"])

def box(c, P, x, y, w, h, r=14, f="white"):
    stroke(c, P["ink"]); c.setLineWidth(1.5); fill(c, P[f]); c.roundRect(x, y, w, h, r, 1, 1)

# ---------- cover / info pages ----------
def cover(c):
    P = COLOR
    fill(c, P["light"]); c.rect(0, 0, W, H, 0, 1)
    stroke(c, P["red"]); c.setLineWidth(10); c.roundRect(20, 20, W - 40, H - 40, 26, 1, 0)
    stroke(c, P["green"]); c.setLineWidth(3); c.roundRect(34, 34, W - 68, H - 68, 20, 1, 0)
    fill(c, P["green"]); c.roundRect(W / 2 - 80, H - 98, 160, 34, 17, 0, 1)
    text(c, W / 2, H - 87, "BodhiCubs", "PB", 16, P["white"])
    for (fx, fy, fs) in [(90, H - 80, 54), (W - 90, H - 80, 54)]:
        icon(c, "firework", fx, fy, fs, P)
    y = H - 175
    for i, ln in enumerate(["New Year Fun", "for Kids"]):
        sz = fit(ln, "PB", 52, W - 220)
        text(c, W / 2, y, ln, "PB", sz, P["red"] if i == 0 else P["dkgreen"]); y -= sz * 1.1
    fill(c, P["gold"]); c.roundRect(W / 2 - 160, y - 10, 320, 38, 19, 0, 1)
    text(c, W / 2, y + 2, "Ages 4–9  •  10 Activity Pages", "PB", 16, P["ink"])
    y -= 70
    ics = ["balloon", "partyhat", "clock", "star", "calendar"]
    for i, n in enumerate(ics): icon(c, n, W / 2 + (i - 2) * 92, y, 74, P)
    y -= 66
    inside = ["My New Year goals + my year in review", "Count, add & countdown math (ages 4–7)",
              "Word search, 2 mazes, picture sudoku", "12 kindness resolutions (one per month)",
              "Black & white version + answer key"]
    bh = 50 + 26 * len(inside)
    box(c, P, 80, y - bh, W - 160, bh, 16)
    text(c, W / 2, y - 26, "What's inside", "PB", 16, P["dkgreen"])
    for i, it in enumerate(inside): text(c, 115, y - 54 - i * 26, "•  " + it, "PM", 13, P["ink"], "l")
    text(c, W / 2, 62, "Free printable  •  Color + Black & White  •  Answer Key", "PM", 12, P["ink"])

def thanks(c):
    P = COLOR; frame(c, P, "Hello, grown-ups!", "Read this before printing", name=False)
    lines = [
        ("Printing tips", ["Choose \"Fit to page\" in your print settings. The pages work on US Letter and A4 paper.",
                           "Low on color ink? The black & white version starts after the color pages.",
                           "Answers for the math and puzzles are at the very end."]),
        ("How to use this pack", ["Pick one page a day over the holidays, or use them in class in the first week of January.",
                                  "Younger kids (4–5): counting, mazes, coloring. Older kids (6–9): word search, sudoku, goals.",
                                  "The goals and kindness pages are great to talk about together as a family."]),
        ("You may", ["Print as many copies as you need for your own family or classroom."]),
        ("Please don't", ["Sell or re-upload these files. Share the link bodhicubs.com/printables instead. Thank you!"]),
        ("More free fun", ["Play free science games, Brain Gym and puzzles at bodhicubs.com"]),
    ]
    y = TOP + 20
    for head, items in lines:
        text(c, 70, y, head, "PB", 17, P["acc"], "l"); y -= 26
        for it in items:
            n = wrap(c, 90, y, "•  " + it, "PR", 12.5, W - 170, P["ink"], 17, "l"); y -= 17 * n + 6
        y -= 12
    for i, n in enumerate(["star", "balloon", "firework", "partyhat", "heart"]):
        icon(c, n, W / 2 + (i - 2) * 80, 90, 56, P)

def divider(c, title, sub, lines, P):
    frame(c, P, title, sub, name=False)
    for i, ln in enumerate(lines): instr(c, P, H / 2 + 40 - i * 30, ln, 15)
    for i, n in enumerate(["balloon", "partyhat", "clock", "firework"]):
        icon(c, n, W / 2 + (i - 1.5) * 100, H / 2 - 110, 70, P)

# ---------- activity pages ----------
def p_goals(c, P):
    frame(c, P, f"My New Year Goals {YEAR}", "Dream big!")
    prompts = ["Something new I want to learn...", "A book I want to read...", "Someone I want to help...",
               "A healthy habit I will try...", "A skill I want to practice...", "I will be proud of myself when..."]
    ics = ["star", "calendar", "heart", "balloon", "clock", "firework"]
    for i, p in enumerate(prompts):
        col, row = i % 2, i // 2; w, h = 255, 172; x = 44 + col * (w + 14); y = TOP - 20 - (row + 1) * (h + 14)
        box(c, P, x, y, w, h)
        icon(c, ics[i], x + 24, y + h - 24, 30, P)
        text(c, x + 46, y + h - 30, p, "PB", fit(p, "PB", 12, w - 56), P["ink"], "l")
        stroke(c, P["ink"])
        for k in range(3): c.setLineWidth(0.8); c.line(x + 16, y + h - 72 - k * 32, x + w - 16, y + h - 72 - k * 32)

def p_review(c, P):
    frame(c, P, "My Year in Review", "Remember the best bits!")
    prompts = ["My favorite day this year was...", "Something new I learned...", "My best friend is...",
               "A book or game I loved...", "Something I did that was hard...", "I am thankful for..."]
    ics = ["star", "clock", "heart", "calendar", "firework", "balloon"]
    for i, p in enumerate(prompts):
        col, row = i % 2, i // 2; w, h = 255, 116; x = 44 + col * (w + 14); y = TOP - 14 - (row + 1) * (h + 12)
        box(c, P, x, y, w, h)
        icon(c, ics[i], x + 22, y + h - 22, 26, P)
        text(c, x + 42, y + h - 27, p, "PB", fit(p, "PB", 11.5, w - 52), P["ink"], "l")
        stroke(c, P["ink"])
        for k in range(2): c.setLineWidth(0.8); c.line(x + 16, y + h - 62 - k * 30, x + w - 16, y + h - 62 - k * 30)
    y = TOP - 14 - 3 * 128 - 18
    box(c, P, 44, 44, W - 88, y - 44, f="soft")
    text(c, W / 2, y - 24, "Draw your happiest moment of the year!", "PB", 13, P["ink"])

def mk_count(seed):
    rng = random.Random(seed); types = ["balloon", "partyhat", "star", "clock"]
    counts = {t: rng.randint(3, 9) for t in types}
    pts = scatter(rng, counts, (60, 240, W - 60, TOP - 50), 46)
    def page(c, P):
        frame(c, P, "Party Count & Write", "Counting to 10")
        instr(c, P, TOP - 18, "Count each picture. Write the number in the box.")
        box(c, P, 48, 228, W - 96, TOP - 266, 18, "soft")
        for x, y, t in pts: icon(c, t, x, y, 46, P)
        gap = (W - 100) / 4
        for i, t in enumerate(types):
            cx = 50 + gap * (i + .5); icon(c, t, cx - 34, 150, 50, P); answer_box(c, P, cx + 2, 128, 52, 44)
    return page, [f"{NAMES[t]}: {counts[t]}" for t in types], counts, pts

def group(c, P, name, n, x, y, s=25, per=5):
    for i in range(n):
        r, cc = divmod(i, per); icon(c, name, x + cc * (s + 3) + s / 2, y - r * (s + 4), s, P)

def mk_add(seed):
    rng = random.Random(seed); probs = []
    while len(probs) < 6:
        a, b = rng.randint(1, 5), rng.randint(1, 5)
        if (a, b) not in [(p[0], p[1]) for p in probs]: probs.append((a, b, rng.choice(TYPES)))
    def page(c, P):
        frame(c, P, "New Year Picture Addition", "Adding up to 10")
        instr(c, P, TOP - 18, "Count the pictures. Add them together. Write the answer.")
        for i, (a, b, t) in enumerate(probs):
            y = TOP - 90 - i * 78
            text(c, 56, y - 6, f"{i + 1}.", "PB", 15, P["acc"], "l")
            group(c, P, t, a, 82, y); text(c, 240, y - 10, "+", "PB", 30, P["ink"])
            group(c, P, t, b, 266, y); text(c, 432, y - 10, "=", "PB", 30, P["ink"])
            answer_box(c, P, 462, y - 22, 60, 46)
    return page, [f"{i + 1}.  {a} + {b} = {a + b}" for i, (a, b, t) in enumerate(probs)], probs

def mk_countdown(seed):
    rng = random.Random(seed)
    specs = [(10, 1, 11, "Count down by 1s"), (20, 1, 11, "Count down by 1s"), (20, 2, 11, "Count down by 2s"),
             (50, 5, 11, "Count down by 5s"), (100, 10, 11, "Count down by 10s"), (15, 1, 11, "Count down by 1s")]
    rows = []
    for st, step, n, lab in specs:
        seq = [st - k * step for k in range(n)]
        hide = sorted(rng.sample(range(1, n - 1), 4))
        rows.append((seq, hide, lab))
    def page(c, P):
        frame(c, P, "New Year Countdown!", "Missing numbers")
        instr(c, P, TOP - 18, "It's almost midnight! Fill in the missing numbers.")
        for i, (seq, hide, lab) in enumerate(rows):
            y = TOP - 92 - i * 86
            text(c, 50, y + 22, f"{i + 1}. {lab}", "PB", 12.5, P["acc"], "l")
            cw = (W - 100) / len(seq)
            for j, v in enumerate(seq):
                x = 50 + j * cw
                if j in hide: answer_box(c, P, x + 2, y - 26, cw - 6, 38)
                else:
                    box(c, P, x + 2, y - 26, cw - 6, 38, 8, "soft")
                    text(c, x + cw / 2 - 1, y - 13, str(v), "PB", 15, P["ink"])
    ans = [f"{i + 1}.  " + ", ".join(str(seq[j]) for j in hide) for i, (seq, hide, lab) in enumerate(rows)]
    return page, ans, rows

WORDS = ["CALENDAR", "CHEER", "CLOCK", "COUNTDOWN", "DREAM", "FIREWORKS", "FRIENDS", "GOALS",
         "HOPE", "JANUARY", "MIDNIGHT", "PARTY"]
def mk_ws(seed):
    g, placed = make_wordsearch(WORDS, 12, [(0, 1), (1, 0), (1, 1)], seed)
    def page(c, P):
        frame(c, P, "New Year Word Search", "12 x 12  •  across, down, diagonal")
        instr(c, P, TOP - 18, "Find and circle each word. Check it off the list!")
        size = 372; x = (W - size) / 2; y = TOP - 48 - size
        draw_wordsearch(c, P, g, placed, x, y, size)
        ws = sorted(WORDS); per = 4
        for i, w in enumerate(ws):
            col, row = divmod(i, per); xx = 90 + col * 160; yy = y - 40 - row * 22
            stroke(c, P["ink"]); c.setLineWidth(1.2); fill(c, P["white"]); c.rect(xx, yy - 2, 12, 12, 1, 1)
            text(c, xx + 20, yy, w, "PM", 12.5, P["ink"], "l")
    def mini(c, P, x, y, s): draw_wordsearch(c, P, g, placed, x, y, s, answers=True)
    return page, mini, g, placed

def mk_maze(seed, title, sub, w, h, ins, icons):
    m = make_maze(w, h, seed)
    def page(c, P):
        frame(c, P, title, sub); instr(c, P, TOP - 18, ins)
        draw_maze(c, P, m, 70, 100, W - 140, TOP - 210, icons=icons)
    def mini(c, P, x, y, s): draw_maze(c, P, m, x, y, s, s, answers=True, icons=None, lw=1.1)
    return page, mini, m

SYMS = ["balloon", "partyhat", "clock", "star"]
def mk_sudoku(seeds, givens=8):
    puz = [make_sudoku(s, givens) for s in seeds]
    def page(c, P):
        frame(c, P, "Party Picture Sudoku", "4 x 4 logic puzzles")
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

KIND = ["Smile and say hello to someone new", "Help cook or set the table", "Make a card for a friend",
        "Share a favorite toy or book", "Help tidy up without being asked", "Give 3 kind compliments",
        "Water a plant or feed the birds", "Read a story to someone younger", "Say thank you to a helper",
        "Call or draw for a grandparent", "Pick up litter with a grown-up", "Do something kind for yourself!"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]
def p_kind(c, P):
    frame(c, P, "12 Kindness Resolutions", "One kind act for every month")
    instr(c, P, TOP - 18, "Do the kind act, then color the heart. How many can you do?")
    w, h = 170, 138; x0 = (W - 3 * w) / 2
    P2 = dict(P); P2["pink"] = (1, 1, 1)
    for i, k in enumerate(KIND):
        col, row = i % 3, i // 3; x = x0 + col * w + 5; y = TOP - 40 - (row + 1) * h
        box(c, P, x, y + 5, w - 10, h - 10)
        text(c, x + (w - 10) / 2, y + h - 26, MONTHS[i], "PB", 11, P["acc"])
        icon(c, "heart", x + (w - 10) / 2, y + h - 58, 44, P2)
        wrap(c, x + (w - 10) / 2, y + 42, k, "PM", 10.5, w - 30, P["ink"], 13)

# ---------- answer pages ----------
def answer_text(blocks):
    def page(c, P):
        frame(c, P, "Answer Key", "Math pages", name=False)
        y = TOP + 10
        for head, lines in blocks:
            text(c, 70, y, head, "PB", 14, P["acc"], "l"); y -= 22
            for ln in lines: text(c, 84, y, ln, "PR", 12, P["ink"], "l"); y -= 18
            y -= 14
    return page

def answer_puzzles(ws_mini, maze_minis):
    def page(c, P):
        frame(c, P, "Answer Key", "Word search & mazes", name=False)
        s = 236
        items = [("Word Search", ws_mini), ("Maze 1: Easy", maze_minis[0]), ("Maze 2: Tricky", maze_minis[1])]
        for i, (t, m) in enumerate(items):
            col, row = i % 2, i // 2
            x = 56 + col * (s + 64); y = TOP - 40 - (row + 1) * (s + 50) + 30
            text(c, x + s / 2, y + s + 16, t, "PB", 12, P["acc"]); m(c, P, x, y, s)
    return page

def answer_sudoku(mini, n):
    def page(c, P):
        frame(c, P, "Answer Key", "Party Picture Sudoku", name=False)
        s = 200
        for i in range(n):
            col, row = i % 2, i // 2
            x = 90 + col * (s + 50); y = TOP - 50 - (row + 1) * (s + 50) + 20
            text(c, x + s / 2, y + s + 10, f"Puzzle {i + 1}", "PB", 12, P["acc"]); mini(c, P, i, x, y, s)
    return page

# ---------- verification ----------
def verify(ws, mazes, puz, counts, pts, add, cd):
    g, placed = ws; n = len(g)
    for w, r, cc, dr, dc in placed:
        assert "".join(g[r + dr * i][cc + dc * i] for i in range(len(w))) == w, w
    assert sorted(p[0] for p in placed) == sorted(WORDS)
    for m in mazes:
        path = m["path"]; assert path[0] == (0, 0) and path[-1] == (m["h"] - 1, m["w"] - 1)
        D = {(-1, 0): "N", (1, 0): "S", (0, 1): "E", (0, -1): "W"}
        for a, b in zip(path, path[1:]): assert D[(b[0] - a[0], b[1] - a[1])] not in m["walls"][a]
    for p, s in puz:
        assert _count(p[:], 3) == 1
        assert all(p[i] is None or p[i] == s[i] for i in range(16))
        for k in range(4):
            assert len({s[k * 4 + j] for j in range(4)}) == 4 and len({s[j * 4 + k] for j in range(4)}) == 4
    for t, k in counts.items(): assert sum(1 for *_, it in pts if it == t) == k
    for a, b, _ in add: assert a + b <= 10
    print("verify OK: words", len(placed), "mazes", len(mazes), "sudoku", len(puz))

def run():
    os.makedirs(OUT, exist_ok=True)
    cnt, a_cnt, counts, pts = mk_count(2027)
    add, a_add, probs = mk_add(2028)
    cd, a_cd, rows = mk_countdown(2029)
    ws, ws_mini, g, placed = mk_ws(2030)
    m1, mm1, maze1 = mk_maze(2031, "Balloon Maze", "Maze 1: Easy", 8, 10, "Help the balloon float to the party hat!", ("balloon", "partyhat"))
    m2, mm2, maze2 = mk_maze(2032, "Midnight Maze", "Maze 2: Tricky", 13, 16, "Find the way to the clock before midnight!", ("star", "clock"))
    sd, sd_mini, puz = mk_sudoku([2033, 2034, 2035, 2036], 8)
    verify((g, placed), [maze1, maze2], puz, counts, pts, probs, rows)
    pages = [p_goals, p_review, cnt, add, cd, ws, m1, m2, sd, p_kind]
    c = canvas.Canvas(os.path.join(OUT, PDF), pagesize=letter)
    c.setTitle("New Year Fun for Kids – Free Printable Pack"); c.setAuthor("BodhiCubs")
    cover(c); c.showPage(); thanks(c); c.showPage()
    for p in pages: p(c, COLOR); c.showPage()
    divider(c, "Black & White Version", "Printer-friendly", ["The same 10 pages in black & white.", "Kids can color them in too!"], BW); c.showPage()
    for p in pages: p(c, BW); c.showPage()
    divider(c, "Answer Key", "For grown-ups", ["Answers for the math, word search,", "mazes and sudoku pages."], COLOR); c.showPage()
    answer_text([("Party Count & Write", a_cnt), ("Picture Addition", a_add), ("New Year Countdown (missing numbers)", a_cd)])(c, COLOR); c.showPage()
    answer_puzzles(ws_mini, [mm1, mm2])(c, COLOR); c.showPage()
    answer_sudoku(sd_mini, len(puz))(c, COLOR); c.showPage()
    c.save(); print("saved", os.path.join(OUT, PDF))

if __name__ == "__main__":
    run()
