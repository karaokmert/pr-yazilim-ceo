"""Gorev #6: yetim memory envanteri — 1537 dosyada deger var mi?

Mert'in ihtiyaci: "agent memory'leri localde kalinca goremiyorum, neler var
neler bayat takip edilemiyor" + "agent bu memory'yi aktif kullanabilmeli."

Bu script ONCE deger olcer, sonra kapi acilir. Cope kapi acmak da maliyet.

Uc olcum:
  1. ESLESME  — hangi v7 kutusunun plugin karsiligi var (project-assistant ->
                ozel-yazilim-project-assistant). Karsiligi olmayan = tamamen yetim.
  2. ORTUSME  — eski kutudaki bir konu yeni kutuda da var mi? (dosya adi + baslik
                bazli). Ortusmuyorsa o bilgi KAYIP.
  3. TAZELIK  — kayit v7 kanonuna mi dayaniyor? (v7-only kavramlar: eski agent
                adlari, skill-project yollari, kalkmis kurallar)

Kullanim: python3 sprint/memory-envanter.py
"""
import re, json
from pathlib import Path
from collections import defaultdict

MEM = Path.home() / ".claude/agent-memory"
PLUGIN = Path.home() / ".claude/plugins/cache/pryazilim-agents"

# v7 -> v8 ad eslemesi (plugin prefix'i)
PREFIX = ["ozel-yazilim-", "websitesi-web-", "websitesi-"]

# v7'ye ozgu isaretler: bunlar geciyorsa kayit eski dunyaya dayaniyor
V7_ISARET = [
    r"skill-project",           # emekli repo
    r"v7\b",
    r"\.claude/skills/",        # v8'de plugin'den geliyor
    r"docs/v8-calisma",
    r"release tag|vX\.Y\.Z",    # kaldirilan sistem
]


def kutular():
    """Her memory klasoru: dosya sayisi, son yazma, plugin karsiligi."""
    out = {}
    for d in sorted(MEM.iterdir()):
        if not d.is_dir():
            continue
        dosyalar = list(d.rglob("*.md"))
        if not dosyalar:
            continue
        son = max(p.stat().st_mtime for p in dosyalar)
        out[d.name] = {"yol": d, "n": len(dosyalar), "son": son,
                       "dosyalar": dosyalar}
    return out


def plugin_karsiligi(ad, hepsi):
    """project-assistant -> ozel-yazilim-project-assistant var mi?"""
    for p in PREFIX:
        if (p + ad) in hepsi:
            return p + ad
    return None


def yeni_mi(ad):
    return any(ad.startswith(p) for p in PREFIX)


def konu_seti(dosyalar):
    """Dosya adlarindan konu seti — ortusme icin."""
    s = set()
    for p in dosyalar:
        if p.name == "MEMORY.md":
            continue
        # tur_konu.md -> konu
        ad = p.stem
        ad = re.sub(r"^(feedback|project|user|reference|domain|pattern)[_-]", "", ad)
        s.add(ad.lower())
    return s


def v7_orani(dosyalar):
    """Kac dosyada v7 isareti var?"""
    isaretli = 0
    for p in dosyalar:
        try:
            tx = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        if any(re.search(r, tx, re.I) for r in V7_ISARET):
            isaretli += 1
    return isaretli


def main():
    K = kutular()
    print("=" * 78)
    print("OLCUM 1 — ESLESME: hangi v7 kutusunun plugin karsiligi var?")
    print("=" * 78)
    eski = {a: v for a, v in K.items() if not yeni_mi(a)}
    yeni = {a: v for a, v in K.items() if yeni_mi(a)}
    print(f"\n  v7 adli kutu: {len(eski)}  ({sum(v['n'] for v in eski.values())} dosya)")
    print(f"  plugin adli : {len(yeni)}  ({sum(v['n'] for v in yeni.values())} dosya)\n")

    ciftler, yetimler = [], []
    for ad, v in sorted(eski.items(), key=lambda x: -x[1]["n"]):
        k = plugin_karsiligi(ad, K)
        if k:
            ciftler.append((ad, k, v["n"], K[k]["n"]))
        else:
            yetimler.append((ad, v["n"]))

    print("  CIFT (eski + yeni kutu ikisi de var — bilgi BOLUNMUS):")
    for e, y, ne, ny in ciftler:
        print(f"    {ne:4d} <- {e:32s} | {y:38s} -> {ny:3d}")
    print(f"\n  TAM YETIM (plugin karsiligi YOK):")
    for a, n in sorted(yetimler, key=lambda x: -x[1]):
        print(f"    {n:4d}  {a}")

    print("\n" + "=" * 78)
    print("OLCUM 2 — ORTUSME: eski kutudaki konu yeni kutuda da var mi?")
    print("=" * 78)
    print("  (ortusmeyen konu = o bilgi bugun ERISILEMEZ)\n")
    for e, y, ne, ny in ciftler:
        se, sy = konu_seti(K[e]["dosyalar"]), konu_seti(K[y]["dosyalar"])
        ortak = se & sy
        sadece_eski = se - sy
        print(f"  {e} -> {y}")
        print(f"    eski konu: {len(se)}  yeni konu: {len(sy)}  ORTAK: {len(ortak)}")
        print(f"    yalniz eskide: {len(sadece_eski)} konu")
        if sadece_eski:
            ornek = sorted(sadece_eski)[:6]
            print(f"      ornek: {', '.join(ornek)}")
        print()

    print("=" * 78)
    print("OLCUM 3 — TAZELIK: kayit v7 dunyasina mi dayaniyor?")
    print("=" * 78)
    print("  (v7 isareti: skill-project, v7, .claude/skills/, release tag)\n")
    for e, y, ne, ny in ciftler:
        iv = v7_orani(K[e]["dosyalar"])
        print(f"  {e:34s} {iv:4d}/{ne:4d} dosyada v7 isareti (%{100*iv//max(ne,1)})")
    for a, n in sorted(yetimler, key=lambda x: -x[1])[:6]:
        iv = v7_orani(K[a]["dosyalar"])
        print(f"  {a:34s} {iv:4d}/{n:4d} dosyada v7 isareti (%{100*iv//max(n,1)})")

    print("\n" + "=" * 78)
    print("KARAR GIRDISI")
    print("=" * 78)
    print("  Ortusme YUKSEK + v7 isareti YUKSEK  -> arsivle/sil (bilgi yeni kutuda var)")
    print("  Ortusme DUSUK  + v7 isareti DUSUK   -> TASI (gercek kayip, deger var)")
    print("  Ortusme DUSUK  + v7 isareti YUKSEK  -> tek tek bak (bilgi var ama eski dunya)")


if __name__ == "__main__":
    main()
