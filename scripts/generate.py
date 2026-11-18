"""제미나이로 힐끔 유머 글 초안을 만든다 (status=draft, 사용자가 검수 후 approved 로 바꿈).
사용법: python scripts/generate.py [개수]   (기본 12개)
쌓여 있는 초안+승인 글이 6개 이상이면 자동 실행 때는 건너뛴다 (force 인자로 강제).
"""
import json, os, re, sys, time, urllib.error, urllib.request

KEY = os.environ.get("GEMINI_API_KEY", "")
MODELS = [m for m in [os.environ.get("GEMINI_MODEL"), "gemini-flash-latest", "gemini-3.6-flash", "gemini-flash-lite-latest"] if m]
MODEL = MODELS[0]
QUEUE = "queue.json"

EXAMPLES = """'피할 수 없으면 즐겨라'라는 명언을 남긴 사람은
분명히 도망치는 데 실패한 사람일 거다.

상사가 "우리 회사는 가족 같은 분위기야"라고 했다.
명절에 잔소리하는 친척들만 싹 다 모아놓은 줄 알았다.

내 MBTI는 혹시 'CCTV'가 아닐까 싶다.
방구석에 누워서 남들 갓생 사는 것만 하루 종일 지켜보고 있다."""

PROMPT = """너는 한국 Threads에서 인기 있는 유머 글 작가야.
글쓴이는 '40대 미혼 남자'다. 이 사람이 직접 쓴 것처럼 새 유머 글 {n}개를 써 줘.

[글쓴이]
- 40대 중반, 미혼, 혼자 산다. 회사에선 중간 관리자급(신입·사회초년생 아님).
- 어울리는 소재: 명절 결혼 잔소리, 혼밥·혼술, 체력·건강검진·노안·허리, 소개팅,
  조카·친구 자녀, 부모님, 동창 모임, 재테크·대출, 주말에 혼자 보내기, 나이 듦.
- 안 어울리는 소재(쓰지 말 것): 신입사원·첫 출근·입사 첫날, 학교·시험, MZ·갓생 말투,
  연애 초보 설렘, 육아·아내·여자친구 이야기, 20대 자취 감성.

[스타일]
- 딱 2줄. 한 줄은 25자 안팎으로 짧게. 군더더기 수식어 빼고 간결하게.
- 1줄: 누구나 아는 명언·속담·흔한 말·상황.
- 2줄: 자기 비하가 섞인 담담한 반전. 설명하지 말고 툭 던진다.
- 아재개그 말장난만 있는 글, 실존 인물 이름, 정치, 성별·지역·외모 비하, 해시태그·이모지 금지.

[예시 — 이 길이와 톤]
"인생은 40부터라길래 기다렸다.
40이 되니 무릎부터 시작했다."

"명절에 '좋은 사람 없냐'는 질문을 받았다.
있으면 내가 여기 왜 앉아 있겠습니까."

"'피할 수 없으면 즐겨라'라는 명언을 남긴 사람은
분명히 도망치는 데 실패한 사람일 거다."

[이미 쓴 글 — 비슷한 소재·문장 금지]
{used}

JSON 배열로만 답해. 예: ["첫 줄\\n둘째 줄", "..."]"""


def ask(n, used):
    """잠깐 붐비면(503·429) 기다렸다 다시, 그래도 안 되면 다른 모델로."""
    global MODEL
    last = None
    for model in MODELS:
        for wait in (0, 15):
            time.sleep(wait)
            try:
                MODEL = model
                return ask_once(n, used)
            except urllib.error.HTTPError as e:
                last = e
                print(f"{model}: {e.code} {e.read().decode()[:150]} — 다시 시도")
                if e.code not in (429, 500, 503):
                    break
            except Exception as e:  # 시간 초과 등
                last = e
                print(f"{model}: {type(e).__name__} — 다시 시도")
    raise last


def ask_once(n, used):
    body = {"contents": [{"parts": [{"text": PROMPT.format(n=n, used=used or "(없음)")}]}],
            "generationConfig": {"responseMimeType": "application/json"}}
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={KEY}"
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=90) as r:
        data = json.loads(r.read())
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    text = re.sub(r"^```(json)?|```$", "", text.strip()).strip()
    return [t.strip() for t in json.loads(text) if isinstance(t, str) and t.strip()]


def main():
    args = sys.argv[1:]
    force = "force" in args
    n = next((int(a) for a in args if a.isdigit()), 12)
    q = json.load(open(QUEUE, encoding="utf-8"))
    waiting = sum(1 for p in q if p.get("status") in ("draft", "approved"))
    if waiting >= 6 and not force:
        print(f"대기 중인 글이 {waiting}개라 이번엔 안 만들어요."); return
    used = "\n---\n".join(p["text"] for p in q[-60:])
    new = ask(n, used)
    have = {p["text"] for p in q}
    start = len(q)
    added = 0
    for t in new:
        if t in have or len(t) > 200:
            continue
        added += 1
        q.append({"id": f"h{start + added:03d}", "text": t, "status": "draft", "by": "gemini"})
    json.dump(q, open(QUEUE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"초안 {added}개 추가 (모델 {MODEL})")
    for p in q[start:]:
        print("-", p["text"].replace("\n", " / "))


if __name__ == "__main__":
    main()
