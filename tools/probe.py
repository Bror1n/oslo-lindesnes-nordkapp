import json,sys,urllib.parse,urllib.request,time
geo=json.load(open('geocache.json'))
def P(x):
    if x in geo: return geo[x]['lon'],geo[x]['lat']
    la,lo=map(float,x.split(',')); return lo,la
def probe(pts,profile="trekking"):
    ll="|".join(f"{P(p)[0]},{P(p)[1]}" for p in pts)
    url="https://brouter.de/brouter?"+urllib.parse.urlencode({"lonlats":ll,"profile":profile,"alternativeidx":0,"format":"geojson"})
    try: raw=urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"bike-route-planner/0.1"}),timeout=120).read().decode()
    except Exception as e: print("ERR",e, getattr(e,'read',lambda:b'')()[:200]); return
    f=json.loads(raw)["features"][0]; pr=f["properties"]; co=f["geometry"]["coordinates"]
    print(pts,profile,f"{float(pr['track-length'])/1000:.1f} km +{pr['filtered ascend']} m")
    m=pr["messages"]; h=m[0]; iD=h.index("Distance"); iT=h.index("WayTags"); iLo=h.index("Longitude"); iLa=h.index("Latitude")
    for row in m[1:]:
        t=row[iT]
        if "tunnel=yes" in t or "route=ferry" in t or "bicycle=no" in t or "bicycle=dismount" in t:
            print(f"    {int(row[iD]):6d} m  {int(row[iLa])/1e6:.4f},{int(row[iLo])/1e6:.4f}  {t}")
    step=max(1,len(co)//14)
    print("    path:"," ".join(f"{c[1]:.3f},{c[0]:.3f}" for c in co[::step]))
for a in sys.argv[1:]:
    prof="trekking"
    if a.startswith("fast:"): prof="fastbike"; a=a[5:]
    probe(a.split(">"),prof); time.sleep(2)
