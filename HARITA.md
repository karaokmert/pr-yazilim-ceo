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

- **Goat: 16 commit push'landı, Buse branch envanteri iki turda tamamlandı, altı agent kapandı** — Push 1eccf465 -> a30aff55, Actions 25/25 yeşil — QA damgaya güvenmedi, iki katman ölçtü (log içeriği + kapsam eşleşmesi), çünkü… · 2026-08-11 · `gunluk/goat/2026-08-11-kapanis.md`
- **Clara'nın proje rolü tanımlandı, üç kök kapatıldı** — Dünkü 17 düzeltmenin üç kökü de kapandı ve üçü tek yere bakıyormuş — Mert'in cümlesi: "beni proje takibinden kopartırsa Clara… · 2026-08-11 · `gunluk/ev/2026-08-11-kapanis-2.md`
Günlük ölçümler ve bulgular `gunluk/{tarih}.md` altında birikir — her bulgu bir başlık,
konu başına ayrı dosya açılmaz. Haritaya yalnız **karar**, **fikir** ve **referans**
girer.

- **ortam işi: agent panosu + tek-tık fabrika + temizlik** — ~/bin/agentlar yazıldı (proje bazlı gruplu açık agent panosu: ad/PID/süre + kanal satırı — izleyici canlı mı, son yazım,… · 2026-08-10 · `gunluk/ev/2026-08-10-kapanis.md`
- **`SendMessage` (cross-session) vs. bizim kanal** — : Claude Code 2.1.224'te agent'lar arası mesajlaşma geldi, dokümante (code.claude.com/docs/en/cross-session-messaging.md).… · 2026-08-08 · `gunluk/2026-08-08.md`
- **Qdrant MCP ölçümü (ARGE)** — : anlam eşleşmesi çalışıyor ama MCP alaka skorunu atıyor, COLLECTION_NAME tanımsız → kutu adını model uyduruyor, 43 koleksiyonun… · 2026-08-06 · `gunluk/2026-08-06.md`
- **ilk sprint planlandı (yedi iş, ClickUp'a taşındı)** — + iki skill yazıldı (sprint-yonetimi, clickup-duzeni, preload YOK — body'den yönlendirme) + ClickUp araç sınırları ölçüldü (yazma… · 2026-08-05 · `gunluk/2026-08-05.md`
- `gunluk/2026-08-04.md` — token maliyeti (OY agent'ı 145k açılış), `cache_create` başa baş 12'de, skill listesi 197→126 (kapatmak≠kaldırmak≠reload), v7 kanonu kazası, disk 1,9GB→42MB, **agent-agent kanalı 7 turluk stres testi** (uyanma+iş taşıma+komut taşıma çalıştı; 8 risk, kimlik ve yetki temel; maliyeti mesaj değil duraklama belirliyor)

## Projeler

- **ClickUp task takip düzeni — PRAG canlı testi** — düzen kuruldu ve 4 saat sahada koşturuldu (3 modül, 6 agent): üç fiil (PA açar/agent yürütür/Clara okur), ana task altında beş sub task (PA'nın discovery… · 2026-08-12 · `gunluk/prag/2026-08-12-kapanis.md` · **yarım**
- **Agent dağıtım yapısı** — hangi kopya yürürlükte: plugin v8 + fabrika repoda; 20 v7 symlink'i ve 27 proje içi kalıntı duruyor (Mert: şimdilik kalsın) · 2026-08-03 · `projeler/agent-dagitim-yapisi.md`
- **Proje envanteri** — 16 + 8 klasör tarandı: kendi ürün WupDoc (+ BalkanBee belirsiz), 8 aktif müşteri projesi, 4 yarı yolda, 3 git dışı, 1 şifre sızıntısı · 2026-08-03 · `projeler/envanter.md`

## Skill'ler

Üç katman: **body** = kim olduğun (her turda yüklenir) · **skill** = bir işin yöntemi
(description'la tetiklenir, kural + gerekçe) · **reference** = kanıt ve ölçüm (atıfla
çağrılır). Deneyim skill'e yazılmaz — reference'a ya da `gunluk/`'e gider.
Gerekçe: kanonda "Üç katman" bölümü.

**GÖREV mi DAVRANIŞ mı** — ayrım işin şekli: başı ve sonu var mı? Görev bir iş akışıdır
(başlar, sürer, biter — Clara'nın **rolleri** bunlar); davranış her işin içinde geçen
bir hamledir. Karışık listelendiğinde ayırt edilemiyor ve *"rollerin ne"* sorusuna
davranışlar sayılıyor — ölçüldü 2026-08-09.

### Görev (ayrı iş akışı — roller)

- **`proje-yonetimi`** — (118) — bir projede agent ekibini yürütme: zincir Clara→PAM→PAD→PQA→Mert'in push onayı, handoff taşıma, denetim turlarını izleme, sapma/tıkanma yakalama,… · 2026-08-09
- **`saha-monitorluk`** — (181) — agent'ları izleme; dört ayrı iş (belirti biriktirme, öğrenme ölçümü, bekçilik, proje durumu), karıştırılırsa yüzlerce olayda bir avuç kalem çıkar. · 2026-08-07
- **`sprint-yonetimi`** — (188) — haftalık sprint döngüsü, planlama sırası, zorunlu bağımlılık çıkarma · 2026-08-05
- **`kanal-kurulumu`** — (464 + 404 ref) — agent kanalı v3: JSON, mesaj başına dosya, beş betik (setup/send/read/watch/archive.py). tail -F ve printf yasak, STATUS.md, canlılık =… · 2026-08-07
- **`agent-sinama`** — (113 + 74 ref) — bir agent'ın davranışını ölçme: ilk soru "kural elinde miydi", mekanik arızalar (preload, frontmatter körlüğü), davranış/hüküm ayrımı,… · 2026-08-07
- **`oturum-duzeni`** — (137 + 88 ref) — açılış/kapanış, iki mod (EV/YÖNETİM), pwd mod vermez, kapanışın beş adımı, hafıza temizliği. · 2026-08-07

### Davranış (her işin içinde — rol değil)

- **`arama-disiplini`** — (51 + 88 ref) — grep / vektör / ls ayrımı ve vektörün üç körlüğü (çıktı adres değil cevap, skor alakayı ölçmüyor, filtre MCP'den kullanılamıyor) · 2026-08-07
- **`hafiza-duzeni`** — (189) — hangi bilgi hangi araca (graph/hafıza/dosya), graph'ta varlık-ilişki, durum tutulmaz, ve kaydın ömrü (ham girdi işlenince silinir) · 2026-08-07
- **`onay-brief`** — (88) — Mert'e iş sunma biçimi: üç blok + üç kapanış satırı, alan listesi türetilir, terim değil akış · 2026-08-07
- **`clickup-duzeni`** — (150) — ClickUp düzeni ve ölçülmüş araç sınırları (yazma güvenilmez: 9 sayfada 2 sessiz hata) · 2026-08-05

## Kararlar

- **PA'nın gereksinim kası şarta bağlanır — kaldırılmaz** — (Mert, 2026-08-11) — PA gövdesindeki "gereksinimi tamamlayansın, kullanıcının aklından geçmeyen senaryoları öne koyarsın" satırı yeni rol tanımıyla… · 2026-08-11 · `kararlar/2026-08-11-pa-gereksinim-kasi-sarta-baglanir.md` · **yarım**
- **Compact öncesi devir hook'u** — (Mert, 2026-08-10) — agent compaction'a girdiğinde işi kesip devir dokümanına geçecek; compaction bir kayıp anı değil kapanış sinyali olarak kullanılacak. · 2026-08-10 · `kararlar/2026-08-10-compact-oncesi-devir-hooku.md` · **yarım**
- **Onay brief'i — TÜM agent'ları bağlar** — (Mert, 2026-08-07) — ona sunulan her iş brief'i üç blok (şu an ne oluyor → nasıl çözüyorum AKIŞ → nereye dokunuyor) + üç kapanış satırı. · 2026-08-07 · `incelemeler/pa-davranis-senaryolari/onay-brief-kalibi.md`
- **Üç katman + skill'e ne yazılır** — (Mert, 2026-08-07) — body kim olduğun (her turda yüklenir, en pahalı yer) · skill bir işin yöntemi (kural + gerekçe) · reference kanıt ve ölçüm (atıfla… · 2026-08-07
- **Açılışta önce NEREDEYİM** — (Mert, 2026-08-07) — iki mod: EV (fikir olgunlaştırma, ölçüm, kanona yazma) · YÖNETİM (agent'ları yönet, trafiği taşı, kanalı ayakta tut). · 2026-08-07

- **Kanal JSON düzenine geçti — beş araç, dört uç doğruladı** — (sprint 3. iş kapandı) — md düzeni bırakıldı: tek dosyaya ekleme okuma maliyeti biriktiriyordu (48 KB = 13.831 token) ve çok satırlı mesajlar iç içe… · 2026-08-07 · `gunluk/2026-08-07-kapanis.md` · **yarım**


- **Çok proje yönetim düzeni** — kanal (Clara taşır, çağırmaz) + oturum belleği (agent detayı yazar, Clara özeti tutar) + kural agent kanonunda (pause skill'i); 11 açık oturum/4 PA… · 2026-08-04 · `kararlar/2026-08-04-cok-proje-yonetim-duzeni.md` · **yarım**

## İncelemeler

- **📌 Memory denetimi + öz değerlendirme — dokuz OY agent'ı** — Mert'in dört maddesi (memory skill'e uygun mu · kanonla çelişen kayıt · her işte lazım olan kuralları ekle · gözden kaçacakları ekle ama index şişmesin) +… · 2026-08-13 · `incelemeler/v8-agent-sinama/` · **yarım**
- **📌 v8 agent sınaması — beş rol, gözetimsiz** — Mert'in isteği: "2 saat yokum, agentların yeni versiyonlarını sına · canonlarını oku · agentlar sorgulanmalı · her agent için ayrı doküman · skillerde… · 2026-08-12 · `incelemeler/v8-agent-sinama/` · **yarım**
- **Fabrika denetimi — dört eksen** — (sprint 1. iş) — "yapılandır, yeniden kurma" kararı ölçümle doğrulandı: teknik kat sağlam (kırık atıf 0, hayalet index 0, hook 4/4 doğru parse, 122 kural,… · 2026-08-06 · `incelemeler/fabrika-denetimi/` · **yarım**
- **Agent memory envanteri** — ~/.claude/agent-memory'de 1744 dosya, 1537'si yetim (v7→v8 ad değişimi: qa-engineer → ozel-yazilim-qa-engineer, yeni kutu açıldı eskisi terk edildi). · 2026-08-06 · `incelemeler/agent-memory-envanteri/kayit.md` · **yarım**
- **Skill preload bulgusu** — agent'lar skills: listesini yükleyemiyor ve kendi frontmatter'ını göremiyor; fabrika hook'u kısmen çözüyor, kapsamı dar · 2026-08-03 · `incelemeler/skill-preload-bulgusu/kayit.md` · **eskimiş olabilir**
- **Fabrika ölçütü** — kuruluş oturumu (13,5 MB) tarandı; ölçüt Mert'in kendi cümlelerinde: sıfırdan üretme + alan bağımsızlığı + kestirmeden yapmama + bakım. · 2026-08-03 · `incelemeler/fabrika-olcutu/kayit.md` · **yarım**
- **Agent araç envanteri** — 46 araç var; fabrika beyaz liste (tools:), v8 OY siyah liste (disallowedTools: Workflow — tek kısıt). · 2026-08-03 · `incelemeler/agent-arac-envanteri/kayit.md` · **yarım**


## Kanal ve fabrika düzeni — 2026-08-06/07 gecesi

- **Canlılık ölçütü çalışmıyor** — PID + BAŞLANGIÇ çifti ölü/canlı ayrımı yapamıyor: kill -0 taraması PQA'yı ölü gösterdi, o anda rapor yazıyordu. · 2026-08-06 · **yarım**
- **Description şişmesi** — v8'in 76 skill'inin 76'sı 300 karakter hedefini aşıyor (medyan 664, min 474, max 892). acs-gorusme 52 satır gövdeye 850 karakter description.… · 2026-08-07 · `gunluk/2026-08-07.md`
- **Atıf haritası onarıldı** — 123 kayıt, 98 atıflı / 25 atıfsız (dar kapsam 36'ydı; docs/ dahil edildi, memory hariç). · 2026-08-07
- **DAG deseni** — atıfsız 25 kaydın 15'i DAG. · 2026-08-07 · `gunluk/2026-08-07.md`
- **Fabrika body/preload ölçümü** — dört body'nin kuralları temiz, URT-BODY-BY-SILENCE uygulanmış (v8'den iyi — v8'de P-1 problemi vardı). · 2026-08-07 · `gunluk/2026-08-07.md`
- **Sabah raporu (gece çalışması)** — fabrikanın kendi kanonu onarıldı: 123 kayıt 97/26, sekiz hüküm karşılığı üç body'ye, beş cascade. · 2026-08-07 · `gunluk/2026-08-07-sabah-raporu.md`
- **`Task` kaldırıldı, iletişim kanal + ekran** — Mert'in üç kararı: (1) agent agent'ı Task ile çağırmaz — kanaldan gelen handoff (agent outbox → yönetici → hedef inbox) ya da ekrandan gelen handoff,… · 2026-08-07 · `kararlar/2026-08-07-task-kaldirildi-iletisim-kanal-ve-ekran.md`
- **BEKLEYEN — çerçeve cümlesi geride kalıyor** — PAM'in önerisi: bir hüküm değişince ona dayanan açıklama cümlesi sessizce yanlış kalıyor ve kimlik taraması onu yapısal olarak kaçırıyor (cümlede kimlik… · 2026-08-07 · `kararlar/BEKLEYEN-cerceve-cumlesi-geride-kaliyor.md`
- **Atıf sahipliği boşluğu — bir günde beş vaka** — rules-index.json'daki atıf listelerini kimin güncelleyeceği kanonda tanımsız: PAD-SYNC-INDEX yalnız kimlik üretimini bağlıyor, atıf üretimini hiçbir hüküm… · 2026-08-08 · `incelemeler/2026-08-08-fabrika-kanon-sorgulama/karar-kalemleri.md`

- **Agent'lar onay akışına düşüyor — oturum modu** — fabrikanın dört agent'ından ikisi (PAD/PQA) Bash komutlarında onay ekranında 44 dakika bekledi ve kanal bunu göremedi. · 2026-08-08

- **Kanal betikleri git'te değil — boşluk BÜYÜK** — beş betik 532 satır, fabrika git'inde hiçbir kopyası yok (iki eksende sınandı). · 2026-08-08 · `incelemeler/kanal-asset-boslugu.md`


- **`claude plugin validate` başarısızlıkta `rc=0` dönüyor** — ekrana "✘ Validation failed" yazıp sıfır döndürüyor; validate && commit zinciri kurulursa başarısız doğrulama geçer. · 2026-08-08 · `incelemeler/plugin-validate-cikis-kodu.md`

## Fikirler

- **📌 Saha agent notları — Mert biriktiriyor, toplu değerlendirilecek** — Mert sahada gördüğü agent aksaklıklarını not olarak veriyor; tartışma sonraya, her not kaydedilir + ölçülür + ön hipotez alır. · 2026-08-10 · `fikirler/saha-agent-notlari/notlar.md`
- **🔴 `relay.sh` komut enjeksiyonu — fabrikaya iletilmeyi bekliyor** — kanal relay betiği mesajın to/from alanını doğrulamadan kabuğa gömüyor: ls -d $K/$hedef-/ tırnaksız + dosya yolu Python kaynağına string… · 2026-08-10 · `fikirler/agent-iletisim-kanali/relay-guvenlik-bulgusu.md` · **yarım**
- **OY v8 pilot rol ÜRETİLDİ ve testten geçti** — (gece nöbeti, 2026-08-10 00:35→08:20) — agent-project/team/ozel-yazilim/: 15 dosya, 9 skill, 83.803 karakter, validate temiz. · 2026-08-10 · `gunluk/fabrika/2026-08-10-sabah-raporu.md` · **yarım**
- **🏭 FABRİKA TAŞINDI + OY v8 DÜZELTME BAŞLADI — gece oturumu** — Mert'in kararı: fabrika ekibi skill-project'e taşındı (81 dosya: 4 rol, 5 skill, hook, rules-index, 65 memory), OY v8 orada düzeltilip sürüm yollanacak,… · 2026-08-11 · `gunluk/fabrika/2026-08-11-sabah-brief.md`
- **⚖️ BE karşılaştırma testi: v8 (plugin) vs FAB (fabrika paketi) — DÖRT TUR** — iki backend-developer yan yana, aynı sorular aynı anda. · 2026-08-10 · `gunluk/fabrika/2026-08-10-be-karsilastirma-testi.md` · **yarım**
- **🏭 Goat sahasından fabrikaya İKİ KALEM (önce beş sanıldı — ÜÇÜ YANLIŞ ÇIKTI)** — hiçbiri kural ihlali değil, fabrikanın ürettiği malzemenin sorunu. · 2026-08-10 · `gunluk/goat/2026-08-10.md` · **yarım**
- **🔴 `pryazilim.core` arama katmanı sessizce yutuyor — tüm OY projelerini etkiler** — (BE ölçümü, 2026-08-10) — SearchManager.cs (582 satır): CreateIndexAsync hatada null dönüyor (ne exception ne hata kodu) ve logManager.Exception'ın… · 2026-08-10 · `gunluk/goat/2026-08-10.md`
- **OY v8 yeniden üretimi — gereksinim** — (Mert'in kararı, 2026-08-09: "artık OY'ye başlayalım") — OY fabrikada yeniden üretilecek, taşınmayacak; sahadaki v8'e dokunulmuyor. · 2026-08-09 · `fikirler/oy-v8-yeniden-uretim/gereksinim-taslagi.md` · **yarım**
- **OY üretim yöntemi** — v8'in tutmama sebebi mekanikmiş (preload); iki eski hipotez geçersiz, hook sonrası v8 iki gündür çalışıyor · 2026-08-03 · `fikirler/oy-uretim-yontemi/durum.md` · **yarım**
- **Agent iletişim kanalı — gereksinim analizi** — kanal fikri henüz mimariye dönüşmeden yazılan discovery; yazan Clara değil web-project-assistant (websitesi/0.8.1), girdisi web-kanal-2 trafiği. · 2026-08-06 · `fikirler/agent-iletisim-kanali/DISCOVERY.md` · **eskimiş olabilir**
- **Kanalda iki agent — yaşanmış deneyim** — PA'nın kendi gözlemi (DO ile 12 saatlik kanal): ne üretildi, nerede tıkandı. · 2026-08-05 · `fikirler/agent-iletisim-kanali/DENEYIM-web-pa.md`

## Sprint

Sprint **ClickUp'ta yaşıyor** (`CLARA DOC → Sprint Planları`), repoda değil. Aşağıdaki
dosya ilk taslak — tarihsel kayıt, yürürlükte değil.

- **İlk sprint iskeleti (5→12 Ağustos)** — yedi işin ilk hâli ve zorunlu sıra; kapsamlar sonradan değişti, ClickUp güncel. · 2026-08-12 · `sprint/2026-08-05-2026-08-12.md` · **eskimiş olabilir**
