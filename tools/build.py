import json, os, math, html
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
st=json.load(open(os.path.join(HERE,'routed.json')))
def esc(s): return html.escape(s,quote=True)
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
    for a,b in (("ø","o"),("å","a"),("æ","ae"),("Ø","O"),("Å","A"),(" – ","_"),(" ","-"),("(",""),(")","")): s=s.replace(a,b)
    return s
os.makedirs(os.path.join(ROOT,'stages'),exist_ok=True)
for f in os.listdir(os.path.join(ROOT,'stages')): os.remove(os.path.join(ROOT,'stages',f))
for i,s in enumerate(st,1):
    open(os.path.join(ROOT,'stages',f'{i:02d}_{slug(s["name"])}.gpx'),'w').write(gpx([(i,s)],s["name"]))
open(os.path.join(ROOT,'oslo-lindesnes-nordkapp.gpx'),'w').write(gpx(list(enumerate(st,1)),"Oslo – Lindesnes – Nordkapp"))
# simplified geometry for the map
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
        if dm>tol: keep.append(im); stack+= [(a,im),(im,b)]
    return [pts[i] for i in sorted(keep)]
import sys; sys.path.insert(0,HERE)
from landmarks import LANDMARKS
LG=json.load(open(os.path.join(HERE,'landmark_geo.json')))
def lms(n,s):
    out=[]
    pts=[c for g in s["segs"] if not g["ferry"] for c in g["coords"]]
    for kind,name,q,la,lo,extra,text in LANDMARKS.get(n,[]):
        if name in LG: la,lo=LG[name]
        elif kind=="route":   # no geocode: snap to the nearest track point
            k=math.cos(math.radians(la)); c=min(pts,key=lambda c:((c[0]-lo)*k)**2+(c[1]-la)**2)
            if math.hypot((c[0]-lo)*k,c[1]-la)<0.1: la,lo=c[1],c[0]
        out.append({"k":kind[0],"n":name,"x":extra,"t":text,"ll":[round(la,5),round(lo,5)]})
    return out
import re
HN=json.load(open(os.path.join(HERE,'huts_near.json')))
KIND={"betjent":"Staffed lodge","selvbetjent":"Self-service cabin","ubetjent":"No-service cabin"}
def huts(n):
    out=[]
    for i,d,name,cls,tour,ele,cap,lock,op,la,lo,web in HN:
        if i!=n or d>5 or cls=="stengt" or re.search(r"dagsturhytt|perletur|sikringsbu",name,re.I): continue
        if not re.match(r"https?://",web or ""): web=""
        out.append({"n":name,"c":KIND.get(cls,"Cabin, type not recorded"),"d":d,"e":ele,"cap":cap,"lock":lock=="yes","op":op,"w":web,"ll":[la,lo]})
    return sorted(out,key=lambda h:h["d"])
m=[]; cum=0
for i,s in enumerate(st,1):
    cum+=s["km"]
    m.append({"n":i,"name":s["name"],"km":round(s["km"]),"asc":int(round(s["asc"],-1)),"cum":round(cum),"unp":round(s["unpaved_km"]),
              "ferries":len(s["ferries"]),"lm":lms(i,s),"huts":huts(i),"segs":[{"f":g["ferry"],"c":[[round(c[1],5),round(c[0],5)] for c in simp(g["coords"])]} for g in s["segs"]]})
json.dump(m,open(os.path.join(HERE,'map.json'),'w'),separators=(",",":"))
rows=["| # | Stage | km | Climb m | Gravel km | Ferries | Total km |","|--:|---|--:|--:|--:|--:|--:|"]
for x in m: rows.append(f'| {x["n"]} | {x["name"]} | {x["km"]} | {x["asc"]} | {x["unp"] or ""} | {x["ferries"] or ""} | {x["cum"]} |')
open(os.path.join(HERE,'table.md'),'w').write("\n".join(rows))
print("\n".join(rows)); print("TOTAL",round(cum),"km",round(sum(s["asc"] for s in st)),"m; unpaved",round(sum(s["unpaved_km"] for s in st)))
print("gpx MB",os.path.getsize(os.path.join(ROOT,'oslo-lindesnes-nordkapp.gpx'))/1e6,"map.json MB",os.path.getsize(os.path.join(HERE,'map.json'))/1e6)
t=open(os.path.join(HERE,'kart.template.html')).read()
b_end=next(i for i,s in enumerate(st,1) if s["name"].endswith("Trondheim"))
open(os.path.join(ROOT,'kart.html'),'w').write(t.replace('/*DATA*/',json.dumps(m,separators=(",",":"))).replace('PART_B_END',str(b_end)))

md=["## Landmarks and detours by stage","","**On the route** needs no extra riding. **Detour** leaves the track, with the added distance or time in brackets. All of them are marked on [kart.html](kart.html).",""]
for x in m:
    md.append(f'### {x["n"]}. {x["name"]}'); md.append("")
    for l in x["lm"]:
        md.append(f'- **{l["n"]}** ({"on the route" if l["k"]=="r" else "detour, "+l["x"][0].lower()+l["x"][1:] if l["x"] else "detour"}). {l["t"]}')
    md.append("")
md+=["## DNT cabins as backup","",
"You are camping, so these are for bad weather, a mechanical or a rest. Cabins come from OpenStreetMap entries tagged as DNT or run by a local turistforening or turlag, within 5 km of the track in a straight line. The distance is not the walking distance. Anything more than about 1 km off the track is usually reached on foot.","",
"- **Staffed lodge**: beds and meals in season, book ahead in July.","- **Self-service cabin**: beds, gas and a food store. Locked with the standard DNT key.","- **No-service cabin**: beds and a stove, bring your own food. Usually locked with the DNT key.","",
"Get the DNT key before you leave. It needs a membership and a deposit, from a DNT office. Check each cabin on ut.no before relying on it, since some need booking and some are closed in parts of the summer.","",
"The cabins are almost all in the mountain section, stages 8 to 18. On the coast north of Trondheim there are very few, so the backup there is a cabin at a campsite, which most campsites along Fv17, in Lofoten and on the E6 have.","",
"| Stage | Cabin | Type | Off track km | Altitude m | Beds | DNT key | Run by |","|--:|---|---|--:|--:|--:|:-:|---|"]
for x in m:
    for h in x["huts"]:
        nm=f'[{h["n"]}]({h["w"]})' if h["w"] else h["n"]
        md.append(f'| {x["n"]} | {nm} | {h["c"]} | {h["d"]} | {h["e"]} | {h["cap"]} | {"yes" if h["lock"] else ""} | {h["op"]} |')
md.append("")
p=os.path.join(ROOT,'RUTE.md'); r=open(p).read()
A="<!-- LANDMARKS:START -->"; B="<!-- LANDMARKS:END -->"
block=A+"\n"+"\n".join(md)+B+"\n\n"
if A in r: r=r[:r.index(A)]+block+r[r.index(B)+len(B):].lstrip("\n")
else: i=r.index("## Things that decide the route"); r=r[:i]+block+r[i:]
open(p,'w').write(r)
print("huts",sum(len(x["huts"]) for x in m),"stages with huts",sum(1 for x in m if x["huts"]))
print("landmarks",sum(len(x["lm"]) for x in m),"detours",sum(1 for x in m for l in x["lm"] if l["k"]=="d"))
