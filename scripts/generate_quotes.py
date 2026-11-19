"""제미나이로 '스치듯 어른' 5장 명언 카드뉴스 초안을 만든다 (status=draft → 사용자 검수 후 approved).
문장 기준: prompts/quote_prompt.md (사용자 프롬프트)
사용: python scripts/generate_quotes.py [세트 개수, 기본 3]
결과: sets/NNN-slug.json + sets/NNN-slug/card_1~5.png, preview.png
"""
import glob, json, os, re, sys, time, urllib.error, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
KEY = os.environ.get("GEMINI_API_KEY", "")
MODELS = [m for m in [os.environ.get("GEMINI_MODEL"), "gemini-flash-latest", "gemini-3.6-flash", "gemini-flash-lite-latest"] if m]
SCENES = ["lamp", "window", "door", "dusk", "candle"]

OUTPUT_RULE = """

[이번 작업의 출력 방식 — 위 '6. 결과물 출력 형식' 대신 이것을 따른다]
- 서로 다른 주제로 카드뉴스 {n}세트를 만든다. 아래 '이미 다룬 주제'와 겹치지 않게.
- 카드 안 문장은 짧게: 큰 문장(lines)은 한 줄 13자 안팎, 2~5줄. 작은 설명(desc)은 0~3줄, 한 줄 16자 안팎. 5장째는 desc 없이 최종 명언만.
- 큰 문장은 '~다'체 또는 명사로, 설명은 자연스러운 한국어로. 맞춤법·띄어쓰기 확인.
- scene은 장마다 다르게, 다음 중에서 고른다: lamp(어둠 속 가로등), window(어두운 방 창문 빛), door(문틈 빛), dusk(해 질 녘 지평선), candle(촛불). 문장 뜻과 어울리게.
- 실존 인물 이름, 출처 표기, 이모지 금지.

[이미 다룬 주제]
{used}

JSON 배열로만 답한다. 형식:
[{{"title":"주제 제목(카드 1장에 작게 표시, 15자 이내)","theme":"주제 분류","intent":"창작 의도 한 문장",
  "cards":[{{"lines":["..."],"desc":["..."],"scene":"lamp"}}, ... 5개],
  "caption":"게시물 소개 문구(2~4문장, 마지막은 독자에게 묻는 질문)","hashtags":["#..."]}}]"""


def ask_once(model, prompt):
    body = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"responseMimeType": "application/json", "temperature": 1.0}}
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={KEY}"
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        data = json.loads(r.read())
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    return json.loads(re.sub(r"^```(json)?|```$", "", text.strip()).strip())


def ask(prompt):
    last = None
    for model in MODELS:
        for wait in (0, 20):
            time.sleep(wait)
            try:
                return ask_once(model, prompt), model
            except urllib.error.HTTPError as e:
                last = e; print(f"{model}: {e.code} — 다시 시도")
                if e.code not in (429, 500, 503):
                    break
            except Exception as e:
                last = e; print(f"{model}: {type(e).__name__} — 다시 시도")
    raise last


def ok(s):
    c = s.get("cards") or []
    return len(c) == 5 and all(x.get("lines") for x in c)


def main():
    n = next((int(a) for a in sys.argv[1:] if a.isdigit()), 3)
    base = open("prompts/quote_prompt.md", encoding="utf-8").read()
    old = [json.load(open(f, encoding="utf-8")) for f in sorted(glob.glob("sets/*.json"))]
    used = "\n".join(f"- {o.get('title')} ({o.get('theme')})" for o in old) or "(없음)"
    sets, model = ask(base + OUTPUT_RULE.format(n=n, used=used))
    from render_cards import render
    num = len(old)
    for s in sets:
        if not ok(s):
            print("형식이 맞지 않아 건너뜀:", s.get("title")); continue
        num += 1
        for i, c in enumerate(s["cards"]):
            if c.get("scene") not in SCENES:
                c["scene"] = SCENES[i]
        s["cards"][0]["label"] = s.get("title", "")
        for c in s["cards"][1:]:
            c["label"] = ""
        s["cards"][-1]["desc"] = []
        s.update(status="draft", by=f"gemini ({model})")
        slug = f"{num:03d}"
        json.dump(s, open(f"sets/{slug}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        render(f"sets/{slug}.json", f"sets/{slug}")
        print(f"\n=== {slug} {s.get('title')} ===")
        for c in s["cards"]:
            print(" /", " ".join(c["lines"]), "|", " ".join(c.get("desc", [])))


if __name__ == "__main__":
    main()
