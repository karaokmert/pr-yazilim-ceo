# Kanal trafigi izleyici - SALT OKUNUR.
# Kutulari dosya sistemi seviyesinde izler; imlec (.cursor) dosyasina DOKUNMAZ.
# Boylece gercek sahipler mesajlarini kaybetmez.
import json, os, time, glob

KOK = os.path.expanduser("~/.pr-kanal")
PROJE = os.environ.get("KANAL_PROJE", "goat")
DIZIN = os.path.join(KOK, PROJE)

gorulen = set()          # mesaj dosya yollari
defter_onceki = None

def kisa(t, n=220):
    return " ".join(str(t).split())[:n]

def mesaj_oku(yol):
    try:
        with open(yol) as f:
            ham = f.read()
    except Exception:
        return None
    try:
        d = json.loads(ham)
        return d
    except Exception:
        return {"_ham": ham}

# baslangicta mevcut mesajlari "gorulmus" say - gecmisi basmayalim
for y in glob.glob(os.path.join(DIZIN, "*", "*box", "*")):
    if os.path.isfile(y):
        gorulen.add(y)

print(f"[KANAL] {PROJE} izleniyor (salt-okunur, imlece dokunulmuyor)", flush=True)

while True:
    try:
        # 1) defter degisimi = yeni agent kanala katildi / ayrildi
        dpath = os.path.join(DIZIN, "live-channel.json")
        if os.path.exists(dpath):
            with open(dpath) as f:
                d = f.read()
            if d != defter_onceki:
                if defter_onceki is not None:
                    try:
                        kayitlar = json.loads(d)
                        roller = ", ".join(k.get("rol", "?") for k in kayitlar) or "(bos)"
                        print(f"[KANAL] DEFTER DEGISTI >> kanalda: {roller}", flush=True)
                    except Exception:
                        print(f"[KANAL] DEFTER DEGISTI (okunamadi)", flush=True)
                defter_onceki = d

        # 2) yeni mesaj dosyalari
        for y in sorted(glob.glob(os.path.join(DIZIN, "*", "*box", "*"))):
            if not os.path.isfile(y) or y in gorulen:
                continue
            gorulen.add(y)
            parcalar = y.split(os.sep)
            kutu = parcalar[-3]
            yon = parcalar[-2]          # inbox / outbox
            d = mesaj_oku(y)
            if d is None:
                continue
            kimden = d.get("from") or d.get("kimden") or "?"
            kime   = d.get("to") or d.get("kime") or kutu
            tur    = d.get("type") or d.get("tur") or "?"
            govde  = d.get("body") or d.get("mesaj") or d.get("_ham") or ""
            ok = "->" if yon == "outbox" else "<-"
            print(f"[KANAL] {kimden} {ok} {kime} [{tur}] {kisa(govde)}", flush=True)
    except Exception as e:
        print(f"[KANAL] HATA: {e}", flush=True)
    time.sleep(5)
