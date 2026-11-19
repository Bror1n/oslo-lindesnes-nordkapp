import json, sys, time, math, os, urllib.parse, urllib.request
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from stages import STAGES, FERRIES
geo=json.load(open(os.path.join(HERE,'geocache.json')))
cache_p=os.path.join(HERE,'segcache2.json')
segc=json.load(open(cache_p)) if os.path.exists(cache_p) else {}
ferry=set(FERRIES)
def hav(a,b):
    R=6371000; la1,lo1,la2,lo2=map(math.radians,(a[1],a[0],b[1],b[0]))
    h=math.sin((la2-la1)/2)**2+math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2*R*math.asin(math.sqrt(h))
def ascent(coords,thr=12):
    up=0; ref=None
    for c in coords:
        if len(c)<3: continue
        e=c[2]
        if ref is None: ref=e; continue
        if e-ref>=thr: up+=e-ref; ref=e
        elif ref-e>=thr: ref=e
    return up
def analyse(f):
    pr=f["properties"]; m=pr["messages"]; h=m[0]
    iD,iT,iLo,iLa=h.index("Distance"),h.index("WayTags"),h.index("Longitude"),h.index("Latitude")
    ferry_m=0; unpaved=0; path=0; tunnels=[]; cur=None
    for row in m[1:]:
        d=int(row[iD]); t=row[iT]
        tags=dict(x.split("=",1) for x in t.split() if "=" in x)
        if tags.get("route")=="ferry": ferry_m+=d; cur=None; continue
        surf=tags.get("surface",""); hw=tags.get("highway","")
        if surf in("gravel","unpaved","compacted","fine_gravel","dirt","ground","pebblestone","sand","grass","earth","mud") or (hw=="track" and surf not in("asphalt","paved","concrete")): unpaved+=d
        if hw in("path","footway","steps") and surf not in("asphalt","paved","concrete"): path+=d
        if tags.get("tunnel")=="yes":
            if cur: cur["m"]+=d
            else: cur={"m":d,"lat":int(row[iLa])/1e6,"lon":int(row[iLo])/1e6,"hw":hw}; tunnels.append(cur)
        else: cur=None
    return {"ferry_m":ferry_m,"unpaved_m":unpaved,"path_m":path,"tunnels":[t for t in tunnels if t["m"]>=400]}
def brouter(a,b,prof="trekking"):
    key=f"{prof}|{a}|{b}|{geo[a]['lat']:.4f},{geo[a]['lon']:.4f}|{geo[b]['lat']:.4f},{geo[b]['lon']:.4f}"
    if key in segc: return segc[key]
    A,B=geo[a],geo[b]
    url="https://brouter.de/brouter?"+urllib.parse.urlencode({"lonlats":f"{A['lon']},{A['lat']}|{B['lon']},{B['lat']}","profile":prof,"alternativeidx":0,"format":"geojson"})
    raw=''; r=None
    for attempt in range(6):
      try:
        raw=urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"bike-route-planner/0.1"}),timeout=120).read().decode()
        f=json.loads(raw)["features"][0]
        r={"ok":True,"coords":f["geometry"]["coordinates"],"len":float(f["properties"]["track-length"]),"asc_br":float(f["properties"]["filtered ascend"])}
        r.update(analyse(f)); break
      except Exception as e:
        r={"ok":False,"err":str(e)[:200]+raw[:200]}
        if any(x in str(e) for x in("403","429","502","503","timed")): time.sleep(20*(attempt+1))
        else: break
    if r["ok"]: segc[key]=r; json.dump(segc,open(cache_p,"w"))
    time.sleep(1.5); return r
out=[]; prev=None
for name,pts in STAGES:
    chain=([prev] if prev and prev!=pts[0] else [])+pts
    if prev and (prev,pts[0]) in ferry: chain=pts
    st={"name":name,"points":chain,"segs":[],"km":0,"asc":0,"asc_br":0,"ferries":[],"unpaved_km":0,"path_km":0,"tunnels":[]}
    for a,b in zip(chain,chain[1:]):
        prof="fastbike" if b.startswith("fast:") else "trekking"
        a=a.replace("fast:",""); b=b.replace("fast:","")
        if (a,b) in ferry:
            A,B=geo[a],geo[b]
            st["segs"].append({"ferry":True,"coords":[[A['lon'],A['lat']],[B['lon'],B['lat']]]}); st["ferries"].append(f"{a} – {b}"); continue
        r=brouter(a,b,prof)
        if not r["ok"]: print("FAIL",name,":",a,"->",b,r["err"]); continue
        d=hav((geo[a]['lon'],geo[a]['lat']),(geo[b]['lon'],geo[b]['lat']))
        ride=(r["len"]-r["ferry_m"])/1000; asc=ascent(r["coords"])
        notes=[]
        if r["len"]>1.7*d+4000: notes.append("DETOUR?")
        if r["ferry_m"]: notes.append(f"router-ferry {r['ferry_m']/1000:.1f}km"); st["ferries"].append(f"(on route between {a} and {b}, {r['ferry_m']/1000:.1f} km)")
        if r["path_m"]>500: notes.append(f"PATH {r['path_m']/1000:.1f}km")
        print(f"   {a} -> {b}: {ride:.1f} km, +{asc:.0f} m (brouter +{r['asc_br']:.0f}; straight {d/1000:.0f}) unpaved {r['unpaved_m']/1000:.1f} {' '.join(notes)}")
        for t in r["tunnels"]: print(f"        tunnel {t['m']} m at {t['lat']:.4f},{t['lon']:.4f} ({t['hw']})")
        st["segs"].append({"ferry":False,"coords":r["coords"]}); st["km"]+=ride; st["asc"]+=asc; st["asc_br"]+=r["asc_br"]
        st["unpaved_km"]+=r["unpaved_m"]/1000; st["path_km"]+=r["path_m"]/1000; st["tunnels"]+=r["tunnels"]
    print(f"{len(out)+1:2d}. {name}: {st['km']:.0f} km, +{st['asc']:.0f} m (br {st['asc_br']:.0f}), unpaved {st['unpaved_km']:.0f} km, ferries: {st['ferries']}")
    st['points']=[p.replace('fast:','') for p in chain]; out.append(st); prev=pts[-1].replace('fast:','')
json.dump(out,open(os.path.join(HERE,'routed.json'),"w"))
print("TOTAL km",round(sum(s["km"] for s in out)),"asc",round(sum(s["asc"] for s in out)),"unpaved",round(sum(s["unpaved_km"] for s in out)))
