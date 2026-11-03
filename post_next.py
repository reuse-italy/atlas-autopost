"""Posts the next approved Atlas of Ruins photo to Instagram.

GitHub runs this once a day. It reads queue.json (the approved photos in
order, kept up to date from the approval board), skips anything already in
posted.json, posts the next photo with its caption, and records it.
At most one photo is posted per day.
"""
import json, os, sys, time, datetime, urllib.request, urllib.parse
from zoneinfo import ZoneInfo

TOKEN = os.environ["IG_ACCESS_TOKEN"].strip()
# Keys made with Instagram login start with "IG"; keys from Meta's business setup start with "EAA".
INSTAGRAM_KEY = TOKEN.startswith("IG")
API = "https://graph.instagram.com/v21.0" if INSTAGRAM_KEY else "https://graph.facebook.com/v21.0"
IG_USER_ID = os.environ.get("IG_USER_ID") or "17841477991236774"   # @atlas_of_ruins
REPO = os.environ["GITHUB_REPOSITORY"]
BRANCH = os.environ.get("GITHUB_REF_NAME", "main")

def post(path, params):
    data = urllib.parse.urlencode({**params, "access_token": TOKEN}).encode()
    with urllib.request.urlopen(urllib.request.Request(f"{API}/{path}", data=data), timeout=60) as r:
        return json.load(r)

def status(container_id):
    q = urllib.parse.urlencode({"fields": "status_code", "access_token": TOKEN})
    with urllib.request.urlopen(f"{API}/{container_id}?{q}", timeout=60) as r:
        return json.load(r).get("status_code")

# Only post once the day's posting time (set on the approval board, Rome time) has been reached.
_now = datetime.datetime.now(ZoneInfo("Europe/Rome"))
_q = json.load(open("queue.json", encoding="utf-8"))
_h, _m = [int(x) for x in (_q.get("time") or "11:00").split(":")[:2]]
if os.environ.get("GITHUB_EVENT_NAME") != "workflow_dispatch" and (_now.hour, _now.minute) < (_h, _m):
    print(f"Not yet: posting time is {_h:02d}:{_m:02d} Rome time."); sys.exit(0)

# Keep the key alive: each refresh extends it by another 60 days.
try:
    if not INSTAGRAM_KEY:
        raise RuntimeError("business key, does not need refreshing")
    q = urllib.parse.urlencode({"grant_type": "ig_refresh_token", "access_token": TOKEN})
    with urllib.request.urlopen(f"https://graph.instagram.com/refresh_access_token?{q}", timeout=60) as r:
        print("Key refreshed, valid for", json.load(r).get("expires_in"), "seconds")
except Exception as e:
    print("Key refresh skipped:", e)

# Check the key works (read only, posts nothing).
q = urllib.parse.urlencode({"fields": "username", "access_token": TOKEN})
with urllib.request.urlopen(f"{API}/{IG_USER_ID}?{q}", timeout=60) as r:
    print("Connected to Instagram as @" + json.load(r).get("username", "?"))

today = datetime.datetime.now(ZoneInfo("Europe/Rome")).date().isoformat()
queue = json.load(open("queue.json", encoding="utf-8"))
posted = json.load(open("posted.json", encoding="utf-8")) if os.path.exists("posted.json") else {}

if today in posted.values():
    print("Already posted today."); sys.exit(0)
if queue.get("start") and today < queue["start"]:
    print("Posting starts on", queue["start"]); sys.exit(0)
todo = [p for p in queue["photos"] if p["id"] not in posted]
if not todo:
    print("Nothing approved is waiting. Approve more rows on the board."); sys.exit(0)

item = todo[0]
image_url = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/posts/{item['id']}.jpg"
print("Posting", item["id"], item["caption"].splitlines()[0])
container = post(f"{IG_USER_ID}/media", {"image_url": image_url, "caption": item["caption"]})["id"]
for _ in range(20):
    if status(container) == "FINISHED":
        break
    time.sleep(6)
result = post(f"{IG_USER_ID}/media_publish", {"creation_id": container})
posted[item["id"]] = today
json.dump(posted, open("posted.json", "w", encoding="utf-8"), indent=1, sort_keys=True)
print("Posted:", result)
