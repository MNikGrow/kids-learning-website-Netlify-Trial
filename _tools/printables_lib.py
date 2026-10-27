import math, random
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import simpleSplit

W, H = letter
GF = "/usr/share/fonts/truetype/google-fonts/"
pdfmetrics.registerFont(TTFont("PB", GF + "Poppins-Bold.ttf"))
pdfmetrics.registerFont(TTFont("PM", GF + "Poppins-Medium.ttf"))
pdfmetrics.registerFont(TTFont("PR", GF + "Poppins-Regular.ttf"))

COLOR = dict(red=(0.86, 0.2, 0.24), green=(0.15, 0.58, 0.36), dkgreen=(0.08, 0.42, 0.26),
             gold=(0.99, 0.77, 0.18), blue=(0.27, 0.56, 0.86), brown=(0.56, 0.36, 0.2),
             orange=(0.98, 0.55, 0.15), white=(1, 1, 1), ink=(0.16, 0.16, 0.22),
             band=(0.86, 0.2, 0.24), bandtxt=(1, 1, 1), light=(1, 0.96, 0.9), soft=(0.93, 0.97, 0.94),
             grey=(0.55, 0.55, 0.6), hi=(0.99, 0.77, 0.18), stripe=(1, 1, 1), acc=(0.86, 0.2, 0.24), bw=False)
BW = {k: (1, 1, 1) for k in COLOR}
BW.update(ink=(0, 0, 0), bandtxt=(0, 0, 0), grey=(0.45, 0.45, 0.45), hi=(0.6, 0.6, 0.6),
          stripe=(0.72, 0.72, 0.72), acc=(0, 0, 0), bw=True)

# ---------- basic helpers ----------
def fill(c, rgb): c.setFillColorRGB(*rgb)
def stroke(c, rgb): c.setStrokeColorRGB(*rgb)

def text(c, x, y, s, font="PR", size=12, rgb=(0.16, 0.16, 0.22), align="c"):
    c.setFont(font, size); fill(c, rgb)
    if align == "c": c.drawCentredString(x, y, s)
    elif align == "l": c.drawString(x, y, s)
    else: c.drawRightString(x, y, s)

def fit(s, font, size, maxw):
    while pdfmetrics.stringWidth(s, font, size) > maxw and size > 6: size -= 0.5
    return size

def wrap(c, x, y, s, font, size, maxw, rgb, lead=None, align="c"):
    lines = simpleSplit(s, font, size, maxw)
    lead = lead or size * 1.2
    for i, ln in enumerate(lines):
        text(c, x, y - i * lead, ln, font, size, rgb, align)
    return len(lines)

def poly(c, pts, f=1, s=1):
    p = c.beginPath(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    p.close(); c.drawPath(p, fill=f, stroke=s)

def star_pts(cx, cy, r, ri=None, n=5, rot=90):
    ri = ri or r * 0.45; pts = []
    for i in range(n * 2):
        a = math.radians(rot + i * 180 / n); rr = r if i % 2 == 0 else ri
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts

# ---------- icons (unit box -0.5..0.5) ----------
def _start(c, x, y, s, P):
    c.saveState(); c.translate(x, y); c.scale(s, s)
    c.setLineWidth(0.035); c.setLineJoin(1); c.setLineCap(1); stroke(c, P["ink"])

def ic_tree(c, x, y, s, P):
    _start(c, x, y, s, P)
    fill(c, P["brown"]); c.rect(-0.07, -0.47, 0.14, 0.14, fill=1, stroke=1)
    fill(c, P["green"])
    poly(c, [(-0.42, -0.34), (0.42, -0.34), (0, 0.08)])
    poly(c, [(-0.34, -0.12), (0.34, -0.12), (0, 0.26)])
    poly(c, [(-0.25, 0.08), (0.25, 0.08), (0, 0.38)])
    fill(c, P["red"]); c.circle(-0.16, -0.24, 0.04, 1, 1); c.circle(0.12, -0.05, 0.04, 1, 1)
    fill(c, P["gold"]); poly(c, star_pts(0, 0.4, 0.1))
    c.restoreState()

def ic_star(c, x, y, s, P):
    _start(c, x, y, s, P); fill(c, P["gold"]); poly(c, star_pts(0, -0.02, 0.48, 0.21)); c.restoreState()

def ic_gift(c, x, y, s, P):
    _start(c, x, y, s, P)
    fill(c, P["red"]); c.rect(-0.36, -0.44, 0.72, 0.56, 1, 1)
    fill(c, P["gold"]); c.rect(-0.07, -0.44, 0.14, 0.56, 1, 1)
    fill(c, P["red"]); c.rect(-0.42, 0.12, 0.84, 0.14, 1, 1)
    fill(c, P["gold"]); c.rect(-0.07, 0.12, 0.14, 0.14, 1, 1)
    c.ellipse(-0.3, 0.26, -0.02, 0.44, 1, 1); c.ellipse(0.02, 0.26, 0.3, 0.44, 1, 1)
    c.restoreState()

def ic_ornament(c, x, y, s, P):
    _start(c, x, y, s, P)
    c.circle(0, 0.43, 0.05, 1, 0)
    fill(c, P["gold"]); c.rect(-0.1, 0.28, 0.2, 0.11, 1, 1)
    fill(c, P["blue"]); c.circle(0, -0.07, 0.37, 1, 1)
    c.setLineWidth(0.07); stroke(c, P["gold"] if not P["bw"] else P["ink"])
    c.line(-0.33, -0.07, 0.33, -0.07)
    c.restoreState()

def ic_bell(c, x, y, s, P):
    _start(c, x, y, s, P)
    fill(c, P["gold"])
    c.circle(0, -0.34, 0.08, 1, 1)
    p = c.beginPath(); p.moveTo(-0.4, -0.28); p.lineTo(0.4, -0.28)
    p.curveTo(0.26, -0.16, 0.3, 0.06, 0.26, 0.16); p.curveTo(0.2, 0.4, -0.2, 0.4, -0.26, 0.16)
    p.curveTo(-0.3, 0.06, -0.26, -0.16, -0.4, -0.28); p.close(); c.drawPath(p, 1, 1)
    fill(c, P["red"]); c.circle(0, 0.38, 0.06, 1, 1)
    c.restoreState()

def ic_snowman(c, x, y, s, P):
    _start(c, x, y, s, P)
    fill(c, P["white"]); c.circle(0, -0.22, 0.25, 1, 1); c.circle(0, 0.13, 0.17, 1, 1)
    fill(c, P["ink"]); c.rect(-0.15, 0.27, 0.3, 0.04, 1, 1); c.rect(-0.09, 0.3, 0.18, 0.17, 1, 1)
    c.circle(-0.06, 0.16, 0.025, 0, 1); c.circle(0.06, 0.16, 0.025, 0, 1)
    c.circle(0, -0.12, 0.025, 0, 1); c.circle(0, -0.24, 0.025, 0, 1)
    fill(c, P["orange"]); poly(c, [(0, 0.12), (0, 0.08), (0.14, 0.1)])
    fill(c, P["red"]); c.rect(-0.16, -0.02, 0.32, 0.06, 1, 1)
    c.restoreState()

def ic_snowflake(c, x, y, s, P):
    _start(c, x, y, s, P)
    c.setLineWidth(0.06); stroke(c, P["blue"] if not P["bw"] else P["ink"])
    for i in range(6):
        a = math.radians(90 + i * 60); ca, sa = math.cos(a), math.sin(a)
        c.line(0, 0, 0.45 * ca, 0.45 * sa)
        for d in (0.25,):
            bx, by = d * ca, d * sa
            for sgn in (-1, 1):
                b = a + sgn * math.radians(40)
                c.line(bx, by, bx + 0.13 * math.cos(b), by + 0.13 * math.sin(b))
    c.restoreState()

def ic_candycane(c, x, y, s, P):
    _start(c, x, y, s, P)
    def path():
        p = c.beginPath(); p.moveTo(0.1, -0.44); p.lineTo(0.1, 0.16)
        p.curveTo(0.1, 0.46, -0.3, 0.46, -0.3, 0.16); p.lineTo(-0.3, 0.06); return p
    c.setLineWidth(0.2); stroke(c, P["ink"]); c.drawPath(path(), stroke=1, fill=0)
    c.setLineWidth(0.13); stroke(c, P["red"] if not P["bw"] else P["white"]); c.drawPath(path(), stroke=1, fill=0)
    c.setLineCap(0); c.setDash(0.07, 0.07); stroke(c, P["stripe"] if P["bw"] else P["white"]); c.drawPath(path(), stroke=1, fill=0)
    c.restoreState()

def ic_mitten(c, x, y, s, P):
    _start(c, x, y, s, P)
    fill(c, P["green"])
    c.ellipse(-0.36, -0.08, -0.08, 0.2, 1, 1)
    c.roundRect(-0.22, -0.3, 0.44, 0.72, 0.2, 1, 1)
    fill(c, P["white"]); c.roundRect(-0.25, -0.46, 0.5, 0.18, 0.05, 1, 1)
    c.restoreState()

ICONS = dict(tree=ic_tree, star=ic_star, gift=ic_gift, ornament=ic_ornament, bell=ic_bell,
             snowman=ic_snowman, snowflake=ic_snowflake, candycane=ic_candycane, mitten=ic_mitten)
NAMES = dict(tree="tree", star="star", gift="gift", ornament="ornament", bell="bell", snowman="snowman",
             snowflake="snowflake", candycane="candy cane", mitten="mitten")

def icon(c, name, x, y, s, P): ICONS[name](c, x, y, s, P)

# ---------- page frame ----------
TOP = H - 150
def frame(c, P, title, sub=None, name=True, brand="BodhiCubs"):
    stroke(c, P["ink"]); c.setLineWidth(1.5)
    fill(c, P["band"]); c.roundRect(36, H - 112, W - 72, 76, 18, stroke=1 if P["bw"] else 0, fill=1)
    sz = fit(title, "PB", 26, W - 200)
    text(c, W / 2, H - 72 if sub else H - 82, title, "PB", sz, P["bandtxt"])
    if sub: text(c, W / 2, H - 96, sub, "PM", 11.5, P["bandtxt"])
    icon(c, "star", 70, H - 74, 34, P); icon(c, "snowflake", W - 70, H - 74, 34, P)
    if name:
        text(c, 40, H - 140, "Name: ______________________________", "PM", 11, P["ink"], "l")
        text(c, W - 40, H - 140, "Date: ______________", "PM", 11, P["ink"], "r")
    text(c, W / 2, 22, f"© 2026 {brand}  •  Personal & single-classroom use only", "PR", 8, P["grey"])

def instr(c, P, y, s, size=13):
    return wrap(c, W / 2, y, s, "PM", size, W - 100, P["ink"])

def answer_box(c, P, x, y, w=46, h=36):
    stroke(c, P["ink"]); c.setLineWidth(1.4); fill(c, P["white"]); c.roundRect(x, y, w, h, 8, 1, 1)

# ---------- scatter ----------
def scatter(rng, counts, box, size, tries=4000):
    x0, y0, x1, y1 = box; pts = []
    items = [n for n, k in counts.items() for _ in range(k)]; rng.shuffle(items)
    for it in items:
        for _ in range(tries):
            x = rng.uniform(x0 + size / 2, x1 - size / 2); y = rng.uniform(y0 + size / 2, y1 - size / 2)
            if all((x - a) ** 2 + (y - b) ** 2 > (size * 1.05) ** 2 for a, b, _ in pts):
                pts.append((x, y, it)); break
        else:
            raise RuntimeError("scatter failed")
    return pts

# ---------- word search ----------
def make_wordsearch(words, n, dirs, seed):
    rng = random.Random(seed)
    for attempt in range(200):
        g = [[None] * n for _ in range(n)]; placed = []; ok = True
        for w in sorted(words, key=len, reverse=True):
            done = False
            for _ in range(800):
                dr, dc = rng.choice(dirs); r = rng.randrange(n); cc = rng.randrange(n)
                er, ec = r + dr * (len(w) - 1), cc + dc * (len(w) - 1)
                if not (0 <= er < n and 0 <= ec < n): continue
                if all(g[r + dr * i][cc + dc * i] in (None, w[i]) for i in range(len(w))):
                    for i in range(len(w)): g[r + dr * i][cc + dc * i] = w[i]
                    placed.append((w, r, cc, dr, dc)); done = True; break
            if not done: ok = False; break
        if ok:
            for r in range(n):
                for cc in range(n):
                    if g[r][cc] is None: g[r][cc] = rng.choice("ABCDEFGHIJKLMNOPRSTUVWY")
            return g, placed
    raise RuntimeError("wordsearch failed")

def draw_wordsearch(c, P, g, placed, x, y, size, answers=False):
    n = len(g); cs = size / n
    stroke(c, P["ink"]); c.setLineWidth(2); fill(c, P["white"]); c.roundRect(x - 8, y - 8, size + 16, size + 16, 12, 1, 1)
    if answers:
        c.saveState(); c.setStrokeColorRGB(*P["hi"]); c.setStrokeAlpha(0.55); c.setLineCap(1); c.setLineWidth(cs * 0.72)
        for w, r, cc, dr, dc in placed:
            er, ec = r + dr * (len(w) - 1), cc + dc * (len(w) - 1)
            c.line(x + (cc + .5) * cs, y + size - (r + .5) * cs, x + (ec + .5) * cs, y + size - (er + .5) * cs)
        c.restoreState()
    fs = cs * 0.55
    for r in range(n):
        for cc in range(n):
            text(c, x + (cc + .5) * cs, y + size - (r + .5) * cs - fs * 0.36, g[r][cc], "PM", fs, P["ink"])

# ---------- maze ----------
def make_maze(w, h, seed):
    rng = random.Random(seed)
    walls = {(r, cc): {"N", "S", "E", "W"} for r in range(h) for cc in range(w)}
    D = {"N": (-1, 0, "S"), "S": (1, 0, "N"), "E": (0, 1, "W"), "W": (0, -1, "E")}
    stack = [(0, 0)]; seen = {(0, 0)}
    while stack:
        r, cc = stack[-1]
        nb = [(d, r + dr, cc + dc, o) for d, (dr, dc, o) in D.items() if (r + dr, cc + dc) in walls and (r + dr, cc + dc) not in seen]
        if not nb: stack.pop(); continue
        d, nr, nc, o = rng.choice(nb)
        walls[(r, cc)].discard(d); walls[(nr, nc)].discard(o); seen.add((nr, nc)); stack.append((nr, nc))
    walls[(0, 0)].discard("N"); walls[(h - 1, w - 1)].discard("S")
    # solve
    from collections import deque
    prev = {(0, 0): None}; q = deque([(0, 0)])
    while q:
        cur = q.popleft()
        if cur == (h - 1, w - 1): break
        for d, (dr, dc, o) in D.items():
            nx = (cur[0] + dr, cur[1] + dc)
            if d not in walls[cur] and nx in walls and nx not in prev: prev[nx] = cur; q.append(nx)
    path = []; cur = (h - 1, w - 1)
    while cur: path.append(cur); cur = prev[cur]
    return dict(w=w, h=h, walls=walls, path=path[::-1])

def draw_maze(c, P, m, x, y, maxw, maxh, answers=False, icons=("gift", "tree"), lw=2.2):
    cs = min(maxw / m["w"], maxh / m["h"]); mw, mh = cs * m["w"], cs * m["h"]
    x += (maxw - mw) / 2; y += (maxh - mh) / 2
    top = y + mh
    if answers:
        c.saveState(); stroke(c, P["red"] if not P["bw"] else P["grey"]); c.setLineWidth(cs * 0.3); c.setLineCap(1); c.setLineJoin(1)
        pts = [(x + (cc + .5) * cs, top - (r + .5) * cs) for r, cc in m["path"]]
        pts = [(pts[0][0], top + cs * 0.4)] + pts + [(pts[-1][0], y - cs * 0.4)]
        p = c.beginPath(); p.moveTo(*pts[0])
        for q in pts[1:]: p.lineTo(*q)
        c.drawPath(p, stroke=1, fill=0); c.restoreState()
    stroke(c, P["ink"]); c.setLineWidth(lw); c.setLineCap(1)
    for (r, cc), ws in m["walls"].items():
        x0, y0 = x + cc * cs, top - r * cs
        if "N" in ws: c.line(x0, y0, x0 + cs, y0)
        if "S" in ws: c.line(x0, y0 - cs, x0 + cs, y0 - cs)
        if "W" in ws: c.line(x0, y0, x0, y0 - cs)
        if "E" in ws: c.line(x0 + cs, y0, x0 + cs, y0 - cs)
    isz = max(26, min(48, cs * 1.6))
    if icons:
        icon(c, icons[0], x + cs / 2, top + isz * 0.6, isz, P)
        icon(c, icons[1], x + mw - cs / 2, y - isz * 0.6, isz, P)

# ---------- 4x4 picture sudoku ----------
def _count(g, limit=2):
    for i in range(16):
        if g[i] is None:
            r, cc = divmod(i, 4); cnt = 0
            for v in range(4):
                if all(g[r * 4 + k] != v for k in range(4)) and all(g[k * 4 + cc] != v for k in range(4)) and \
                   all(g[(r // 2 * 2 + a) * 4 + cc // 2 * 2 + b] != v for a in range(2) for b in range(2)):
                    g[i] = v; cnt += _count(g, limit); g[i] = None
                    if cnt >= limit: return cnt
            return cnt
    return 1

def make_sudoku(seed, givens=7):
    rng = random.Random(seed)
    base = [[0, 1, 2, 3], [2, 3, 0, 1], [1, 0, 3, 2], [3, 2, 1, 0]]
    sym = list(range(4)); rng.shuffle(sym)
    bands = [0, 1]; rng.shuffle(bands); rows = []
    for b in bands:
        rr = [b * 2, b * 2 + 1]; rng.shuffle(rr); rows += rr
    stacks = [0, 1]; rng.shuffle(stacks); cols = []
    for s_ in stacks:
        cc = [s_ * 2, s_ * 2 + 1]; rng.shuffle(cc); cols += cc
    sol = [sym[base[r][cc]] for r in rows for cc in cols]
    puz = sol[:]; idx = list(range(16)); rng.shuffle(idx)
    for i in idx:
        if sum(v is not None for v in puz) <= givens: break
        keep = puz[i]; puz[i] = None
        if _count(puz[:]) != 1: puz[i] = keep
    return puz, sol

def draw_sudoku(c, P, g, syms, x, y, size, lw=2):
    cs = size / 4
    stroke(c, P["ink"]); fill(c, P["white"]); c.setLineWidth(lw * 1.6); c.rect(x, y, size, size, 1, 1)
    for i in range(1, 4):
        c.setLineWidth(lw * (1.6 if i == 2 else 0.7))
        c.line(x + i * cs, y, x + i * cs, y + size); c.line(x, y + i * cs, x + size, y + i * cs)
    for i, v in enumerate(g):
        if v is None: continue
        r, cc = divmod(i, 4); icon(c, syms[v], x + (cc + .5) * cs, y + size - (r + .5) * cs, cs * 0.7, P)
