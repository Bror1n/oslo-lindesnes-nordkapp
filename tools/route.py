import json, sys, time, math, os, urllib.parse, urllib.request
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from stages import STAGES, FERRIES
geo=json.load(open(os.path.join(HERE,'geocache.json')))
cache_p=os.path.join(HERE,'segcache2.json')
segc=json.load(open(cache_p)) if os.path.exists(cache_p) else {}
from variants import VARIANTS, V_FERRIES, GRAVEL_BLOCK
ferry=set(FERRIES)|set(V_FERRIES)
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
    ferry_m=0; unpaved=0; path=0; tunnels=[]; cur=None; pos=0; unp_r=[]; fer_r=[]
    def add(L,a,b):
        if L and a-L[-1][1]<1: L[-1][1]=b
        else: L.append([a,b])
    for row in m[1:]:
        d=int(row[iD]); t=row[iT]; p0=pos; pos+=d
        tags=dict(x.split("=",1) for x in t.split() if "=" in x)
        if tags.get("route")=="ferry": ferry_m+=d; cur=None; add(fer_r,p0,pos); continue
        surf=tags.get("surface",""); hw=tags.get("highway","")
        if surf in("gravel","unpaved","compacted","fine_gravel","dirt","ground","pebblestone","sand","grass","earth","mud") or (hw=="track" and surf not in("asphalt","paved","concrete")): unpaved+=d; add(unp_r,p0,pos)
        if hw in("path","footway","steps") and surf not in("asphalt","paved","concrete"): path+=d
        if tags.get("tunnel")=="yes":
            if cur: cur["m"]+=d
            else: cur={"m":d,"lat":int(row[iLa])/1e6,"lon":int(row[iLo])/1e6,"hw":hw}; tunnels.append(cur)
        else: cur=None
    return {"msg_m":pos,"unp_r":unp_r,"fer_r":fer_r,"ferry_m":ferry_m,"unpaved_m":unpaved,"path_m":path,"tunnels":[t for t in tunnels if t["m"]>=400]}
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
def pick_gravel(a,b,r,prof):
    """gravel mode: use the router's gravel profile for this leg only where it adds real gravel at a fair price"""
    g=brouter(a,b,"gravel")
    if not g["ok"]: return r,None
    gain=(g["unpaved_m"]-r["unpaved_m"])/1000; rk=(r["len"]-r["ferry_m"])/1000; gk=(g["len"]-g["ferry_m"])/1000
    ok=(gain>=3 and gk<=rk*1.15+3 and ascent(g["coords"])<=ascent(r["coords"])*1.4+150
        and g["path_m"]<=r["path_m"]+500 and abs(g["ferry_m"]-r["ferry_m"])<=500)
    return (g,gain) if ok else (r,None)
def route_stages(STAGES,prev=None,gravel=False):
    out=[]
    for name,pts in STAGES:
        chain=([prev] if prev and prev!=pts[0] else [])+pts
        st={"name":name,"points":chain,"segs":[],"km":0,"asc":0,"asc_br":0,"ferries":[],"unpaved_km":0,"path_km":0,"tunnels":[]}
        for a,b in zip(chain,chain[1:]):
            prof="fastbike" if b.startswith("fast:") else "trekking"
            a=a.replace("fast:",""); b=b.replace("fast:","")
            if (a,b) in ferry:
                A,B=geo[a],geo[b]
                st["segs"].append({"ferry":True,"coords":[[A['lon'],A['lat']],[B['lon'],B['lat']]]}); st["ferries"].append(f"{a} – {b}"); continue
            r=brouter(a,b,prof)
            if not r["ok"]: print("FAIL",name,":",a,"->",b,r["err"]); continue
            if gravel:
                r,gain=pick_gravel(a,b,r,prof)
                if gain: print(f"   GRAVEL +{gain:.1f} km on {a} -> {b}")
            d=hav((geo[a]['lon'],geo[a]['lat']),(geo[b]['lon'],geo[b]['lat']))
            ride=(r["len"]-r["ferry_m"])/1000; asc=ascent(r["coords"])
            notes=[]
            if r["len"]>1.7*d+4000: notes.append("DETOUR?")
            if r["ferry_m"]: notes.append(f"router-ferry {r['ferry_m']/1000:.1f}km"); st["ferries"].append(f"(on route between {a} and {b}, {r['ferry_m']/1000:.1f} km)")
            if r["path_m"]>500: notes.append(f"PATH {r['path_m']/1000:.1f}km")
            print(f"   {a} -> {b}: {ride:.1f} km, +{asc:.0f} m (brouter +{r['asc_br']:.0f}; straight {d/1000:.0f}) unpaved {r['unpaved_m']/1000:.1f} {' '.join(notes)}")
            for t in r["tunnels"]: print(f"        tunnel {t['m']} m at {t['lat']:.4f},{t['lon']:.4f} ({t['hw']})")
            st["segs"].append({"ferry":False,"coords":r["coords"],"msg_m":r.get("msg_m",0),"unp_r":r.get("unp_r",[]),"fer_r":r.get("fer_r",[])}); st["km"]+=ride; st["asc"]+=asc; st["asc_br"]+=r["asc_br"]
            st["unpaved_km"]+=r["unpaved_m"]/1000; st["path_km"]+=r["path_m"]/1000; st["tunnels"]+=r["tunnels"]
        print(f"{len(out)+1:2d}. {name}: {st['km']:.0f} km, +{st['asc']:.0f} m (br {st['asc_br']:.0f}), unpaved {st['unpaved_km']:.0f} km, ferries: {st['ferries']}")
        st['points']=[p.replace('fast:','') for p in chain]; out.append(st); prev=pts[-1].replace('fast:','')
    return out
def upgrade():
    """re-fetch cached segments that lack per-stretch surface ranges; keep the cached geometry"""
    todo=[k for k,v in segc.items() if "unp_r" not in v and k.count("|")==4]; print("to upgrade",len(todo),flush=True)
    for n,k in enumerate(todo):
        prof,a,b2,ca,cb=k.split("|"); la1,lo1=ca.split(","); la2,lo2=cb.split(",")
        A,B=geo.get(a),geo.get(b2)
        if not A or not B or f"{A['lat']:.4f},{A['lon']:.4f}"!=ca or f"{B['lat']:.4f},{B['lon']:.4f}"!=cb: continue
        url="https://brouter.de/brouter?"+urllib.parse.urlencode({"lonlats":f"{A['lon']},{A['lat']}|{B['lon']},{B['lat']}","profile":prof,"alternativeidx":0,"format":"geojson"})
        for attempt in range(6):
            try:
                f=json.loads(urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"bike-route-planner/0.1"}),timeout=120).read().decode())["features"][0]
                an=analyse(f); L=float(f["properties"]["track-length"]); old=segc[k]
                drift=abs(L-old["len"])/max(old["len"],1)
                if drift>0.02: old.update({"coords":f["geometry"]["coordinates"],"len":L,"asc_br":float(f["properties"]["filtered ascend"])}); old.update(an); print("  CHANGED",k[:60],f"{drift:.1%}",flush=True)
                else: old.update({"msg_m":an["msg_m"],"unp_r":an["unp_r"],"fer_r":an["fer_r"]})
                break
            except Exception as e:
                print("  retry",k[:50],str(e)[:60],flush=True); time.sleep(20*(attempt+1))
        if n%10==0: json.dump(segc,open(cache_p,"w")); print(n,flush=True)
        time.sleep(1.5)
    json.dump(segc,open(cache_p,"w")); print("left",sum(1 for v in segc.values() if "unp_r" not in v))
if __name__=="__main__":
    if "upgrade" in sys.argv: upgrade(); sys.exit()
    if "gravel" in sys.argv:
        res={"variants":{}}
        print("=== GRAVEL main",flush=True); res["main"]=route_stages(STAGES,None,True)
        print("=== GRAVEL block",flush=True); res["block"]=route_stages(GRAVEL_BLOCK["stages"],GRAVEL_BLOCK["start"],True)
        for v in VARIANTS:
            print("=== GRAVEL VARIANT",v["id"],flush=True); res["variants"][v["id"]]=route_stages(v["stages"],v["start"],True)
        json.dump(res,open(os.path.join(HERE,'routed_gravel.json'),"w")); sys.exit()
    if "variants" in sys.argv:
        res={}
        for v in VARIANTS:
            print("=== VARIANT",v["id"],flush=True)
            res[v["id"]]=route_stages(v["stages"],v["start"],v.get("gravel",False))
            print("   variant total",round(sum(s["km"] for s in res[v["id"]])),"km",round(sum(s["asc"] for s in res[v["id"]])),"m",flush=True)
        json.dump(res,open(os.path.join(HERE,'routed_variants.json'),"w"))
    else:
        out=route_stages(STAGES)
        json.dump(out,open(os.path.join(HERE,'routed.json'),"w"))
        print("TOTAL km",round(sum(s["km"] for s in out)),"asc",round(sum(s["asc"] for s in out)),"unpaved",round(sum(s["unpaved_km"] for s in out)))
