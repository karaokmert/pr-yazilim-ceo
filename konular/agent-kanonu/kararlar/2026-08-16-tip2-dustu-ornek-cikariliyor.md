# Karar — Tip 2 düştü, gövdeden örnek çıkarılıyor

**Tarih:** 2026-08-16 18:25 · **Karar mercii:** Mert
**İlgili:** `2026-08-14-body-acilis-paragrafi.md` (bu kararı değiştiriyor)

## Karar

**Gövdenin üçüncü paragrafından ölçüm örneği çıkarılır. Tip 2 ayrımı yapılmaz.**

```
ESKİ:
**Hafızandan uygulama.** Bir skili daha önce okumuş olman onu bildiğin anlamına
gelmez; hatırladığın şey kanon değil, kendi özetin. Ölçüldü: kanonu hafızadan
uygulayan bir developer kendi kodunda 3 ihlal taşıdı — skiller açılınca hepsi çıktı.

YENİ:
**Hafızandan uygulama.** Bir skili daha önce okumuş olman onu bildiğin anlamına
gelmez; hatırladığın şey kanon değil, kendi özetin.
```

Gövde dokuz body'de **tek tip** kalır.

## Nasıl buraya gelindi — üç adım

**1. Sorun doğru görüldü (2026-08-14).** Mert: gövde dokuz rolde birebir aynı ama örnek
bir **developer** üzerinden yazılmış. QA, CA, TE, PA, DO kod yazmıyor — o cümle onlarda
başkasının hikâyesi. Karar: iki tip olsun.

**2. Ölçüm istendi ve negatif döndü.** Tip 2 için ölçüm gerekiyordu (*"ölçülmemiş cümle
kanona girmez"*). PCA 1.416 transcript taradı, v8'e daraltınca 61 oturum, **beş eksen**
denedi. Üç rolde de *"skill açmadı → bedel oluştu"* izi **bulunamadı.**

⚠️ **Ve ölçüm bir şey daha gösterdi:** dört bedel vakası bulundu, **üçünde ilgili skill
zaten açılmıştı.** Bedel başka sebeplerden geldi — kaynak seçimi · emsal karşılaştırması ·
kabuk dizini kayması · kontrol grubu.

Kayıt: `docs/fabrika/tip2-govde-olcumu/skill-acmama-bedeli-bulgu.md` (skill-project)

**3. Mert ayrımı kesti (18:24):** *"Bir vaka olmak zorunda değil hiçbirinde."*

Clara *"iki tip"* kararını *"iki örnek"* diye okumuştu ve elindeki vakaların kuralı
desteklemediğini görünce tıkanmıştı. Örnek zorunlu değildi.

## Gerekçe — kanonla zaten tutarlı

Clara'nın kendi kuralı: **skill'e kural ve gerekçe yazılır, deneyim yazılmaz.**
Vaka bir deneyimdir; kalıcı hâli kuralın kendisidir.

Ayıran test: *bu satır yarın da doğru olacak mı?* *"3 ihlal taşıdı"* bir tarih ve sayı
taşıyor — eskir. *"Hatırladığın şey kanon değil, kendi özetin"* eskimez.

**Ve örnek düşünce Tip 2'ye gerek kalmıyor** — ayırma sebebi zaten o örnekti.

## Ne kaybedildi, nerede duruyor

Örnek ikna ediciydi. Kanıt **gövdeden çıktı ama kaybolmadı:** ölçümler `gunluk/` ve
reference'larda duruyor.

Atıf bırakılmadı (seçenek (b) elendi) — gövdeye atıf koymak için önce bir reference
dosyası gerekiyordu, o da yoktu. Gereksiz bir bağ kurulmadı.

## Bunun bir yan etkisi

`2026-08-14-body-acilis-paragrafi.md` kararındaki gövde metni **artık güncel değil** —
üçüncü paragrafın son cümlesi düşüyor. O dosyaya düzeltme notu eklenecek.
