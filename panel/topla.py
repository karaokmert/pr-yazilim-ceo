#!/usr/bin/env python3
"""Clara paneli — acik agent oturumlarini toplar, panel/durum.json'a yazar.

Calistir:  python3 panel/topla.py          (surekli, 10 sn'de bir)
           python3 panel/topla.py --once   (tek sefer)
"""
import glob
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta

BASE = os.path.expanduser("~/.claude/projects")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "durum.json")
TZ = timezone(timedelta(hours=3))

# Bekleme kaliplari — "sana ihtiyacim var" bes ayri bicimde geliyor
ONAY_KALIP = [
    "onayını bekliyorum", "onayini bekliyorum", "onay bekliyorum",
    "onaylıyor musun", "onayliyor musun", "uygun mu", "şimdi söyle",
    "simdi soyle", "başlayayım mı", "baslayayim mi", "devam edeyim mi",
    "geçeyim mi", "yapayım mı", "onayınla", "onayinla", "karar senin",
]
IZIN_ARAC = ("Bash", "Write", "Edit", "NotebookEdit")


def canli_oturumlar():
    """ps + lsof ile acik agent süreçlerini bul."""
    out = []
    try:
        ps = subprocess.run(["ps", "ax", "-o", "pid=,etime=,command="],
                            capture_output=True, text=True, timeout=10).stdout
    except Exception:
        return out
    for satir in ps.splitlines():
        if "--agent" not in satir or "grep" in satir or "/bin/zsh" in satir:
            continue
        m = re.match(r"\s*(\d+)\s+(\S+)\s+(.*)", satir)
        if not m:
            continue
        pid, etime, cmd = m.group(1), m.group(2), m.group(3)
        rm = re.search(r"--agent\s+(\S+)", cmd)
        rol = rm.group(1).split(":")[-1] if rm else "?"
        cwd = "?"
        try:
            lf = subprocess.run(["lsof", "-a", "-p", pid, "-d", "cwd", "-Fn"],
                                capture_output=True, text=True, timeout=8).stdout
            for l in lf.splitlines():
                if l.startswith("n/"):
                    cwd = l[1:]
                    break
        except Exception:
            pass
        out.append({"pid": pid, "rol": rol, "proje": os.path.basename(cwd),
                    "yol": cwd, "sure": etime})
    return out


def sure_sn(etime):
    """ps etime -> saniye.  [[dd-]hh:]mm:ss"""
    try:
        gun = 0
        if "-" in etime:
            g, etime = etime.split("-", 1)
            gun = int(g)
        p = [int(x) for x in etime.split(":")]
        while len(p) < 3:
            p.insert(0, 0)
        return gun * 86400 + p[0] * 3600 + p[1] * 60 + p[2]
    except Exception:
        return 0


def oturum_tara(dosya):
    """Bir .jsonl oturum kaydini oku: rol + son olay + bekleme durumu."""
    son_mesaj = ""
    son_kim = ""
    son_ts = None
    bekleyen_arac = {}
    bekleme = None
    bekleme_ne = ""
    skiller = []
    rol = "?"
    baslik = ""
    try:
        with open(dosya, errors="replace") as fh:
            for line in fh:
                if not line.strip():
                    continue
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                ts = d.get("timestamp")
                if ts:
                    son_ts = ts
                t = d.get("type")
                if t == "agent-setting":
                    rol = str(d.get("agentSetting", "?")).split(":")[-1]
                    continue
                if t in ("agent-name", "custom-title"):
                    baslik = d.get("agentName") or d.get("customTitle") or baslik
                    continue
                if t == "user":
                    c = (d.get("message") or {}).get("content")
                    if isinstance(c, list):
                        for b in c:
                            if b.get("type") == "tool_result":
                                bekleyen_arac.pop(b.get("tool_use_id"), None)
                    elif isinstance(c, str) and not c.startswith("<") and len(c) > 10:
                        son_mesaj = " ".join(c.split())[:220]
                        son_kim = "MERT"
                        bekleme = None
                        bekleme_ne = ""
                elif t == "assistant":
                    c = (d.get("message") or {}).get("content")
                    if not isinstance(c, list):
                        continue
                    for b in c:
                        tip = b.get("type")
                        if tip == "tool_use":
                            ad = b.get("name")
                            inp = b.get("input") or {}
                            if ad == "Skill":
                                s = inp.get("skill")
                                if s:
                                    skiller.append(s)
                            elif ad == "AskUserQuestion":
                                qs = inp.get("questions") or []
                                if qs:
                                    bekleme = "SECENEKLI SORU"
                                    bekleme_ne = " ".join(
                                        str(qs[0].get("question", "")).split())[:200]
                            elif ad in IZIN_ARAC:
                                ne = inp.get("command") or inp.get("file_path") or ""
                                bekleyen_arac[b.get("id")] = (ad, " ".join(str(ne).split())[:160])
                        elif tip == "text":
                            tx = b.get("text", "")
                            if len(tx) < 40:
                                continue
                            son_mesaj = " ".join(tx.split())[-220:]
                            son_kim = "AGENT"
                            sonluk = tx[-450:].lower()
                            if "HANDOFF" in tx.upper() and len(tx) > 200:
                                bekleme = "HANDOFF URETTI"
                                i = tx.upper().find("HANDOFF")
                                bekleme_ne = " ".join(tx[i:i + 160].split())
                            elif any(k in sonluk for k in ONAY_KALIP):
                                bekleme = "ONAY BEKLIYOR"
                                bekleme_ne = " ".join(tx[-200:].split())
                            elif tx.rstrip().endswith("?"):
                                bekleme = "SORU"
                                parc = [p.strip() for p in tx.replace("\n", " ").split("?") if p.strip()]
                                bekleme_ne = (" ".join(parc[-1][-160:].split()) + "?") if parc else ""
                            else:
                                bekleme = None
                                bekleme_ne = ""
    except Exception:
        pass

    if bekleyen_arac:
        ad, ne = list(bekleyen_arac.values())[-1]
        bekleme = "IZIN BEKLIYOR"
        bekleme_ne = f"[{ad}] {ne}"

    return {"son_mesaj": son_mesaj, "son_kim": son_kim, "son_ts": son_ts,
            "bekleme": bekleme, "bekleme_ne": bekleme_ne,
            "rol": rol, "baslik": baslik, "skiller": skiller[-12:]}


def gecen(ts):
    """ISO timestamp -> insan okunur gecen sure + saniye."""
    if not ts:
        return "?", 0
    try:
        t = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        sn = int((datetime.now(timezone.utc) - t).total_seconds())
    except Exception:
        return "?", 0
    if sn < 60:
        return f"{sn} sn", sn
    if sn < 3600:
        return f"{sn // 60} dk", sn
    if sn < 86400:
        return f"{sn // 3600} sa {(sn % 3600) // 60} dk", sn
    return f"{sn // 86400} gun {(sn % 86400) // 3600} sa", sn


def topla():
    canli = canli_oturumlar()
    projeler = {}
    for c in canli:
        projeler.setdefault(c["proje"], []).append(c)

    kayit = []
    for pdir in glob.glob(os.path.join(BASE, "*")):
        if not os.path.isdir(pdir):
            continue
        m = re.match(r"-Users-karaok-p-(?:ozel-yazilim-)?(.+)$", os.path.basename(pdir))
        proje = m.group(1) if m else os.path.basename(pdir)
        if proje not in projeler:
            continue
        dosyalar = glob.glob(os.path.join(pdir, "*.jsonl"))
        if not dosyalar:
            continue
        # acik surec sayisi kadar en yeni oturum (+ pay) — rol kayittan gelecek
        dosyalar.sort(key=os.path.getmtime, reverse=True)
        n = min(len(dosyalar), len(projeler[proje]) + 2)
        for f in dosyalar[:n]:
            bilgi = oturum_tara(f)
            gs, gsn = gecen(bilgi["son_ts"])
            kayit.append({
                "proje": proje,
                "oturum": os.path.basename(f)[:8],
                "rol": bilgi["rol"],
                "baslik": bilgi["baslik"],
                "son_hareket": gs,
                "son_hareket_sn": gsn,
                "son_kim": bilgi["son_kim"],
                "son_mesaj": bilgi["son_mesaj"],
                "bekleme": bilgi["bekleme"],
                "bekleme_ne": bilgi["bekleme_ne"],
                "skiller": bilgi["skiller"],
            })

    # ayni projede ayni rolden kac canli surec var — oturum "canli mi" isareti
    for proje, srcs in projeler.items():
        sayim = {}
        for s in srcs:
            sayim[s["rol"]] = sayim.get(s["rol"], 0) + 1
        satirlar = sorted([k for k in kayit if k["proje"] == proje],
                          key=lambda k: k["son_hareket_sn"])
        for k in satirlar:
            if sayim.get(k["rol"], 0) > 0:
                k["canli"] = True
                sayim[k["rol"]] -= 1
            else:
                k["canli"] = False

    kayit.sort(key=lambda k: (k["proje"], k["son_hareket_sn"]))
    veri = {
        "guncelleme": datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S"),
        "acik_surec": len(canli),
        "proje_sayisi": len(projeler),
        "oturumlar": kayit,
    }
    tmp = OUT + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(veri, fh, ensure_ascii=False, indent=1)
    os.replace(tmp, OUT)
    return veri


if __name__ == "__main__":
    tek = "--once" in sys.argv
    while True:
        try:
            v = topla()
            print(f"[{v['guncelleme']}] {v['acik_surec']} surec / "
                  f"{v['proje_sayisi']} proje / {len(v['oturumlar'])} oturum",
                  flush=True)
        except Exception as e:
            print("HATA:", e, flush=True)
        if tek:
            break
        time.sleep(10)
