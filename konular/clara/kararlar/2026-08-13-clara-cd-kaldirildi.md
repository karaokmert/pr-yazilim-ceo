# Clara kısayolundan `cd` kaldırıldı — projesi ölçülebilir oldu

**Tarih:** 2026-08-13 · **Karar:** Mert · **Durum:** adım 1-2 uygulandı, adım 3 Mert'te

## Sorun — ölçüldü

Clara kısayolu şöyle çağırıyordu:
```
zsh -c claude --agent clara ...
```

PA ise `cd` **olmadan**:
```
zsh -c claude --agent ozel-yazilim:project-assistant ...
```

**Sonuç:** `lsof -a -p {pid} -d cwd` PA'ların gerçek projesini veriyor
(ölçüldü: `egelisaglik` · `goat` ×3), ama **üç Clara'nın üçü de**
`pr-yazilim-ceo` gösteriyor — oysa ikisi CEO'da, biri `skill-project`'te.

Mert'in tespiti: *"Clara açılışında bir hata var, symlink olmasına rağmen
`cd` ile çağrılıyor — aslında öyle çağrılmaması lazım."*

**`cd` gereksiz:** agent tanımı zaten symlink'le global bulunuyor —
`~/.claude/agents/clara.md → /Users/karaok/p/pr-yazilim-ceo/.claude/agents/clara.md`
(6 Ağustos'ta kurulmuş). `cd` muhtemelen symlink'ten önce kondu, sonra kaldırılması
unutuldu.

## Kazanç

- Clara'nın projesi **PA gibi ölçülebilir** olur (`cwd`)
- Tek-Clara kilidi defter yokken bile `ps` ile kurulabilir
- Açılışta *"hangi projedeyim"* sorusu ölçümle cevaplanır — şimdi Mert'e sormak gerekiyor

## Bedeli — iki risk ölçüldü, ikisi de kapatıldı

**Risk 1: skill'ler proje-yerel.** `cd` kalkarsa başka dizinden açılan Clara
skill'lerini bulamaz. **Ölçüldü: 11 skill'in 6'sında symlink YOKTU**
(`hafiza-duzeni` · `i-have-adhd` · `onay-brief` · `oturum-duzeni` ·
`proje-yonetimi` · `saha-monitorluk` — içlerinde en kritik olanı `oturum-duzeni`).
→ **Kuruldu: 11/11 symlink, hepsi doğru hedefte.**

**Risk 2: kanonda 20 göreli yol, 0 mutlak yol.** Başka dizinden açılınca
`konular/`, `gunluk/` yanlış yeri gösterir.
→ **Kanona mutlak kök satırı eklendi:** *"kayıtların kökü sabit
`/Users/karaok/p/pr-yazilim-ceo`, hangi dizinden açılırsan açıl."*

## Uygulama sırası

1. ✅ **Eksik 6 symlink kuruldu** (11/11 doğrulandı)
2. ✅ **Kanona mutlak kök + `pwd` kuralı güncellemesi**
3. ⏳ **`cd` kısayoldan kaldırılacak** — Mert yapacak

Sıra önemli: `cd` önce kaldırılsaydı skill'siz ve yanlış yol varsayımlı bir
Clara doğardı.

## Yan etki — bir kanon kuralı değişiyor

`"Ayrımı pwd VERMEZ"` kuralı bu `cd` yüzünden yazılmıştı. `cd` kalkınca `pwd`
**anlamlı sinyal** olur — ama **tek başına kanıt değil**: bir oturum `goat`'ta
açılıp başka projeye kayabilir.

Yeni sıra: **defter → `pwd`/`cwd` → Mert'in cümlesi.**
