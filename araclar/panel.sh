#!/usr/bin/env bash
# Canlı agent paneli — tüm projelerdeki aktif Claude Code oturumlarını tek ekranda gösterir.
# Kullanım: bash panel.sh          (5 sn'de bir yeniler)
#           bash panel.sh 10       (10 sn'de bir)
# Çıkış: Ctrl+C
#
# Ne gösterir: hangi agent aktif/durmuş, kaç API çağrısı, ağırlıklı token, son kullandığı araç.
# Ne GÖSTEREMEZ: onay kutusu — o Claude Code'un izin katmanında, oturum kaydına düşmüyor.
#                "3dk sessiz" satırı dolaylı işaret: agent bir şey bekliyor olabilir.

ARALIK="${1:-5}"

while true; do
  clear
  python3 - "$ARALIK" <<'PY'
import json, glob, os, time, sys
from datetime import datetime

ARALIK = sys.argv[1]
now = time.time()
KOK = os.path.expanduser('~/.claude/projects')
AKTIF_ESIK = 3600          # son 60 dk dokunulan oturumlar
SESSIZ_UYARI = 3           # 3 dk+ sessizse işaretle

satirlar = []
for pdir in glob.glob(KOK + '/*'):
    proje = os.path.basename(pdir).replace('-Users-karaok-p-', '').replace('ozel-yazilim-', '')
    for f in glob.glob(pdir + '/*.jsonl'):
        yas = now - os.path.getmtime(f)
        if yas > AKTIF_ESIK:
            continue
        seen, title, sonarac, sonrol = {}, None, None, None
        try:
            for line in open(f, encoding='utf-8'):
                try: d = json.loads(line)
                except: continue
                if d.get('type') == 'custom-title':
                    title = d.get('customTitle')
                m = d.get('message') or {}
                u, mid = m.get('usage'), m.get('id')
                if u and mid and mid not in seen:
                    seen[mid] = (u.get('cache_creation_input_tokens', 0),
                                 u.get('cache_read_input_tokens', 0),
                                 u.get('input_tokens', 0))
                c = m.get('content')
                if isinstance(c, list):
                    for b in c:
                        if isinstance(b, dict) and b.get('type') == 'tool_use':
                            sonarac = b.get('name')
                if d.get('type') == 'user':
                    sonrol = 'kullanici'
                elif d.get('type') == 'assistant':
                    sonrol = 'agent'
        except Exception:
            continue
        if not seen:
            continue
        cc = sum(v[0] for v in seen.values())
        cr = sum(v[1] for v in seen.values())
        un = sum(v[2] for v in seen.values())
        esd = un + cc * 1.25 + cr * 0.1
        ad = title or f'({os.path.basename(f)[:8]})'
        satirlar.append({
            'ad': ad, 'proje': proje, 'n': len(seen), 'esd': esd,
            'basina': esd / max(len(seen), 1), 'dk': yas / 60,
            'arac': sonarac or '-', 'rol': sonrol or '-',
        })

satirlar.sort(key=lambda r: r['dk'])

print(f"\033[1m  CANLI AGENT PANELİ\033[0m   {datetime.now().strftime('%H:%M:%S')}"
      f"   ·  {len(satirlar)} aktif oturum  ·  {ARALIK}sn yenileme  ·  Ctrl+C çıkış")
print("─" * 116)
print(f"  {'DURUM':<11}{'AGENT / OTURUM':<40}{'ÇAĞRI':>7}{'AĞIRLIKLI':>13}{'BAŞINA':>9}   {'SON ARAÇ':<22}{'SESSİZ':>7}")
print("─" * 116)

for r in satirlar:
    if r['dk'] < 1:
        durum, renk = '● çalışıyor', '\033[32m'
    elif r['dk'] < SESSIZ_UYARI:
        durum, renk = '◐ yavaş',     '\033[33m'
    else:
        durum, renk = '○ BEKLİYOR',  '\033[31m'
    pahali = '\033[31m' if r['basina'] > 40000 else ''
    reset = '\033[0m'
    ad = (r['ad'][:38] + '…') if len(r['ad']) > 39 else r['ad']
    print(f"  {renk}{durum:<11}{reset}{ad:<40}{r['n']:>7}"
          f"{pahali}{r['esd']:>13,.0f}{reset}{r['basina']:>9,.0f}   "
          f"{r['arac'][:20]:<22}{r['dk']:>6.0f}d")

print("─" * 116)
if satirlar:
    tot = sum(r['esd'] for r in satirlar)
    bekleyen = [r for r in satirlar if r['dk'] >= SESSIZ_UYARI]
    print(f"  toplam ağırlıklı: {tot:>13,.0f}   ·   çalışan: "
          f"{sum(1 for r in satirlar if r['dk'] < 1)}   ·   bekleyen: {len(bekleyen)}")
    if bekleyen:
        print(f"  \033[31m→ bekleyenler:\033[0m " +
              ", ".join(f"{r['ad'][-24:]} ({r['dk']:.0f}d)" for r in bekleyen[:4]))
else:
    print("  (son 60 dakikada aktif oturum yok)")
print()
print("  \033[2mnot: 'BEKLİYOR' = 3dk+ yazma yok — onay kutusu ya da senin cevabın bekleniyor olabilir.")
print("       onay kutusunun kendisi oturum kaydına düşmüyor, panel onu göremez.\033[0m")
PY
  sleep "$ARALIK"
done
