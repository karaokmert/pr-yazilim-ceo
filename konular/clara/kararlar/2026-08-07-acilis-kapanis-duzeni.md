# Clara'nın kanonuna açılış ve kapanış düzeni eklendi

**Tarih:** 2026-08-07 · **Karar veren:** Mert
**Nereye:** `.claude/agents/clara.md` — `Nasıl çalışırsın` bölümünün başına (724 → 788
satır)

Mert'in talebi: *"Kendi kurallarına açılış ve kapanış kurallarını ekle. Bir iş bittiğinde
ya da kapanış geldiğinde ne yapacaksın, açılışta ne yapacaksın."*

Ve öncesinde: *"Gece görevlerinde kapanış dokümanı da yaz ki sabah yeni session ile
başlayabilelim. İlerlemeleri mutlaka hafızana al — yeni session okuyarak başlayabilsin,
sürekli context taşımayalım. Ama memory düzenini iyi yap ki şişme olmasın."*

---

## Neden gerekliydi — ölçüldü

**Kanonda açılış ve kapanış hiçbir yerde tarif edilmemişti.** Tarama:
`clara.md`'nin 15 bölüm başlığında ne açılış ne kapanış var; kelime olarak yalnız dört
yerde geçiyor ve hiçbiri oturum düzeniyle ilgili değil.

`CLA-WRITE-BEFORE-CLOSE` vardı ama o **"ne zaman yaz"** kuralı, *"oturum nasıl
açılır/kapanır"* değil. Yani bir refleks vardı, bir prosedür yoktu.

**Ve boşluğun bedeli 2026-08-07 gecesinde görüldü:** gece boyunca dört agent'la iş
yürütüldü, sonuç commit'lendi, ama sabah yeni bir oturum açılsa **konuşma geçmişi
olmadan hiçbir şeyi bilemezdi.** Kapanış dokümanı o gece **elle** yazıldı çünkü Mert
istedi — kural olsaydı kendiliğinden yazılırdı.

## Açılış — üç adım

`project_durum.md` (hafızada, tek satırlık işaret) → kapanış dokümanı
(`gunluk/{tarih}-kapanis.md`) → kanal canlılığı.

**Üçüncü adımın gerekçesi ölçülmüş:** oturum kapanınca `Monitor` task'ı gidiyor ama
dizin duruyor, `DURUM.md` `ACIK` yazıyor, mesajlar yerinde — **hiçbir şey arızalı
görünmüyor.** PAM bunu 2026-08-07'de ölçtü ve *"yeni oturumda agent monitörünün de açık
olduğunu sanabilir"* dedi.

**Ve bir uyarı yazıldı:** `PID` canlılık kanıtı değil. `kill -0` taraması çalışan bir
agent'ı (PQA) **ölü** gösterdi, o anda rapor yazıyordu. Mekanizma yeniden ölçülmeden ölü
kanal temizliği yapılmaz.

**Yapılmayacak şey de yazıldı:** açılışta işe başlamak. Kapanış dokümanı okunmadan
alınan karar, önceki oturumun kararını bilmeden alınmış olur.

## Kapanış — beş adım

Kalıcı olanı yaz → kapanış dokümanı → hafıza temizliği → görev listesi → commit.

**Kapanış dokümanının beş bölümü:** ne bitti (commit hash'leriyle) · ne yarım kaldı ·
Mert'in kararını bekleyen · ölçüldü ama çözülmedi · bir sonraki hareket.

**Ölçütü:** yeni oturum bunu okuyup **çalışmaya başlayabilmeli.** Konuşma geçmişi
gerekmemeli.

**Ve kimin için yazıldığı yazıldı:** sonraki oturum için, Mert için değil. Mert
konuşmayı hatırlıyor; sonraki oturum hatırlamıyor. Bu ayrım dokümanın içeriğini
belirliyor — Mert'e özet gerekmez, sonraki oturuma bağlam gerekir.

## Hafıza şişmesi — ölçüldü ve kanonla çelişiyordu

**Ölçüm (2026-08-07):** 23 dosya / 943 satır. En büyük dosya
`project_sprint_3_kanal_kurulumu.md` — **149 satır**, ve içeriğinin çoğu **bitmiş** işi
anlatıyordu. Üç `project` kaydı toplam **260 satır**, yani hafızanın **%28'i**
tamamlanmış işlerin ayrıntısı.

**Ve kanonun kendi kuralıyla çelişiyordu:** *"İş hakkında olan dosyaya gider"* diyor.
Üç `project` kaydı o kuralın ihlaliydi — Clara kendi kuralını uygulamıyordu.

**Kural: `user` ve `feedback` kalıcı, `project` geçici.**

Ayrım pratik: `user`/`feedback` iş bitince değer kaybetmez (Mert'in nasıl çalıştığı,
düzeltilmesi gereken bir davranış). `project` iş bitince değeri düşer ve **silinir** —
ayrıntı zaten günlükte, `HARITA.md`'de, `kararlar/` altında.

**Ölçüt:** *bu kaydı silsem iki ay sonra bir şeyi bilemez miyim?* Hayırsa sil. Evetse o
kayıt `project` değil; tipini düzelt.

## Uygulandı — ve silmeden önce kontrol edildi

Üç `project` kaydı silindi (260 → 25 satır, tek `project_durum.md`). Hafıza 943 → 796
satır.

**Körlemesine silinmedi.** İçerik kontrol edildi:
- preload arızası (`#25834`) → kanonda ve hook'ta zaten var
- agent'ın kendi frontmatter'ını görmemesi → kanonda var
- monitör kurulum şartları → `kanal-kurulumu` skill'inde var
- **tek kayıp riski:** *"kanal altyapısı Clara'nın, içerik Mert'in"* yetki ayrımı —
  yalnız `MEMORY.md`'deydi, `kanal-kurulumu` skill'ine taşındı

## Kabul edilen bir maliyet

`MEMORY.md` 24 → 37 satıra çıktı. Konu başlıkları eklendi (Mert / nasıl konuşulur /
ölçüm disiplini / agent'larla çalışma) ve o başlıklar yer tutuyor.

İndeks her oturumda yükleniyor, yani 13 satır bir bedel. Karşılığı: 22 kayıt düz liste
hâlinde aranamıyordu. Bedel Mert'e bildirildi.
