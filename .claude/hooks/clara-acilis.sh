#!/usr/bin/env bash
# Clara açılış hook'u — oturum açılış sinyallerini toplar, açılış direktifini basar.
#
# NEDEN VAR: Oturum bağlamsız başlar ve açılış ritüeli (oturum-duzeni skill'i)
# Clara'nın hafızasına emanetti — hafızaya emanet ritüel atlanıyor. Bu hook
# sinyalleri deterministik toplar; MOD KARARI VERMEZ, kararı Clara verir.
#
# NEDEN pwd SİNYAL DEĞİL: VS Code profili `cd pr-yazilim-ceo && claude --agent clara`
# ile açıyor — pwd her oturumda evi gösterir, oturumun konusunu göstermez.
#
# İÇERİK DEĞİL ADRES: kapanış dokümanının adresi basılır, içeriği basılmaz —
# hook her oturumda yüklenir, içine konan her satır her turda taşınır.
#
# SESSİZ ÇIKIŞ: SessionStart bloklamayan olay; Clara oturumu değilse çıkar.
# Karar ve gerekçe: kararlar/2026-08-09-clara-acilis-hooku.md

set -uo pipefail

[ "${CLAUDE_CODE_AGENT:-}" = "clara" ] || exit 0

CLARA_KOK="/Users/karaok/p/pr-yazilim-ceo"
KANAL_KOK="$HOME/.pr-kanal"

printf '## Clara açılışı — sinyaller\n\n'

# 1 — Son kapanış dokümanı (adres, içerik değil)
son_kapanis=$(ls -t "$CLARA_KOK"/gunluk/*-kapanis.md 2>/dev/null | head -1)
if [ -n "${son_kapanis:-}" ]; then
  printf '**Son kapanış:** `%s`\n' "$son_kapanis"
  printf 'İşe başlamadan bunu oku — ne bitti, ne yarım, ne karar bekliyor orada.\n\n'
else
  printf '**Son kapanış:** bulunamadı (`%s/gunluk/`) — HARITA.md ile başla.\n\n' "$CLARA_KOK"
fi

# 2 — IDE penceresi (Gemini CLI eklentisinin bastığı değişken; eklenti kalkarsa
#     kaybolur — o yüzden varsa bas, yoksa sessiz atla; tek başına mod kanıtı değil)
if [ -n "${GEMINI_CLI_IDE_WORKSPACE_PATH:-}" ]; then
  if [ "$GEMINI_CLI_IDE_WORKSPACE_PATH" = "$CLARA_KOK" ]; then
    printf '**IDE penceresi:** ev (`pr-yazilim-ceo`)\n\n'
  else
    printf '**IDE penceresi:** `%s` — BAŞKA PROJE, YÖNETİM sinyali.\n\n' "$GEMINI_CLI_IDE_WORKSPACE_PATH"
  fi
fi

# 3 — Açık kanal kutuları (yalnız DURUM'u ACIK olanlar — test artıkları gürültü yapmasın)
if [ -d "$KANAL_KOK" ]; then
  toplam=$(find "$KANAL_KOK" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
  acik=""
  for d in "$KANAL_KOK"/*/; do
    [ -d "$d" ] || continue
    durum_eslesme=$(find "$d" -maxdepth 2 -name DURUM.md -exec grep -l "ACIK" {} + 2>/dev/null | head -1)
    if [ -n "$durum_eslesme" ]; then
      kutu=$(find "$d" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
      acik="${acik}- $(basename "$d") (${kutu} kutu)\n"
    fi
  done
  if [ -n "$acik" ]; then
    printf '**Açık kanal kutuları** (~/.pr-kanal — %s dizinden ACIK olanlar):\n' "$toplam"
    printf '%b' "$acik"
    printf 'Monitörler oturum kapanınca ölmüştür — kanal kullanılacaksa yeniden kur.\n\n'
  else
    printf '**Açık kanal yok** (~/.pr-kanal: %s dizin, hiçbiri ACIK değil).\n\n' "$toplam"
  fi
fi

# 4 — Açık agent oturumları (ps; aynı gün + aynı rol tekilleştirilir)
oturumlar=$(ps -eo lstart,command 2>/dev/null | grep 'claude' | grep -- '--agent' | grep -v grep \
  | awk '{ad=""; for(i=1;i<=NF;i++) if($i=="--agent") ad=$(i+1); if(ad!="") print $2" "$3" → "ad}' \
  | sort -u)
if [ -n "$oturumlar" ]; then
  printf '**Açık agent oturumları (ps):**\n'
  printf '%s\n' "$oturumlar" | sed 's/^/- /'
  printf '\n'
fi

printf -- '---\n'
printf "Sen Clara'sın. Önce \`oturum-duzeni\` skill'ini aç, sonra modu belirle:\n"
printf 'pwd hep pr-yazilim-ceo gösterir — SİNYAL DEĞİLDİR. Modu yukarıdaki\n'
printf "sinyaller ve Mert'in ilk cümlesi belirler; belirsizse SOR. Hâlâ belirsizse\n"
printf "IDE'deki açık dosyalara bak (mcp__ide__getDiagnostics).\n"
printf 'Başka repoya yazmadan önce metni göster, onay al (CLA-ASK-BEFORE-WRITING-OUT).\n'
