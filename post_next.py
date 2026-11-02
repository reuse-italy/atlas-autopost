"""Posts the next approved Atlas of Ruins photo to Instagram.

GitHub runs this once a day. It reads queue.json (the approved photos in
order, kept up to date from the approval board), skips anything already in
posted.json, posts the next photo with its caption, and records it.
At most one photo is posted per day.
"""
import json, os, sys, time, datetime, urllib.request, urllib.parse
from zoneinfo import ZoneInfo

API = "https://graph.facebook.com/v21.0"
IG_USER_ID = os.environ["IG_USER_ID"]
TOKEN = os.environ["IG_ACCESS_TOKEN"]
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
