"""힐끔(@peek_0.0) Threads 유머 글 자동 업로드.

queue.json 의 글 중 status 가 approved 인 것을 순서대로,
하루 2번(점심 12시대·밤 9시대, 한국시간) 무작위 시각에 1개씩 올린다.
사용법: python scripts/post.py run | check | now
"""
import datetime, hashlib, json, os, sys, time, urllib.parse, urllib.request

KST = datetime.timezone(datetime.timedelta(hours=9))
BASE = "https://graph.threads.net/v1.0"
TOKEN = os.environ.get("THREADS_TOKEN", "")
QUEUE = "queue.json"
SLOTS = [12, 21]  # 한국시간 '시' — 이 시간대 안의 무작위 분에 1개씩


def call(method, path, params):
    params = dict(params, access_token=TOKEN)
    data = urllib.parse.urlencode(params).encode()
    url = f"{BASE}/{path}"
    if method == "GET":
        req = urllib.request.Request(url + "?" + data.decode())
    else:
        req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{e.code} {e.read().decode()[:300]}")


def publish(text):
    c = call("POST", "me/threads", {"media_type": "TEXT", "text": text[:500]})
    time.sleep(5)
    p = call("POST", "me/threads_publish", {"creation_id": c["id"]})
    info = call("GET", p["id"], {"fields": "permalink"})
    return {"id": p["id"], "permalink": info.get("permalink", "")}


def load():
    return json.load(open(QUEUE, encoding="utf-8"))


def save(q):
    json.dump(q, open(QUEUE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


def slot_now(now):
    """지금이 올릴 시간대이고 그 시간대의 무작위 분이 지났으면 해당 '시'를 돌려준다."""
    for h in SLOTS:
        target = int(hashlib.md5(f"{now.date()}-{h}".encode()).hexdigest(), 16) % 56
        if now.hour == h and now.minute >= target:
            return h
        if now.hour == h + 1:  # GitHub 실행이 늦어진 날 따라잡기
            return h
    return None


def run(force=False):
    now = datetime.datetime.now(KST)
    q = load()
    slot = None
    if not force:
        slot = slot_now(now)
        if slot is None:
            print("올릴 시간이 아니에요."); return
        key = f"{now.date()}-{slot}"
        if any(p.get("slot") == key for p in q):
            print("이 시간대에는 이미 올렸어요."); return
    nxt = next((p for p in q if p.get("status") == "approved"), None)
    if not nxt:
        print("승인된 글이 없어요. 새 글을 채워 주세요."); return
    res = publish(nxt["text"])
    nxt.update(status="published", published_at=now.isoformat(timespec="minutes"),
               permalink=res["permalink"], slot=f"{now.date()}-{slot}" if slot else "manual")
    save(q)
    left = sum(1 for p in q if p.get("status") == "approved")
    print(f"올림: {res['permalink']} (남은 승인 글 {left}개)")


def check():
    me = call("GET", "me", {"fields": "username"})
    print(f"Threads 연결 OK: @{me.get('username')}")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "run"
    {"run": run, "check": check, "now": lambda: run(force=True)}[mode]()
