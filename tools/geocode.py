import json, sys, time, urllib.parse, urllib.request, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stages import STAGES
out_path = sys.argv[1]
cache = json.load(open(out_path)) if os.path.exists(out_path) else {}
names = []
for _, pts in STAGES:
    for p in pts:
        if p not in names: names.append(p)
for q in names:
    if q in cache: continue
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode(
        {"q": q + ", Norway", "format": "json", "limit": 3, "countrycodes": "no"})
    req = urllib.request.Request(url, headers={"User-Agent": "bike-route-planner/0.1"})
    try:
        res = json.load(urllib.request.urlopen(req, timeout=30))
    except Exception as e:
        print("ERR", q, e); res = []
    if res:
        r = res[0]
        cache[q] = {"lat": float(r["lat"]), "lon": float(r["lon"]), "display": r["display_name"], "type": r.get("type")}
        print(f"{q:35s} {r['lat'][:8]:>9} {r['lon'][:8]:>9}  {r['display_name'][:70]}")
    else:
        print("NOT FOUND", q)
    json.dump(cache, open(out_path, "w"), indent=1, ensure_ascii=False)
    time.sleep(1.1)
