import subprocess, glob, os, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = "/home/claude/xmas/out/"; PD = "/home/claude/xmas/pins/"; TMP = "/home/claude/xmas/chk/pin/"
os.makedirs(PD, exist_ok=True); os.makedirs(TMP, exist_ok=True)
GF = "/usr/share/fonts/truetype/google-fonts/"
def F(b, s): return ImageFont.truetype(GF + ("Poppins-Bold.ttf" if b else "Poppins-Medium.ttf"), s)
W, H = 1000, 1500
RED, GREEN, GOLD, CREAM, INK, BLUE = (214, 50, 60), (30, 130, 82), (252, 196, 46), (255, 246, 232), (40, 40, 56), (50, 100, 180)

def page(pdf, n, width):
    key = f"{TMP}{os.path.basename(pdf)[:2]}_{n}"
    if not os.path.exists(key + ".png"):
        subprocess.run(["pdftoppm", "-r", "130", "-png", "-singlefile", "-f", str(n), "-l", str(n), pdf, key], check=True)
    im = Image.open(key + ".png").convert("RGB")
    return im.resize((width, int(width * im.height / im.width)), Image.LANCZOS)

def paste(base, im, x, y, rot=0):
    im = im.convert("RGBA")
    if rot: im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    sh = Image.new("RGBA", (im.width + 60, im.height + 60), (0, 0, 0, 0))
    sh.paste((0, 0, 0, 100), (30, 30, 30 + im.width, 30 + im.height), im.split()[3])
    sh = sh.filter(ImageFilter.GaussianBlur(16))
    base.alpha_composite(sh, (x - 15, y - 5)); base.alpha_composite(im, (x, y))

def snow(im, seed):
    d = ImageDraw.Draw(im); r = random.Random(seed)
    for _ in range(40):
        x, y, s = r.randint(0, W), r.randint(0, H), r.randint(4, 12)
        d.ellipse((x - s, y - s, x + s, y + s), fill=(255, 255, 255, 70))

def centered_lines(d, lines, y, font, fill, gap=1.05):
    for ln in lines:
        d.text((W / 2, y), ln, font=font, fill=fill, anchor="mt"); y += int(font.size * gap)
    return y

def pill(d, cx, cy, txt, font, bg, fg, padx=34):
    w = d.textlength(txt, font=font); h = font.size + 30
    d.rounded_rectangle((cx - w / 2 - padx, cy - h / 2, cx + w / 2 + padx, cy + h / 2), radius=h / 2, fill=bg)
    d.text((cx, cy), txt, font=font, fill=fg, anchor="mm")

def pin_a(pdf, pages, lines, badge, color, name):
    im = Image.new("RGBA", (W, H), color + (255,)); snow(im, len(name))
    d = ImageDraw.Draw(im)
    fs = 96 if max(len(l) for l in lines) <= 14 else 80
    y = centered_lines(d, lines, 70, F(True, fs), (255, 255, 255))
    pill(d, W / 2, y + 50, badge, F(True, 40), GOLD, INK)
    top = y + 130
    paste(im, page(pdf, pages[1], 560), 380, top + 40, -5)
    paste(im, page(pdf, pages[0], 560), 60, top, 4)
    d = ImageDraw.Draw(im)
    d.rectangle((0, H - 110, W, H), fill=(255, 255, 255))
    d.text((W / 2, H - 55), "BodhiCubs  •  Free learning for kids", font=F(True, 40), fill=INK, anchor="mm")
    im.convert("RGB").save(PD + name + "_A.jpg", quality=92)

def pin_b(pdf, pg, lines, badge, color, name):
    im = Image.new("RGBA", (W, H), CREAM + (255,))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((-40, -40, W + 40, 300), radius=60, fill=color)
    fs = 82 if max(len(l) for l in lines) <= 16 else 70
    centered_lines(d, lines, 50, F(True, fs), (255, 255, 255))
    paste(im, page(pdf, pg, 760), 120, 340, -2)
    d = ImageDraw.Draw(im)
    d.ellipse((760, 250, 960, 450), fill=GOLD); d.text((860, 350), "FREE", font=F(True, 54), fill=INK, anchor="mm")
    pill(d, W / 2, H - 80, badge, F(True, 40), color, (255, 255, 255))
    im.convert("RGB").save(PD + name + "_B.jpg", quality=92)

P = lambda pre: glob.glob(OUT + pre + "*.pdf")[0]
SPECS = [
    ("0_", "01_BrainTeasers", [2, 4], 3, ["FREE Christmas", "Brain Teasers", "for Kids"], ["Christmas Brain", "Teasers for Kids"], "Printable PDF • Ages 5–8", GREEN),
    ("1_", "02_Math", [5, 3], 8, ["Christmas Math", "Worksheets"], ["Christmas Addition", "Worksheets"], "Ages 5–7 • 11 Pages", RED),
    ("2_", "03_WordSearch", [3, 7], 6, ["Christmas Word", "Search & Scramble"], ["Christmas Word", "Search for Kids"], "Ages 6–9 • With Answers", GREEN),
    ("3_", "04_Mazes", [3, 9], 8, ["Christmas Mazes", "& Logic Puzzles"], ["Christmas Mazes", "for Kids"], "Ages 5–8 • Easy to Hard", BLUE),
    ("4_", "05_Routine", [3, 4], 7, ["Winter Break", "Routine Charts"], ["30 Screen-Free", "Activities for Kids"], "Ages 4–9 • Printable", RED),
    ("5_", "06_ScreenFree", [3, 8], 9, ["25 Days of", "Christmas Fun"], ["Christmas Bingo", "Printable Cards"], "Screen-Free • Ages 4–9", GREEN),
]
for pre, name, pa, pb, la, lb, badge, col in SPECS:
    pdf = P(pre)
    pin_a(pdf, pa, la, "FREE PRINTABLE", col, name)
    pin_b(pdf, pb, lb, badge, col, name)
print("ok")
