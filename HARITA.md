# Harita — bu odada ne var

Clara'nın kayıt haritası. Bir konu açıldığında **önce buraya** bakılır: daha önce
konuşulmuş mu, karar verilmiş mi, yarım mı kalmış.

Her satır bir kayıt. Biçim:
`- **{konu}** — {ne bulundu} · {tarih} · `{yol}` · {durum}`

Durumlar: **kapalı** (karar verildi, tartışılmaz) · **yarım** (iş bitmedi, devam edilir)
· **eskimiş olabilir** (bir dayanağı değişmiş olabilir, kullanmadan önce bakılır)

Kural: bir kayıt yazıldığında buraya satırı da yazılır. Haritasız kayıt kaybolur;
kayıtsız harita satırı yalan olur.

## Projeler

- **Agent dağıtım yapısı** — hangi kopya yürürlükte: plugin v8 + fabrika repoda; 20 v7 symlink'i ve 27 proje içi kalıntı duruyor (Mert: şimdilik kalsın) · 2026-08-03 · `projeler/agent-dagitim-yapisi.md` · **referans** (okuma öncesi yol doğrulaması)
- **Proje envanteri** — 16 + 8 klasör tarandı: kendi ürün WupDoc (+ BalkanBee belirsiz), 8 aktif müşteri projesi, 4 yarı yolda, 3 git dışı, 1 şifre sızıntısı · 2026-08-03 · `projeler/envanter.md` · **referans** (durum değişince güncellenir)

## Kararlar

- **Clara kurulumu** — bu odanın neden ayrı olduğu, tek personel, üç sert kuralın gerekçesi · 2026-08-02 · `kararlar/2026-08-02-clara-kurulumu.md` · kapalı
- **Memory disiplini** — üretim hattının memory kanonundan iki kural alındı, üçü bilinçli bırakıldı · 2026-08-03 · `kararlar/2026-08-03-clara-memory-disiplini.md` · kapalı ama "kendi kanonuna yazmaz" bölümü **iptal** (bkz. kanon yetkisi)
- **Clara'nın büyüme düzeni** — ne hafızaya ne repoya gider, ne zaman yazılır, oturum başında ne okunur; araç eşiği · 2026-08-03 · `kararlar/2026-08-03-clara-buyume-duzeni.md` · kapalı
- **Clara'nın kanon yetkisi** — kanona yazma yasağı kaldırıldı; kural içeride/gerekçe dışarıda, üç dokunulmaz, şişme freni · 2026-08-03 · `kararlar/2026-08-03-clara-kanon-yetkisi.md` · kapalı
- **Yazma sınırı değişti** — `CLA-WRITE-HERE-ONLY` kaldırıldı, yerine `CLA-ASK-BEFORE-WRITING-OUT`: başka repoya yazılır ama metni gösterip onay alınır; izin kuralı hâlâ yasak · 2026-08-03 · `kararlar/2026-08-03-clara-yazma-sinirinin-degismesi.md` · kapalı

## İncelemeler

- **Clara'nın ilk sınaması** — kanon dört baskı testinde davranış üretti; sekiz boşluk kapatıldı · 2026-08-02 · `incelemeler/clara-ilk-sinama/kayit.md` · kapalı
- **v7 iletişim düzeni** — v7'nin kural biçimi nasıl davranış üretiyordu (kısıt, negatif liste, rol-ton) · 2026-08-03 · `incelemeler/v7-iletisim-duzeni/bulgu.md` · kapalı
- **Skill preload bulgusu** — agent'lar `skills:` listesini yükleyemiyor ve kendi frontmatter'ını göremiyor; fabrika hook'u kısmen çözüyor, kapsamı dar · 2026-08-03 · `incelemeler/skill-preload-bulgusu/kayit.md` · eskimiş olabilir (Claude Code sürümüne bağlı; `anthropics/claude-code#25834`)
- **Fabrika ölçütü** — kuruluş oturumu (13,5 MB) tarandı; ölçüt Mert'in kendi cümlelerinde: sıfırdan üretme + alan bağımsızlığı + kestirmeden yapmama + bakım. Fabrika bitmedi, 08-02 23:50'de beklemeye alındı · 2026-08-03 · `incelemeler/fabrika-olcutu/kayit.md` · yarım (fabrika ölçütle okunmadı; devam mı baştan mı — Mert'te)
- **Agent araç envanteri** — 46 araç var; fabrika beyaz liste (`tools:`), v8 OY siyah liste (`disallowedTools: Workflow` — tek kısıt). QA/CA artık Write/Edit'e sahip, "kod yazmazsın" yalnız metinde · 2026-08-03 · `incelemeler/agent-arac-envanteri/kayit.md` · yarım (QA/CA'dan Write alınacak mı — Mert'te)
- **PAM'in `CLAUDE.md` yetkisi** — üç dosya düzeltildi (yazma sınırı değiştikten sonra); auto-mode bloğu ölçüldü: geçici, ikinci denemede geçti, izin kuralı gereksiz · 2026-08-03 · `incelemeler/pam-claude-md-yetkisi/kayit.md` · kapalı (commit fabrikada)
- **`CLAUDE.md` otomatik yükleme** — subagent `CLAUDE.md` hiyerarşisini görüyor ve uyguluyor (3/3 tuhaf kural); agent tanımı/skill gövdesi gelmiyor — iki mekanizma ayrı · 2026-08-03 · `incelemeler/claude-md-otomatik-yukleme/kayit.md` · kapalı (ölçek ölçülmedi)
- **Kanon yetkisi sınaması** — üç baskı testi (yetkiyi kendine karşı kullanma, yanlış teşhis, kötü fikir + acele); dört yeni kural da davranış üretti · 2026-08-03 · `incelemeler/clara-kanon-yetkisi-sinamasi/kayit.md` · kapalı
- **Clara'nın beyni — ilk tespit** — üç kat (kanon/kayıt/hafıza), hafızada tek `user` kaydı yok, `.remember` git dışı, RAG gerekmiyor · 2026-08-03 · `incelemeler/clara-beyni/tespit.md` · kapalı

## Fikirler

- **OY üretim yöntemi** — v8'in tutmama sebebi mekanikmiş (preload); iki eski hipotez geçersiz, hook sonrası v8 iki gündür çalışıyor · 2026-08-03 · `fikirler/oy-uretim-yontemi/durum.md` · yarım (açık soru: kural eline geçtiğinde davranış üretiyor mu — ölçülmedi)
