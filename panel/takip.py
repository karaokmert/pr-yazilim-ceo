import json, os, time, glob

BASE = os.path.expanduser("~/.claude/projects")
PROJ = {
    "-Users-karaok-p-ozel-yazilim-goat": "GOAT",
    "-Users-karaok-p-ozel-yazilim-egelisaglik": "EGELI",
    "-Users-karaok-p-ozel-yazilim-platin-agent-web": "PLATIN",
    "-Users-karaok-p-agent-project": "FABRIKA",
    "-Users-karaok-p-ozel-yazilim-osinif": "OSINIF",
}

pos = {}
for d in PROJ:
    for f in glob.glob(os.path.join(BASE, d, "*.jsonl")):
        pos[f] = os.path.getsize(f)


def kisa(t, n=130):
    return " ".join(str(t).split())[:n]


BEKLEYEN = {}   # tool_use_id -> (tag, sid, arac, ne)
DUYURULAN = set()
GORULDU = set()


def isle(dd, tag, sid):
    t = dd.get("type")

    if t == "user":
        c = (dd.get("message") or {}).get("content")
        # arac sonucu geldiyse bekleyen listesinden dus
        if isinstance(c, list):
            for b in c:
                if b.get("type") == "tool_result":
                    BEKLEYEN.pop(b.get("tool_use_id"), None)
            return
        if isinstance(c, str) and not c.startswith("<") and len(c) > 15:
            bas = c.lstrip()[:40].upper()
            if bas.startswith("---HANDOFF") or bas.startswith("HANDOFF") or bas.startswith("**HANDOFF"):
                print(f"[{tag}/{sid}] MERT HANDOFF TASIDI >> {kisa(c, 100)}", flush=True)
            else:
                # Mert'in mesaji KIRPILMAZ - kayit degeri tam metinde.
                print(f"[{tag}/{sid}] MERT: {' '.join(c.split())}", flush=True)
        return

    if t != "assistant":
        return

    c = (dd.get("message") or {}).get("content")
    if not isinstance(c, list):
        return

    for b in c:
        tip = b.get("type")

        if tip == "tool_use" and b.get("name") == "AskUserQuestion":
            for q in (b.get("input") or {}).get("questions") or []:
                h = q.get("header", "")
                print(f"[{tag}/{sid}] >>> AGENT SECENEKLI SORDU [{h}]: {kisa(q.get('question',''))}", flush=True)
            continue

        if tip == "tool_use" and b.get("name") in ("Bash", "Write", "Edit"):
            # Sonucu gelmeyen cagri = izin bekliyor. Kaydi tut, sonuc gelirse dus.
            BEKLEYEN[b.get("id")] = (tag, sid, b.get("name"),
                                     kisa((b.get("input") or {}).get("command")
                                          or (b.get("input") or {}).get("file_path", ""), 80))
            continue

        if tip != "text":
            continue

        tx = b.get("text", "")
        if len(tx) < 60:
            continue

        son = tx[-450:].lower()
        bekleme = [
            "onayını bekliyorum", "onayini bekliyorum", "onay bekliyorum",
            "beklediğim:** plan onayı", "beklediğim: plan onayı",
            "onaylıyor musun", "onayliyor musun", "uygun mu",
            "şimdi söyle", "simdi soyle", "karar senin", "kararı senin",
            "onayınla", "onayinla", "başlayayım mı", "baslayayim mi",
            "devam edeyim mi", "geçeyim mi", "gecyim mi", "yapayım mı",
        ]
        bekliyor = any(k in son for k in bekleme)

        # Gercek handoff: SATIR BASINDA "---HANDOFF" ya da "HANDOFF (TUR)" kalibi.
        # Metnin ortasinda gecen "handoff" kelimesi handoff URETIMI degildir.
        gercek = None
        for ln in tx.splitlines():
            s = ln.strip()
            u = s.upper()
            if u.startswith("---HANDOFF") or u.startswith("**HANDOFF") or (
                u.startswith("HANDOFF") and "(" in s[:20]
            ):
                gercek = s
                break

        if gercek and len(tx) > 200:
            i = tx.find(gercek)
            print(f"[{tag}/{sid}] AGENT HANDOFF URETTI >> {kisa(tx[i:i+130])}", flush=True)
            if bekliyor:
                print(f"[{tag}/{sid}] >>> VE ONAY BEKLIYOR", flush=True)
        elif bekliyor:
            print(f"[{tag}/{sid}] >>> AGENT ONAY BEKLIYOR: {kisa(tx[-200:])}", flush=True)
        elif tx.rstrip().endswith("?"):
            parc = [p.strip() for p in tx.replace("\n", " ").split("?") if p.strip()]
            q = (parc[-1][-140:] + "?") if parc else tx[-140:]
            print(f"[{tag}/{sid}] >>> AGENT SORDU: {kisa(q)}", flush=True)


while True:
    for d, tag in PROJ.items():
        for f in glob.glob(os.path.join(BASE, d, "*.jsonl")):
            try:
                sz = os.path.getsize(f)
            except OSError:
                continue

            sid = os.path.basename(f)[:8]

            if f not in pos:
                pos[f] = sz
                print(f"[{tag}] YENI OTURUM acildi ({sid})", flush=True)
                continue

            if sz <= pos[f]:
                continue

            try:
                with open(f) as fh:
                    fh.seek(pos[f])
                    yeni = fh.read()
            except OSError:
                continue
            pos[f] = sz

            for line in yeni.splitlines():
                if not line.strip():
                    continue
                try:
                    dd = json.loads(line)
                except Exception:
                    continue
                try:
                    isle(dd, tag, sid)
                except Exception:
                    pass

    # sonucu gelmemis arac cagrisi = izin bekliyor
    for tid, (tag, sid, arac, ne) in list(BEKLEYEN.items()):
        if tid in DUYURULAN:
            continue
        # bir tur bekle: sonucu ayni okumada gelmemis olabilir
        if tid not in GORULDU:
            GORULDU.add(tid)
            continue
        DUYURULAN.add(tid)
        print(f"[{tag}/{sid}] >>> IZIN BEKLIYOR [{arac}]: {ne}", flush=True)

    time.sleep(15)
