import json, glob, os, statistics, re
from collections import defaultdict

def ajan(f):
    try:
        d=open(f,encoding="utf-8",errors="replace").read(200000)
    except: return "?"
    m=re.search(r'"agentName":"([^"]*)"', d)
    if not m: return "?"
    s=m.group(1)
    if s.startswith("Clara"): return "Clara"
    m2=re.match(r'OY · (\w+)', s)
    return "OY-"+m2.group(1) if m2 else s[:20]

def analiz(f):
    kayit=[]
    with open(f, encoding="utf-8", errors="replace") as fh:
        for ln in fh:
            try: o=json.loads(ln)
            except: continue
            t=o.get("type")
            if t not in ("assistant","user"): continue
            c=(o.get("message") or {}).get("content")
            txt=""; tool=False; tres=False
            if isinstance(c,list):
                for x in c:
                    if not isinstance(x,dict): continue
                    if x.get("type")=="text": txt+=x.get("text","")
                    if x.get("type")=="tool_use": tool=True
                    if x.get("type")=="tool_result": tres=True
            elif isinstance(c,str): txt=c
            kayit.append((t,txt.strip(),tool,tres))
    A=[];R=[]
    for i,(t,txt,tool,tres) in enumerate(kayit):
        if t!="assistant" or not txt: continue
        nxt=None
        for j in range(i+1,len(kayit)):
            tt,_,tl,tr=kayit[j]
            if tt=="assistant" and tl: nxt="TOOL"; break
            if tt=="user" and not tr: nxt="USER"; break
            if tt=="assistant": nxt="TEXT"; break
        (R if nxt=="TOOL" else A).append(len(txt))
    return A,R

files = sorted(glob.glob("*.jsonl"), key=os.path.getmtime)[-40:]
g=defaultdict(lambda:{"A":[], "R":[], "n":0})
for f in files:
    a=ajan(f)
    k = "Clara" if a=="Clara" else ("OY-ekip" if a.startswith("OY-") else "diger")
    A,R=analiz(f)
    g[k]["A"]+=A; g[k]["R"]+=R; g[k]["n"]+=1

for k,v in sorted(g.items()):
    A,R=sorted(v["A"]),sorted(v["R"])
    if not A and not R: continue
    tA,tR=sum(A),sum(R)
    print(f"### {k}  ({v['n']} oturum)")
    if A: print(f"  ASIL CEVAP : adet={len(A)} medyan={A[len(A)//2]} ort={int(statistics.mean(A))} p90={A[int(len(A)*.9)]} max={A[-1]}")
    if R: print(f"  ARA METIN  : adet={len(R)} medyan={R[len(R)//2]} ort={int(statistics.mean(R))} p90={R[int(len(R)*.9)]}")
    print(f"  ARA ORANI  : %{100*tR/max(1,(tA+tR)):.0f}   |  kullanici mesaji basina ara blok: {len(R)/max(1,len(A)):.1f}")
    if A:
        ust=[x for x in A if x>1803]
        print(f"  1803+ asan asil cevap: %{100*len(ust)/len(A):.0f} ({len(ust)}/{len(A)})")
    print()
