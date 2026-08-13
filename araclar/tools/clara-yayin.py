#!/usr/bin/env python3
"""Clara yayın kanalı — merkezden (pr-yazilim-ceo) proje Clara'larına toplu mesaj.

YALNIZ Clara kutularına yazar. Agent kutularına ASLA yazmaz (CLA-NO-CALL-TEAMS).

Kullanım:
  clara-yayin.py --liste                          # kimler canlı, kim izliyor
  clara-yayin.py --tip INFO --stdin               # tüm canlı Clara'lara
  clara-yayin.py --tip TASK --hedef goat --stdin  # tek projeye
  clara-yayin.py --tip INFO --stdin --kuru        # yazmadan dene

Teslim doğrulanır: yazılan her dosya tekrar okunur, gövde uzunluğu karşılaştırılır.
rc=0 yalnız HEPSİ teslim edildiyse döner.
"""
import sys, os, json, glob, subprocess, argparse
from datetime import datetime

KOK = os.path.expanduser("~/.pr-kanal")
BEN = "clara-ev"
TIPLER = ("TASK", "INFO", "QUESTION", "CLOSE")
HARIC = {"ceo"}          # kendi kutum
ESKI_GUN_SINIRI = 1      # bugünden eski kutular ölü sayılır


def izleyiciler():
    try:
        c = subprocess.run(["ps", "aux"], capture_output=True, text=True, timeout=10)
        return "\n".join(l for l in c.stdout.splitlines() if "watch.py" in l and "grep" not in l)
    except Exception:
        return ""


def clara_kutulari():
    ps = izleyiciler()
    bugun = datetime.now().strftime("%Y%m%d")
    out = []
    for yol in sorted(glob.glob(os.path.join(KOK, "*", "*"))):
        if not os.path.isdir(yol):
            continue
        kutu, proje = os.path.basename(yol), os.path.basename(os.path.dirname(yol))
        if proje in HARIC or not kutu.lower().startswith("clara"):
            continue
        inbox = os.path.join(yol, "inbox")
        if not os.path.isdir(inbox):
            continue
        out.append({
            "proje": proje, "kutu": kutu, "inbox": inbox,
            "izleniyor": f"{proje}/{kutu}/inbox" in ps,
            "bugun": bugun in kutu,
            "mesaj": len(glob.glob(os.path.join(inbox, "*.json"))),
        })
    return out


def yaz(inbox, tip, govde):
    """Yazar ve GERİ OKUYARAK doğrular. (ok, ayrıntı) döner."""
    ad = datetime.now().strftime("%Y%m%d-%H%M%S.%f") + f"-{BEN}.json"
    hedef = os.path.join(inbox, ad)
    kayit = {"from": BEN, "to": "Clara",
             "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
             "type": tip, "body": govde}
    try:
        with open(hedef, "w", encoding="utf-8") as f:
            json.dump(kayit, f, ensure_ascii=False, indent=2)
    except Exception as e:
        return False, f"yazma hatasi: {e}"
    # DOĞRULAMA — rc=0 yeterli değil (ölçüldü: send.py yanlış yere yazıp rc=0 döndü)
    if not os.path.exists(hedef):
        return False, "dosya yazildiktan sonra YOK"
    try:
        g = json.load(open(hedef, encoding="utf-8"))
    except Exception as e:
        return False, f"geri okunamadi: {e}"
    if len(g.get("body", "")) != len(govde):
        return False, f"govde kesildi: {len(g.get('body',''))}/{len(govde)}"
    return True, ad


def main():
    a = argparse.ArgumentParser(add_help=False)
    a.add_argument("--liste", action="store_true")
    a.add_argument("--tip", choices=TIPLER)
    a.add_argument("--hedef")
    a.add_argument("--stdin", action="store_true")
    a.add_argument("--govde")
    a.add_argument("--kuru", action="store_true")
    a.add_argument("--olu-dahil", action="store_true")
    a.add_argument("-h", "--help", action="store_true")
    o = a.parse_args()

    if o.help:
        print(__doc__); return 0

    kutular = clara_kutulari()

    if o.liste or not o.tip:
        print(f"{'PROJE':<16}{'KUTU':<28}{'IZLEYICI':<10}{'BUGUN':<8}MESAJ")
        print("-" * 70)
        for k in kutular:
            print(f"{k['proje']:<16}{k['kutu']:<28}"
                  f"{'VAR' if k['izleniyor'] else 'yok':<10}"
                  f"{'evet' if k['bugun'] else 'ESKI':<8}{k['mesaj']}")
        canli = [k for k in kutular if k["izleniyor"] and k["bugun"]]
        print(f"\nCanli hedef: {len(canli)}/{len(kutular)} "
              f"({', '.join(k['proje'] for k in canli) or 'yok'})")
        if not o.tip:
            return 0

    govde = sys.stdin.read() if o.stdin else (o.govde or "")
    if not govde.strip():
        print("HATA: govde bos (--stdin ya da --govde)"); return 1

    hedefler = [k for k in kutular if o.olu_dahil or (k["izleniyor"] and k["bugun"])]
    if o.hedef:
        hedefler = [k for k in hedefler if k["proje"] == o.hedef]
    if not hedefler:
        print("HATA: hedef yok"); return 1

    print(f"\n{'KURU DENEME' if o.kuru else 'YAYIN'} · tip={o.tip} · "
          f"{len(govde)} karakter · {len(hedefler)} hedef\n")
    ok = 0
    for k in hedefler:
        if o.kuru:
            print(f"  [kuru] {k['proje']}/{k['kutu']}"); ok += 1; continue
        basarili, ayrinti = yaz(k["inbox"], o.tip, govde)
        print(f"  {'OK  ' if basarili else 'HATA'} {k['proje']:<16}{ayrinti}")
        ok += basarili

    print(f"\nTeslim: {ok}/{len(hedefler)}")
    return 0 if ok == len(hedefler) else 2


if __name__ == "__main__":
    sys.exit(main())
