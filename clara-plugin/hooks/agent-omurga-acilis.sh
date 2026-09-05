#!/usr/bin/env bash
# Agent omurga açılış direktifi — açılan agent'ın kendi frontmatter'ındaki
# `skills:` listesini okur ve onları açmasını söyler.
#
# NEDEN VAR: skill'ler preload edilmiyor. Bir agent'ın frontmatter'ında
# `skills:` yazması onları yüklemiyor; description'a "her oturumda açılır"
# yazmak da açtırmıyor — o bir niyet beyanı, tetikleyici değil.
# Ölçüldü 2026-08-23: iki Clara oturumu açıldı, ikisi de sıfır skill açtı.
#
# NEDEN İSİM GÖMÜLÜ DEĞİL: skill adı hook'a yazılırsa bir ad değiştiğinde ya da
# yeni bir omurga eklendiğinde hook sessizce eskir. Kaynak agent'ın kendi
# gövdesi — orası değişince hook kendiliğinden takip eder.

AGENT="$CLAUDE_CODE_AGENT"
[ -n "$AGENT" ] || exit 0

# agent gövdesini bul (global symlink dizini)
BODY="${CLAUDE_PLUGIN_ROOT}/agents/${AGENT}.md"
[ -f "$BODY" ] || BODY="$HOME/.claude/agents/${AGENT}.md"
[ -f "$BODY" ] || exit 0

# frontmatter'daki skills: listesini oku
LISTE=$(awk '
  /^---$/ { fm++; next }
  fm==1 && /^skills:/ { insk=1; next }
  fm==1 && insk && /^[a-z]/ { insk=0 }
  fm==1 && insk && /^[[:space:]]*-[[:space:]]*/ {
    gsub(/^[[:space:]]*-[[:space:]]*/, ""); print
  }
  fm>=2 { exit }
' "$BODY")

[ -z "$LISTE" ] && exit 0

SATIRLAR=""
for s in $LISTE; do
  SATIRLAR="${SATIRLAR}- \`${s}\`\\n"
done

# ⚠️ BACKTICK KAÇIRILIR: aşağıdaki metin `cat << EOF` içinde, yani shell
# genişletmesine açık. Kaçırılmamış bir backtick komut olarak çalıştırılır ve
# metinden SESSİZCE SİLİNİR — hata vermez, JSON geçerli kalır, yalnız o kelime
# yok olur. Ölçüldü 2026-08-30: `project-assistant` yazıldı, çıktıda boşluk çıktı.
# Metne dokunulduktan sonra hep çalıştırılıp çıktısı okunur.

cat << EOF
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "## ⚠️ AÇILIŞ DİREKTİFİ — ilk hareket bu\n\nHenüz hiçbir şey yapma. Önce **omurga skill'lerini aç** — bunlar gövdende \`skills:\` olarak tanımlı ve her oturumda yüklenmesi gereken kanonun:\n\n${SATIRLAR}\n**Neden bu direktif var:** skill'ler preload edilmiyor. Gövdende \`skills:\` yazması onları yüklemiyor; description'a *\"her oturumda açılır\"* yazmak da açtırmıyor — o bir niyet beyanı, bir tetikleyici değil. Ölçüldü (2026-08-23): iki oturum açıldı, ikisi de sıfır skill açtı ve kanonun yarısı elde yoktu.\n\nBu liste **senin gövdenden okunuyor** — bir omurga eklenir ya da çıkarılırsa burada kendiliğinden görünür.\n\nAçtıktan sonra kanonunun söylediği açılış sırasını izle.\n\n**Sonra işe başla.** Skill'leri açmadan iş yapmak, kanonunun yarısını görmeden karar vermek demektir.\n\n---\n\n## SendMessage düzeni — bir proje ekibinde çalışıyorsan\n\nBir proje ekibinin parçasıysan — Özel Yazılım (OY) ya da Websitesi (WS) takımlarından birinde bir saha rolüysen — iletişimin **SendMessage üzerinden** yürür ve merkez **proje asistanıdır** (OY'da \`project-assistant\`, WS'de \`web-project-assistant\`; aşağıda kısaca **PA**).\n\n**Ekranda onay bekleme.** İşini bitirdiğinde ya da bir karara ihtiyacın olduğunda sonucu merkeze ilet — PA'ya. Onay senden değil, PA'nın ekranını takip eden kullanıcıdan gelir.\n\n**AskUserQuestion yalnız merkezindir.** Sen bir soru ya da onay beklentisi yazarsan o ekranda kalır, PA'ya gitmez — ve iş sessizce durur. Sorunu SendMessage ile PA'ya yaz; kullanıcıya soracaksa PA sorar.\n\n**PA kullanıcıya sorarken iki tur işletir:**\n1. Önce açıklar ve *\"anladım\"* onayını alır — kararın dayanağı seçenek metnine sığmaz.\n2. Sonra kararı sorar."
  }
}
EOF

exit 0
