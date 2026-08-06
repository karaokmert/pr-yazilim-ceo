#!/usr/bin/env bash
# Clara açılış hook'u — skill'lerini dışarıdan yükletir.
#
# NEDEN VAR: `skills:` frontmatter alanı skill gövdesini context'e enjekte etmiyor
# (2026-08-03'te ölçüldü, `anthropics/claude-code#25834`). Personel kanonunu yüklü
# sanır, elinde yalnız description vardır. Fabrikanın aynı sorunu için yazılmış
# hook'un Clara karşılığı.
#
# NEDEN DIŞARIDAN: Clara kendi frontmatter'ını okuyamaz. "Tanımındaki listeyi yükle"
# demek yetmez; personel tahmin eder ve yanlış yükler, üstelik yüklediğini sanır.
#
# NEREDE ÇALIŞIR: Clara artık symlink'li — herhangi bir repodan çağrılabiliyor.
# Bu hook onun kanonunu nerede olursa olsun eline verir.
#
# SESSİZ ÇIKIŞ: SessionStart bloklamayan bir olay. Clara oturumu değilse çıkar.

set -uo pipefail

AGENT_ADI="${CLAUDE_CODE_AGENT:-}"
[ "$AGENT_ADI" = "clara" ] || exit 0

# Clara'nın kanonu bu repoda yaşıyor — mutlak yol, çünkü Clara başka bir repodan
# çağrılmış olabilir ve göreli yol o zaman kırılır (ölçüldü: göreli yol iki mesajı
# sessizce kaybettirdi).
CLARA_KOK="/Users/karaok/p/pr-yazilim-ceo"
SKILL_DIZIN="$CLARA_KOK/.claude/skills"

[ -d "$SKILL_DIZIN" ] || exit 0

printf '## Oturum açılışı — kanonunu yükle\n\n'
printf 'Sen Clara'"'"'sın. Kuralların `%s/.claude/agents/clara.md` içinde,\n' "$CLARA_KOK"
printf 'skill'"'"'lerin ayrı dosyalarda — ve **preload bu ortamda çalışmıyor.**\n'
printf 'Tanımındaki `skills:` listesi context'"'"'ine girmedi; kendi frontmatter'"'"'ını da\n'
printf 'okuyamazsın. O yüzden liste aşağıda dışarıdan veriliyor.\n\n'

printf '**Şu an hangi repoda olduğuna bak.** Buradaysan (`pr-yazilim-ceo`) ev sahibisin;\n'
printf 'başka bir repodaysan **misafirsin** — o reponun kendi kapıları var ve\n'
printf '`CLA-ASK-BEFORE-WRITING-OUT` yürürlükte: yazmadan önce metni göster, onay al.\n\n'

printf '**Bu üçünü şimdi oku** (mutlak yolla, `Read` aracıyla):\n\n'
printf -- '- `%s/HARITA.md` — bu odada ne var; bir konu açılınca ilk bakılacak yer\n' "$CLARA_KOK"

for d in "$SKILL_DIZIN"/*/; do
  ad=$(basename "$d")
  [ -f "$d/SKILL.md" ] || continue
  case "$ad" in
    i-have-adhd) continue ;;   # Clara'nın kanonu değil
  esac
  printf -- '- `%sSKILL.md` — %s\n' "$d" "$ad"
done

printf '\n'
printf 'Sonra kendini tek satırda tanıt ve işe başla. Kullanıcı soru sorana kadar\n'
printf 'bekleme — yüklemeyi şimdi yap.\n'
