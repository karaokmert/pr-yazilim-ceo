#!/bin/bash
# Kanal relay — bir agent'in outbox'undaki, baskasina yazilmis ve HENUZ TASINMAMIS
# mesajlari hedefin inbox'una tasir. ISD-RELAY-DONT-CALL geregi tasima yoneticinin isi.
K=~/.pr-kanal/agent-project
S=$K/.relay-state
touch $S
tasindi=0
for out in $K/pr-agent-*/outbox/*.json; do
  [ -f "$out" ] || continue
  grep -qF "$(basename $out)" $S && continue
  hedef=$(python3 -c "import json;print(json.load(open('$out'))['to'])" 2>/dev/null)
  [ -z "$hedef" ] && continue
  hedef_kutu=$(ls -d $K/$hedef-*/ 2>/dev/null | head -1)
  [ -z "$hedef_kutu" ] && continue
  cp "$out" "$hedef_kutu/inbox/" && echo "$(basename $out)" >> $S
  gonderen=$(python3 -c "import json;print(json.load(open('$out'))['from'])" 2>/dev/null)
  echo "RELAY: $gonderen -> $hedef ($(basename $out))"
  tasindi=$((tasindi+1))
done
exit 0
