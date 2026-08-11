#!/usr/bin/env python3
"""Proje Clara'larini SUREKLI izler — Monitor araci icin.

takip.py tek seferlik ozet cikarir; bu betik canli izler: yeni Mert mesaji
geldiginde tek satir olay basar. Amac Clara'nin davranisini degil,
MERT'IN YONETIMINI yakalamak (referans ornek).

Cikti formati (grep'lenebilir):
  MERT | <oturum8> | <saat> | <mesajin ilk 200 karakteri>
  CLARA| <oturum8> | <saat> | <cevabin ilk 160 karakteri>
  YENI | <oturum8> | yeni clara oturumu acildi
  INFO | ...

Kullanim: python3 izle.py [--poll 20] [--with-clara]
"""
import json, glob, os, sys, time

POLL = 20
if '--poll' in sys.argv:
    try:
        POLL = int(sys.argv[sys.argv.index('--poll') + 1])
    except Exception:
        pass
WITH_CLARA = '--with-clara' in sys.argv

# oturum dosyasi -> islenmis satir sayisi
cursor = {}
known = set()

SKIP_PREFIX = ('<', '[Request interrupted')
SKIP_CONTAINS = ('tool_result', 'Base directory for this skill',
                 'The previous response failed', 'Continue from where',
                 'Caveat: The messages below', 'system-reminder')
CANON_MARKS = ['Adın Clara', 'CLA-ASK-BEFORE-WRITING-OUT', 'CLA-FIX-THE-CAUSE',
               'oturum-duzeni', 'pr-yazilim-ceo/.claude/skills', 'CLA-ARGUE-BACK']

# YONETIM modu — izlenecek olan yalniz proje yoneten Clara.
# Her Clara oturumu proje yonetmiyor (olculdu 2026-08-10: biri QR kod uretiyordu,
# biri tmux kuruyordu — ikisi de Clara, ikisi de konu disi).
#
# KELIME SAYMAK ISE YARAMIYOR — iki deneme de coktu:
#   · varlik: acilis hook'u her oturuma ".pr-kanal" basiyor, skill listesi
#     "proje-yonetimi"/"kanal-kurulumu" adlarini tasiyor → QR isi bile gecti
#   · yogunluk: handoff/1000satir → CLARA-B 35.2 vs QR isi 30.3, ayirmiyor
#
# DOGRU AYIRICI: metin degil DAVRANIS — yoneten Clara kanal kutusuna gercekten
# YAZAR. Transcript'te `send.py .../outbox` calistirmasi aranir; bu bir arac
# cagrisi, anlatim degil, ve taklit edilmiyor.
YONETIM_KANIT = '/outbox'


def is_clara(path):
    """Clara oturumu mu — iki sartin IKISI birden.

    (1) `slug` alani var  → ana oturum (alt-agent / denetim oturumunda YOK)
    (2) >=2 kanon izi     → Clara kanonu bu oturumda dolasiyor

    NEDEN iki sart: ikisi de tek basina yaniltiyor, olculdu 2026-08-10.
    · Yalniz kanon izi: Clara'nin YAZDIGI betigi okuyan guvenlik denetimi
      (`9ae9f686`) Clara sanildi — dosyada `CLA-FIX-THE-CAUSE` geciyordu.
    · Yalniz sistem prompt: `"Adın Clara"` transcript'e HIC yazilmiyor —
      bes oturumun besi de kacti (ilk teshis "ilk 120KB'da degil" idi,
      yanlisti; hicbir yerde yok).
    · Yalniz slug: her ana oturumda var, Clara'ya ozgu degil.
    """
    try:
        has_slug = False
        marks = 0
        yonetim = 0
        for line in open(path, errors='ignore'):
            if not has_slug and '"slug"' in line:
                has_slug = True
            if marks < 2:
                marks += sum(1 for m in CANON_MARKS if m in line)
            if YONETIM_KANIT in line and 'send.py' in line:
                yonetim += 1
            if has_slug and marks >= 2 and yonetim >= 1:
                return True
    except Exception:
        return False
    return False


def _son_mesaj_yasi(path):
    """Son GERCEK MESAJIN yasi (dakika). Bulunamazsa 9999 (= eski say).

    Iki tuzak, ikisi de olculdu 2026-08-10:
    · `mtime` guvenilmez — dosyaya mesaj YAZILMADAN da dokunuluyor.
    · Son satirin timestamp'i de yetmiyor — kapanmis oturuma arka planda
      `attachment` / `last-prompt` gibi META satirlar dusuyor. Iki oturum
      "3 dk once aktif" gorundu, son gercek mesajlari 8 saat oncesiydi.

    Dogru olcut: yalnizca `message.role` tasiyan satirlar sayilir.
    """
    try:
        lines = open(path, errors='ignore').readlines()
    except Exception:
        return 9999
    import calendar
    for line in reversed(lines[-400:]):
        try:
            d = json.loads(line)
        except Exception:
            continue
        m = d.get('message') or {}
        if m.get('role') not in ('user', 'assistant'):
            continue                      # attachment / last-prompt / meta → atla
        # Bos yanit da mesaj sayilmaz: kapanmis oturuma "No response requested."
        # dusuyor ve oturumu canli gosteriyor (olculdu 2026-08-10).
        c = m.get('content')
        gövde = c if isinstance(c, str) else ' '.join(
            b.get('text', '') for b in c if isinstance(b, dict) and b.get('type') == 'text'
        ) if isinstance(c, list) else ''
        if gövde.strip() in ('No response requested.', ''):
            continue
        ts = d.get('timestamp')
        if not ts:
            continue
        try:
            t = time.strptime(ts[:19], '%Y-%m-%dT%H:%M:%S')
            return (time.time() - calendar.timegm(t)) / 60
        except Exception:
            continue
    return 9999


def new_rows(path):
    """Imlecten sonraki satirlari dondurur, imleci ilerletir."""
    try:
        lines = open(path, errors='ignore').readlines()
    except Exception:
        return []
    start = cursor.get(path, 0)
    cursor[path] = len(lines)
    return lines[start:]


def extract(line):
    try:
        d = json.loads(line)
    except Exception:
        return None
    m = d.get('message') or {}
    role = m.get('role')
    ts = (d.get('timestamp') or '')[11:19]
    c = m.get('content')
    texts = []
    if isinstance(c, str):
        texts.append(c)
    elif isinstance(c, list):
        for b in c:
            if isinstance(b, dict) and b.get('type') == 'text':
                texts.append(b.get('text', ''))
    if not texts:
        return None
    return (ts, role, ' '.join(texts).strip())


def useful(role, txt):
    if not txt or len(txt) < 6:
        return False
    if txt.startswith(SKIP_PREFIX):
        return False
    if any(x in txt[:80] for x in SKIP_CONTAINS):
        return False
    return True


print("INFO | clara izleyici basladi | poll=%ds" % POLL, flush=True)

# ilk turda mevcut dosyalarin sonuna atla — gecmisi tekrar bagirma
for f in glob.glob('/Users/karaok/.claude/projects/*/*.jsonl'):
    try:
        cursor[f] = sum(1 for _ in open(f, errors='ignore'))
    except Exception:
        cursor[f] = 0

while True:
    try:
        for f in sorted(glob.glob('/Users/karaok/.claude/projects/*/*.jsonl'),
                        key=os.path.getmtime, reverse=True)[:40]:
            # 25 dk sessiz kalan oturum kapanmis sayilir — bagirma.
            # (Kapanmis oturumun artiklarini olay olarak basmak gurultu:
            #  olculdu 2026-08-10, tmux oturumu 14:32'de kapanmisti.)
            age = (time.time() - os.path.getmtime(f)) / 60
            if age > 25:
                continue
            if f not in cursor:
                cursor[f] = 0
            sid = os.path.basename(f)[:8]
            rows = new_rows(f)
            if not rows:
                continue
            if f not in known:
                if not is_clara(f):
                    continue
                # mtime YETMIYOR: dosya yazilmadan da dokunulabiliyor
                # (olculdu 2026-08-10: sekiz saat once kapanmis iki oturum
                #  "yeni" diye bagirdi, son gercek mesajlari 10:12 ve 10:31'di).
                # Gercek olcut: SON SATIRIN kendi zaman damgasi.
                if _son_mesaj_yasi(f) > 40:
                    known.add(f)   # sessizce isaretle, bagirma
                    continue
                known.add(f)
                print(f"YENI | {sid} | clara oturumu izlemeye alindi "
                      f"| {f.split('/')[-2]}", flush=True)
            for line in rows:
                r = extract(line)
                if not r:
                    continue
                ts, role, txt = r
                if not useful(role, txt):
                    continue
                if role == 'user':
                    print(f"MERT | {sid} | {ts} | "
                          f"{txt.replace(chr(10), ' ')[:200]}", flush=True)
                elif role == 'assistant' and WITH_CLARA:
                    print(f"CLARA| {sid} | {ts} | "
                          f"{txt.replace(chr(10), ' ')[:160]}", flush=True)
        time.sleep(POLL)
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"ERROR| {e}", flush=True)
        time.sleep(POLL)
