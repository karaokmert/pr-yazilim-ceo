#!/bin/bash
# Goat nabzı — kim canlı, kim sessiz, kuyrukta ne var
G=~/.pr-kanal/goat
echo "════ GOAT NABZI · $(date '+%H:%M') ════"
echo "--- açık oturumlar ---"
ps aux | grep "[c]laude" | grep -oE "\-\-name [^ ]+ · [A-Za-z]+ - [0-9:-]+ - goat" | sed 's/.*· /  /' | sort -u
echo "--- kanal kutuları (son çıkış) ---"
for k in "$G"/*/; do
  b=$(basename "$k"); [ "$b" = tools ] || [ "$b" = archive ] && continue
  son=$(ls -t "$k/outbox"/*.json 2>/dev/null | head -1 | xargs -I{} stat -f "%Sm" -t "%H:%M" {} 2>/dev/null)
  inb=$(ls "$k/inbox"/*.json 2>/dev/null | wc -l | tr -d ' ')
  [ -n "$son" ] && printf "  %-34s çıkış:%s inbox:%s\n" "${b%%-2026*}" "$son" "$inb"
done
echo "--- git ---"
cd ~/p/ozel-yazilim/goat 2>/dev/null && {
  echo "  ağaç: $(git status --porcelain 2>/dev/null | wc -l | tr -d ' ') değişiklik"
  echo "  kuyruk: $(git log origin/main..HEAD --oneline 2>/dev/null | wc -l | tr -d ' ') commit"
}
