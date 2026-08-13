#!/usr/bin/env python3
"""Proje Clara'larini izler.

Ne yapar: calisan `--agent clara` oturumlarini bulur, her birinin
transcript'inden Mert'in mesajlarini cikarir. Amac Clara'nin davranisini
degil, MERT'IN YONETIMINI kaydetmek — referans ornek uretmek icin.

Kullanim:
  python3 takip.py           → her oturumun son 8 Mert mesaji
  python3 takip.py --full    → tum Mert mesajlari
  python3 takip.py --tools   → Clara'nin arac kullanim dagilimi da

Kimlik tespiti `ps` uzerinden yapilir — transcript icinde "Adın Clara"
aramak GUVENILMEZ (sistem prompt ilk 120KB'da olmayabilir, olculdu 2026-08-10).
"""
import json, glob, os, sys, time, subprocess, collections

FULL  = '--full'  in sys.argv
TOOLS = '--tools' in sys.argv


def clara_pids():
    """Calisan clara oturumlarinin baslangic zamanlarini dondurur."""
    try:
        out = subprocess.run(['ps', 'axo', 'lstart,command'],
                             capture_output=True, text=True, timeout=10).stdout
    except Exception:
        return []
    return [l for l in out.splitlines()
            if '--agent clara' in l and 'zsh -c' not in l]


def recent_transcripts(max_age_min=600):
    fs = sorted(glob.glob('/Users/karaok/.claude/projects/*/*.jsonl'),
                key=os.path.getmtime, reverse=True)[:40]
    return [(f, (time.time() - os.path.getmtime(f)) / 60)
            for f in fs if (time.time() - os.path.getmtime(f)) / 60 < max_age_min]


def parse(f):
    """(ts, role, kind, text) satirlari."""
    r = []
    for line in open(f, errors='ignore'):
        try:
            d = json.loads(line)
        except Exception:
            continue
        m = d.get('message') or {}
        role = m.get('role')
        ts = (d.get('timestamp') or '')[11:19]
        c = m.get('content')
        if isinstance(c, str):
            r.append((ts, role, 'T', c))
        elif isinstance(c, list):
            for b in c:
                if not isinstance(b, dict):
                    continue
                if b.get('type') == 'text':
                    r.append((ts, role, 'T', b.get('text', '')))
                elif b.get('type') == 'tool_use':
                    r.append((ts, role, 'TOOL:' + b.get('name', ''),
                              str(b.get('input'))[:150]))
    return r


def is_clara(rows):
    """Clara oturumu mu — kanon izlerinden anlar."""
    blob = ' '.join(t for _, _, k, t in rows[:400] if k == 'T')[:200000]
    marks = ['Adın Clara', 'CLA-ASK-BEFORE-WRITING-OUT', 'CLA-FIX-THE-CAUSE',
             'oturum-duzeni', 'pr-yazilim-ceo/.claude/skills']
    return sum(m in blob for m in marks) >= 2


def mert_msgs(rows):
    skip_prefix = ('<', '[Request interrupted')
    skip_contains = ('tool_result', 'Base directory for this skill',
                     'The previous response failed', 'Continue from where',
                     'Caveat: The messages below')
    out = []
    for ts, role, k, t in rows:
        if role != 'user' or k != 'T':
            continue
        s = t.strip()
        if not s or len(s) < 6:
            continue
        if s.startswith(skip_prefix):
            continue
        if any(x in s[:60] for x in skip_contains):
            continue
        out.append((ts, s))
    return out


print(f"# Proje Clara takibi — {time.strftime('%Y-%m-%d %H:%M')}")
running = clara_pids()
print(f"# Calisan clara oturumu (ps): {len(running)}")

found = 0
for f, age in recent_transcripts():
    rows = parse(f)
    if not rows or not is_clara(rows):
        continue
    msgs = mert_msgs(rows)
    if not msgs:
        continue
    found += 1
    print(f"\n{'=' * 72}")
    print(f"▸ {os.path.basename(f)[:8]} | {f.split('/')[-2]}")
    print(f"  son aktivite: {age:.0f} dk once | Mert mesaji: {len(msgs)}")
    print(f"  ACILIS: {msgs[0][1][:120]}")
    print(f"{'=' * 72}")
    show = msgs if FULL else msgs[-8:]
    for ts, t in show:
        print(f"  [{ts}] {t.replace(chr(10), ' | ')[:320]}")
    if TOOLS:
        c = collections.Counter(k[5:] for _, _, k, _ in rows if k.startswith('TOOL:'))
        print(f"  --- arac: {dict(c.most_common(8))}")

if not found:
    print("\n(clara oturumu bulunamadi — ps'de var ama transcript eslesmedi olabilir)")
