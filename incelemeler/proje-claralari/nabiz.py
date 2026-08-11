#!/usr/bin/env python3
"""Kanal nabzi — hangi uc akiyor, hangisi sessiz.

"Duran is var mi?" sorusu 2026-08-10'da DORT kez soruldu ve her seferinde
elle olcum gerekti. Bu betik onu tek satira indiriyor.

Kullanim:
  python3 nabiz.py            → tablo
  python3 nabiz.py --watch    → Monitor icin; yalniz DURUM DEGISINCE satir basar

Isaretler:  ● <15dk akiyor   ◐ 15-45dk yavas   ○ >45dk sessiz
Sessizlik TEK BASINA ariza degil — uc tur var:
  · sira bekliyor (anlamli)  · is bitti bildirmedi (eksik)  · takildi (ariza)
Nabiz hangisine BAKILACAGINI gosterir, teshis koymaz.
"""
import glob, os, time, sys

WATCH = '--watch' in sys.argv
ESIK_AKIYOR = 15
ESIK_YAVAS = 45
ESIK_OLU = 360        # bu yastan buyuk kutular kapanmis sayilir, listelenmez


def nabiz():
    out = []
    for kutu in sorted(glob.glob(os.path.expanduser('~/.pr-kanal/*/*/outbox'))):
        fs = glob.glob(kutu + '/*.json')
        ad = kutu.split('/')[-2]
        proje = kutu.split('/')[-3]
        if not fs or ad.lower().startswith('clara'):
            continue          # merkezin kendi kutusu sayilmaz
        yas = (time.time() - max(os.path.getmtime(x) for x in fs)) / 60
        out.append((yas, proje, ad, len(fs)))
    out.sort()
    return out


def isaret(yas):
    return '●' if yas < ESIK_AKIYOR else ('◐' if yas < ESIK_YAVAS else '○')


def toplu_sessizlik(canli):
    """Bir projedeki uclarin HEPSI sessizse ve ayni pencerede sustularsa,
    sebep iste degil ALTYAPIDA (5 saatlik oturum limiti).

    Olculdu 2026-08-11: goat'ta uc uc 339/342/352 dk — 13 dakika icinde
    hepsi sustu. Izleyen Clara "SQL turunu bekliyor" dedi, YANLISTI.
    Ayirt edici isaret EŞZAMANLILIK: tek tek susma is kaynakli,
    toplu susma sistem kaynakli. `ps` bunu ayirt ETMIYOR — surec ayakta
    gorunur ama oturum tukenmistir.
    """
    projeler = {}
    for yas, proje, ad, n in canli:
        projeler.setdefault(proje, []).append(yas)
    uyari = []
    for proje, yaslar in projeler.items():
        if len(yaslar) < 2:
            continue
        if all(y >= ESIK_YAVAS for y in yaslar) and (max(yaslar) - min(yaslar)) < 30:
            uyari.append((proje, len(yaslar), min(yaslar)))
    return uyari


def tablo():
    rows = nabiz()
    canli = [r for r in rows if r[0] <= ESIK_OLU]
    print(f"KANAL NABZI — {time.strftime('%H:%M')}  "
          f"({sum(1 for r in canli if r[0] < ESIK_AKIYOR)} akiyor / {len(canli)} acik)")
    for yas, proje, ad, n in canli:
        print(f"  {isaret(yas)} {proje:14s} {ad:34s} {yas:5.0f} dk  ({n} msj)")
    olu = len(rows) - len(canli)
    if olu:
        print(f"  ({olu} kutu >6 saat sessiz — kapanmis sayildi)")
    for proje, adet, en_yeni in toplu_sessizlik(canli):
        print(f"  ⚠ TOPLU SESSIZLIK: {proje} — {adet} ucun hepsi birden sustu "
              f"({en_yeni:.0f}+ dk). Muhtemelen OTURUM LIMITI, is degil.")


if not WATCH:
    tablo()
    raise SystemExit

# --watch: yalniz DURUM DEGISINCE bagir (her turda degil — gurultu olur)
onceki = {}
while True:
    try:
        for yas, proje, ad, n in nabiz():
            if yas > ESIK_OLU:
                continue
            durum = isaret(yas)
            anahtar = f'{proje}/{ad}'
            eski = onceki.get(anahtar)
            if eski != durum:
                # YALNIZ KOTULESME bagirilir. Iyilesme (◐→●) haber degil:
                # uc zaten calisiyor demektir. Ve "◐" tek basina ariza degil —
                # olculdu 2026-08-10: PA 16 dk "sessiz" gorundu, aslinda o anda
                # cevap yaziyordu (olcum ani ile kontrol ani arasi kayma).
                # O yuzden esik ◐ degil ○: gercek sessizlik 45 dk.
                kotulesme = eski is not None and eski == '●' and durum == '○' \
                    or (eski == '◐' and durum == '○')
                if kotulesme:
                    print(f"NABIZ | {anahtar} | {eski} → {durum} "
                          f"| {yas:.0f} dk sessiz", flush=True)
                onceki[anahtar] = durum
        time.sleep(60)
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"ERROR| nabiz: {e}", flush=True)
        time.sleep(60)
