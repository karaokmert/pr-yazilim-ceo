#!/bin/bash
# Tikanma tespiti: transcript sessizligi + kutu durumu BIRLIKTE okunur.
# Sessizlik tek basina tikanma DEGIL - is beklemek de sessizdir.
# TIKANMA = inbox'ta okunmamis is var AMA transcript hareketsiz.
P=~/.claude/projects/-Users-karaok-p-agent-project
K=~/.pr-kanal/agent-project
simdi=$(date +%s)

kontrol() {
  rol=$1; dosya=$2
  f=$P/$dosya
  [ -f "$f" ] || return
  sessiz=$(( (simdi - $(stat -f %m $f)) / 60 ))
  kutu=$(ls -d $K/$rol-*/ 2>/dev/null | head -1)
  [ -z "$kutu" ] && return
  cur=$(cat $kutu/inbox/.cursor 2>/dev/null || echo "")
  yeni=0
  for m in $(find $kutu/inbox -name '*.json' -type f 2>/dev/null | sort); do
    if [ "$(basename $m)" \> "$cur" ]; then yeni=$((yeni+1)); fi
  done
  # En yeni okunmamis mesajin YASI - mesaj yeni dusmusse tikanma degil
  enyeni=$(find $kutu/inbox -name '*.json' -type f -newer $kutu/inbox/.cursor 2>/dev/null | head -1)
  if [ -n "$enyeni" ]; then
    myas=$(( (simdi - $(stat -f %m $enyeni)) / 60 ))
  else
    myas=0
  fi
  # TIKANMA: mesaj 6 dk+ once dustu AMA transcript o mesajdan beri hareketsiz
  if [ "$yeni" -gt 0 ] && [ "$myas" -ge 6 ] && [ "$sessiz" -ge "$myas" ]; then
    echo "TIKANMA: $rol - $myas dk once dusen mesaj okunmamis, transcript $sessiz dk sessiz"
  fi
  if [ "$yeni" -eq 0 ] && [ "$sessiz" -ge 25 ]; then
    echo "SESSIZ: $rol - $sessiz dk hareketsiz, inbox bos"
  fi
}

kontrol pr-agent-manager 1504d896-549d-4cd9-b569-12d55822eaa0.jsonl
kontrol pr-agent-developer 16cf9736-4a18-4e54-a1b1-75dcb1680edb.jsonl
kontrol pr-agent-qa 46abe430-df5a-40e5-84db-622c726cd2d2.jsonl
kontrol pr-agent-context-analyst 197cf511-ee58-497f-b688-5f82c82920af.jsonl
exit 0
