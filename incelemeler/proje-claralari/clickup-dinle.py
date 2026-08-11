#!/usr/bin/env python3
"""ClickUp kanalini dinler — Mert yazinca haber verir.

NEDEN AYRI BETIK: Clara MCP araclarini bir monitor icinden cagiramaz
(araclar konusma katmaninda yasar, betikte degil). Bu yuzden ClickUp
API'sine dogrudan gidilir.

TOKEN: koda YAZILMAZ. mcp-remote'un OAuth onbellegi calisma aninda okunur
(~/.mcp-auth/.../*_tokens.json). Boylece kimlik betikte saklanmaz,
Clara'nin baglamina da girmez.

Kullanim:
  python3 clickup-dinle.py <channel_id> [--poll 30]

Cikti (grep'lenebilir tek satir):
  CLICKUP | <kim> | <saat> | <mesajin ilk 300 karakteri>
"""
import json, glob, os, sys, time, urllib.request

if len(sys.argv) < 2:
    print("kullanim: clickup-dinle.py <channel_id> [--poll 30]")
    raise SystemExit(1)

CHANNEL = sys.argv[1]
POLL = 30
if '--poll' in sys.argv:
    try:
        POLL = int(sys.argv[sys.argv.index('--poll') + 1])
    except Exception:
        pass

API = 'https://api.clickup.com/api/v3'

# Clara kendi mesajlarini bu imzayla baslatir; dinleyici onlari eler.
# Gerekli cunku token Mert'in hesabina ait — Clara'nin yazdigi mesaj da
# gonderen olarak Mert gorunur, `user_id` ayirt etmiyor.
CLARA_IMZA = '🤖'


def token():
    """ClickUp kisisel API anahtarini dondurur (pk_...).

    KAYNAK SIRASI:
      1. CLICKUP_TOKEN ortam degiskeni
      2. ~/.clickup-token dosyasi (tek satir)

    Token KODA YAZILMAZ. Sebep: kod git'e giriyor, anahtar girmemeli.

    NOT (olculdu 2026-08-11): mcp-remote'un OAuth onbellegindeki token
    ISE YARAMIYOR — o `mcp.clickup.com` icin, `api.clickup.com` icin degil.
    Ikisi ayri kapi; API 401 doner.
    """
    t = os.environ.get('CLICKUP_TOKEN')
    if t:
        return t.strip()
    p = os.path.expanduser('~/.clickup-token')
    if os.path.exists(p):
        return open(p).read().strip()
    raise RuntimeError(
        'Token yok. CLICKUP_TOKEN ver ya da ~/.clickup-token dosyasina yaz.')


def cek(tok, limit=10):
    url = f'{API}/workspaces/{WS}/chat/channels/{CHANNEL}/messages?limit={limit}'
    req = urllib.request.Request(url, headers={
        'Authorization': tok if tok.startswith('pk_') else f'Bearer {tok}',
        'Accept': 'application/json',
    })
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())


WS = os.environ.get('CLICKUP_WORKSPACE', '24450758')

tok = token()
gorulen = set()
ilk = True

print(f"INFO | clickup dinleyici basladi | kanal={CHANNEL} poll={POLL}s", flush=True)

while True:
    try:
        d = cek(tok)
        msgs = d.get('data') or d.get('messages') or []
        # API en yeniyi basa koyar — eskiden yeniye isle
        for m in reversed(msgs):
            mid = str(m.get('id'))
            if mid in gorulen:
                continue
            gorulen.add(mid)
            if ilk:
                continue          # ilk turda gecmisi bagirma
            kim = (m.get('user') or {}).get('username') or m.get('user_id') or '?'
            # Clara'nin KENDI yazdigi mesaj olay degildir.
            # Token Mert'in hesabina ait, yani Clara'nin gonderdigi mesaj da
            # `user_id = Mert` gorunur — ayirt edici isaret ICERIK imzasi.
            # (Olculdu 2026-08-11: ilk turda kendi mesajim bana geri bagirildi.)
            icerik_ham = str(m.get('content') or '')
            if icerik_ham.startswith(CLARA_IMZA):
                continue
            ts = m.get('date')
            saat = time.strftime('%H:%M', time.localtime(int(ts) / 1000)) if ts else '--:--'
            icerik = str(m.get('content') or '').replace('\n', ' ')[:300]
            print(f"CLICKUP | {kim} | {saat} | {icerik}", flush=True)
        ilk = False
        time.sleep(POLL)
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"ERROR| clickup-dinle: {e}", flush=True)
        time.sleep(POLL)
