"""스치듯 어른 계정 자동화 점검 (아무것도 올리지 않음)."""
import json, os, urllib.parse, urllib.request

def get(url, params):
    try:
        with urllib.request.urlopen(url + "?" + urllib.parse.urlencode(params), timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"error": f"{e.code} {e.read().decode()[:300]}"}

T = os.environ.get("THREADS_TOKEN", "")
print("[Threads]")
if not T:
    print("  THREADS_TOKEN 없음")
else:
    me = get("https://graph.threads.net/v1.0/me", {"fields": "id,username,name", "access_token": T})
    print("  계정:", me)
    lim = get("https://graph.threads.net/v1.0/me/threads_publishing_limit", {"fields": "quota_usage,config", "access_token": T})
    print("  하루 게시 한도:", lim)
    dbg = get("https://graph.threads.net/v1.0/debug_token", {"input_token": T, "access_token": T})
    print("  토큰 정보:", dbg)

I, U = os.environ.get("IG_TOKEN", ""), os.environ.get("IG_USER_ID", "")
print("[Instagram]")
if not (I and U):
    print("  IG_TOKEN / IG_USER_ID 없음 → 인스타 연결 설정이 아직 안 됨")
else:
    print("  계정:", get(f"https://graph.facebook.com/v21.0/{U}", {"fields": "username,account_type", "access_token": I}))
    print("  하루 게시 한도:", get(f"https://graph.facebook.com/v21.0/{U}/content_publishing_limit", {"fields": "quota_usage,config", "access_token": I}))
