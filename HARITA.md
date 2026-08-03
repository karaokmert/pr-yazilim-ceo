# Harita — bu odada ne var

Clara'nın kayıt haritası. Bir konu açıldığında **önce buraya** bakılır: daha önce
konuşulmuş mu, karar verilmiş mi, yarım mı kalmış.

Her satır bir kayıt. Biçim:
`- **{konu}** — {ne bulundu} · {tarih} · `{yol}` · {durum}`

Durumlar: **kapalı** (karar verildi, tartışılmaz) · **yarım** (iş bitmedi, devam edilir)
· **eskimiş olabilir** (bir dayanağı değişmiş olabilir, kullanmadan önce bakılır)

Kural: bir kayıt yazıldığında buraya satırı da yazılır. Haritasız kayıt kaybolur;
kayıtsız harita satırı yalan olur.

## Kararlar

- **Clara kurulumu** — bu odanın neden ayrı olduğu, tek personel, üç sert kuralın gerekçesi · 2026-08-02 · `kararlar/2026-08-02-clara-kurulumu.md` · kapalı
- **Memory disiplini** — üretim hattının memory kanonundan iki kural alındı, üçü bilinçli bırakıldı · 2026-08-03 · `kararlar/2026-08-03-clara-memory-disiplini.md` · kapalı ama "kendi kanonuna yazmaz" bölümü **iptal** (bkz. kanon yetkisi)
- **Clara'nın büyüme düzeni** — ne hafızaya ne repoya gider, ne zaman yazılır, oturum başında ne okunur; araç eşiği · 2026-08-03 · `kararlar/2026-08-03-clara-buyume-duzeni.md` · kapalı
- **Clara'nın kanon yetkisi** — kanona yazma yasağı kaldırıldı; kural içeride/gerekçe dışarıda, üç dokunulmaz, şişme freni · 2026-08-03 · `kararlar/2026-08-03-clara-kanon-yetkisi.md` · kapalı

## İncelemeler

- **Clara'nın ilk sınaması** — kanon dört baskı testinde davranış üretti; sekiz boşluk kapatıldı · 2026-08-02 · `incelemeler/clara-ilk-sinama/kayit.md` · kapalı
- **v7 iletişim düzeni** — v7'nin kural biçimi nasıl davranış üretiyordu (kısıt, negatif liste, rol-ton) · 2026-08-03 · `incelemeler/v7-iletisim-duzeni/bulgu.md` · kapalı
- **Skill preload bulgusu** — agent'lar `skills:` listesini yükleyemiyor ve kendi frontmatter'ını göremiyor; fabrika hook'u kısmen çözüyor, kapsamı dar · 2026-08-03 · `incelemeler/skill-preload-bulgusu/kayit.md` · eskimiş olabilir (Claude Code sürümüne bağlı; `anthropics/claude-code#25834`)
- **Clara'nın beyni — ilk tespit** — üç kat (kanon/kayıt/hafıza), hafızada tek `user` kaydı yok, `.remember` git dışı, RAG gerekmiyor · 2026-08-03 · `incelemeler/clara-beyni/tespit.md` · kapalı

## Fikirler

- **OY üretim yöntemi** — v8'in tutmama sebebi mekanikmiş (preload); iki eski hipotez geçersiz, hook sonrası v8 iki gündür çalışıyor · 2026-08-03 · `fikirler/oy-uretim-yontemi/durum.md` · yarım (açık soru: kural eline geçtiğinde davranış üretiyor mu — ölçülmedi)
