# Gereksinim taslağı — denetim kaydı

**Denetleyen:** isimsiz `general-purpose` yardımcı (adversaryal görev: kusur bul)
**Tarih:** 2026-08-09 · **Denetlenen:** `gereksinim-taslagi.md` ilk sürüm

Bu odada ikinci göz yok; denetim bu yüzden dışarıdan istendi. Bulgular ham hâliyle
kaydedildi, altısı da işlendi.

---

## Temiz çıkan — atıf disiplini

**Kırık atıf yok.** 14 birincil yol doğrulandı. İkincil sayılar da birebir tuttu:
`agent-dogrulama/` 8 dosya, `SONUC-*` 9 rapor, `*-skill-karar.md` 8 dosya,
`*-mekanik.md` 19 taslak.

Ölçüm iddiaları da doğrulandı: 76 skill / 77 reference / 9 rol / backend body 105 satır
(gerçekten dokuz rolün medyanı) ve **üç ölü MCP adresi tam belirtilen satır
numaralarında** — doğru desen kaynakta 0 kez geçiyor. Beş kural kimliği fabrikada
mevcut.

Denetçinin cümlesi: *"ölü atıf sorununu çözmek için yazılmış bir belge olarak kendi
standardını tutturmuş."*

---

## Altı bulgu — hepsi işlendi

**1. Yanlış sayı (fabrika yükü).** Belge *"18 iş klasörü, 17'sinde STATE yok"* diyordu.
Kaynaktan sayıldı: **19 iş klasörü, 18'inde yok.** Düzeltildi.

Denetçinin şerhi kayda değer: *"havuzdaki sayılar kendi içinde denetlenmemiş olabilir"*
diyen bir belge kendi sayısını denetlememiş.

**2. Uydurma alıntı — en ciddi bulgu.** Belge `docs/filo/durum.md`'nin *"Kurulmuş takım:
henüz yok"* dediğini **tırnak içinde** yazmıştı. Dosyada o dizilim yok: `## Kurulmuş
takımlar` başlığı ve ayrı satırda `Henüz yok.` var. Anlam doğruydu, **alıntı uyduruktu.**
Düzeltildi — artık iki parça ayrı ayrı ve doğru gösteriliyor.

**Bu bir hesap hatası değil, mekanizma hatası:** iki satır okunup zihinde birleştirilip
tırnağa alınmış. Ve tam da ölü/yanlış atıfla savaşan bir belgede.

**3. Rol açma ölçütü sahipsizdi.** *"Çıkarılacak"*, *"geçirilecek"* — iki edilgen fiil,
fail yok. Ve PAD kuyruğundaki `uretim-refleksi` işiyle ilişkisi kararsızdı; PAM ya
varsayımla ilerleyecek ya geri dönecekti. Düzeltildi: **ölçütü PAM çıkarır, dokuz
gerçek rolden; `uretim-refleksi` beklenmez, ona girdi devredilir.** Dosya çakışması
olmadığı da yazıldı.

**4. Kabul ölçütünde eşik yoktu — asıl kusur.** Belge *"sahada açıldı"*yı işin en önemli
maddesi ilan edip ölçüm yöntemini `ISD-SCOPE-NOT-METHOD` ile PAD/PCA'ya bırakmıştı.
Denetçinin ayrımı doğru: **yöntemi bırakmak meşru, eşiği bırakmak değil** — eşik kapsam
sorusudur.

Düzeltildi. Eşik sabitlendi: en az üç gerçek iş · preload listesinin tamamı açılmalı ·
"konu geçti, alet açılmadı" vakası sıfır · rapor biçimi *"hangi beklenen skill açılmadı
ve konusu geçti mi"*.

**5. Kapsam dışı çelişkisi.** Üç ölü MCP adresi *"kapsam dışı"* başlığındaydı ama
devamı *"yeniden üretimde zaten doğru yazılacak"* diyordu — yani kapsam içi. PAM başlığı
okuyup adresleri eski hâliyle taşısaydı üç ölü atıf yeni takıma aynen geçerdi.
Düzeltildi: madde **"ne yapılacak"** bölümüne taşındı, kapsam dışında yalnız *"sahadaki
v8'de ayrı onarım işi açılmayacak"* kaldı.

**6. Gereksiz yük.** *"Cevaplanmamış sorular"* altındaki iki madde PAM'in cevaplayacağı
şeyler değil, PCA'nın ölçüm sınırlarıydı — etiket yanlış izlenim veriyordu. Düzeltildi:
ayrı başlık altına alındı (*"Ölçümün bilinen sınırları — cevap beklenmiyor"*).

**Ek not:** `team/team-1-oy` boş yer tutucusu belgede anılmıyordu; eklendi ve
adlandırma kararı PAM'e bırakıldı, *"iki klasör kalmayacak"* şartıyla.

---

## Denetçinin hükmü (ham)

> Bu gereksinimle **PAM işe başlayabilir ama aşama 2'yi kapatamaz** — çünkü atıflar ve
> girdiler eksiksiz doğrulandığından aşama 1 derlemesi bugün başlatılabilir durumda,
> fakat işin "en önemli maddesi" ilan edilen kabul ölçütü geçme eşiği taşımıyor
> (bulgu 4) ve rol açma ölçütünün PAD kuyruğundaki `uretim-refleksi` işiyle ilişkisi
> kararsız bırakılmış (bulgu 3); bu ikisi netleşmeden PAM ya varsayımla ilerler ya
> geri döner.

**İkisi de düzeltildi.**

---

## Ders — kayda geçen

**Kendi belgeni kendin denetleyemiyorsun.** Altı bulgunun ikisi (yanlış sayı, uydurma
alıntı) benim kendi ölçümümdü ve ikisini de yeniden okurken görmedim. Görülmeleri için
*"kusur bul"* diye görevlendirilmiş bir göz gerekti.

**Ve ikisi de aynı sınıftan: kaynağa gidip getirdiğim şeyi yeniden kontrol etmemek.**
Sayıyı bir kez saydım, alıntıyı bir kez okudum, ikisini de doğru sandım. Atıf yollarını
tek tek doğruladım ama **kendi cümlelerimin içindeki veriyi doğrulamadım.**
