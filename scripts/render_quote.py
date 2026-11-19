"""'스치듯 어른' 명언 카드 그리기 (1080x1350).
사용: python3 scripts/render_quote.py quotes.json 출력폴더
quotes.json 항목: {"lines":["줄1","줄2"], "author":"마르쿠스 아우렐리우스", "work":"『명상록』 4권", "theme":"paper|night"}
글꼴: fonts/NotoSerifKR.ttf (SIL OFL, fonts/OFL.txt)
"""
import json, os, random, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1350
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "..", "fonts", "NotoSerifKR.ttf")
BRAND = "스치듯 어른"
THEMES = {
    "paper": {"bg": (245, 240, 230), "ink": (34, 32, 30), "sub": (110, 102, 92), "accent": (181, 84, 60)},
    "night": {"bg": (28, 32, 44), "ink": (242, 236, 224), "sub": (170, 164, 152), "accent": (214, 170, 110)},
}


def F(size, weight):
    f = ImageFont.truetype(FONT, size)
    f.set_variation_by_axes([weight])
    return f


def grain(im, amount=7, seed=1):
    rnd = random.Random(seed)
    noise = Image.effect_noise((W, H), 40).filter(ImageFilter.GaussianBlur(0.6))
    return Image.blend(im, Image.merge("RGB", (noise,) * 3), amount / 255)


def fit(d, lines, max_w, start=72, low=48):
    size = start
    while size > low:
        f = F(size, 600)
        if max(d.textlength(l, font=f) for l in lines) <= max_w:
            return f, size
        size -= 2
    return F(low, 600), low


def card(q, out):
    t = THEMES[q.get("theme", "paper")]
    im = Image.new("RGB", (W, H), t["bg"])
    im = grain(im, seed=hash(out) % 1000)
    d = ImageDraw.Draw(im)
    left = 110
    # 큰 따옴표
    d.text((left - 12, 150), "“", font=F(220, 700), fill=t["accent"])
    # 본문
    lines = q["lines"]
    f, size = fit(d, lines, W - left * 2)
    gap = int(size * 1.62)
    block = gap * len(lines)
    y = max(400, (H - block) // 2 - 10)
    for l in lines:
        d.text((left, y), l, font=f, fill=t["ink"])
        y += gap
    # 구분선 + 출처
    y += 34
    d.line([(left, y), (left + 70, y)], fill=t["accent"], width=4)
    y += 34
    d.text((left, y), q["author"], font=F(38, 500), fill=t["ink"])
    if q.get("work"):
        d.text((left, y + 58), q["work"], font=F(32, 400), fill=t["sub"])
    # 계정 이름
    bf = F(30, 500)
    d.text((W - left - d.textlength(BRAND, font=bf), H - 110), BRAND, font=bf, fill=t["sub"])
    im.save(out, optimize=True)


if __name__ == "__main__":
    src, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    for i, q in enumerate(json.load(open(src, encoding="utf-8")), 1):
        card(q, os.path.join(outdir, f"quote_{i}.png"))
    print("완료")
