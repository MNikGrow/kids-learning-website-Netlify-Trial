import random, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from reportlab.pdfgen import canvas
from lib import *

OUT = "/home/claude/xmas/out/"
SUB_BRAND = "BodhiCubs"

# ================= shared pages =================
def cover(c, meta):
    P = COLOR
    fill(c, P["light"]); c.rect(0, 0, W, H, 0, 1)
    stroke(c, P["red"]); c.setLineWidth(10); c.roundRect(20, 20, W - 40, H - 40, 26, 1, 0)
    stroke(c, P["green"]); c.setLineWidth(3); c.roundRect(34, 34, W - 68, H - 68, 20, 1, 0)
    fill(c, P["green"]); c.roundRect(W / 2 - 80, H - 98, 160, 34, 17, 0, 1)
    text(c, W / 2, H - 87, "BodhiCubs", "PB", 16, P["white"])
    y = H - 170
    for i, ln in enumerate(meta["title_lines"]):
        sz = fit(ln, "PB", 50, W - 120)
        text(c, W / 2, y, ln, "PB", sz, P["red"] if i % 2 == 0 else P["dkgreen"]); y -= sz * 1.08
    fill(c, P["gold"]); c.roundRect(W / 2 - 150, y - 10, 300, 38, 19, 0, 1)
    text(c, W / 2, y + 2, meta["badge"], "PB", 16, P["ink"])
    y -= 70
    ics = meta.get("icons", ["tree", "gift", "snowman", "ornament", "candycane"])
    for i, n in enumerate(ics):
        icon(c, n, W / 2 + (i - (len(ics) - 1) / 2) * 92, y, 74, P)
    y -= 70
    bh = 50 + 26 * len(meta["inside"])
    fill(c, P["white"]); stroke(c, P["ink"]); c.setLineWidth(1.5); c.roundRect(80, y - bh, W - 160, bh, 16, 1, 1)
    text(c, W / 2, y - 26, "What's inside", "PB", 16, P["dkgreen"])
    for i, it in enumerate(meta["inside"]):
        text(c, 115, y - 54 - i * 26, "•  " + it, "PM", 13, P["ink"], "l")
    text(c, W / 2, 62, meta.get("footer", "Color + Black & White  •  Answer Key  •  Print at home"), "PM", 12, P["ink"])

def thanks(c, meta):
    P = COLOR; frame(c, P, "Thank you!", "Read this before printing", name=False)
    lines = [
        ("Printing tips", ["Print at \"Fit to page\" — works on US Letter and A4 paper.",
                           "No color ink? Use the black & white version at the back of this file.",
                           "Laminate the charts or put them in sheet protectors to reuse with dry-erase markers."]),
        ("You may", ["Print as many copies as you need for your own family or one classroom."]),
        ("Please don't", ["Share, resell or upload these files anywhere. Send friends to the shop instead — thank you!"]),
        ("More free fun", ["Play free brain games, science games and puzzles at BodhiCubs."]),
    ]
    y = TOP + 20
    for head, items in lines:
        text(c, 70, y, head, "PB", 17, P["acc"], "l"); y -= 26
        for it in items:
            n = wrap(c, 90, y, "•  " + it, "PR", 12.5, W - 170, P["ink"], 17, "l"); y -= 17 * n + 6
        y -= 16
    for i, n in enumerate(["star", "tree", "gift", "bell", "snowflake"]):
        icon(c, n, W / 2 + (i - 2) * 80, 110, 56, P)

def divider(c, s):
    P = BW; frame(c, P, s, "Same activities, printer-friendly", name=False)
    instr(c, P, H / 2 + 40, "The next pages are the same worksheets in black & white.", 15)
    instr(c, P, H / 2 + 10, "Kids can color them in too!", 15)
    for i, n in enumerate(["tree", "gift", "snowman", "bell"]):
        icon(c, n, W / 2 + (i - 1.5) * 100, H / 2 - 110, 70, P)

def answer_text_page(title, blocks):
    def page(c, P):
        frame(c, P, title, "For grown-ups", name=False)
        col_x = [56, W / 2 + 10]; y0 = TOP + 10; y = y0; col = 0
        for head, lines in blocks:
            need = 22 + 16 * len(lines) + 12
            if y - need < 50:
                col += 1; y = y0
            x = col_x[col]
            text(c, x, y, head, "PB", 12.5, P["acc"], "l"); y -= 18
            for ln in lines:
                text(c, x + 8, y, ln, "PR", 10.5, P["ink"], "l"); y -= 15
            y -= 10
    return page

def build(fname, meta, pages, answers, bw=True):
    c = canvas.Canvas(OUT + fname, pagesize=letter)
    c.setTitle(meta["title_lines"][0] + " " + " ".join(meta["title_lines"][1:])); c.setAuthor("BodhiCubs")
    cover(c, meta); c.showPage()
    thanks(c, meta); c.showPage()
    for p in pages: p(c, COLOR); c.showPage()
    if bw:
        divider(c, "Black & White Version"); c.showPage()
        for p in pages: p(c, BW); c.showPage()
    if answers:
        divider_ans(c); c.showPage()
        for a in answers: a(c, COLOR); c.showPage()
    c.save()

def divider_ans(c):
    P = COLOR; frame(c, P, "Answer Key", "For grown-ups", name=False)
    icon(c, "star", W / 2, H / 2, 140, P)

# ================= math pages =================
TYPES = ["tree", "star", "gift", "ornament", "bell", "snowman", "candycane", "mitten", "snowflake"]

def mk_count(seed, title, ntypes=4, lo=3, hi=9, size=46):
    rng = random.Random(seed); types = rng.sample(TYPES, ntypes)
    counts = {t: rng.randint(lo, hi) for t in types}
    box = (60, 240, W - 60, TOP - 50)
    pts = scatter(rng, counts, box, size)
    def page(c, P):
        frame(c, P, title, "Christmas Counting")
        instr(c, P, TOP - 18, "Count each picture. Write the number in the box.")
        stroke(c, P["ink"]); c.setLineWidth(1.5); fill(c, P["soft"]); c.roundRect(48, 228, W - 96, TOP - 266, 18, 1, 1)
        for x, y, t in pts: icon(c, t, x, y, size, P)
        n = len(types); gap = (W - 100) / n
        for i, t in enumerate(types):
            cx = 50 + gap * (i + .5)
            icon(c, t, cx - 34, 150, 50, P); answer_box(c, P, cx + 2, 128, 52, 44)
    return page, [f"{NAMES[t]}: {counts[t]}" for t in types]

def group(c, P, name, n, x, y, s=25, per=5):
    for i in range(n):
        r, cc = divmod(i, per); icon(c, name, x + cc * (s + 3) + s / 2, y - r * (s + 4), s, P)

def mk_add_pics(seed, title):
    rng = random.Random(seed); probs = []
    while len(probs) < 6:
        a, b = rng.randint(1, 5), rng.randint(1, 5)
        if (a, b) not in [(p[0], p[1]) for p in probs]: probs.append((a, b, rng.choice(TYPES[:8])))
    def page(c, P):
        frame(c, P, title, "Picture Addition (up to 10)")
        instr(c, P, TOP - 18, "Count the pictures. Add them together. Write the answer.")
        for i, (a, b, t) in enumerate(probs):
            y = TOP - 90 - i * 78
            text(c, 56, y - 6, f"{i + 1}.", "PB", 15, P["acc"], "l")
            group(c, P, t, a, 82, y)
            text(c, 240, y - 10, "+", "PB", 30, P["ink"])
            group(c, P, t, b, 266, y)
            text(c, 432, y - 10, "=", "PB", 30, P["ink"])
            answer_box(c, P, 462, y - 22, 60, 46)
    return page, [f"{i + 1}. {a} + {b} = {a + b}" for i, (a, b, t) in enumerate(probs)]

def mk_sub_pics(seed, title):
    rng = random.Random(seed); probs = []
    while len(probs) < 6:
        n = rng.randint(4, 10); k = rng.randint(1, n - 1)
        if (n, k) not in [(p[0], p[1]) for p in probs]: probs.append((n, k, rng.choice(TYPES[:8])))
    def page(c, P):
        frame(c, P, title, "Picture Subtraction")
        instr(c, P, TOP - 18, "Some pictures are crossed out. How many are left?")
        for i, (n, k, t) in enumerate(probs):
            y = TOP - 90 - i * 78
            text(c, 50, y - 6, f"{i + 1}.", "PB", 15, P["acc"], "l")
            for j in range(n):
                x = 82 + j * 30; icon(c, t, x, y, 26, P)
                if j >= n - k:
                    stroke(c, P["ink"]); c.setLineWidth(2.5); c.line(x - 13, y - 13, x + 13, y + 13); c.line(x - 13, y + 13, x + 13, y - 13)
            text(c, 440, y - 8, f"{n} − {k} =", "PB", 20, P["ink"])
            answer_box(c, P, 492, y - 22, 54, 44)
    return page, [f"{i + 1}. {n} − {k} = {n - k}" for i, (n, k, t) in enumerate(probs)]

def mk_numbers(seed, title, sub, op):
    rng = random.Random(seed); probs = []
    while len(probs) < 20:
        if op == "+":
            a, b = rng.randint(1, 12), rng.randint(1, 10)
            if a + b > 20: continue
        else:
            a = rng.randint(5, 20); b = rng.randint(1, min(10, a))
        if (a, b) not in probs: probs.append((a, b))
    def page(c, P):
        frame(c, P, title, sub)
        instr(c, P, TOP - 18, "Solve each problem. Color an ornament for every one you get right!")
        for i, (a, b) in enumerate(probs):
            col, row = divmod(i, 10); x = 90 + col * 260; y = TOP - 72 - row * 50
            icon(c, "ornament", x - 22, y + 6, 24, P)
            text(c, x, y, f"{a} {op if op == '+' else '−'} {b} =", "PM", 21, P["ink"], "l")
            stroke(c, P["ink"]); c.setLineWidth(1.4); c.line(x + 118, y - 4, x + 178, y - 4)
    res = [a + b if op == "+" else a - b for a, b in probs]
    return page, [f"{i + 1}. {a} {op if op == '+' else '−'} {b} = {r}" for i, ((a, b), r) in enumerate(zip(probs, res))]

def mk_compare(seed, title):
    rng = random.Random(seed); probs = []
    while len(probs) < 12:
        a, b = rng.randint(1, 20), rng.randint(1, 20)
        if len(probs) in (4, 9): b = a
        probs.append((a, b))
    def page(c, P):
        frame(c, P, title, "Greater Than, Less Than, Equal")
        instr(c, P, TOP - 18, "Write  >  <  or  =  in each circle.")
        text(c, W / 2, TOP - 44, "Tip: the hungry crocodile mouth opens toward the BIGGER number!", "PR", 11, P["grey"])
        for i, (a, b) in enumerate(probs):
            col, row = divmod(i, 6); cx = 170 + col * 270; y = TOP - 110 - row * 72
            fill(c, P["white"]); stroke(c, P["ink"]); c.setLineWidth(1.4)
            c.roundRect(cx - 105, y - 24, 210, 56, 14, 1, 1)
            text(c, cx - 62, y - 4, str(a), "PB", 26, P["ink"]); text(c, cx + 62, y - 4, str(b), "PB", 26, P["ink"])
            fill(c, P["white"]); c.circle(cx, y + 4, 20, 1, 1)
    sym = lambda a, b: ">" if a > b else "<" if a < b else "="
    return page, [f"{i + 1}. {a} {sym(a, b)} {b}" for i, (a, b) in enumerate(probs)]

def mk_patterns(seed, title):
    rng = random.Random(seed); kinds = ["AB", "ABC", "AAB", "ABB", "AABB", "ABC"]
    rows = []
    for k in kinds:
        letters = sorted(set(k)); icons = rng.sample(TYPES[:8], len(letters))
        m = dict(zip(letters, icons)); seq = [m[k[i % len(k)]] for i in range(7)]
        rows.append(seq)
    def page(c, P):
        frame(c, P, title, "Christmas Patterns")
        instr(c, P, TOP - 18, "What comes next? Draw it in the box.")
        for i, seq in enumerate(rows):
            y = TOP - 90 - i * 78
            text(c, 50, y - 6, f"{i + 1}.", "PB", 15, P["acc"], "l")
            for j, t in enumerate(seq[:6]): icon(c, t, 104 + j * 62, y, 48, P)
            stroke(c, P["ink"]); c.setLineWidth(1.6); c.setDash(5, 4); fill(c, P["white"])
            c.roundRect(470, y - 30, 64, 60, 10, 1, 1); c.setDash()
    return page, [f"{i + 1}. {NAMES[s[6]]}" for i, s in enumerate(rows)]

def mk_missing(seed, title):
    rng = random.Random(seed); rows = []
    for step in [1, 1, 2, 2, 5, 10, -1, 1]:
        start = rng.randint(1, 12) if step in (1, 2) else (rng.randint(1, 4) * step if step > 1 else rng.randint(10, 20))
        seq = [start + step * i for i in range(6)]
        blanks = sorted(rng.sample(range(1, 6), 2)); rows.append((seq, blanks, step))
    def page(c, P):
        frame(c, P, title, "Count by 1s, 2s, 5s and 10s")
        instr(c, P, TOP - 18, "Write the missing numbers on the ornaments.")
        for i, (seq, blanks, step) in enumerate(rows):
            y = TOP - 76 - i * 60
            for j, v in enumerate(seq):
                x = 110 + j * 76
                stroke(c, P["ink"]); c.setLineWidth(1.4); c.line(x, y + 26, x, y + 36)
                fill(c, P["gold"] if P is COLOR else P["white"]); c.rect(x - 7, y + 20, 14, 7, 1, 1)
                fill(c, (P["red"], P["green"], P["blue"])[j % 3] if not P["bw"] else P["white"])
                if j in blanks: fill(c, P["white"])
                c.circle(x, y, 22, 1, 1)
                if j not in blanks: text(c, x, y - 7, str(v), "PB", 18, P["white"] if not P["bw"] else P["ink"])
    return page, [f"{i + 1}. " + ", ".join(str(seq[b]) for b in blanks) for i, (seq, blanks, s) in enumerate(rows)]

# ================= word pages =================
WORDS = ["TREE", "STAR", "GIFT", "BELL", "SNOW", "SLED", "CANDY", "COOKIE", "ANGEL", "WREATH", "REINDEER",
         "SANTA", "STOCKING", "MITTEN", "SNOWMAN", "CAROL", "HOLLY", "JOY", "PRESENT", "ORNAMENT", "CHIMNEY",
         "SLEIGH", "WINTER", "TINSEL", "GINGERBREAD", "CANDLE", "SCARF", "ICICLE", "PENGUIN", "COCOA",
         "MERRY", "FAMILY", "CHEER", "ELF", "LIGHTS", "WISH"]

def mk_ws(seed, title, sub, words, n, dirs):
    g, placed = make_wordsearch(words, n, dirs, seed)
    def page(c, P, ans=False, x=None, y=None, size=None):
        frame(c, P, title, sub)
        instr(c, P, TOP - 18, "Find and circle each word. Check it off the list!")
        size = 372; x = (W - size) / 2; y = TOP - 48 - size
        draw_wordsearch(c, P, g, placed, x, y, size)
        ws = sorted(words); cols = 3; per = (len(ws) + cols - 1) // cols
        for i, w in enumerate(ws):
            col, row = divmod(i, per); xx = 90 + col * 160; yy = y - 40 - row * 22
            stroke(c, P["ink"]); c.setLineWidth(1.2); fill(c, P["white"]); c.rect(xx, yy - 2, 12, 12, 1, 1)
            text(c, xx + 20, yy, w, "PM", 12.5, P["ink"], "l")
    def mini(c, P, x, y, size):
        draw_wordsearch(c, P, g, placed, x, y, size, answers=True)
    return page, mini

def ws_answer_page(minis, titles):
    def page(c, P):
        frame(c, P, "Answer Key", "Word Searches", name=False)
        for i, (m, t) in enumerate(zip(minis, titles)):
            col, row = i % 2, i // 2; s = 236
            x = 50 + col * (s + 58) + 6; y = TOP - 26 - (row + 1) * (s + 44) + 30
            text(c, x + s / 2, y + s + 16, t, "PB", 12, P["acc"]); m(c, P, x, y, s)
    return page

def scramble(w, rng):
    while True:
        l = list(w); rng.shuffle(l); s = "".join(l)
        if s != w: return s

def mk_scramble(seed, title, words):
    rng = random.Random(seed); sc = [scramble(w, rng) for w in words]
    def page(c, P):
        frame(c, P, title, "Christmas Word Scramble")
        instr(c, P, TOP - 18, "Unscramble the letters to make a Christmas word.")
        for i, s in enumerate(sc):
            y = TOP - 74 - i * 54
            text(c, 50, y - 4, f"{i + 1}.", "PB", 14, P["acc"], "l")
            for j, ch in enumerate(s):
                x = 82 + j * 26; fill(c, (P["soft"])); stroke(c, P["ink"]); c.setLineWidth(1.2)
                c.roundRect(x, y - 10, 22, 26, 5, 1, 1); text(c, x + 11, y - 3, ch, "PB", 14, P["ink"])
            stroke(c, P["ink"]); c.setLineWidth(1.4); c.line(370, y - 8, W - 56, y - 8)
    return page, [f"{i + 1}. {w}" for i, w in enumerate(words)]

def mk_missing_letters(seed, title, words):
    rng = random.Random(seed); rows = []
    for w in words:
        k = 1 if len(w) <= 4 else 2
        idx = sorted(rng.sample(range(len(w)), k)); rows.append((w, idx))
    def page(c, P):
        frame(c, P, title, "Fill in the Missing Letters")
        instr(c, P, TOP - 18, "Write the missing letters to finish each word.")
        for i, (w, idx) in enumerate(rows):
            col, row = divmod(i, 6); x0 = 70 + col * 270; y = TOP - 80 - row * 80
            text(c, x0 - 22, y + 2, f"{i + 1}.", "PB", 13, P["acc"], "l")
            for j, ch in enumerate(w):
                x = x0 + j * 24
                if j in idx:
                    stroke(c, P["ink"]); c.setLineWidth(1.5); c.line(x + 2, y - 2, x + 20, y - 2)
                else: text(c, x + 11, y + 2, ch, "PB", 18, P["ink"])
    return page, [f"{i + 1}. {w}" for i, (w, idx) in enumerate(rows)]

# ================= puzzle pages =================
def mk_maze_page(seed, title, sub, w, h):
    m = make_maze(w, h, seed)
    def page(c, P):
        frame(c, P, title, sub)
        instr(c, P, TOP - 18, "Help the gift find its way to the tree!")
        draw_maze(c, P, m, 70, 100, W - 140, TOP - 210, icons=("gift", "tree"))
    def mini(c, P, x, y, s): draw_maze(c, P, m, x, y, s, s, answers=True, icons=None, lw=1.1)
    return page, mini

def maze_answer_page(minis, titles):
    def page(c, P):
        frame(c, P, "Answer Key", "Mazes", name=False)
        for i, (m, t) in enumerate(zip(minis, titles)):
            col, row = i % 2, i // 2; s = 230
            x = 60 + col * (s + 52); y = TOP - 40 - (row + 1) * (s + 40) + 30
            text(c, x + s / 2, y + s + 12, t, "PB", 12, P["acc"]); m(c, P, x, y, s)
    return page

SUDO_SETS = [["tree", "star", "gift", "bell"], ["snowman", "ornament", "candycane", "mitten"]]
def mk_sudoku_page(seeds, title, symset, givens=7):
    puz = [make_sudoku(s, givens) for s in seeds]
    def page(c, P):
        frame(c, P, title, "Picture Sudoku (4 x 4)")
        instr(c, P, TOP - 18, "Draw the missing pictures. Each row, column and 2x2 box")
        instr(c, P, TOP - 36, "must have one of each:")
        for i, n in enumerate(symset): icon(c, n, W / 2 - 75 + i * 50, TOP - 66, 36, P)
        for i, (p, s) in enumerate(puz):
            col, row = i % 2, i // 2; size = 206
            x = 78 + col * (size + 50); y = TOP - 110 - (row + 1) * (size + 36) + 20
            text(c, x + size / 2, y + size + 8, f"Puzzle {i + 1}", "PB", 12, P["acc"])
            draw_sudoku(c, P, p, symset, x, y, size)
    def mini(c, P, i, x, y, s): draw_sudoku(c, P, puz[i][1], symset, x, y, s, lw=1.2)
    return page, mini, len(puz)

def sudoku_answer_page(groups):
    def page(c, P):
        frame(c, P, "Answer Key", "Picture Sudoku", name=False)
        k = 0
        for title, mini, n in groups:
            for i in range(n):
                col, row = k % 4, k // 4; s = 118
                x = 50 + col * (s + 20); y = TOP - 30 - (row + 1) * (s + 34)
                text(c, x + s / 2, y + s + 8, f"{title} #{i + 1}", "PB", 10, P["acc"]); mini(c, P, i, x, y, s); k += 1
    return page

def mk_odd(seed, title):
    rng = random.Random(seed); rows = []
    for _ in range(6):
        a, b = rng.sample(TYPES, 2); pos = rng.randrange(5); rows.append((a, b, pos))
    def page(c, P):
        frame(c, P, title, "Spot the Odd One Out")
        instr(c, P, TOP - 18, "Circle the picture that is different in each row.")
        for i, (a, b, pos) in enumerate(rows):
            y = TOP - 92 - i * 80
            text(c, 50, y - 6, f"{i + 1}.", "PB", 15, P["acc"], "l")
            fill(c, P["soft"]); stroke(c, P["ink"]); c.setLineWidth(1.2); c.roundRect(80, y - 34, W - 140, 68, 14, 1, 1)
            for j in range(5): icon(c, b if j == pos else a, 130 + j * 92, y, 50, P)
    return page, [f"Row {i + 1}: picture {pos + 1} ({NAMES[b]})" for i, (a, b, pos) in enumerate(rows)]

# ================= screen-free pages =================
ADVENT = ["Make a paper snowflake", "Bake cookies together", "Write a letter to a friend", "Build a blanket fort",
          "Read a winter story", "Make a gift for someone", "Have a dance party", "Draw your dream gingerbread house",
          "Do a secret act of kindness", "Go on a winter walk", "Make hot cocoa", "Play a board game",
          "Make a paper chain", "Sing your favorite carol", "Donate a toy or book", "Make a thank-you card",
          "Look at holiday lights", "Do a puzzle together", "Make salt dough ornaments", "Family story night",
          "Make a bird feeder", "Write 3 things you are thankful for", "Help decorate the tree",
          "Call or visit a grandparent", "Merry Christmas! Share a big hug"]

def p_advent(c, P):
    frame(c, P, "25 Days of Christmas Fun", "Screen-Free Advent Activity Calendar")
    instr(c, P, TOP - 18, "Do one activity each day in December. Color the box when you finish!")
    cs = 100; x0 = (W - cs * 5) / 2; ytop = TOP - 40
    for i, a in enumerate(ADVENT):
        r, cc = divmod(i, 5); x = x0 + cc * cs; y = ytop - (r + 1) * cs
        stroke(c, P["ink"]); c.setLineWidth(1.4); fill(c, P["white"]); c.rect(x, y, cs, cs, 1, 1)
        fill(c, (P["red"], P["green"])[i % 2] if not P["bw"] else P["white"]); c.circle(x + 18, y + cs - 18, 13, 1, 1)
        text(c, x + 18, y + cs - 23, str(i + 1), "PB", 12, P["white"] if not P["bw"] else P["ink"])
        wrap(c, x + cs / 2, y + cs - 50, a, "PM", 10, cs - 14, P["ink"], 12.5)

HUNT = ["Something red", "Something soft", "A star shape", "Something that smells nice", "Something shiny",
        "A book with snow in it", "Something green", "A ribbon or bow", "Something warm to wear", "A spoon",
        "Something round", "Something that makes a sound", "A blanket", "Something sparkly", "A picture of family",
        "Something white", "A sock", "Something tiny"]

def p_hunt(c, P):
    frame(c, P, "Indoor Christmas Scavenger Hunt", "Find it around your home!")
    instr(c, P, TOP - 18, "Can you find everything? Check each box when you find it.")
    for i, h in enumerate(HUNT):
        col, row = divmod(i, 9); x = 70 + col * 250; y = TOP - 80 - row * 50
        stroke(c, P["ink"]); c.setLineWidth(1.5); fill(c, P["white"]); c.roundRect(x, y - 8, 24, 24, 5, 1, 1)
        text(c, x + 36, y - 1, h, "PM", 13, P["ink"], "l")
    for i, n in enumerate(["tree", "gift", "candycane", "mitten", "star"]):
        icon(c, n, W / 2 + (i - 2) * 90, 90, 56, P)

def mk_ispy(seed, title):
    rng = random.Random(seed); types = rng.sample(TYPES, 6)
    counts = {t: rng.randint(2, 8) for t in types}
    pts = scatter(rng, counts, (60, 210, W - 60, TOP - 48), 42)
    def page(c, P):
        frame(c, P, title, "Christmas I Spy")
        instr(c, P, TOP - 18, "I spy with my little eye... Count and write how many!")
        stroke(c, P["ink"]); c.setLineWidth(1.5); fill(c, P["soft"]); c.roundRect(48, 200, W - 96, TOP - 236, 18, 1, 1)
        for x, y, t in pts: icon(c, t, x, y, 42, P)
        for i, t in enumerate(types):
            col, row = i % 3, i // 3; cx = 120 + col * 180; y = 150 - row * 66
            icon(c, t, cx - 26, y, 44, P); answer_box(c, P, cx + 4, y - 20, 48, 40)
    return page, [f"{NAMES[t]}: {counts[t]}" for t in types]

DRAW = ["Draw a snowman wearing sunglasses", "Draw the biggest present ever", "Draw your family on a sled",
        "Design your own ornament"]
def p_draw(c, P):
    frame(c, P, "Christmas Drawing Prompts", "Imagine, then draw!")
    for i, d in enumerate(DRAW):
        col, row = i % 2, i // 2; w, h = 250, 270; x = 46 + col * (w + 20); y = TOP - 20 - (row + 1) * (h + 18)
        stroke(c, P["ink"]); c.setLineWidth(1.6); fill(c, P["white"]); c.roundRect(x, y, w, h, 14, 1, 1)
        fill(c, P["soft"]); c.roundRect(x, y + h - 40, w, 40, 14, 1, 1)
        text(c, x + w / 2, y + h - 26, d, "PB", fit(d, "PB", 12.5, w - 20), P["ink"])

WYR = ["...build a snowman or have a snowball fight?", "...ride in a sleigh or fly with reindeer?",
       "...eat a giant cookie or a mountain of candy canes?", "...wear mittens on your feet or socks on your hands?",
       "...live in a gingerbread house or an igloo?", "...open one big gift or ten tiny gifts?",
       "...have a talking snowman or a flying sled?", "...sing a carol or dance to it?",
       "...decorate a tree or decorate cookies?", "...have snow every day or never see snow?",
       "...be an elf for a day or a reindeer for a day?", "...drink hot cocoa or eat a warm cookie?"]
def p_wyr(c, P):
    frame(c, P, "Christmas Would You Rather?", "Cut out the cards and take turns!", name=False)
    w, h = 170, 140; x0 = (W - 3 * w) / 2
    for i, q in enumerate(WYR):
        col, row = i % 3, i // 3; x = x0 + col * w; y = TOP + 10 - (row + 1) * h
        stroke(c, P["grey"]); c.setLineWidth(1); c.setDash(4, 4); c.rect(x, y, w, h, 1, 0); c.setDash()
        text(c, x + w / 2, y + h - 34, "Would you rather...", "PB", 12, P["acc"] if not P["bw"] else P["ink"])
        wrap(c, x + w / 2, y + h - 58, q[3:], "PM", 11, w - 24, P["ink"], 14)
        icon(c, ["snowflake", "star", "tree"][i % 3], x + w / 2, y + 20, 22, P)

BINGO = ["TREE", "STAR", "GIFT", "BELL", "SNOW", "SLED", "CANDY", "COOKIE", "ANGEL", "WREATH", "REINDEER",
         "SANTA", "STOCKING", "MITTEN", "SNOWMAN", "CAROL", "HOLLY", "PRESENT", "SLEIGH", "TINSEL", "CANDLE",
         "SCARF", "COCOA", "LIGHTS", "ELF", "JOY", "WISH", "ICICLE", "PENGUIN", "CHIMNEY"]
def mk_bingo(seed, k):
    rng = random.Random(seed); cells = rng.sample(BINGO, 24); cells.insert(12, None)
    def page(c, P):
        frame(c, P, f"Christmas Bingo — Card {k}", "Cover the word when it's called!", name=False)
        cs = 96; x0 = (W - 5 * cs) / 2; ytop = TOP - 30
        for j, ch in enumerate("SNOWY"):
            fill(c, (P["red"], P["green"])[j % 2] if not P["bw"] else P["white"]); stroke(c, P["ink"]); c.setLineWidth(1.4)
            c.roundRect(x0 + j * cs + 6, ytop, cs - 12, 44, 10, 1, 1)
            text(c, x0 + j * cs + cs / 2, ytop + 11, ch, "PB", 26, P["white"] if not P["bw"] else P["ink"])
        for i, w in enumerate(cells):
            r, cc = divmod(i, 5); x = x0 + cc * cs; y = ytop - 10 - (r + 1) * cs
            stroke(c, P["ink"]); c.setLineWidth(1.6); fill(c, P["white"]); c.rect(x, y, cs, cs, 1, 1)
            if w is None:
                icon(c, "star", x + cs / 2, y + cs / 2 + 8, 52, P); text(c, x + cs / 2, y + 10, "FREE", "PB", 13, P["ink"])
            else:
                text(c, x + cs / 2, y + cs / 2 - 5, w, "PB", fit(w, "PB", 15, cs - 12), P["ink"])
    return page

def p_calling(c, P):
    frame(c, P, "Bingo Calling Cards", "Cut out, put in a hat, and draw one at a time", name=False)
    w, h = 108, 84; x0 = (W - 5 * w) / 2
    for i, b in enumerate(BINGO):
        col, row = i % 5, i // 5; x = x0 + col * w; y = TOP + 10 - (row + 1) * h
        stroke(c, P["grey"]); c.setLineWidth(1); c.setDash(4, 4); c.rect(x, y, w, h, 1, 0); c.setDash()
        text(c, x + w / 2, y + h / 2 - 6, b, "PB", fit(b, "PB", 15, w - 14), P["ink"])

# ================= routine pages =================
DAYS = ["M", "T", "W", "T", "F", "S", "S"]
def chart(c, P, title, sub, tasks, blank=2, head="My Task"):
    frame(c, P, title, sub)
    instr(c, P, TOP - 18, "Put a check or a sticker in the box each day you do it!")
    rows = tasks + [""] * blank; rh = min(54, (TOP - 120) / (len(rows) + 1))
    x0, tw, dw = 50, 230, 38; ytop = TOP - 46
    fill(c, P["band"] if not P["bw"] else P["white"]); stroke(c, P["ink"]); c.setLineWidth(1.4)
    c.rect(x0, ytop - rh, tw + 7 * dw, rh, 1, 1)
    text(c, x0 + 14, ytop - rh / 2 - 6, head, "PB", 15, P["bandtxt"], "l")
    for j, d in enumerate(DAYS): text(c, x0 + tw + (j + .5) * dw, ytop - rh / 2 - 6, d, "PB", 15, P["bandtxt"])
    ics = ["star", "tree", "gift", "bell", "ornament", "snowflake", "mitten", "candycane", "snowman"]
    for i, t in enumerate(rows):
        y = ytop - (i + 2) * rh
        fill(c, P["white"] if i % 2 else P["soft"]); c.rect(x0, y, tw + 7 * dw, rh, 1, 1)
        for j in range(8): c.line(x0 + tw + j * dw, y, x0 + tw + j * dw, y + rh)
        if t:
            icon(c, ics[i % len(ics)], x0 + 22, y + rh / 2, rh * 0.55, P)
            text(c, x0 + 44, y + rh / 2 - 5, t, "PM", fit(t, "PM", 14, tw - 50), P["ink"], "l")
        else:
            c.line(x0 + 14, y + 12, x0 + tw - 14, y + 12)

def p_morning(c, P):
    chart(c, P, "My Morning Routine", "Winter Break Routine Chart",
          ["Wake up & stretch", "Make my bed", "Brush my teeth", "Get dressed", "Eat breakfast", "Tidy my room", "Read for 15 minutes"])
def p_bed(c, P):
    chart(c, P, "My Bedtime Routine", "Winter Break Routine Chart",
          ["Clean up my toys", "Bath or shower", "Put on pajamas", "Brush my teeth", "Pick out clothes", "Story time", "Lights out"])
def p_chores(c, P):
    chart(c, P, "My Helper Chart", "Christmas Chores & Jobs",
          ["Feed the pet", "Set the table", "Water the plants", "Help wrap gifts", "Put away laundry"], blank=4, head="My Job")
    text(c, W / 2, 56, "This week I earned ______ stars!", "PB", 16, P["ink"])

SCREENFREE = ["Build a blanket fort", "Make paper snowflakes", "Bake something", "Play a board game", "Do a puzzle",
              "Draw a comic", "Have a dance party", "Read a book", "Write a story", "Make a card",
              "Play hide and seek", "Build with blocks", "Do yoga", "Go for a walk", "Play I spy",
              "Make a paper airplane", "Help cook dinner", "Play charades", "Sing a song", "Make a craft",
              "Plant a seed", "Look at the stars", "Play with play dough", "Make a treasure map", "Call a friend",
              "Do a science experiment", "Have a picnic indoors", "Play freeze dance", "Sort your toys", "Make a thank-you note"]
def p_screenfree(c, P):
    frame(c, P, "30 Screen-Free Activities", "Winter Break Challenge")
    instr(c, P, TOP - 18, "How many can you do this break? Check them off!")
    for i, a in enumerate(SCREENFREE):
        col, row = divmod(i, 15); x = 70 + col * 250; y = TOP - 60 - row * 33
        stroke(c, P["ink"]); c.setLineWidth(1.3); fill(c, P["white"]); c.roundRect(x, y - 6, 18, 18, 4, 1, 1)
        text(c, x + 28, y - 2, a, "PM", 12, P["ink"], "l")

def p_reading(c, P):
    frame(c, P, "My Winter Reading Log", "Read, record, and rate!")
    instr(c, P, TOP - 18, "Write each book you read. Color the stars to rate it!")
    cols = [("Date", 70), ("Book Title", 250), ("Minutes", 80), ("My Rating", 112)]; x0 = 44; ytop = TOP - 40; rh = 40
    stroke(c, P["ink"]); c.setLineWidth(1.4); x = x0
    fill(c, P["green"] if not P["bw"] else P["white"]); c.rect(x0, ytop - rh, sum(w for _, w in cols), rh, 1, 1)
    for nm, w in cols:
        text(c, x + w / 2, ytop - rh / 2 - 5, nm, "PB", 13, P["bandtxt"]); x += w
    for r in range(12):
        y = ytop - (r + 2) * rh; x = x0
        fill(c, P["white"] if r % 2 else P["soft"]); c.rect(x0, y, sum(w for _, w in cols), rh, 1, 1)
        for nm, w in cols[:-1]:
            x += w; c.line(x, y, x, y + rh)
        for k in range(5):
            fill(c, P["white"]); poly(c, star_pts(x + 16 + k * 20, y + rh / 2, 9))

def p_goals(c, P):
    frame(c, P, "My Winter Break Goals", "Dream big!")
    prompts = ["Something new I want to learn...", "Someone I want to help...", "A book I want to read...",
               "Something fun I want to try...", "A skill I want to practice...", "I will be proud of myself when..."]
    for i, p in enumerate(prompts):
        col, row = i % 2, i // 2; w, h = 255, 170; x = 44 + col * (w + 14); y = TOP - 20 - (row + 1) * (h + 14)
        stroke(c, P["ink"]); c.setLineWidth(1.5); fill(c, P["white"]); c.roundRect(x, y, w, h, 14, 1, 1)
        icon(c, ["star", "gift", "tree", "bell", "snowflake", "ornament"][i], x + 24, y + h - 24, 30, P)
        text(c, x + 46, y + h - 30, p, "PB", fit(p, "PB", 12, w - 56), P["ink"], "l")
        for k in range(3): c.setLineWidth(0.8); c.line(x + 16, y + h - 70 - k * 32, x + w - 16, y + h - 70 - k * 32)

KIND = ["Hold the door for someone", "Make a card for a neighbor", "Share a toy", "Help clean up without being asked",
        "Say thank you 5 times today", "Give someone a compliment", "Donate a book", "Help cook a meal",
        "Draw a picture for a grandparent", "Make someone laugh", "Feed the birds", "Give a big hug"]
def p_kind(c, P):
    frame(c, P, "Christmas Kindness Challenge", "12 Acts of Kindness")
    instr(c, P, TOP - 18, "Do one kind act each day. Color the ornament when you finish!")
    w, h = 170, 138; x0 = (W - 3 * w) / 2
    for i, k in enumerate(KIND):
        col, row = i % 3, i // 3; x = x0 + col * w + 5; y = TOP - 40 - (row + 1) * h
        stroke(c, P["ink"]); c.setLineWidth(1.4); fill(c, P["white"]); c.roundRect(x, y + 5, w - 10, h - 10, 14, 1, 1)
        P2 = dict(P); P2["blue"] = (1, 1, 1); icon(c, "ornament", x + (w - 10) / 2, y + h - 42, 48, P2)
        text(c, x + (w - 10) / 2, y + h - 48, str(i + 1), "PB", 14, P["ink"])
        wrap(c, x + (w - 10) / 2, y + 48, k, "PM", 11, w - 30, P["ink"], 13.5)

def p_dayplan(c, P):
    frame(c, P, "My Winter Break Day Plan", "Plan your day like a pro!")
    instr(c, P, TOP - 18, "Write or draw what you will do at each time.")
    times = ["8:00", "9:00", "10:00", "11:00", "12:00", "1:00", "2:00", "3:00", "4:00", "5:00", "6:00", "7:00", "8:00"]
    rh = (TOP - 80) / len(times); ytop = TOP - 40
    for i, t in enumerate(times):
        y = ytop - (i + 1) * rh
        stroke(c, P["ink"]); c.setLineWidth(1.3)
        fill(c, (P["red"], P["green"])[i % 2] if not P["bw"] else P["white"]); c.roundRect(50, y + 4, 70, rh - 8, 8, 1, 1)
        text(c, 85, y + rh / 2 - 5, t, "PB", 13, P["white"] if not P["bw"] else P["ink"])
        c.setLineWidth(0.9); c.line(134, y + 8, W - 50, y + 8)

# ================= BUILD =================
def run():
    os.makedirs(OUT, exist_ok=True)
    # ---- 1. Math ----
    pages, ans = [], []
    for spec in [mk_count(11, "Count & Write"), mk_count(12, "Count & Write", 4, 5, 10),
                 mk_add_pics(21, "Picture Addition"), mk_add_pics(22, "Picture Addition"),
                 mk_sub_pics(31, "Picture Subtraction"),
                 mk_numbers(41, "Christmas Addition", "Adding within 20", "+"), mk_numbers(42, "Christmas Addition", "Adding within 20", "+"),
                 mk_numbers(43, "Christmas Subtraction", "Subtracting within 20", "-"),
                 mk_compare(51, "Compare Numbers"), mk_patterns(61, "What Comes Next?"), mk_missing(71, "Missing Numbers")]:
        pages.append(spec[0]); ans.append(spec[1])
    names = ["Count & Write 1", "Count & Write 2", "Picture Addition 1", "Picture Addition 2", "Picture Subtraction",
             "Addition 1", "Addition 2", "Subtraction", "Compare Numbers", "Patterns", "Missing Numbers"]
    blocks = list(zip(names, ans))
    build("1_Christmas_Math_Worksheets_Ages5-7.pdf",
          dict(title_lines=["Christmas Math", "Worksheets"], badge="Ages 5–7  •  11 Worksheets",
               inside=["Count & write (2 pages)", "Picture addition & subtraction (3 pages)", "Addition & subtraction within 20 (3 pages)",
                       "Compare numbers, patterns, missing numbers (3 pages)", "Black & white version + full answer key"]),
          pages, [answer_text_page("Answer Key", blocks[:5]), answer_text_page("Answer Key", blocks[5:7]), answer_text_page("Answer Key", blocks[7:])])
    # ---- 2. Words ----
    rng = random.Random(5)
    ws_specs = [(101, "Word Search: Easy", "10 x 10 • across and down", rng.sample([w for w in WORDS if len(w) <= 6], 10), 10, [(0, 1), (1, 0)]),
                (102, "Word Search: Easy", "10 x 10 • across and down", rng.sample([w for w in WORDS if len(w) <= 6], 10), 10, [(0, 1), (1, 0)]),
                (103, "Word Search: Medium", "12 x 12 • across, down, diagonal", rng.sample([w for w in WORDS if len(w) <= 9], 12), 12, [(0, 1), (1, 0), (1, 1)]),
                (104, "Word Search: Tricky", "14 x 14 • every direction but backwards", rng.sample(WORDS, 15), 14, [(0, 1), (1, 0), (1, 1), (-1, 1)])]
    pages, minis = [], []
    for s in ws_specs:
        p, m = mk_ws(*s); pages.append(p); minis.append(m)
    sc1, a1 = mk_scramble(111, "Word Scramble: Easy", rng.sample([w for w in WORDS if 3 <= len(w) <= 5], 10))
    sc2, a2 = mk_scramble(112, "Word Scramble: Harder", rng.sample([w for w in WORDS if 6 <= len(w) <= 9], 10))
    ml, a3 = mk_missing_letters(113, "Missing Letters", rng.sample([w for w in WORDS if len(w) <= 8], 12))
    pages += [sc1, sc2, ml]
    t = ["Easy #1", "Easy #2", "Medium", "Tricky"]
    build("2_Christmas_Word_Search_Scramble_Ages6-9.pdf",
          dict(title_lines=["Christmas Word", "Search & Scramble"], badge="Ages 6–9  •  7 Puzzle Pages",
               icons=["star", "bell", "gift", "tree", "snowflake"],
               inside=["4 word searches (easy, medium, tricky)", "2 word scrambles", "1 missing letters page",
                       "Black & white version", "Full answer key"]),
          pages, [ws_answer_page(minis, t), answer_text_page("Answer Key", [("Word Scramble: Easy", a1), ("Word Scramble: Harder", a2), ("Missing Letters", a3)])])
    # ---- 3. Mazes & logic ----
    mz = [(201, "Christmas Maze 1", "Easy", 7, 8), (202, "Christmas Maze 2", "Easy", 9, 10), (203, "Christmas Maze 3", "Medium", 11, 13),
          (204, "Christmas Maze 4", "Medium", 13, 15), (205, "Christmas Maze 5", "Hard", 16, 18), (206, "Christmas Maze 6", "Hard", 19, 22)]
    pages, minis = [], []
    for s, ti, sub, w, h in mz:
        p, m = mk_maze_page(s, ti, sub, w, h); pages.append(p); minis.append(m)
    s1, sm1, n1 = mk_sudoku_page([301, 302, 303, 304], "Picture Sudoku 1", SUDO_SETS[0], 8)
    s2, sm2, n2 = mk_sudoku_page([305, 306, 307, 308], "Picture Sudoku 2", SUDO_SETS[1], 6)
    od, ao = mk_odd(311, "Odd One Out"); pt, ap = mk_patterns(312, "What Comes Next?")
    pages += [s1, s2, od, pt]
    build("3_Christmas_Mazes_Logic_Puzzles_Ages5-8.pdf",
          dict(title_lines=["Christmas Mazes", "& Logic Puzzles"], badge="Ages 5–8  •  10 Puzzle Pages",
               icons=["gift", "tree", "star", "snowman", "bell"],
               inside=["6 mazes from easy to hard", "8 picture sudoku puzzles (2 pages)", "Odd one out + patterns",
                       "Black & white version", "Answer key with solved mazes"]),
          pages, [maze_answer_page(minis[:4], [m[1] for m in mz[:4]]), maze_answer_page(minis[4:], [m[1] for m in mz[4:]]),
                  sudoku_answer_page([("Sudoku 1", sm1, n1), ("Sudoku 2", sm2, n2)]),
                  answer_text_page("Answer Key", [("Odd One Out", ao), ("What Comes Next?", ap)])])
    # ---- 4. Routine charts ----
    build("4_Winter_Break_Routine_Charts_for_Kids.pdf",
          dict(title_lines=["Winter Break", "Routine Charts"], badge="Ages 4–9  •  9 Printables",
               icons=["snowman", "star", "mitten", "snowflake", "tree"],
               footer="Color + Black & White  •  Reusable  •  Print at home",
               inside=["Morning & bedtime routine charts", "Helper / chore chart", "Day plan schedule",
                       "30 screen-free activities checklist", "Reading log, goals & kindness challenge"]),
          [p_morning, p_bed, p_chores, p_dayplan, p_screenfree, p_reading, p_goals, p_kind], None)
    # ---- 5. Screen-free activity pack ----
    i1, ai1 = mk_ispy(401, "I Spy Christmas 1"); i2, ai2 = mk_ispy(402, "I Spy Christmas 2")
    pages = [p_advent, p_hunt, i1, i2, p_draw, p_wyr] + [mk_bingo(410 + k, k) for k in range(1, 5)] + [p_calling]
    build("5_Christmas_Screen_Free_Activity_Pack.pdf",
          dict(title_lines=["Christmas", "Screen-Free Fun"], badge="Ages 4–9  •  11 Activity Pages",
               icons=["tree", "candycane", "gift", "snowman", "star"],
               inside=["25 Days of Christmas activity calendar", "Indoor scavenger hunt", "2 I Spy counting pages",
                       "Drawing prompts + Would You Rather cards", "4 bingo cards + calling cards"]),
          pages, [answer_text_page("Answer Key", [("I Spy 1", ai1), ("I Spy 2", ai2)])])
    # ---- FREE ----
    od, ao = mk_odd(501, "Odd One Out"); ct, ac = mk_count(502, "Count & Write")
    mp, mm = mk_maze_page(503, "Christmas Maze", "Easy", 8, 9)
    def promo(c, P):
        frame(c, P, "Loved these? There's more!", "Full Christmas packs from BodhiCubs", name=False)
        items = [("Christmas Math Worksheets", "11 worksheets • ages 5–7"), ("Word Search & Scramble", "7 puzzle pages • ages 6–9"),
                 ("Mazes & Logic Puzzles", "6 mazes + picture sudoku • ages 5–8"), ("Winter Break Routine Charts", "9 printables • ages 4–9"),
                 ("Screen-Free Activity Pack", "Advent calendar, bingo & more • ages 4–9")]
        for i, (a, b) in enumerate(items):
            y = TOP - 30 - i * 82
            stroke(c, P["ink"]); c.setLineWidth(1.4); fill(c, P["soft"]); c.roundRect(70, y - 44, W - 140, 66, 14, 1, 1)
            icon(c, ["ornament", "star", "gift", "snowman", "tree"][i], 108, y - 11, 46, P)
            text(c, 145, y - 6, a, "PB", 16, P["ink"], "l"); text(c, 145, y - 28, b, "PR", 12, P["grey"], "l")
        instr(c, P, 120, "Find them in the BodhiCubs shop.", 15)
        instr(c, P, 92, "Play free learning games for kids at BodhiCubs!", 13)
    build("0_FREE_Christmas_Brain_Teasers_Mini_Pack.pdf",
          dict(title_lines=["FREE Christmas", "Brain Teasers"], badge="Ages 5–8  •  3 Activities",
               inside=["Odd one out", "Count & write", "Christmas maze", "Answer key"],
               footer="Free to print and share the link  •  BodhiCubs"),
          [od, ct, mp], [answer_text_page("Answer Key", [("Odd One Out", ao), ("Count & Write", ac), ("Maze", ["See solved maze below"])]),
                         maze_answer_page([mm], ["Christmas Maze"])] if False else
          [answer_text_page("Answer Key", [("Odd One Out", ao), ("Count & Write", ac)]), maze_answer_page([mm], ["Christmas Maze"])])
    # append promo to free pack: rebuild with promo as last page
    from reportlab.pdfgen import canvas as cv
    return promo, (od, ct, mp), (ao, ac, mm)

if __name__ == "__main__":
    promo, pages, (ao, ac, mm) = run()
    meta = dict(title_lines=["FREE Christmas", "Brain Teasers"], badge="Ages 5–8  •  3 Activities",
                inside=["Odd one out", "Count & write", "Christmas maze", "Answer key"],
                footer="Free to print  •  BodhiCubs")
    c = canvas.Canvas(OUT + "0_FREE_Christmas_Brain_Teasers_Mini_Pack.pdf", pagesize=letter)
    c.setTitle("FREE Christmas Brain Teasers"); c.setAuthor("BodhiCubs")
    cover(c, meta); c.showPage()
    for p in pages: p(c, COLOR); c.showPage()
    answer_text_page("Answer Key", [("Odd One Out", ao), ("Count & Write", ac)])(c, COLOR); c.showPage()
    maze_answer_page([mm], ["Christmas Maze"])(c, COLOR); c.showPage()
    promo(c, COLOR); c.showPage()
    c.save()
    print("built")
