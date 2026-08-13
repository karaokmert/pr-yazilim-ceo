#!/usr/bin/env python3
"""Mert'e YENI atanan ClickUp task'lerini yakalar.

Kanal dinleyicisinden (clickup-dinle.py) FARKI: o mesaji dinler, bu ATAMAYI.

Nasil calisir: acik+bana-atanmis task listesi cekilir, ilk turda hepsi
"gorulmus" sayilir (gecmis bagirilmaz), sonraki turlarda listeye YENI giren
task olay olarak basilir.

TOKEN koda yazilmaz — ~/.clickup-token ya da CLICKUP_TOKEN.

Kullanim:
  python3 clickup-task-dinle.py [--poll 120] [--user 36576051]

Cikti:
  YENI-TASK | <PRY-id> | <statu> | <baslik>
  STATU     | <PRY-id> | <eski> → <yeni> | <baslik>
"""
import json, os, sys, time, urllib.request, urllib.parse

POLL = 120
USER = '36576051'
if '--poll' in sys.argv:
    try:
        POLL = int(sys.argv[sys.argv.index('--poll') + 1])
    except Exception:
        pass
if '--user' in sys.argv:
    try:
        USER = sys.argv[sys.argv.index('--user') + 1]
    except Exception:
        pass

WS = os.environ.get('CLICKUP_WORKSPACE', '24450758')


def token():
    t = os.environ.get('CLICKUP_TOKEN')
    if t:
        return t.strip()
    p = os.path.expanduser('~/.clickup-token')
    if os.path.exists(p):
        return open(p).read().strip()
    raise RuntimeError('Token yok — ~/.clickup-token ya da CLICKUP_TOKEN')


def tasks(tok):
    q = urllib.parse.urlencode({
        'order_by': 'updated',
        'subtasks': 'true',
        'include_closed': 'false',
    }) + f'&assignees[]={USER}'
    url = f'https://api.clickup.com/api/v2/team/{WS}/task?{q}'
    req = urllib.request.Request(url, headers={
        'Authorization': tok, 'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return (json.loads(r.read().decode()) or {}).get('tasks') or []


tok = token()
bilinen = {}          # task_id -> statu
ilk = True

print(f"INFO | task dinleyici basladi | user={USER} poll={POLL}s", flush=True)

while True:
    try:
        for t in tasks(tok):
            tid = t.get('custom_id') or t.get('id')
            statu = (t.get('status') or {}).get('status', '?')
            ad = (t.get('name') or '')[:60]
            if tid not in bilinen:
                if not ilk:
                    print(f"YENI-TASK | {tid} | {statu} | {ad}", flush=True)
                bilinen[tid] = statu
            elif bilinen[tid] != statu:
                # Statu degisimi de haber degeri tasir (ornek: live-dev → done)
                if not ilk:
                    print(f"STATU | {tid} | {bilinen[tid]} → {statu} | {ad}",
                          flush=True)
                bilinen[tid] = statu
        ilk = False
        time.sleep(POLL)
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"ERROR| task-dinle: {e}", flush=True)
        time.sleep(POLL)
