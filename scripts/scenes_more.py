"""명언 카드 추가 장면 27가지 (render_cards.SCENES에 합쳐짐). 글자 자리(왼쪽 위)는 어둡게 비워 둔다."""
import math, random

R = random.Random(7)
BG = '<rect width="1080" height="1350" fill="{c}"/>'


_gid = [0]


def glow(x, y, r, color="#ffd29a", op=.18):
    """부드럽게 번지는 빛 (가장자리가 딱딱하지 않게 방사형 그라디언트)."""
    _gid[0] += 1
    g = f"gl{_gid[0]}"
    return (f'<defs><radialGradient id="{g}"><stop offset="0" stop-color="{color}" stop-opacity="{min(1, op*2.2):.2f}"/>'
            f'<stop offset=".45" stop-color="{color}" stop-opacity="{op*.8:.2f}"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient></defs>'
            f'<circle cx="{x}" cy="{y}" r="{r*1.4:.0f}" fill="url(#{g})"/>')


def lingrad(id_, stops, vertical=True):
    xy = 'x1="0" y1="0" x2="0" y2="1"' if vertical else 'x1="0" y1="0" x2="1" y2="0"'
    s = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
    return f'<linearGradient id="{id_}" {xy}>{s}</linearGradient>'


def stars(n, y_max=1350, seed=1):
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.randint(0,1080)}" cy="{r.randint(0,y_max)}" r="{r.choice([1,1,1.5,2])}" fill="#fff" opacity="{r.uniform(.2,.8):.2f}"/>' for _ in range(n))


S = {}

S["lighthouse"] = ('<defs>' + lingrad("lhs", [(0, "#07090f", 1), (1, "#1d2433", 1)]) + lingrad("beam", [(0, "#ffe2a8", .45), (1, "#ffe2a8", 0)], False) + '</defs>'
    '<rect width="1080" height="1350" fill="url(#lhs)"/>'
    '<defs><linearGradient id="beam2" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#ffe2a8" stop-opacity=".4"/><stop offset="1" stop-color="#ffe2a8" stop-opacity="0"/></linearGradient></defs><polygon points="800,740 300,600 300,880" fill="url(#beam2)"/>'
    '<path d="M560 1350 L620 1080 Q 760 1040 1080 1100 V1350Z" fill="#050608"/>'
    '<polygon points="770,1080 830,1080 815,760 785,760" fill="#0b0c10"/><rect x="778" y="720" width="44" height="40" fill="#ffe2a8"/>'
    + glow(800, 740, 90, "#ffe2a8", .35) + '<rect x="0" y="1180" width="620" height="170" fill="#0a0d14"/>')

S["boat"] = ('<defs>' + lingrad("bs", [(0, "#0a0c14", 1), (.6, "#3b2a2e", 1), (.75, "#a7643e", 1), (1, "#0a0c12", 1)]) + '</defs>'
    '<rect width="1080" height="1350" fill="url(#bs)"/><rect x="0" y="1010" width="1080" height="340" fill="#0b0d14"/>'
    + "".join(f'<rect x="{R.randint(450,900)}" y="{1030+i*22}" width="{R.randint(60,200)}" height="4" fill="#e3a464" opacity="{.4-i*.03:.2f}"/>' for i in range(12)) +
    '<path d="M600 1000 L860 1000 L820 1040 L640 1040Z" fill="#050507"/><line x1="730" y1="1000" x2="730" y2="840" stroke="#050507" stroke-width="6"/>'
    '<polygon points="734,850 734,990 820,990" fill="#050507"/>')

S["bridge"] = ('<rect width="1080" height="1350" fill="#0b0c12"/>'
    '<path d="M0 960 Q 540 640 1080 960" stroke="#050507" stroke-width="26" fill="none"/>'
    '<rect x="0" y="950" width="1080" height="24" fill="#050507"/>'
    + "".join(f'<line x1="{x}" y1="{960 - 320*math.sin(math.pi*x/1080)*0.95:.0f}" x2="{x}" y2="952" stroke="#050507" stroke-width="5"/>' for x in range(80, 1080, 80)) +
    "".join(glow(x, 940, 26, "#ffcf8a", .5) + f'<circle cx="{x}" cy="940" r="5" fill="#ffe1b0"/>' for x in range(60, 1080, 120)) +
    '<rect x="0" y="980" width="1080" height="370" fill="#0e1018"/>'
    + "".join(f'<rect x="{x-3}" y="{1000+R.randint(0,200)}" width="6" height="{R.randint(20,80)}" fill="#ffcf8a" opacity=".25"/>' for x in range(60, 1080, 120)))

S["city"] = ('<rect width="1080" height="1350" fill="#0a0b11"/>' + glow(540, 1350, 500, "#c9864c", .18) +
    "".join((lambda x, w, h: f'<rect x="{x}" y="{1350-h}" width="{w}" height="{h}" fill="#050508"/>' +
             "".join(f'<rect x="{x+8+cx*22}" y="{1350-h+14+cy*30}" width="10" height="14" fill="#ffd79c" opacity="{R.choice([0,0,0,.8,.5])}"/>'
                     for cx in range(max(1,(w-16)//22)) for cy in range(max(1,(h-20)//30))))(x, w, h)
            for x, w, h in [(300,110,420),(410,90,560),(500,140,380),(640,100,640),(740,120,470),(860,90,700),(950,130,520)]))

S["alley"] = ('<rect width="1080" height="1350" fill="#0b0a0c"/>'
    '<polygon points="380,1350 640,820 700,820 1080,1350" fill="#151316"/>'
    '<polygon points="0,1350 380,1350 640,820 640,500 0,300" fill="#080709"/><polygon points="1080,1350 700,820 700,500 1080,300" fill="#080709"/>'
    '<line x1="640" y1="560" x2="700" y2="560" stroke="#222" stroke-width="2"/><circle cx="670" cy="600" r="10" fill="#ffd9a0"/>'
    + glow(670, 620, 160, "#f0ad62", .25) + glow(670, 1000, 200, "#f0ad62", .1))

S["desk"] = ('<rect width="1080" height="1350" fill="#0d0b0b"/>' + glow(760, 980, 380, "#f2b46c", .2) +
    '<rect x="340" y="1100" width="740" height="30" fill="#1c1512"/><rect x="340" y="1130" width="740" height="220" fill="#090707"/>'
    '<path d="M900 1100 L900 960 L780 860" stroke="#050505" stroke-width="12" fill="none"/>'
    '<polygon points="730,820 820,850 790,920 700,890" fill="#050505"/>'
    '<polygon points="745,905 790,920 620,1100 900,1100" fill="#ffd59a" opacity=".22" filter="url(#b)"/>'
    '<rect x="560" y="1080" width="200" height="20" fill="#e9dcc4" opacity=".75"/><rect x="580" y="1066" width="180" height="16" fill="#cbbfa8" opacity=".7"/>')

S["book"] = ('<rect width="1080" height="1350" fill="#0c0a09"/>' + glow(640, 1080, 320, "#f4c27c", .3) +
    '<path d="M380 1120 Q 520 1060 640 1110 Q 760 1060 900 1120 L900 1180 Q 760 1130 640 1180 Q 520 1130 380 1180Z" fill="#efe4cd"/>'
    '<line x1="640" y1="1110" x2="640" y2="1180" stroke="#b7a98e" stroke-width="3"/>'
    + "".join(f'<line x1="{x0}" y1="{y}" x2="{x0+180}" y2="{y-6}" stroke="#a89a80" stroke-width="2" opacity=".6"/>' for x0 in (420, 670) for y in range(1110, 1160, 12)) +
    '<rect x="0" y="1190" width="1080" height="160" fill="#070605"/>')

S["cup"] = ('<rect width="1080" height="1350" fill="#0d0b0a"/>' + glow(700, 1060, 300, "#e7a35f", .22) +
    '<rect x="0" y="1150" width="1080" height="200" fill="#080706"/>'
    '<path d="M600 980 L800 980 L780 1140 Q 700 1170 620 1140Z" fill="#e8ddc9"/><path d="M800 1010 Q 860 1020 850 1070 Q 840 1110 790 1100" stroke="#e8ddc9" stroke-width="16" fill="none"/>'
    '<ellipse cx="700" cy="1150" rx="170" ry="16" fill="#e8ddc9" opacity=".6"/>'
    + "".join(f'<path d="M{660+i*40} 960 q -30 -60 0 -120 q 30 -60 0 -120" stroke="#ffffff" stroke-opacity=".18" stroke-width="10" fill="none" filter="url(#b)"/>' for i in range(3)))

S["umbrella"] = ('<rect width="1080" height="1350" fill="#0b0d12"/>' + glow(760, 980, 260, "#f0b270", .16) +
    "".join(f'<line x1="{R.randint(0,1080)}" y1="{y}" x2="{0}" y2="0" stroke="#cfd8e3" stroke-opacity=".25" stroke-width="2" transform="translate(0,0)"/>'.replace(' x2="0" y2="0"', f' x2="{0}" y2="{0}"') for y in []) +
    "".join(f'<line x1="{x}" y1="{y}" x2="{x-8}" y2="{y+46}" stroke="#cfd8e3" stroke-opacity=".28" stroke-width="2"/>' for x, y in [(R.randint(0,1080), R.randint(300,1350)) for _ in range(110)]) +
    '<path d="M640 900 Q 760 800 880 900Z" fill="#050608"/><line x1="760" y1="860" x2="760" y2="1000" stroke="#050608" stroke-width="5"/>'
    '<circle cx="760" cy="945" r="28" fill="#050608"/><path d="M720 975 L800 975 L815 1180 L705 1180Z" fill="#050608"/>'
    '<rect x="722" y="1180" width="24" height="90" fill="#050608"/><rect x="774" y="1180" width="24" height="90" fill="#050608"/>'
    '<ellipse cx="760" cy="1280" rx="160" ry="14" fill="#f0b270" opacity=".15" filter="url(#b)"/>')

S["busstop"] = ('<rect width="1080" height="1350" fill="#0b0c10"/>' + glow(780, 1020, 280, "#f2c27e", .22) +
    '<rect x="560" y="860" width="440" height="20" fill="#050507"/><rect x="580" y="880" width="10" height="340" fill="#050507"/><rect x="970" y="880" width="10" height="340" fill="#050507"/>'
    '<rect x="600" y="885" width="360" height="230" fill="#f2d3a0" opacity=".16"/><rect x="640" y="1150" width="280" height="14" fill="#050507"/>'
    '<rect x="0" y="1220" width="1080" height="130" fill="#08090c"/>')

S["booth"] = ('<rect width="1080" height="1350" fill="#0a0b0f"/>' + glow(780, 1000, 300, "#ffd28e", .25) +
    '<rect x="680" y="760" width="200" height="460" fill="#050507"/><rect x="700" y="800" width="160" height="380" fill="#ffdca6" opacity=".55"/>'
    '<line x1="780" y1="800" x2="780" y2="1180" stroke="#050507" stroke-width="6"/>' + "".join(f'<line x1="700" y1="{y}" x2="860" y2="{y}" stroke="#050507" stroke-width="5"/>' for y in (900, 1000, 1100)) +
    '<polygon points="680,1220 880,1220 1000,1350 560,1350" fill="#ffd28e" opacity=".12" filter="url(#b)"/>')

S["mountain"] = ('<defs>' + lingrad("ms", [(0, "#0a0c14", 1), (.6, "#2a2a3a", 1), (1, "#c4865a", 1)]) + '</defs><rect width="1080" height="1350" fill="url(#ms)"/>'
    '<polygon points="0,1100 260,820 420,980 640,700 900,1000 1080,860 1080,1350 0,1350" fill="#14141c"/>'
    '<polygon points="0,1200 300,1000 560,1150 820,960 1080,1120 1080,1350 0,1350" fill="#07070b"/>')

S["field"] = ('<defs>' + lingrad("fs", [(0, "#0b0c12", 1), (.62, "#5a3a2a", 1), (.72, "#d79a5a", 1), (.73, "#1a120c", 1), (1, "#0a0806", 1)]) + '</defs><rect width="1080" height="1350" fill="url(#fs)"/>'
    + glow(760, 980, 160, "#ffd59a", .45) +
    "".join(f'<line x1="{x}" y1="1350" x2="{x+R.randint(-12,12)}" y2="{R.randint(1000,1200)}" stroke="#050403" stroke-width="3"/>' for x in range(0, 1080, 9)))

S["forest"] = ('<rect width="1080" height="1350" fill="#090b0b"/>'
    + "".join(f'<polygon points="{x},{360} {x+40},{360} {x+180},1350 {x-120},1350" fill="#f3d39a" opacity=".07" filter="url(#b)"/>' for x in (560, 760, 900)) +
    "".join(f'<rect x="{x}" y="0" width="{w}" height="1350" fill="#030404"/>' for x, w in [(420,30),(520,60),(690,26),(820,48),(960,70),(1040,40)]) +
    '<rect x="0" y="1260" width="1080" height="90" fill="#050606"/>')

S["river"] = ('<defs>' + lingrad("rs", [(0, "#0a0c14", 1), (1, "#22283a", 1)]) + '</defs><rect width="1080" height="1350" fill="url(#rs)"/>'
    '<path d="M600 820 Q 760 900 640 1000 Q 480 1100 700 1200 Q 860 1280 760 1350 L1080 1350 L1080 820Z" fill="#06070b"/>'
    '<path d="M600 820 Q 760 900 640 1000 Q 480 1100 700 1200 Q 860 1280 760 1350 L380 1350 Q 520 1250 420 1170 Q 300 1060 500 980 Q 640 910 560 820Z" fill="#c8d2e2" opacity=".2"/>'
    '<rect x="0" y="780" width="1080" height="44" fill="#06070b"/>' + glow(580, 760, 70, "#ffe4b8", .5))

S["desert"] = ('<rect width="1080" height="1350" fill="#090a12"/>' + stars(160, 900, 3) +
    '<path d="M0 1050 Q 300 940 560 1040 T 1080 1000 V1350 H0Z" fill="#2a1f22"/><path d="M0 1180 Q 400 1080 700 1170 T 1080 1150 V1350 H0Z" fill="#120d0f"/>')

S["stars"] = ('<rect width="1080" height="1350" fill="#06070c"/>' + stars(380, 1350, 9) +
    '<path d="M1080 300 Q 700 700 300 1350" stroke="#d8d4e8" stroke-width="160" stroke-opacity=".07" fill="none" filter="url(#b)"/>'
    '<path d="M0 1260 Q 540 1200 1080 1260 V1350 H0Z" fill="#030305"/>')

S["aurora"] = ('<rect width="1080" height="1350" fill="#05070b"/>' + stars(150, 1100, 5) +
    '<path d="M300 700 Q 600 520 1080 640" stroke="#7ee0b0" stroke-width="140" stroke-opacity=".2" fill="none" filter="url(#b)"/>'
    '<path d="M400 820 Q 700 640 1080 780" stroke="#7ec8e0" stroke-width="90" stroke-opacity=".16" fill="none" filter="url(#b)"/>'
    '<polygon points="0,1240 200,1120 380,1200 600,1080 820,1190 1080,1100 1080,1350 0,1350" fill="#020304"/>')

S["fireplace"] = ('<rect width="1080" height="1350" fill="#0c0908"/>' + glow(720, 1120, 360, "#f08a3c", .28) +
    '<rect x="480" y="860" width="480" height="400" fill="#050404"/><rect x="540" y="920" width="360" height="300" fill="#140b07"/>'
    '<ellipse cx="720" cy="1190" rx="150" ry="30" fill="#ff9a4a" opacity=".7" filter="url(#b)"/>'
    '<path d="M640 1190 Q 660 1080 700 1150 Q 720 1040 760 1140 Q 790 1090 800 1190Z" fill="#ffb25c" opacity=".85" filter="url(#b)"/>'
    '<rect x="440" y="840" width="560" height="26" fill="#050404"/>')

S["clock"] = ('<rect width="1080" height="1350" fill="#0c0b0d"/>' + glow(760, 980, 300, "#e6b277", .18) +
    '<circle cx="760" cy="980" r="190" fill="#141216" stroke="#d9c4a0" stroke-opacity=".5" stroke-width="6"/>'
    + "".join(f'<line x1="{760+165*math.sin(a):.0f}" y1="{980-165*math.cos(a):.0f}" x2="{760+180*math.sin(a):.0f}" y2="{980-180*math.cos(a):.0f}" stroke="#d9c4a0" stroke-opacity=".7" stroke-width="5"/>' for a in [i*math.pi/6 for i in range(12)]) +
    '<line x1="760" y1="980" x2="760" y2="860" stroke="#e8d6b4" stroke-width="8"/><line x1="760" y1="980" x2="850" y2="1030" stroke="#e8d6b4" stroke-width="6"/>')

S["curtain"] = ('<rect width="1080" height="1350" fill="#0d0c10"/>'
    '<rect x="580" y="500" width="380" height="620" fill="#e6c38c" opacity=".55"/>' + glow(770, 800, 260, "#f2c98c", .2) +
    '<path d="M580 480 Q 640 700 600 900 Q 570 1060 640 1140 L560 1140 L560 480Z" fill="#c9b8a8" opacity=".35"/>'
    '<path d="M960 480 Q 900 720 940 920 Q 980 1060 900 1140 L980 1140 L980 480Z" fill="#c9b8a8" opacity=".35"/>'
    '<polygon points="580,1140 960,1140 820,1350 300,1350" fill="#e6c38c" opacity=".12" filter="url(#b)"/>')

S["corridor"] = ('<rect width="1080" height="1350" fill="#0a0a0c"/>'
    '<polygon points="440,1350 680,900 740,900 1080,1350" fill="#151417"/>'
    '<rect x="680" y="760" width="60" height="140" fill="#ffd9a0"/>' + glow(710, 830, 150, "#ffd9a0", .3) +
    '<polygon points="680,900 740,900 900,1350 520,1350" fill="#ffd9a0" opacity=".1" filter="url(#b)"/>'
    + "".join(f'<rect x="{680-int(280*t)}" y="{760-int(420*t)}" width="2" height="{int(560*t)+140}" fill="#222"/>' for t in (0.3, 0.6, 0.9)))

S["rooftop"] = ('<rect width="1080" height="1350" fill="#0a0b12"/>' + glow(700, 1350, 520, "#d08a4e", .22) +
    "".join(f'<circle cx="{R.randint(300,1080)}" cy="{R.randint(1150,1330)}" r="{R.choice([2,3])}" fill="#ffd9a0" opacity="{R.uniform(.3,.8):.2f}"/>' for _ in range(160)) +
    '<rect x="0" y="1060" width="1080" height="40" fill="#040406"/><rect x="0" y="1100" width="300" height="250" fill="#040406"/>'
    '<line x1="0" y1="1000" x2="1080" y2="1000" stroke="#040406" stroke-width="5"/>' + "".join(f'<line x1="{x}" y1="1000" x2="{x}" y2="1060" stroke="#040406" stroke-width="5"/>' for x in range(40, 1080, 90)))

S["lantern"] = ('<rect width="1080" height="1350" fill="#0b0a0c"/>' + glow(760, 940, 300, "#f09a4c", .25) +
    '<line x1="760" y1="0" x2="760" y2="800" stroke="#1c1a1e" stroke-width="3"/>'
    '<ellipse cx="760" cy="940" rx="110" ry="150" fill="#f3a55a" opacity=".9"/>'
    + "".join(f'<ellipse cx="760" cy="940" rx="{110-k*22}" ry="150" fill="none" stroke="#a0512a" stroke-opacity=".35" stroke-width="3"/>' for k in range(1, 5)) +
    '<rect x="720" y="782" width="80" height="18" fill="#2a1a12"/><rect x="720" y="1080" width="80" height="18" fill="#2a1a12"/>')

S["cliff"] = ('<defs>' + lingrad("cs", [(0, "#0a0b13", 1), (.7, "#3a2a30", 1), (1, "#cf8a52", 1)]) + '</defs><rect width="1080" height="1350" fill="url(#cs)"/>'
    + glow(860, 1180, 200, "#ffcf8f", .35) +
    '<path d="M0 1080 L640 1080 Q 680 1090 700 1130 L760 1350 L0 1350Z" fill="#050507"/>'
    '<circle cx="560" cy="990" r="20" fill="#050507"/><path d="M538 1012 L582 1012 L590 1080 L530 1080Z" fill="#050507"/>')

S["swing"] = ('<defs>' + lingrad("ws", [(0, "#0a0b11", 1), (1, "#2c2730", 1)]) + '</defs><rect width="1080" height="1350" fill="url(#ws)"/>'
    + glow(780, 1100, 260, "#e9b277", .12) +
    '<path d="M500 640 Q 760 600 1080 660" stroke="#050506" stroke-width="22" fill="none"/>'
    '<line x1="720" y1="630" x2="700" y2="1060" stroke="#0e0d10" stroke-width="4"/><line x1="860" y1="626" x2="840" y2="1060" stroke="#0e0d10" stroke-width="4"/>'
    '<rect x="690" y="1056" width="160" height="16" fill="#050506"/><rect x="0" y="1240" width="1080" height="110" fill="#060608"/>')

S["path"] = ('<defs>' + lingrad("ps", [(0, "#0a0c12", 1), (1, "#202530", 1)]) + '</defs><rect width="1080" height="1350" fill="url(#ps)"/>'
    + glow(640, 860, 120, "#ffd9a0", .3) +
    "".join(f'<ellipse cx="{640 + int(math.sin(i*0.9)*60*(i/6))}" cy="{880+i*44+i*i*2}" rx="{18+i*7}" ry="{6+i*2}" fill="#d5dbe4" opacity="{.18+i*.02:.2f}"/>' for i in range(10)))
