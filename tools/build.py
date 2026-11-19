import json, os, math, html, re, sys
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE); sys.path.insert(0,HERE)
from landmarks import LANDMARKS, VLANDMARKS
from variants import VARIANTS, GRAVEL_BLOCK, GRAVEL_NOTES
st=json.load(open(os.path.join(HERE,'routed.json')))
vr=json.load(open(os.path.join(HERE,'routed_variants.json')))
LG=json.load(open(os.path.join(HERE,'landmark_geo.json')))
def esc(s): return html.escape(s,quote=True)

# ---------- DNT huts: filter the raw OSM dump once, keep the small list in the repo ----------
raw=os.path.join(HERE,'huts.json'); dnt_p=os.path.join(HERE,'dnt_huts.json')
if os.path.exists(raw):
    H=[]
    for x in json.load(open(raw))['elements']:
        t=x['tags']
        isdnt=any(k.startswith('dnt:') for k in t) or re.search(r'turistforening|turlag|\bDNT\b|fjellsportlag',t.get('operator','')+' '+t.get('network',''),re.I)
        if not isdnt or 'name' not in t: continue
        la=x.get('lat') or x['center']['lat']; lo=x.get('lon') or x['center']['lon']
        H.append([round(la,5),round(lo,5),t['name'],t.get('dnt:classification','?'),t.get('ele',''),t.get('capacity',''),t.get('dnt:lock',''),t.get('operator',''),t.get('website','')])
    json.dump(H,open(dnt_p,'w'),ensure_ascii=False)
HUTS=json.load(open(dnt_p))
KIND={"betjent":"Staffed lodge","selvbetjent":"Self-service cabin","ubetjent":"No-service cabin"}
def track(s): return [c for g in s["segs"] if not g["ferry"] for c in g["coords"]]
def dist_km(pts,la,lo):
    k=math.cos(math.radians(la)); best=9e9
    for c in pts:
        dy=c[1]-la
        if abs(dy)>0.06: continue
        d=((c[0]-lo)*k)**2+dy*dy
        if d<best: best=d
    return math.sqrt(best)*111.2
def huts_for(stages):
    """assign each hut within 5 km to the nearest stage of this list"""
    tr=[track(s)[::4] for s in stages]; out=[[] for _ in stages]
    boxes=[(min(c[1] for c in t)-.06,max(c[1] for c in t)+.06,min(c[0] for c in t)-.15,max(c[0] for c in t)+.15) for t in tr]
    for la,lo,name,cls,ele,cap,lock,op,web in HUTS:
        if cls=="stengt" or re.search(r"dagsturhytt|perletur|sikringsbu",name,re.I): continue
        best=(9e9,None)
        for i,t in enumerate(tr):
            b=boxes[i]
            if not(b[0]<=la<=b[1] and b[2]<=lo<=b[3]): continue
            d=dist_km(t,la,lo)
            if d<best[0]: best=(d,i)
        if best[1] is not None and best[0]<=5:
            if not re.match(r"https?://",web or ""): web=""
            out[best[1]].append({"n":name,"c":KIND.get(cls,"Cabin, type not recorded"),"d":round(best[0],1),"e":ele,"cap":cap,"lock":lock=="yes","op":op,"w":web,"ll":[la,lo]})
    return [sorted(o,key=lambda h:h["d"]) for o in out]
def lms(items,s):
    out=[]; pts=track(s)
    for kind,name,q,la,lo,extra,text in items:
        if name in LG: la,lo=LG[name]
        elif kind=="route":
            k=math.cos(math.radians(la)); c=min(pts,key=lambda c:((c[0]-lo)*k)**2+(c[1]-la)**2)
            if math.hypot((c[0]-lo)*k,c[1]-la)<0.1: la,lo=c[1],c[0]
        out.append({"k":kind[0],"n":name,"x":extra,"t":text,"ll":[round(la,5),round(lo,5)]})
    return out
def simp(pts,tol=0.0004):
    if len(pts)<3: return pts
    keep=[0,len(pts)-1]; stack=[(0,len(pts)-1)]
    while stack:
        a,b=stack.pop(); ax,ay=pts[a][0],pts[a][1]; bx,by=pts[b][0],pts[b][1]; dm=0; im=None
        k=math.cos(math.radians(ay))
        for i in range(a+1,b):
            px,py=pts[i][0],pts[i][1]; dx,dy=(bx-ax)*k,by-ay; l=dx*dx+dy*dy
            t=0 if l==0 else max(0,min(1,(((px-ax)*k)*dx+(py-ay)*dy)/l))
            d=math.hypot((px-ax)*k-t*dx,(py-ay)-t*dy)
            if d>dm: dm=d; im=i
        if dm>tol: keep.append(im); stack+=[(a,im),(im,b)]
    return [pts[i] for i in sorted(keep)]
def pieces(g):
    """split one routed segment into paved / gravel / ferry pieces, using the distance ranges from the router"""
    co=g["coords"]
    if g["ferry"]: return [{"f":True,"c":[[round(c[1],5),round(c[0],5)] for c in co]}]
    cum=[0]
    for a,b in zip(co,co[1:]):
        k=math.cos(math.radians(a[1])); cum.append(cum[-1]+math.hypot((b[0]-a[0])*k,b[1]-a[1])*111200)
    sc=cum[-1]/g["msg_m"] if g.get("msg_m") else 1
    gr=[]
    for a,b in g.get("unp_r",[]):
        if gr and a-gr[-1][1]<150: gr[-1][1]=b          # bridge short paved gaps
        else: gr.append([a,b])
    iv=[(a*sc,b*sc,"g") for a,b in gr if b-a>=200]+[(a*sc,b*sc,"f") for a,b in g.get("fer_r",[])]
    def typ(m):
        for a,b,t in iv:
            if a<=m<b: return t
        return "p"
    out=[]; cur=None
    for i in range(len(co)-1):
        t=typ((cum[i]+cum[i+1])/2)
        if t!=cur: out.append([t,[co[i]]]); cur=t
        out[-1][1].append(co[i+1])
    return [dict({"f":t=="f","c":[[round(c[1],5),round(c[0],5)] for c in simp(c2)]},**({"g":1} if t=="g" else {})) for t,c2 in out]
def entry(s,landmarks,huts):
    return {"name":s["name"],"km":round(s["km"]),"asc":int(round(s["asc"],-1)),"unp":round(s["unpaved_km"]),"ferries":len(s["ferries"]),
            "lm":lms(landmarks,s),"huts":huts,
            "segs":[x for g in s["segs"] for x in pieces(g)]}
gr=json.load(open(os.path.join(HERE,'routed_gravel.json')))
def with_g(E,S,GS):
    """attach the gravel-mode version to every stage whose track differs"""
    gh=huts_for(GS)
    for e,s,g,h in zip(E,S,GS,gh):
        if abs(s["km"]-g["km"])>0.05 or abs(s["unpaved_km"]-g["unpaved_km"])>0.05:
            ge=entry(g,[],h); e["g"]={k:ge[k] for k in("km","asc","unp","ferries","huts","segs")}
eff=lambda e:dict(e,**e["g"]) if "g" in e else e
mh=huts_for(st)
main=[entry(s,LANDMARKS.get(i,[]),mh[i-1]) for i,s in enumerate(st,1)]
names=[s["name"] for s in st]
with_g(main,st,gr["main"])
ba=names.index(GRAVEL_BLOCK["first"])+1; bb=names.index(GRAVEL_BLOCK["last"])+1
bh=huts_for(gr["block"]); BE=[entry(s,VLANDMARKS.get(s["name"],[]),bh[i]) for i,s in enumerate(gr["block"])]
gmain=[eff(e) for e in main[:ba-1]]+BE+[eff(e) for e in main[bb:]]      # gravel mode with no variant switched on
variants=[]
for v in VARIANTS:
    S=vr[v["id"]]; vh=huts_for(S)
    a=names.index(v["first"])+1; b=names.index(v["last"])+1
    E=[entry(s,VLANDMARKS.get(s["name"]) or (LANDMARKS.get(names.index(s["name"])+1,[]) if s["name"] in names else []),vh[i]) for i,s in enumerate(S)]
    with_g(E,S,gr["variants"][v["id"]])
    repl=main[a-1:b]
    variants.append({"id":v["id"],"title":v["title"],"blurb":v["blurb"],"first":a,"last":b,"stages":E,
        "dkm":sum(e["km"] for e in E)-sum(e["km"] for e in repl),"dasc":sum(e["asc"] for e in E)-sum(e["asc"] for e in repl),"ddays":len(E)-len(repl)})
b_end=next(i for i,s in enumerate(st,1) if s["name"].endswith("Trondheim"))
DATA={"main":main,"variants":variants,"gblock":{"first":ba,"last":bb,"stages":BE},"parts":[[1,5,"A · Oslo – Lindesnes","#c2410c"],[6,b_end,"B · Lindesnes – Trondheim","#15803d"],[b_end+1,len(main),"C · Trondheim – Nordkapp","#1d4ed8"]]}

# ---------- GPX ----------
def gpx(stages,title):
    o=['<?xml version="1.0" encoding="UTF-8"?>','<gpx version="1.1" creator="rute/tools/build.py (BRouter, OpenStreetMap data)" xmlns="http://www.topografix.com/GPX/1/1">',f'<metadata><name>{esc(title)}</name></metadata>']
    for i,s in stages:
        o.append(f'<trk><name>{i:02d} {esc(s["name"])}</name>')
        for seg in s["segs"]:
            o.append('<trkseg>')
            for c in seg["coords"]:
                e=f'<ele>{c[2]:.0f}</ele>' if len(c)>2 else ''
                o.append(f'<trkpt lat="{c[1]:.5f}" lon="{c[0]:.5f}">{e}</trkpt>')
            o.append('</trkseg>')
        o.append('</trk>')
    o.append('</gpx>'); return "\n".join(o)
def slug(s):
    for a,b in (("ø","o"),("å","a"),("æ","ae"),("Ø","O"),("Å","A"),(" – ","_"),(" ","-"),("(",""),(")",""),(",","")): s=s.replace(a,b)
    return s
for d in ('stages','variants'):
    os.makedirs(os.path.join(ROOT,d),exist_ok=True)
    for f in os.listdir(os.path.join(ROOT,d)): os.remove(os.path.join(ROOT,d,f))
for i,s in enumerate(st,1): open(os.path.join(ROOT,'stages',f'{i:02d}_{slug(s["name"])}.gpx'),'w').write(gpx([(i,s)],s["name"]))
open(os.path.join(ROOT,'oslo-lindesnes-nordkapp.gpx'),'w').write(gpx(list(enumerate(st,1)),"Oslo – Lindesnes – Nordkapp"))
for v in VARIANTS:
    open(os.path.join(ROOT,'variants',f'{v["id"]}.gpx'),'w').write(gpx(list(enumerate(vr[v["id"]],1)),v["title"]))
    if any("g" in e for e in next(x for x in variants if x["id"]==v["id"])["stages"]):
        open(os.path.join(ROOT,'variants',f'{v["id"]}-gravel.gpx'),'w').write(gpx(list(enumerate(gr["variants"][v["id"]],1)),v["title"]+", gravel mode"))
open(os.path.join(ROOT,'variants','gravel.gpx'),'w').write(gpx(list(enumerate(gr["main"][:ba-1]+gr["block"]+gr["main"][bb:],1)),"Oslo – Lindesnes – Nordkapp, gravel mode"))

# ---------- map ----------
t=open(os.path.join(HERE,'kart.template.html')).read()
open(os.path.join(ROOT,'kart.html'),'w').write(t.replace('/*DATA*/',json.dumps(DATA,separators=(",",":"),ensure_ascii=False)))

# ---------- RUTE.md generated blocks ----------
def lm_lines(e):
    return [f'- **{l["n"]}** ({"on the route" if l["k"]=="r" else ("detour, "+l["x"][0].lower()+l["x"][1:] if l["x"] else "detour")}). {l["t"]}' for l in e["lm"]]
def hut_rows(label,e):
    return [f'| {label} | {"["+h["n"]+"]("+h["w"]+")" if h["w"] else h["n"]} | {h["c"]} | {h["d"]} | {h["e"]} | {h["cap"]} | {"yes" if h["lock"] else ""} | {h["op"]} |' for h in e["huts"]]
sgn=lambda x:f'+{x}' if x>0 else (f'−{-x}' if x<0 else '±0')
vm=["## Alternative routes","",f"{[0,'One','Two','Three','Four','Five','Six','Seven'][len(variants)]} variants can replace part of the main route. Variants that cover the same stages cannot be combined. Switch them on in [kart.html](kart.html) to see the line and the new totals. Each has its own GPX in [variants/](variants/).","",
    "| Variant | Replaces stages | Distance | Climbing | Days |","|---|---|--:|--:|--:|"]
for v,V in zip(variants,VARIANTS):
    vm.append(f'| {v["title"]} | {v["first"]}–{v["last"]}' .replace(f'{v["first"]}–{v["first"]}',str(v["first"]))+f' | {sgn(v["dkm"])} km | {sgn(v["dasc"])} m | {sgn(v["ddays"])} |')
vm.append("")
for v,V in zip(variants,VARIANTS):
    vm+=[f'### {v["title"]}',"",v["blurb"],""]
    for n in V.get("notes",[]): vm.append(f'- {n}')
    if V.get("notes"): vm.append("")
    vm+=["| Stage | km | Climb m | Gravel km | Ferries |","|---|--:|--:|--:|--:|"]
    for e in v["stages"]: vm.append(f'| {e["name"]} | {e["km"]} | {e["asc"]} | {e["unp"] or ""} | {e["ferries"] or ""} |')
    vm.append("")
    for e in v["stages"]:
        if e["lm"]: vm+=[f'**{e["name"]}**',""]+lm_lines(e)+[""]
    hr=[r for e in v["stages"] for r in hut_rows(e["name"],e)]
    if hr: vm+=["Backup cabins:","","| Stage | Cabin | Type | Off track km | Altitude m | Beds | DNT key | Run by |","|---|---|---|--:|--:|--:|:-:|---|"]+hr+[""]
T=lambda L:(sum(e["km"] for e in L),sum(e["asc"] for e in L),sum(e["unp"] for e in L))
tm,tg=T(main),T(gmain)
vm+=["## Gravel mode","","A switch on the map that moves the route onto gravel roads wherever that makes sense. It also applies to any alternative route that is switched on.","",
     f'With no alternative switched on: {tg[2]} km gravel instead of {tm[2]} km, {sgn(tg[0]-tm[0])} km, {sgn(tg[1]-tm[1])} m climbing, {sgn(len(gmain)-len(main))} day. GPX in [variants/gravel.gpx](variants/gravel.gpx).',""]
vm+=[f'- {n}' for n in GRAVEL_NOTES]
vm+=["","Main route stages that change in gravel mode:","","| Stage | km | Climb m | Gravel km | Without gravel mode |","|---|--:|--:|--:|--:|"]
for i,e in enumerate(main,1):
    if i==ba:
        for x in BE: vm.append(f'| {x["name"]} | {x["km"]} | {x["asc"]} | {x["unp"]} | new, replaces stages {ba}–{bb} |')
    if "g" in e and not ba<=i<=bb: vm.append(f'| {i}. {e["name"]} | {e["g"]["km"]} | {e["g"]["asc"]} | {e["g"]["unp"]} | {e["km"]} km, {e["unp"]} km gravel |')
vm.append("")
for e in BE:
    if e["lm"]: vm+=[f'**{e["name"]}**',""]+lm_lines(e)+[""]
hr=[r for e in BE for r in hut_rows(e["name"],e)]
if hr: vm+=["Backup cabins on the new stages:","","| Stage | Cabin | Type | Off track km | Altitude m | Beds | DNT key | Run by |","|---|---|---|--:|--:|--:|:-:|---|"]+hr+[""]
vm+=["Alternative routes in gravel mode:","","| Variant | Gravel km | Gravel km in gravel mode | Distance change | Stages rerouted | GPX |","|---|--:|--:|--:|--:|---|"]
for v in variants:
    E=v["stages"]; G=[eff(e) for e in E]; n=sum(1 for e in E if "g" in e)
    vm.append(f'| {v["title"]} | {T(E)[2]} | {T(G)[2]} | {sgn(T(G)[0]-T(E)[0])} km | {n} | {"[variants/"+v["id"]+"-gravel.gpx](variants/"+v["id"]+"-gravel.gpx)" if n else "same track"} |')
vm.append("")
md=["## Landmarks and detours by stage","","**On the route** needs no extra riding. **Detour** leaves the track, with the added distance or time in brackets. All of them are marked on [kart.html](kart.html).",""]
for i,e in enumerate(main,1): md+=[f'### {i}. {e["name"]}',""]+lm_lines(e)+[""]
md+=["## DNT cabins as backup","",
"You are camping, so these are for bad weather, a mechanical or a rest. Cabins come from OpenStreetMap entries tagged as DNT or run by a local turistforening or turlag, within 5 km of the track in a straight line. The distance is not the walking distance. Anything more than about 1 km off the track is usually reached on foot.","",
"- **Staffed lodge**: beds and meals in season, book ahead in July.","- **Self-service cabin**: beds, gas and a food store. Locked with the standard DNT key.","- **No-service cabin**: beds and a stove, bring your own food. Usually locked with the DNT key.","",
"Get the DNT key before you leave. It needs a membership and a deposit, from a DNT office. Check each cabin on ut.no before relying on it, since some need booking and some are closed in parts of the summer.","",
"The cabins are almost all in the mountain section, stages 8 to 18. On the coast north of Trondheim there are very few, so the backup there is a cabin at a campsite, which most campsites along Fv17, in Lofoten and on the E6 have.","",
"| Stage | Cabin | Type | Off track km | Altitude m | Beds | DNT key | Run by |","|--:|---|---|--:|--:|--:|:-:|---|"]
for i,e in enumerate(main,1): md+=hut_rows(i,e)
md.append("")
p=os.path.join(ROOT,'RUTE.md'); r=open(p).read()
def put(r,tag,lines,before):
    A=f"<!-- {tag}:START -->"; B=f"<!-- {tag}:END -->"; block=A+"\n"+"\n".join(lines)+"\n"+B+"\n\n"
    if A in r: return r[:r.index(A)]+block+r[r.index(B)+len(B):].lstrip("\n")
    i=r.index(before); return r[:i]+block+r[i:]
r=put(r,"LANDMARKS",md,"## Things that decide the route")
r=put(r,"VARIANTS",vm,"<!-- LANDMARKS:START -->")
open(p,'w').write(r)
print("main",len(main),"stages",sum(e["km"] for e in main),"km; huts",sum(len(e["huts"]) for e in main),"landmarks",sum(len(e["lm"]) for e in main))
print("gravel mode main:",len(gmain),"stages",tg,"vs",tm)
for v in variants: print("   g",v["id"],T(v["stages"]),"->",T([eff(e) for e in v["stages"]]),sum(1 for e in v["stages"] if "g" in e),"stages rerouted")
for v in variants: print(" ",v["id"],"replaces",v["first"],v["last"],"dkm",v["dkm"],"dasc",v["dasc"],"ddays",v["ddays"],"huts",sum(len(e["huts"]) for e in v["stages"]),"lm",sum(len(e["lm"]) for e in v["stages"]))
print("kart.html MB",os.path.getsize(os.path.join(ROOT,'kart.html'))/1e6)
