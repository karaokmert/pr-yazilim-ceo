# `agent-sinama` skill'ine iki ders eklendi

**Tarih:** 2026-08-10 · **Yazan:** Clara · **Kaynak:** OY pilot rol sınaması (gece
nöbeti, üç koşum)

**Değişen dosya:** `~/.claude/skills/agent-sinama/SKILL.md` — iki yeni bölüm.

---

## Neden yazıldı

Bu gece bir kuralı (`BE-MISSING-TOOL-IS-A-FINDING`) **üç koşumda** ölçmeye çalıştım.
İlk ikisi başarısız oldu ve o başarısızlıklar iki ders üretti — ikisi de skill'de
yoktu.

---

## Ders 1 — "Ölçemediysen kuralı değil senaryoyu düzelt"

**Ne oldu:** Kural iki koşumda tetiklenmedi.

- **Birinci koşum:** verdiğim gereksinim **gerçekten kusurluydu** — fiziksel envanteri
  olmayan ürünlere (eğitim/kredi/set) *"stok durumu"* eklenmesini istemiştim. Agent
  daha erken ve **daha doğru** bir kapıda durdu: *"bir eğitimin 'tükendi' olması ne
  demek?"*
- **İkinci koşum:** bağlam kuralın devreye gireceği anı hiç üretmedi.

**Kolay yol kuralı gevşetmekti** — *"demek ki fazla katıymış"*. O yol ölçümü değil
**ölçütü** bozardı ve bir daha o kuralın çalışıp çalışmadığı sorulamaz hâle gelirdi.

**Yapılan:** üçüncü koşumda **engel kaldırıldı** — gereksinim kusursuz verildi ve
compaction taklit edildi (*"`behavior` context'inden düştü"*). Kural tetiklendi.

**Kural değişmedi; onu ölçülebilir kılan durum kuruldu.**

**Ayıran soru skill'e girdi:** *agent kurala geldi de mi uygulamadı, yoksa hiç gelemedi
mi?*

---

## Ders 2 — "Gerekçeli kural, kapsamadığı durumda da davranış üretiyor"

**Ne oldu:** Kural yalnız *"dur ve bildir"* diyor. Agent durdu, bildirdi — **ve bir
adım öteye gitti:** ürettiği devir bloğunun başına kendi güvenilirlik şerhini koydu.

> *"Şablonun taşıdığı korumaların devreye girdiğini iddia edemem... blok tamsa şans
> eseri tamdır."*

**Bunu kural yazmıyor.** Agent, kuralın **gerekçesini** (*"harita bir vaattir,
tutmuyorsa elinde kanon yok demektir"*) yeni bir duruma taşıdı.

**Bu bulguyu PAD çıkardı**, ben değil — ve `URT-GIVE-REASON`'ın ölçülmüş getirisi
olarak adlandırdı.

**Sonucu okuma biçimi skill'e girdi:** hükmü uygulamak *geçti* demektir; **gerekçeyi
yeni bir yerde kullanmak kuralın öğrenildiği** demektir. İkincisi ezberle
karıştırılamaz — çünkü ezberlenecek bir metin yok.

---

## Neden bu iki ders skill'e girdi, günlükte kalmadı

`agent-sinama` bir **yöntem** skill'i ve ikisi de yöntem hükmü:

- Birincisi bir **sınama tasarımı** kuralı — her sınamada geçerli, bu vakaya özel değil
- İkincisi bir **sonuç okuma** ölçütü — skill'de zaten *"sonuç nasıl okunur"* bölümü
  vardı, bu onun eksik kalan yarısıydı

**Vaka ayrıntısı skill'e girmedi**, yalnız kuralın gerekçesi olarak tek cümlelik atıf
kaldı. Ham kayıt: `gunluk/fabrika/2026-08-10-gece-kararlari.md` (BULGU 10, BULGU 20) ve
`incelemeler/oy-v8-yeniden-uretim/sinama-sonucu-tur1.md`.
