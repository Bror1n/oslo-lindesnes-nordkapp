import json,sys,urllib.parse,urllib.request,time,collections
geo=json.load(open('geocache.json'))
def run(a,b,prof):
    A,B=geo[a],geo[b]
    url="https://brouter.de/brouter?"+urllib.parse.urlencode({"lonlats":f"{A['lon']},{A['lat']}|{B['lon']},{B['lat']}","profile":prof,"alternativeidx":0,"format":"geojson"})
    f=json.loads(urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"bike-route-planner/0.1"}),timeout=120).read().decode())["features"][0]
    m=f["properties"]["messages"]; h=m[0]; iD,iT=h.index("Distance"),h.index("WayTags")
    agg=collections.Counter()
    for r in m[1:]:
        tags=dict(x.split("=",1) for x in r[iT].split() if "=" in x)
        k=" ".join(f"{k}={tags[k]}" for k in("highway","surface","tracktype","tunnel","bicycle","route","route_bicycle_ncn","route_bicycle_rcn","route_bicycle_lcn") if k in tags)
        agg[k]+=int(r[iD])
    print(f"== {a} -> {b} [{prof}] {float(f['properties']['track-length'])/1000:.1f} km +{f['properties']['filtered ascend']}")
    for k,v in agg.most_common(9): print(f"   {v/1000:6.1f} km  {k}")
for arg in sys.argv[1:]:
    a,b,prof=arg.split(">"); 
    try: run(a,b,prof)
    except Exception as e: print("ERR",arg,e)
    time.sleep(2)
