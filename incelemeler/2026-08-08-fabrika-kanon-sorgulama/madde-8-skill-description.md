# Madde 8 — Skill description ve içerik güncelliği

**Tarih:** 2026-08-08, 13:11
**Ölçen:** PAD (fabrika uygulamacısı)
**Doğrulayan:** Clara (bağımsız, beyana dayanmadan)

---

## Bu ölçüm neden ayrı bir şey ölçtü

Madde 7 (davranış testi) kanonu **elle okutarak** ölçtü: dosyaları verdim,
durum sordum, 16/16 çıktı. Ama o test bir şeyi varsayıyordu — **skill'in
açıldığını.**

Madde 8 tam o varsayımı ölçtü: skill kendiliğinden açılıyor mu? Ve cevap
**hayır** çıktı. İki ölçüm birlikte okunmalı:

- Kanonun **içeriği** doğru davranış üretiyor (madde 7).
- Kanonun **tetiklenmesi** bir yerde kırık (madde 8).

İkincisi olmadan birincisi sahada işe yaramaz.

---

## Yöntem — neden güvenilir

PAD description'ları okuyup *"iyi görünüyor"* demedi. Temiz bir yardımcıya
**yalnız ad + description** verdi (gövde vermeden, çünkü ölçülen şey tetiklenme)
ve sekiz gerçek durum sordu.

Bu doğru ayrım: gövdeyi verseydi ölçülen şey tetiklenme değil anlaşılırlık
olurdu.

**Taranan:** beş skill (behavior 586 · dagitim 416 · is-duzeni 749 · uretim 367 ·
yapi-taslari 513) + iki reference. Sayı o an sayıldı, taşınmadı.

---

## Bulgu 1 — `is-duzeni` description'ı eskimiş (en ciddi)

**Test:** *"Oturumun yeni açıldı, kanal kutunu kurman gerekiyor"* → yardımcı
**"hiçbiri"** dedi.

Oysa `ISD-OPEN-YOUR-BOX` dün `is-duzeni`'ne girdi ve tam o durumu tarif ediyor.

**Doğrulama (Clara, bağımsız):** description'da `kanal` yok · `kutu` yok ·
`açılış` yok · `izleyici` yok. Dördü de yok. Gövdede var, description'da yok.

**Daha ağır olan ikinci sonuç:** yardımcı boşluğu **başka bir skill'le** doldurdu
— *"bu iş `kanal-kurulumu` skill'inin alanı"* dedi. O skill Clara'nın kişisel
alanında; **fabrikada yok.** Yani agent yalnız açmıyor değil, olmayan bir yere
gidiyor.

**Sınıfı:** `ISD-CASCADE-COVERS-DESCRIPTIONS`'ın tarif ettiği durumun ta kendisi
— hüküm değişti, onu tarif eden yer değişmedi. Cascade yarım kaldı.

**Bedeli somut:** kanal kurulmazsa iş hiç gelmez.

---

## Bulgu 2 — `behavior` description'ı eksik kaldı

**Test:** *"İşe başladın, adımlarını çıkarıp görev listesi yapacaksın"* →
behavior seçildi, **ama gerekçesi genel maddeydi** ("bir işe başlarken").
`BHV-LIST-BEFORE-RUNNING` görünmedi.

**Doğrulama (Clara):** description'da `görev listesi` yok · `adım` yok ·
`ölçüm` yok · `okuma` yok.

Dün behavior'a **beş** yeni kimlik girdi (`BHV-LIST-BEFORE-RUNNING`,
`BHV-LIST-HOLDS-WORK-ONLY`, `BHV-READ-TO-CLOSE`, `BHV-DONT-AIM-AT-LAST-MISS`,
`BHV-DATE-THE-MEASUREMENT`) ve description hiçbirini anmıyor.

**Neden bulgu, madem doğru skill açıldı:** PAD'in kendi cümlesi — *"doğru skill
açıldı ama YANLIŞ SEBEPLE."* Tetiklenme tesadüfi. *"Bir işe başlarken"* çok geniş
olduğu için bu kez tuttu; daha dar bir durumda tutmayabilir.

---

## Bulgu 3 — `yapi-taslari`'nda bir cümle artık yanıltıcı

Satır 153-155: *"Son maddeye dikkat: o yalnız `Task` ile çağrılan sub-agent'ta
geçerli."*

Cümle **mekanik olarak doğru** — preload `Task` yolunda gerçekten çalışıyor. Ama
`Task` bu ekipte artık kullanılmıyor (dün kaldırıldı). Okuyan *"demek `Task`'la
çağrılınca preload çalışıyor, o yolu kullanabilirim"* diye okuyabilir.

**Karar: silinmez, şerh eklenir.** Olgu değişmedi; değişen şey bizim o yolu
kullanmamız. Silmek doğru bir mekanik bilgiyi kaybettirir.

---

## Bulgu 4 — Çakışma var ama zararsız (değişiklik önerilmedi)

`uretim` ve `yapi-taslari` description'ları beş anahtar ifadeyi paylaşıyor:
katman · üretil · kural · hook · skill.

**Ama testte arıza üretmedi.** İki durumda da yardımcı ikisini birden seçti ve
gerekçesi doğruydu: *"uretim kanonu verir, yapi-taslari sınır değerini."*

**Sınıfı:** belirsizlik değil **tamamlayıcılık**. Ayırmaya çalışmak ikisinden
birini yanlış durumda kapatır. Dokunulmadı.

---

## Sorunsuz

`dagitim` — tetiklenmesi net, içeriği güncel, çakışması yok.

**İçerik güncelliği genel tarama:** eski kimlik izi sıfır, *"Task ile çağırır"*
izi sıfır, *"kesin cevap tarama"* izi sıfır. Dün kapatılan cascade'ler skill'lerde
temiz — Bulgu 3 dışında.

---

## Ölçümün sınırı (PAD kendi yazdı)

**Ölçülmeyen:** iki reference'ın içerik güncelliği (`kanal.md` dün yazıldı,
`arac-envanteri.md` dün iki kez düzeltildi — ikisi de taze ama tam okunmadı).

**Clara'nın eklediği sınır:** bu ölçüm yalnız beş skill'in description'ını
kapsıyor. Fabrikanın ürettiği takımların (`team/` altı) skill'leri taranmadı.
