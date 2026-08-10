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


def is_clara(path):
    """Kanon izlerinden Clara oturumu mu anlar.

    NOT: sistem prompt ilk 120KB'da olmayabilir (olculdu 2026-08-10) —
    o yuzden dosyanin TAMAMI taranir, >=2 isaret aranir.
    """
    try:
        blob = open(path, errors='ignore').read()
    except Exception:
        return False
    return sum(m in blob for m in CANON_MARKS) >= 2


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
            age = (time.time() - os.path.getmtime(f)) / 60
            if age > 180:
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
