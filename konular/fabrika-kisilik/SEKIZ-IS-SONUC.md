# Sekiz iş — sonuç · 2026-08-24 07:13

Denetim bulgularından çıkan sekiz iş, sekizi de kapandı. FPA→FPD→FQA zinciri
sekiz tur koştu; Clara her turda `git log` ile ölçüp sıradakini verdi.

| # | İş | Kayıt |
|---|---|---|
| 1 | `uretim` gövde standardı: dört parça → **altı grup** | `873d85c` |
| 2 | Gövdelerde kalan saflık ihlalleri | `462af8d` |
| 3 | Üç gövde altı gruplu standarda uyduruldu | `43f535a` |
| 4 | `docs/isler` → `docs/tasks` (metin + disk) | `ef9c90d` |
| 5 | İki kırık atıf kapandı | `d7f0d99` |
| 6 | `fabrika-davranis` vaka fazlalığı + boşluk | `4a73ea1` |
| 7 | Bakılmamış eksenler — dört bulgu | `9956c48` |
| 8 | FPD gövdesinde üç şüpheli madde | `8acf558` |

---

## Listede olmayan ama en değerli kazanç: SINAMA ZAMANI

**Kanona girdi:** *"Sınama denetimden önce gelir — üretimin son adımıdır."*

Sebebi ölçüldü:
```
dün gece:  kural yazıldı, gövdelere UYGULANMADI
           → ilk denetimde YEDİ satır kaçtı
           → biri kuralın KENDİ yasak örneğiydi, üç temizlik turundan geçmişti

bugün:     standart yazıldı, AYNI TURDA sınandı
           → sınama bir belirsizlik buldu, sahaya İNMEDİ
```

**Ve üç kez kendini kanıtladı:**
- Sınama kuralının kendisi yazıldı, kendi hükmüne uyarak sınandı, sınama **o
  kuralın kendi eksiğini** buldu (dört mekanik boşluk)
- İş 2'de beş kalemi kapatan iş, kapatırken **üç tekrar üretti** ve aynı turda
  yakalandı — bir tur önce bu sınıf denetime kalıyordu
- İş 7'de kapatan el, kapattığı bulgunun **aynı sınıfını üretti ve kendi
  yakaladı** (`6c507d5`)

---

## Kanona giren diğer ölçütler

**Gövde bir sonuçtur** — yorum, analiz, gerekçe, risk uyarısı gövdede yaşamaz.
Ayırt edici soru: ***"okuyan agent bunu kendisi hakkında ne sanır?"***
⚠️ *"Bu cümle zamanla yanlış olur mu"* DEĞİL — gövdeye yazılan teşhis hiç
bayatlamayabilir, her oturumda agent'a kendini eksik tanıtır.

**Hâl / koşul ölçütü** (`uretim:116`):
```
Hâl bildirimi   "hatanı yakalayacak kimse yok"  → sürekli durum   → DÜŞER
Koşullu durum   "bir bulgu reddedildiğinde"     → olay + davranış → KALIR
```

**Özne ölçüsü bir muafiyet, ayırt edici soru bir yer tayini** — FQA'nın ayrımı.
Aynı sonuca varsalar da ikincisi bir **yer** söylüyor.

**Sıklık ifadeleri koşul değildir** (`af3ea6f`).

---

## Mert'in bu gece verdiği kararlar

- **Vizyon kalsın, korkuya gerek yok** — korku yarısı *"gövdede risk uyarısı
  yaşamaz"* kuralıyla kesişiyordu; gerilim vizyonu daraltarak çözüldü
- **`tasks` olsun, `isler` olmasın** — dizin çelişkisinin yönü
- **Sıraya al, bitti dedikçe ver** — sekiz işin akış biçimi
- **Yayın yok** — *"sürüme tam ikna olmadan yayına çıkarmam"*

---

## Clara'nın bu gece yaptığı ölçüm hataları — hepsi aynı sınıf

**Bir işarete bakıp içine bakmamak.**

| # | Ne yaptım | Doğrusu |
|---|---|---|
| 1 | *"commit yok = iş başlamamış"* | okuma da iş, commit üretmez |
| 2 | *"rapor dosyası var = iş bitmiş"* | rapor turun fotoğrafı, zincirin hâli değil |
| 3 | *"commit mesajı 'kapandı' diyor = kapandı"* | **hedefe bak, mesaja değil** — benzer kelimeler, farklı arıza |
| 4 | 48 satıra bakıp *"bölünsün"* önerdim | **önce kes, sonra ölç** — kesilmemiş sayıya bakarak karar verilmez |

⚠️ Dördü de kendi kanonumda yazılı olanın ihlali: *"sayı bir işarettir, hüküm
değil"* ve *"bir şeyin sonucunu, o şey bitmeden okumazsın."*

**FPA'nın verdiği ölçü kanona geçmeli:** *"kapandı denen şeyin hedefine bak,
commit mesajına değil."*

---

## FPA'nın bana yönelttiği eleştiri — kabul

> *"Bir dersi üç yerde çıkarmak onu kanona yazmak değil."*

Sınama dersi bir gün içinde **dört ayrı yerde** yaşadı (iş emri, iki devir bloğu,
denetim) ve hiçbirinde yürürlükte değildi. Ben üçünde tespit ettim, hiçbirinde
kanona yazdırmadım.

⚠️ Gövdemde yazılı olanın ihlali: *"sebebi ararsın, üstüne kontrol koymazsın."*

---

## Bir sonraki oturuma kalanlar

- **`uretim` bölme** (466 satır) — bugün sekiz kez değişti, **hareket eden şey
  bölünmez**
- **`uretim` vaka fazlalığı** (7 vaka izi, `fabrika-davranis`'ın 1.4 katı)
- **"Desen oluştuysa söyle" bölümünde eşik yok** — sayı yazmak kanonda yasak ama
  eşiksiz desen tanımı uygulanamıyor. ⚠️ **Bu bana da bakıyor:** bugün üç kez
  *"bu bir desen"* dedim ve ölçüm yazılı değildi
- **Yayın** — bu gecenin tüm değişiklikleri yayınlanmayı bekliyor (Mert'in kararı)
- **`~/.claude/skills/` altındaki diğer skiller taranmadı** — altı grup kavramını
  taşıyabilirler
