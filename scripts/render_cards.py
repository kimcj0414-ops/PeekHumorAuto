"""'스치듯 어른' 5장 명언 카드뉴스 (1080x1350, 4:5). HTML+SVG 장면을 헤드리스 크롬으로 찍는다.
사용: python3 scripts/render_cards.py set.json 출력폴더
set.json: {"title":..., "cards":[{"label":"우리가 흔히 착각하는 것","lines":[...],"desc":[...],"scene":"lamp|window|door|dusk|candle"}...]}
글꼴: fonts/NotoSerifKR.ttf (SIL OFL)
"""
import html, json, os, sys

W, H = 1080, 1350
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.abspath(os.path.join(HERE, "..", "fonts", "NotoSerifKR.ttf"))
BRAND = "스치듯 어른"
# 세트마다 바꾸는 빛의 색 (장면 레이어에만 적용)
PALETTES = {"amber": "none", "moon": "hue-rotate(185deg) saturate(.7)", "rose": "hue-rotate(-28deg) saturate(1.15)",
            "mist": "hue-rotate(95deg) saturate(.45)", "gold": "hue-rotate(12deg) saturate(.8) brightness(1.05)"}

SCENES = {
 # 어둠 속 가로등 하나
 "lamp": """
  <defs><radialGradient id="g" cx="74%" cy="44%" r="60%"><stop offset="0" stop-color="#f3b866" stop-opacity=".55"/><stop offset=".35" stop-color="#8a5a2b" stop-opacity=".18"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
  <linearGradient id="c" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd59a" stop-opacity=".38"/><stop offset="1" stop-color="#ffd59a" stop-opacity="0"/></linearGradient></defs>
  <rect width="1080" height="1350" fill="#0c0d12"/><rect width="1080" height="1350" fill="url(#g)"/>
  <polygon points="800,600 600,1350 1000,1350" fill="url(#c)" filter="url(#b)"/>
  <rect x="796" y="600" width="8" height="750" fill="#050507"/><rect x="770" y="584" width="60" height="20" rx="4" fill="#050507"/>
  <circle cx="800" cy="610" r="10" fill="#ffe2b0" filter="url(#b)"/>
  <ellipse cx="800" cy="1330" rx="260" ry="26" fill="#f0b46a" opacity=".16" filter="url(#b)"/>""",
 # 어두운 방, 창문으로 드는 빛
 "window": """
  <defs><linearGradient id="w" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f6c98a"/><stop offset="1" stop-color="#b9783c"/></linearGradient>
  <linearGradient id="f" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e9b57a" stop-opacity=".32"/><stop offset="1" stop-color="#e9b57a" stop-opacity=".04"/></linearGradient></defs>
  <rect width="1080" height="1350" fill="#121014"/>
  <rect x="640" y="560" width="300" height="420" fill="url(#w)" opacity=".9"/>
  <rect x="784" y="560" width="12" height="420" fill="#121014"/><rect x="640" y="764" width="300" height="12" fill="#121014"/>
  <polygon points="640,980 940,980 760,1350 260,1350" fill="url(#f)" filter="url(#b)"/>
  <rect x="0" y="1180" width="1080" height="170" fill="#000" opacity=".25"/>""",
 # 반쯤 열린 문 틈의 빛
 "door": """
  <defs><linearGradient id="s" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffe0ad" stop-opacity="0"/><stop offset=".5" stop-color="#ffe0ad"/><stop offset="1" stop-color="#ffe0ad" stop-opacity="0"/></linearGradient>
  <linearGradient id="sp" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f2be7c" stop-opacity=".35"/><stop offset="1" stop-color="#f2be7c" stop-opacity="0"/></linearGradient></defs>
  <rect width="1080" height="1350" fill="#0d0c0f"/>
  <rect x="520" y="520" width="380" height="720" fill="#18151a"/>
  <rect x="700" y="520" width="26" height="720" fill="url(#s)" filter="url(#b)"/>
  <polygon points="700,1240 726,1240 1000,1350 480,1350" fill="url(#sp)" filter="url(#b)"/>""",
 # 해 질 녘 지평선
 "dusk": """
  <defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b0d16"/><stop offset=".55" stop-color="#2a2230"/><stop offset=".8" stop-color="#9a5a35"/><stop offset="1" stop-color="#e3a15c"/></linearGradient>
  <radialGradient id="sun" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#ffd9a0"/><stop offset=".4" stop-color="#f3a35a" stop-opacity=".6"/><stop offset="1" stop-color="#f3a35a" stop-opacity="0"/></radialGradient></defs>
  <rect width="1080" height="1350" fill="url(#sky)"/>
  <circle cx="700" cy="1130" r="260" fill="url(#sun)"/><circle cx="700" cy="1130" r="54" fill="#ffe4b8"/>
  <path d="M0 1120 Q 200 1080 380 1110 T 760 1100 T 1080 1090 V1350 H0Z" fill="#0a0a0e"/>
  <path d="M0 1190 Q 300 1150 600 1185 T 1080 1170 V1350 H0Z" fill="#050507"/>""",
 # 어둠 속 촛불 하나
 "candle": """
  <defs><radialGradient id="cg" cx="50%" cy="76%" r="55%"><stop offset="0" stop-color="#f6b25e" stop-opacity=".55"/><stop offset=".3" stop-color="#7a4a22" stop-opacity=".2"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
  <radialGradient id="fl" cx="50%" cy="60%" r="50%"><stop offset="0" stop-color="#fff4d6"/><stop offset=".5" stop-color="#ffc265"/><stop offset="1" stop-color="#ff9a3c" stop-opacity="0"/></radialGradient></defs>
  <rect width="1080" height="1350" fill="#09090b"/><rect width="1080" height="1350" fill="url(#cg)"/>
  <rect x="510" y="1060" width="60" height="200" rx="6" fill="#e8dcc6" opacity=".85"/><rect x="510" y="1060" width="60" height="200" rx="6" fill="#000" opacity=".25"/>
  <rect x="538" y="1036" width="4" height="26" fill="#222"/>
  <ellipse cx="540" cy="1008" rx="22" ry="48" fill="url(#fl)" filter="url(#b)"/>
  <ellipse cx="540" cy="1262" rx="230" ry="22" fill="#f0a75a" opacity=".12" filter="url(#b)"/>""",
}

SCENES.update({
 # 비 오는 창
 "rain": """
  <defs><linearGradient id="rw" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a4150"/><stop offset="1" stop-color="#c88a4e"/></linearGradient></defs>
  <rect width="1080" height="1350" fill="#0d0f14"/>
  <rect x="560" y="480" width="420" height="640" fill="url(#rw)" opacity=".75"/>
  <circle cx="820" cy="980" r="60" fill="#ffcf8a" opacity=".55" filter="url(#b)"/><circle cx="660" cy="900" r="36" fill="#ffd9a0" opacity=".4" filter="url(#b)"/>
  """ + "".join(f'<line x1="{560+((i*53)%420)}" y1="{480+((i*97)%560)}" x2="{562+((i*53)%420)}" y2="{540+((i*97)%560)}" stroke="#e6edf5" stroke-opacity=".35" stroke-width="2"/>' for i in range(60)) + """
  <rect x="764" y="480" width="12" height="640" fill="#0d0f14"/><rect x="560" y="790" width="420" height="12" fill="#0d0f14"/>""",
 # 달빛 바다
 "sea": """
  <defs><linearGradient id="ss" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#07090f"/><stop offset=".7" stop-color="#1b2232"/><stop offset="1" stop-color="#2b3346"/></linearGradient></defs>
  <rect width="1080" height="1350" fill="url(#ss)"/>
  <circle cx="760" cy="760" r="70" fill="#f4e6c8"/><circle cx="760" cy="760" r="180" fill="#f4e6c8" opacity=".12" filter="url(#b)"/>
  <rect x="0" y="960" width="1080" height="390" fill="#080a10"/>
  """ + "".join(f'<rect x="{760-w//2}" y="{980+i*26}" width="{w}" height="5" rx="2" fill="#f4e6c8" opacity="{0.55-i*0.04:.2f}"/>' for i,w in enumerate([120,180,90,220,140,260,100,200,160,240,120,180])),
 # 빈 의자와 전구
 "chair": """
  <rect width="1080" height="1350" fill="#0e0c0c"/>
  <line x1="760" y1="0" x2="760" y2="560" stroke="#222" stroke-width="3"/>
  <circle cx="760" cy="580" r="26" fill="#ffd9a0"/><circle cx="760" cy="600" r="320" fill="#e9a65c" opacity=".16" filter="url(#b)"/>
  <ellipse cx="760" cy="1240" rx="300" ry="40" fill="#e9a65c" opacity=".14" filter="url(#b)"/>
  <g fill="#040404"><rect x="660" y="900" width="200" height="22"/><rect x="660" y="740" width="18" height="182"/><rect x="842" y="740" width="18" height="182"/><rect x="660" y="740" width="200" height="16"/>
  <rect x="666" y="920" width="16" height="320"/><rect x="838" y="920" width="16" height="320"/></g>""",
 # 빛이 내려오는 계단
 "stairs": """
  <defs><linearGradient id="st" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6c88c" stop-opacity=".55"/><stop offset="1" stop-color="#f6c88c" stop-opacity="0"/></linearGradient></defs>
  <rect width="1080" height="1350" fill="#0c0b0e"/>
  <polygon points="620,420 1080,420 1080,1350 300,1350" fill="url(#st)" opacity=".5" filter="url(#b)"/>
  """ + "".join(f'<rect x="{300+i*40}" y="{1290-i*70}" width="{780-i*40}" height="{70}" fill="#{"151317" if i%2 else "1c191e"}"/>' for i in range(12)),
 # 구름 사이 큰 달
 "moon": """
  <defs><radialGradient id="mh" cx="50%" cy="50%" r="50%"><stop offset=".4" stop-color="#efe3c6" stop-opacity=".22"/><stop offset="1" stop-color="#efe3c6" stop-opacity="0"/></radialGradient></defs>
  <rect width="1080" height="1350" fill="#090b12"/>
  <circle cx="720" cy="980" r="460" fill="url(#mh)"/><circle cx="720" cy="980" r="190" fill="#efe3c6"/>
  <ellipse cx="520" cy="1150" rx="420" ry="70" fill="#0d0f17" opacity=".95" filter="url(#b)"/><ellipse cx="900" cy="1190" rx="300" ry="60" fill="#0d0f17" opacity=".9" filter="url(#b)"/>""",
 # 밤 기차역 승강장
 "station": """
  <rect width="1080" height="1350" fill="#0b0c10"/>
  <polygon points="540,760 560,760 1080,1350 0,1350" fill="#16171d"/>
  <line x1="548" y1="760" x2="250" y2="1350" stroke="#c9a46e" stroke-opacity=".5" stroke-width="4"/><line x1="552" y1="760" x2="830" y2="1350" stroke="#c9a46e" stroke-opacity=".5" stroke-width="4"/>
  """ + "".join(f'<circle cx="{560+ (i*i*9)}" cy="{700-i*28}" r="{4+i*3}" fill="#ffd79c" opacity=".9"/><circle cx="{560+(i*i*9)}" cy="{700-i*28}" r="{20+i*12}" fill="#ffc06a" opacity=".12" filter="url(#b)"/>' for i in range(1,8)),
 # 눈 내리는 길
 "snow": """
  <defs><linearGradient id="sn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0a0d14"/><stop offset="1" stop-color="#26303f"/></linearGradient></defs>
  <rect width="1080" height="1350" fill="url(#sn)"/>
  <polygon points="520,880 560,880 900,1350 180,1350" fill="#d9dee6" opacity=".18"/>
  <circle cx="540" cy="880" r="14" fill="#ffd9a0"/><circle cx="540" cy="880" r="120" fill="#ffd9a0" opacity=".15" filter="url(#b)"/>
  """ + "".join(f'<circle cx="{(i*131)%1080}" cy="{(i*277)%1350}" r="{1+(i%4)}" fill="#fff" opacity="{0.25+(i%5)*0.1:.2f}"/>' for i in range(140)),
 # 언덕 위 나무 한 그루
 "tree": """
  <defs><linearGradient id="tr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b0c14"/><stop offset=".75" stop-color="#3a2a2c"/><stop offset="1" stop-color="#b9714a"/></linearGradient></defs>
  <rect width="1080" height="1350" fill="url(#tr)"/>
  <path d="M0 1180 Q 540 1040 1080 1180 V1350 H0Z" fill="#060608"/>
  <g stroke="#060608" stroke-linecap="round" fill="none"><path d="M760 1100 L760 860" stroke-width="22"/><path d="M760 960 L680 860 M760 920 L850 830 M760 880 L720 790 M760 870 L800 780 M680 860 L640 820 M850 830 L900 810" stroke-width="10"/></g>
  <circle cx="760" cy="800" r="140" fill="#060608" opacity=".9"/>"""
})


def esc(t):
    return html.escape(t)


def page(card, i, n, palette="amber"):
    lines = "<br>".join(esc(l) for l in card["lines"])
    desc = "<br>".join(esc(l) for l in card.get("desc", []))
    big = "final" if i == n else ""
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:S;src:url('file://{FONT}');font-weight:200 900}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;overflow:hidden;background:#000;font-family:S,serif;color:#f3ece0}}
svg{{position:absolute;inset:0}}\n.scene{{filter:{PALETTES.get(palette, "none")}}}
.shade{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.62) 0%,rgba(0,0,0,.35) 45%,rgba(0,0,0,0) 70%),radial-gradient(120% 90% at 50% 45%,rgba(0,0,0,0) 55%,rgba(0,0,0,.55) 100%)}}
.grain{{position:absolute;inset:0;opacity:.09;mix-blend-mode:overlay}}
.txt{{position:absolute;left:96px;right:96px;top:120px}}
.no{{font-size:28px;font-weight:500;letter-spacing:.12em;color:#d9b47c}}
.label{{font-size:30px;font-weight:500;color:#cdbfa8;margin-top:14px}}
.q{{font-size:66px;font-weight:600;line-height:1.5;margin-top:46px;word-break:keep-all;letter-spacing:-.01em;text-shadow:0 2px 18px rgba(0,0,0,.5)}}
.final .q{{font-size:74px}}
.rule{{width:64px;height:3px;background:#d9b47c;margin:44px 0 30px}}
.d{{font-size:36px;font-weight:400;line-height:1.6;color:#e2d8c6;word-break:keep-all;text-shadow:0 2px 12px rgba(0,0,0,.6)}}
.cta{{margin-top:56px;font-size:34px;font-weight:600;color:#e8c48c;letter-spacing:.01em}}
.brand{{position:absolute;right:96px;bottom:70px;font-size:30px;font-weight:500;color:#cdbfa8;letter-spacing:.06em}}
</style></head><body class="{big}">
<svg class="scene" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><defs><filter id="b" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter></defs>{SCENES[card['scene']]}</svg>
<div class="shade"></div>
<svg class="grain" viewBox="0 0 {W} {H}"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="{i}"/></filter><rect width="100%" height="100%" filter="url(#n)"/></svg>
<div class="txt"><div class="no">{i:02d} / {n:02d}</div><div class="label">{esc(card.get('label',''))}</div>
<div class="q">{lines}</div>{'<div class="rule"></div><div class="d">'+desc+'</div>' if desc else ''}{'<div class="cta">'+esc(card['cta'])+'</div>' if card.get('cta') else ''}</div>
<div class="brand">{BRAND}</div></body></html>"""


CTA = "팔로우하고 하루 한 문장 만나요"


def render(src, outdir):
    from playwright.sync_api import sync_playwright
    data = json.load(open(src, encoding="utf-8"))
    os.makedirs(outdir, exist_ok=True)
    cards = data["cards"]
    cards[-1].setdefault("cta", CTA)  # 마지막 장에 팔로우 문구
    with sync_playwright() as p:
        exe = "/usr/bin/google-chrome" if os.path.exists("/usr/bin/google-chrome") else None
        b = p.chromium.launch(**({"executable_path": exe} if exe else {}))
        pg = b.new_page(viewport={"width": W, "height": H})
        for i, c in enumerate(cards, 1):
            tmp = os.path.join(outdir, f"_card{i}.html")
            open(tmp, "w", encoding="utf-8").write(page(c, i, len(cards), data.get("palette", "amber")))
            pg.goto("file://" + os.path.abspath(tmp))
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(300)
            pg.screenshot(path=os.path.join(outdir, f"card_{i}.png"))
            os.remove(tmp)
        b.close()
    from PIL import Image
    ims = [Image.open(os.path.join(outdir, f"card_{i}.png")).convert("RGB") for i in range(1, len(cards) + 1)]
    sw = 360; sh = int(sw * H / W); pad = 14
    sheet = Image.new("RGB", (pad + len(ims) * (sw + pad), sh + 2 * pad), "#BBBBBB")
    for i, im in enumerate(ims):
        sheet.paste(im.resize((sw, sh)), (pad + i * (sw + pad), pad))
    sheet.save(os.path.join(outdir, "preview.png"), optimize=True)
    print("완료", outdir)


if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2])
