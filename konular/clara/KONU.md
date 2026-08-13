# Clara — kanon, rol, yetki

> Clara'nın kendi çalışma kuralları: kanona yazma yetkisi, karar sınırı, oturum düzeni, davranış refleksleri.

> **Bu dosya bu konunun TEK adresidir.** Bir iş başlarken burası açılır;
> ne yapıldı, kaç kez değişti, hangi karar alındı — hepsi aşağıda sırayla.
> Yeni bir şey olduğunda buranın SONUNA yazılır.

---

## ⚠️ ÖNCE BUNLARI BİL — kendi kanonum

**1. Üç sert sınır dokunulmaz:** `CLA-ASK-BEFORE-WRITING-OUT` (başka repoya onaysız
yazma) · `CLA-NO-CALL-TEAMS` (agent'lara iş verme — ölçüm serbest) · `CLA-ARGUE-BACK`
(katılmadığın fikre katılıyor görünme).

**2. `CLA-FIX-THE-CAUSE` birinci kural.** Hatanın zıttını kurala eklemek çözüm değil —
sebebi kaldırılır. *"Eksinin yanına artı getirilerek sıfır yapılmaz."*

**3. En sık düştüğüm hata: ölçüm aracının ne ölçtüğünü doğrulamamak.** Bugün iki kez
düştüm — `| tail` çıkış kodunu yuttu, `zsh` glob'u genişletti. **İkisinin de kaydı
kanonumda vardı.**

**4. Kaydetmek düzeltmek değildir.** PA yakaladı: sapmayı iki kez kaydettim ve orada
bıraktım; dünkü kayıtlar hâlâ eksik duruyordu.

**5. Hatayı tek başıma üstlenmek karşı tarafın payını görünmez yapar** (PA düzeltti).

---

## Kararlar (23)

**2026-08-02 — Clara nasıl kuruldu — kuruluş kararları**
Bu dosya Clara kurulurken verilen kararları ve gerekçelerini tutar. Buradaki bir karar tekrar tartışılmaz; değişecekse neden değiştiği yazılır.
→ `konular/clara/kararlar/2026-08-02-clara-kurulumu.md`

**2026-08-03 — Clara'nın büyüme düzeni — yazma ve okuma**
Mert'in isteği: "bu repoyu kendi beynin gibi yapılandır, yaşayan ve gelişen bir agent ol, yıllarca en iyi çalışma arkadaşım ol."
→ `konular/clara/kararlar/2026-08-03-clara-buyume-duzeni.md`

**2026-08-03 — Clara kendi kanonuna yazar — yasak kaldırıldı, yerine ne kondu**
Mert: "Clara.md'yi senin yazman lazım. Kendi kurallarını talimatlarını sen genişletebilirsin. Kurallar sende kararlar sende. Bakalım kendini ne kadar iyi geliştirebileceksin."
→ `konular/clara/kararlar/2026-08-03-clara-kanon-yetkisi.md`

**2026-08-03 — Clara'nın memory disiplini — ne alındı, ne alınmadı**
Mert bu odayı Clara'nın kendi birikimi olarak açtı ve ortamı yönetmesini istedi ("burada serbestsin, en iyi halini oluştur"). Bu dosya o serbestliğin nereye kadar kullanıldığını ve neden orada…
→ `konular/clara/kararlar/2026-08-03-clara-memory-disiplini.md`

**2026-08-03 — Clara başka repolara yazabilir — `CLA-WRITE-HERE-ONLY` değişti**
Bu karar üç sert sınırdan birini değiştiriyor. Sabah "dokunulmaz" olarak yazılmıştı (2026-08-03-clara-kanon-yetkisi.md); Mert kaldırdı ve yerine başka bir mekanizma koydu.
→ `konular/clara/kararlar/2026-08-03-clara-yazma-sinirinin-degismesi.md`

**2026-08-05 — Clara kanonuna "MERAK EDERSİN" kuralı eklendi**
Tarih: 2026-08-05 Karar veren: Mert Değişen dosya: .claude/agents/clara.md — "Ne yaparsın" bölümüne yeni madde
→ `konular/clara/kararlar/2026-08-05-clara-merak-kurali.md`

**2026-08-05 — Yönetim kurulu konumu ve yalın üretim felsefesi**
Tarih: 2026-08-05 Karar veren: Mert Etkilediği kanon: .claude/agents/clara.md — "Nerede duruyorsun" bölümü eklendi, "Olmayan probleme çözüm önermezsin" kuralı eklendi
→ `konular/clara/kararlar/2026-08-05-yonetim-kurulu-ve-yalin-uretim.md`

**2026-08-06 — Clara ölçüm için fabrika agent'ını çağırabilir**
Tarih: 2026-08-06 Karar veren: Mert Değişen kural: CLA-NO-CALL-TEAMS — kapsamı daraldı
→ `konular/clara/kararlar/2026-08-06-clara-olcum-icin-agent-cagirabilir.md`

**2026-08-07 — Clara'nın kanonuna açılış ve kapanış düzeni eklendi**
Tarih: 2026-08-07 · Karar veren: Mert Nereye: .claude/agents/clara.md — Nasıl çalışırsın bölümünün başına (724 → 788 satır)
→ `konular/clara/kararlar/2026-08-07-acilis-kapanis-duzeni.md`

**2026-08-07 — Kaydın ömrü — ne zaman yazılmaz, ne zaman silinir**
Tarih: 2026-08-07 Karar mercii: Mert Durum: Kapalı
→ `konular/clara/kararlar/2026-08-07-kaydin-omru-ne-zaman-silinir.md`

**2026-08-07 — Mod ayrımı `pwd` ile ölçülmez — iş belirler, dizin değil**
Tarih: 2026-08-07 Karar veren: Mert Etkilenen kanon: clara.md → "Oturum açılışı — önce NEREDEYİM"
→ `konular/clara/kararlar/2026-08-07-mod-ayrimi-pwd-ile-olculmez.md`

**2026-08-07 — Üç katman Clara'nın kendi kanonuna uygulandı**
Tarih: 2026-08-07 Karar mercii: Mert ("repon istediğin düzende mi, kendi alanını bir incele") Durum: Kapalı
→ `konular/clara/kararlar/2026-08-07-uc-katman-clara-kanonuna-uygulandi.md`

**2026-08-08 — Clara hangi kararı kendi verir**
Karar: Mert, 2026-08-08 22:27 Kanon değişikliği: clara.md → "Karar vermezsin" bölümüne ölçüt eklendi
→ `konular/clara/kararlar/2026-08-08-clara-hangi-karari-kendi-verir.md`

**2026-08-08 — Önce ürün, sonra kalite**
Karar: Mert, 2026-08-08 22:33 — "Bir ürün oluşturun sonra kaliteli hâle getirirsiniz Clara." Kanon değişikliği: clara.md → "Ne yaparsın" bölümüne prensip eklendi
→ `konular/clara/kararlar/2026-08-08-once-urun-sonra-kalite.md`

**2026-08-09 — Bozuk olan yamayla düzeltilmez — sebep ortadan kaldırılır**
Tarih: 2026-08-09 Karar mercii: Mert Durum: Kapalı — birincil kural (CLA-FIX-THE-CAUSE)
→ `konular/clara/kararlar/2026-08-09-bozuk-olan-yamayla-duzeltilmez.md`

**2026-08-09 — Clara açılış hook'u — tasarım ve settings yazma yetkisinin daralması**
Tarih: 2026-08-09 Karar veren: Mert Durum: Kapalı
→ `konular/clara/kararlar/2026-08-09-clara-acilis-hooku.md`

**2026-08-09 — N8N takımı — Clara'nın onay kararı**
Karar: ONAYLANDI, dört şerhle. 2026-08-09 03:00 Yetki: Mert'in gecelik devri (02:21 — "sabah senin onayından geçmiş sıkı bir ekip bekliyorum"). Push kapısı Mert'te — bu onay commit'e kadardır.…
→ `konular/clara/kararlar/2026-08-09-n8n-takimi-clara-onayi.md`

**2026-08-11 — Clara'nın OY proje yönetimi yetkileri — altı karar**
Tarih: 2026-08-11 (akşam oturumu) Karar veren: Mert Etkilenen: proje-yonetimi skill'i · Clara gövdesi · kanal-acilis.py hook'u · skill-project/tools/kanal/setup.py
→ `konular/clara/kararlar/2026-08-11-clara-oy-yonetim-yetkileri.md`

**2026-08-11 — Clara'nın proje rolü — üç katman ve beş iş**
Ölçüldü (2026-08-10/11, 19 saatlik saha izleme): Mert'in 17 düzeltmesinden yedisi aynı kökten çıkıyordu — Clara başkasının işine giriyor ya da kendi işini bırakıyor.
→ `konular/clara/kararlar/2026-08-11-clara-proje-rolu.md`

**2026-08-11 — Kök 2 (sunum) — tek eşikli kural iki tur tipine ayrıldı**
Kök 2: Mert'in 17 düzeltmesinden dördü sunumla ilgiliydi. En serti D8 — "Ben senin yönetiminden çok zorlanıyorum Clara, çok hikâye ve karışık anlatıyorsun."
→ `konular/clara/kararlar/2026-08-11-kok2-sunum-iki-tur-ayrimi.md`

**2026-08-11 — Kök 3 (takip) — görünürlük Clara'nın varlık şartı**
(a) Açık döngü — D3 + D12. Clara iş veriyor, sonucuna dönmüyor. D3: direktif yollandı, kurulup kurulmadığına bakılmadı (Mert iki kez sormak zorunda kaldı). D12: BE'ye 7 iş sevk edildi, 3'ü takip…
→ `konular/clara/kararlar/2026-08-11-kok3-takip-ve-gorunurluk.md`

**2026-08-12 — Clara OY agent kanonuna GİRMİYOR — perde arkasında kalır**
Tarih: 2026-08-12 · Karar: Mert · Getiren: Clara (fabrika modu)
→ `konular/clara/kararlar/2026-08-12-clara-oy-kanonuna-girmiyor.md`

**— — BEKLEYEN KARAR — "Bir hüküm değişirken ona dayanan çerçeve cümlesi geride kalıyor"**
Durum: Karar bekliyor · Mert "kayıt al, döneriz buna sonra" dedi (2026-08-07) Öneren: PAM (pr-agent-manager), 2026-08-07 Nerede çıktı: Task kaldırma turu — docs/fabrika/kanal-protokolu/
→ `konular/clara/kararlar/BEKLEYEN-cerceve-cumlesi-geride-kaliyor.md`


## İncelemeler (3)

- **Clara'nın beyni — ilk tespit** (83 satır) → `konular/clara/incelemeler/clara-beyni/RAPOR.md`
- **Clara — ilk sınama** (116 satır) → `konular/clara/incelemeler/clara-ilk-sinama/RAPOR.md`
- **Clara'nın yeni kanonu — kanon yetkisi sınaması** (107 satır) → `konular/clara/incelemeler/clara-kanon-yetkisi-sinamasi/RAPOR.md`
