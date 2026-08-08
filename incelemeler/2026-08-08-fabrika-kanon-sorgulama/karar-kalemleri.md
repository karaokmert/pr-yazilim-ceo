# Karar kalemleri — Mert'e sunulacak

**Tarih:** 2026-08-08
**Durum:** sekiz maddenin hepsi ölçüldü. Aşağıdakiler **karar bekliyor**;
hiçbiri uygulanmadı.

Kararı veren Mert. Her kalemde: ne bulundu · neden önemli · seçenekler ·
Clara'nın görüşü.

---

## KALEM 1 — Atıf sahipliği boşluğu (bugün dört kez arıza üretti)

**Ne bulundu:** `rules-index.json`'daki atıf listelerini kimin güncelleyeceği
kanonda tanımsız.

`PAD-SYNC-INDEX` yalnız **kimlik** üretimini bağlıyor ("bir kimlik ürettiğin ya
da değiştirdiğin turda"). Ama bir dosya **atıf** ürettiğinde — yani mevcut bir
kimliği andığında — hiçbir hüküm devreye girmiyor.

PAM bir katman derinleştirdi: index'in kendi şeması denetimde atıf güncelliğini
**arıyor**, ama hiçbir hüküm onu bir role **bağlamıyor.** Sonuç: denetçi eksik
atıf bulduğunda kimin ihlali olduğunu gösteremiyor.

**Neden önemli:** bugün aynı yapısal noktadan **dört** ayrı arıza doğdu:

1. **Zamanlama** — ölçüm PAM'in commit'inden önce koştu
2. **Kapsam** — dar tarama (Clara yalnız not bölümüne baktı)
3. **Sahiplik** — PAM atıf üretti, index'e yazamıyor (PQA Bulgu 14)
4. **Commit'lenmemişlik** — dosya diskte değişti, git'e girmedi (PQA Bulgu 15)

Dördü de aynı yerden: **index ile kaynak arasında tetik yok** — ne rolde, ne
zamanda, ne araçta.

**Seçenekler:**

- **A** — `PAD-SYNC-INDEX`'in kapsamını genişlet: "kimlik ya da atıf ürettiğin
  turda". Sorun: `docs/` yazan PAM index'e yazamaz, yani PAD'in başkasının
  ürettiği atfı takip etmesi gerekir.
- **B** — `docs/` yazanına dar bir index yetkisi ver (yalnız `atif_verenler`
  alanı). **PAM bu seçeneği kendi lehine olduğu için önermedi ve bunu beyan etti.**
- **C** — Mekanik çözüm: atıf listesini bir script üretsin, elle tutulmasın.
  İndeks zaten türev bir dosya.

**Clara'nın görüşü:** C. Sebep — bu bir yetki sorunu gibi görünüyor ama aslında
bir **elle senkron** sorunu. Dört arızanın dördü de "kim yapacak" sorusundan
değil, "birinin yapması gerekiyor ve unutuluyor" durumundan doğdu. Türetilebilen
bir şeyi elle taşımak, kanonun kendi kuralına (`ISD-CLOSE-WITH-IDENTITIES`)
aykırı: *"türetilebilen bir şeyi elle taşımak, elle taşınan her şey gibi, bir gün
yanlış taşınır."*

Gereksinim kalemi zaten açık: `docs/fabrika/atif-sahipligi/gereksinim.md` (8b7fa20).

---

## KALEM 2 — Cascade işinin tetikleyicisi yok

**Ne bulundu:** *"Bir kuralı değiştirdin, etkilenen yerleri bul"* durumunda
**hiçbir skill açılmıyor.** PAD ölçtü, temiz yardımcı "hiçbiri" dedi.

Yardımcının cümlesi: *"en yakını `uretim` ama o ÜRETİM ANINA bakıyor, değişiklik
sonrası YAYILIMA değil. Tetikleyici yoksa kural pratikte yok."*

**Neden önemli:** cascade kanonun en çok işlenen konusu — `BHV-READ-TO-CLOSE`,
`ISD-CASCADE-IN-ONE-TURN`, `ISD-CASCADE-COVERS-DESCRIPTIONS` ve `PAD-CASCADE-SAME-TURN`
hepsi bunu tarif ediyor. Ama o kuralları taşıyan skill'lerin hiçbiri o **anda**
açılmıyor.

**Seçenekler:** `behavior`'a eklemek (`BHV-READ-TO-CLOSE` orada) · `is-duzeni`'ne
eklemek (`ISD-CASCADE-*` orada) · ikisine birden (çakışma riski).

**Clara'nın görüşü:** düzeltilmeli ama **bu push'tan sonra.** Bugün üç commit
zinciri açık ve yeni bir kanon değişikliği push kapsamını büyütür.

---

## KALEM 3 — Aynı cümle iki yerde (tekrar)

**Ne bulundu:** `BHV-SCAN-FIRST` ile `uretim`'in "İhtiyaç doğrulaması" adımı
**kelimesi kelimesine aynı cümleyi** taşıyor:

> "Bu taramanın/adımın en sık sonucu şudur: ihtiyaç yok, mevcut bir kural zaten
> kapsıyor."

PCA buldu, Clara okurken bağımsız olarak da çıktı.

**Neden önemli:** `URT-NO-DUPLICATE-ID`'nin tarif ettiği durumun kendisi. Şu an
ayrışmamışlar; ayrışma zamanla gelir ve o zaman hangisinin geçerli olduğu
belirsizleşir.

**Clara'nın görüşü:** biri kalmalı, diğeri atıf vermeli. Hangisinin kalacağı
katman kararı — PAD'in alanı.

---

## KALEM 4 — Kanonun ağırlığı işin ağırlığını yansıtmıyor

**Ne bulundu (PAM):** `DAG` 26 kural — dört rolün kendi kurallarının **toplamının
bir buçuk katı** (PAD 6 + PQA 4 + PCA 4 + PAM 3 = 17).

Ve sayıyı içerikle sınadı: `team/` altında tek klasör var ve **içi boş**.
Yani 26 kural **henüz hiç yapılmamış** bir iş için yazılmış.

Tersi de doğru: bugün yapılan iş dağıtım değildi. 21 iş klasörünün hepsi kanon
bakımı, ölçüm, rol sınırı, cascade, kanal.

**Clara'nın görüşü:** bu bir "sil" kalemi değil — ölçülmemiş kural silinmez ve
DAG kuralları ilk takım paketlendiğinde lazım olacak. Ama bir **uyarı**: kanon
yapılmayan işi ayrıntılı, yapılan işi kaba tarif ediyor. İlk takım paketlendiğinde
DAG'ın 26 kuralının kaçının gerçekten tuttuğu ölçülmeli.

---

## KALEM 5 — PCA'nın yeni işlevi kanonda tanımsız

**Ne bulundu (PAM):** Mert dün *"PCA bütünsel tarar, her turda iş ona gitmez"*
dedi. Ama bu yeni işlev kanonda yok: **ne zaman koşar, kapsamını kim çizer,
çıktısı nereye gider** — dördü de yazılı değil.

Bugün PCA iki bütünsel tarama yaptı ve **ikisi de merkezin talebiyle** oldu,
kuralla değil.

**Clara'nın görüşü:** gerçek boşluk. Bir işlev kuralla değil taleple koşuyorsa,
talep eden olmadığı gün koşmaz — ve koşmadığı fark edilmez.

---

## KALEM 6 — İki küçük tutarsızlık (PCA)

**PAM body'sinde devir bölümü yalnız "verdiklerini" sayıyor.** Aldığı üç kalem
(PCA bulgusu, PQA raporu, kapanış bildirimi) o bölümde yok — diğer üç body'de
"Alırsın/Verirsin" çiftinin ikisi de var.

**Devir bölümü üç farklı biçimde yazılmış:** PCA+PQA etiketli çift, PAD düz
paragraf, PAM yalnız verme yönü. PCA bunun Bulgu D'nin **sebebi** olabileceğini
söyledi ama korelasyon ölçmediğini de yazdı.

---

## KALEM 7 — Üç kural tek ölçüme dayanıyor (izleme kalemi, karar değil)

`BHV-READ-TO-CLOSE` · `ISD-RETURN-TO-PLANNER` · `ISD-CASCADE-COVERS-DESCRIPTIONS`
— üçü de tek ölçümden doğdu, üçü de **aynı gün aynı işten** (2026-08-07 cascade
işi), ve üçü de bunu kendi gövdesinde yazıyor.

PAM davranışsal bir ölçüm yaptı: atıf sayıları 12, 7, 7 — eski ve çok kullanılan
`BHV-SCAN-FIRST` yalnız 2 atıf alıyor. Yani bir günde birçok eski kuraldan fazla
anılmışlar; bir **olay** kodlayan kural böyle davranmaz.

**Ama PAM kanıtının zayıflığını da yazdı:** atıfların çoğu aynı günün iş
dosyalarından geliyor, yani *"olay hâlâ tazeyken çok anıldı"* da aynı sonucu
verir. Ayırt edici ölçüm: **bir hafta sonra tekrar bakmak.**

**Clara'nın görüşü:** karar gerekmiyor. Takvime bir hatırlatma: 2026-08-15'te
bu üç kuralın atıf sayısına yeniden bakılsın.
