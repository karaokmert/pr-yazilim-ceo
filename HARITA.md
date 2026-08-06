# Harita — bu odada ne var

Clara'nın kayıt haritası. Bir konu açıldığında **önce buraya** bakılır: daha önce
konuşulmuş mu, karar verilmiş mi, yarım mı kalmış.

Her satır bir kayıt. Biçim:
`- **{konu}** — {ne bulundu} · {tarih} · `{yol}` · {durum}`

Durumlar: **kapalı** (karar verildi, tartışılmaz) · **yarım** (iş bitmedi, devam edilir)
· **eskimiş olabilir** (bir dayanağı değişmiş olabilir, kullanmadan önce bakılır)

Kural: bir kayıt yazıldığında buraya satırı da yazılır. Haritasız kayıt kaybolur;
kayıtsız harita satırı yalan olur.

## Günlük

Günlük ölçümler ve bulgular `gunluk/{tarih}.md` altında birikir — her bulgu bir başlık,
konu başına ayrı dosya açılmaz. Haritaya yalnız **karar**, **fikir** ve **referans**
girer.

- `gunluk/2026-08-06.md` — **Qdrant MCP ölçümü (ARGE, yarım)**: anlam eşleşmesi çalışıyor ama MCP alaka skorunu atıyor (400 kayıtta her sorgu 10 alakasız not döndürür), `COLLECTION_NAME` tanımsız → kutu adını model uyduruyor, 43 koleksiyonun 26'sı ölü. **Grep 0.041 sn vs vektör 11+ dk indeksleme** — ama grep'in bulamadığı niyet sorusu ölçülmedi, karşılaştırma script'i `arge/qdrant/` altında koşulmayı bekliyor
- `gunluk/2026-08-05.md` — **ilk sprint planlandı (yedi iş, ClickUp'a taşındı)** + iki skill yazıldı (`sprint-yonetimi`, `clickup-duzeni`, preload YOK — body'den yönlendirme) + ClickUp araç sınırları ölçüldü (yazma güvenilmez: 9 sayfada 2 sessiz hata; sayfa silinemiyor; arama tam kelimeyi kaçırıyor) + **`skill-creator` eval koşucusu kırık** (gövdesiz kopya ölçüyor — recall %0 bulgusu geçersiz, düzeltildi) + web kanal deneyi 2. tur + **saha izleme (23 bulgu)**: `#PRY-17533` tam zinciri (16 handoff/7 oturum/dev→prod), QA prod GO verdi Mert SQL hatasını yakaladı, discovery kapanışta okunmuyor (GOAT), kanon aletin adını veriyor amacını vermiyor (Platin BE), **ÖRÜNTÜ (Bulgu 23): agent'lar yetki sınırını biliyor dayanağa dönmeyi bilmiyor — 5 ölçüm noktası**
- `gunluk/2026-08-04.md` — token maliyeti (OY agent'ı 145k açılış), `cache_create` başa baş 12'de, skill listesi 197→126 (kapatmak≠kaldırmak≠reload), v7 kanonu kazası, disk 1,9GB→42MB, **agent-agent kanalı 7 turluk stres testi** (uyanma+iş taşıma+komut taşıma çalıştı; 8 risk, kimlik ve yetki temel; maliyeti mesaj değil duraklama belirliyor)

## Projeler

- **Agent dağıtım yapısı** — hangi kopya yürürlükte: plugin v8 + fabrika repoda; 20 v7 symlink'i ve 27 proje içi kalıntı duruyor (Mert: şimdilik kalsın) · 2026-08-03 · `projeler/agent-dagitim-yapisi.md` · **referans** (okuma öncesi yol doğrulaması)
- **Proje envanteri** — 16 + 8 klasör tarandı: kendi ürün WupDoc (+ BalkanBee belirsiz), 8 aktif müşteri projesi, 4 yarı yolda, 3 git dışı, 1 şifre sızıntısı · 2026-08-03 · `projeler/envanter.md` · **referans** (durum değişince güncellenir)

## Kararlar

- **Sprint planlama kararları** — ilk sprint (5→12 Ağustos) planlandı, yedi iş detaylandı. Üç karar verildi: fabrika yeniden kurulmuyor **yapılandırılıyor**, PAM düğümü (planı Clara yazar), kanal kimliği (proje bazlı oturum kimliği → keşif zorunlu hâle geldi). Üç karar ölçüme bırakıldı: yönlendirme, preload, onay akışı · 2026-08-05 · `kararlar/2026-08-05-sprint-planlama-kararlari.md` · kapalı
- **Yönetim kurulu konumu + yalın üretim** — Mert+Clara yönetim kurulu, fabrika üretici, birimler saha; ihtiyaç doğmadan kapasite kurulmaz. Kanona iki madde: "Nerede duruyorsun" + "olmayan probleme çözüm önermezsin" · 2026-08-05 · `kararlar/2026-08-05-yonetim-kurulu-ve-yalin-uretim.md` · kapalı
- **Clara merak kuralı** — ClickUp araması ölçülmeden hüküm verildi (elli aracın ikisi okundu, `hasContentMatch` kanıtı görmezden gelindi). Kanona **MERAK EDERSİN** maddesi eklendi · 2026-08-05 · `kararlar/2026-08-05-clara-merak-kurali.md` · kapalı

- **Devir kaydı — 4/5 Ağustos oturumu** — 21 saatlik oturumun kazanımları, açık ölçümler, bekleyen işler, Clara'nın hataları · 2026-08-05 · `gunluk/2026-08-05-devir.md` · kapalı

- **Release tag sistemi kaldırıldı** — `vX.Y.Z` tag'i akıştan çıkıyor; EGELI `v1.3.3` canlı izlendi: prod'a çıktıktan SONRA atıldı, 5 adım/0 bilgi kazancı, rollback SHA ile çalışıyor · 2026-08-05 · `kararlar/2026-08-05-release-tag-sistemi-kaldirildi.md` · kapalı (kanondan çıkarılması PAM'de — devir bloğu yazılmadı)

- **Clara kurulumu** — bu odanın neden ayrı olduğu, tek personel, üç sert kuralın gerekçesi · 2026-08-02 · `kararlar/2026-08-02-clara-kurulumu.md` · kapalı
- **Memory disiplini** — üretim hattının memory kanonundan iki kural alındı, üçü bilinçli bırakıldı · 2026-08-03 · `kararlar/2026-08-03-clara-memory-disiplini.md` · kapalı ama "kendi kanonuna yazmaz" bölümü **iptal** (bkz. kanon yetkisi)
- **Clara'nın büyüme düzeni** — ne hafızaya ne repoya gider, ne zaman yazılır, oturum başında ne okunur; araç eşiği · 2026-08-03 · `kararlar/2026-08-03-clara-buyume-duzeni.md` · kapalı
- **Clara'nın kanon yetkisi** — kanona yazma yasağı kaldırıldı; kural içeride/gerekçe dışarıda, üç dokunulmaz, şişme freni · 2026-08-03 · `kararlar/2026-08-03-clara-kanon-yetkisi.md` · kapalı
- **Yazma sınırı değişti** — `CLA-WRITE-HERE-ONLY` kaldırıldı, yerine `CLA-ASK-BEFORE-WRITING-OUT`: başka repoya yazılır ama metni gösterip onay alınır; izin kuralı hâlâ yasak · 2026-08-03 · `kararlar/2026-08-03-clara-yazma-sinirinin-degismesi.md` · kapalı
- **Çok proje yönetim düzeni** — kanal (Clara taşır, çağırmaz) + oturum belleği (agent detayı yazar, Clara özeti tutar) + kural agent kanonunda (`pause` skill'i); 11 açık oturum/4 PA ölçüldü, bir iş 4 durak geziyor; Mert düzeltmiyor besliyor (21 mesajda 2 düzeltme) · 2026-08-04 · `kararlar/2026-08-04-cok-proje-yonetim-duzeni.md` · yarım (AG'ye 3 üretim kalemi gitmedi; 3 açık soru)

## İncelemeler

- **Clara'nın ilk sınaması** — kanon dört baskı testinde davranış üretti; sekiz boşluk kapatıldı · 2026-08-02 · `incelemeler/clara-ilk-sinama/kayit.md` · kapalı
- **v7 iletişim düzeni** — v7'nin kural biçimi nasıl davranış üretiyordu (kısıt, negatif liste, rol-ton) · 2026-08-03 · `incelemeler/v7-iletisim-duzeni/bulgu.md` · kapalı
- **Skill preload bulgusu** — agent'lar `skills:` listesini yükleyemiyor ve kendi frontmatter'ını göremiyor; fabrika hook'u kısmen çözüyor, kapsamı dar · 2026-08-03 · `incelemeler/skill-preload-bulgusu/kayit.md` · eskimiş olabilir (Claude Code sürümüne bağlı; `anthropics/claude-code#25834`)
- **Fabrika ölçütü** — kuruluş oturumu (13,5 MB) tarandı; ölçüt Mert'in kendi cümlelerinde: sıfırdan üretme + alan bağımsızlığı + kestirmeden yapmama + bakım. Fabrika bitmedi, 08-02 23:50'de beklemeye alındı · 2026-08-03 · `incelemeler/fabrika-olcutu/kayit.md` · yarım (fabrika ölçütle okunmadı; devam mı baştan mı — Mert'te)
- **Yerel symlink temizliği** — `~/.claude/skills` ve `agents` boşaltıldı (50 symlink, 30 skill + 20 agent); v7 emekli. Gerekçe: agent v8'den çağrılıp v7 kanonu okuyordu (ölçüldü) · 2026-08-04 · `kararlar/2026-08-04-yerel-symlink-temizligi.md` · kapalı
- **Fabrikanın saha davranışı** — 41 oturum tarandı; zincir 2 kez döndü ve **düzgün döndü** (5 PAD/5 PQA turu, 4 red, 7 bulgu, ihlal yok). Ama `team/` boş: sıfırdan üretme hiç denenmedi · 2026-08-03 · `incelemeler/fabrika-olcutu/saha-davranisi.md` · kapalı
- **Fabrikanın zayıf noktaları** — filo bakımı sahipsiz (fabrikanın var olma sebebi!); `Skill` aracı 7 oturumda 0 çağrı; `dagitim` 20 kural sıfır test; PQA aracı olmadan Write yaptı; kanonun yalnız yasak tarafı sınandı · 2026-08-03 · `incelemeler/fabrika-olcutu/zayif-noktalar.md` · kapalı (kayıt tam; işlenmesi Mert'te)
- **Agent araç envanteri** — 46 araç var; fabrika beyaz liste (`tools:`), v8 OY siyah liste (`disallowedTools: Workflow` — tek kısıt). QA/CA artık Write/Edit'e sahip, "kod yazmazsın" yalnız metinde · 2026-08-03 · `incelemeler/agent-arac-envanteri/kayit.md` · yarım (QA/CA'dan Write alınacak mı — Mert'te)
- **PAM'in `CLAUDE.md` yetkisi** — üç dosya düzeltildi (yazma sınırı değiştikten sonra); auto-mode bloğu ölçüldü: geçici, ikinci denemede geçti, izin kuralı gereksiz · 2026-08-03 · `incelemeler/pam-claude-md-yetkisi/kayit.md` · kapalı (commit fabrikada)
- **`CLAUDE.md` otomatik yükleme** — subagent `CLAUDE.md` hiyerarşisini görüyor ve uyguluyor (3/3 tuhaf kural); agent tanımı/skill gövdesi gelmiyor — iki mekanizma ayrı · 2026-08-03 · `incelemeler/claude-md-otomatik-yukleme/kayit.md` · kapalı (ölçek ölçülmedi)
- **Kanon yetkisi sınaması** — üç baskı testi (yetkiyi kendine karşı kullanma, yanlış teşhis, kötü fikir + acele); dört yeni kural da davranış üretti · 2026-08-03 · `incelemeler/clara-kanon-yetkisi-sinamasi/kayit.md` · kapalı
- **Clara'nın beyni — ilk tespit** — üç kat (kanon/kayıt/hafıza), hafızada tek `user` kaydı yok, `.remember` git dışı, RAG gerekmiyor · 2026-08-03 · `incelemeler/clara-beyni/tespit.md` · kapalı

- **Onay brief kalıbı** — Mert'in onaylayabildiği biçim bulundu (4 denemede). Her iş: şu an ne oluyor / akış / **nereye yazılıyor** (Handler·DataLayer·Cache·Tablo·Emsal, boş olan da yazılır). Ölçütü: "başka biri sorsa anlatabilir miyim" · 2026-08-04 · `incelemeler/pa-davranis-senaryolari/onay-brief-kalibi.md` · kapalı (gereksinim PAM'e gitmedi)
- **PA Senaryo 1 — erken adımlama** — GOAT'ta 6 düzeltme, tek kök: eldeki bilgi tamamlanmadan adıma geçme. Kural elinde VAR (`WEB-PA-DANISMA-EYLEM-AYRIMI`) ama görev adımı ID'siz olduğu için tespit edilemiyor. Mert'in istediği 7 maddelik yöntem + PA'nın kendi teşhisleri · 2026-08-04 · `incelemeler/pa-davranis-senaryolari/senaryo-1-erken-adimlama.md` · kapalı (gereksinim PAM'e gitmedi)

## Fikirler

- **OY üretim yöntemi** — v8'in tutmama sebebi mekanikmiş (preload); iki eski hipotez geçersiz, hook sonrası v8 iki gündür çalışıyor · 2026-08-03 · `fikirler/oy-uretim-yontemi/durum.md` · yarım (açık soru: kural eline geçtiğinde davranış üretiyor mu — ölçülmedi)
