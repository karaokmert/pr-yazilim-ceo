# Karar — saha ölçümü transkript dolmadan yapılmaz

**Tarih:** 2026-08-17 16:26 · **Karar mercii:** Mert

## Mert'in cümlesi

> *"Sahada işlemler bitince ölçüm yapılacak. Kanal değişimlerinde sadece PCA etki
> analizi yapabilir. Sahayı takip edersin. Çalışmayan şeyleri not alırsın. Ancak
> bunun için öncelikle biraz transkription dolması gerekiyor."*

## Üç hüküm

**1. ÖLÇÜM SAHADA İŞ BİTİNCE.** Transkript dolmadan ölçüm yapılmaz —
yarım oturumdan çıkan bulgu bulgu değildir.

**2. KANAL DEĞİŞİMİNDE ETKİ ANALİZİ YALNIZ PCA'DA.** Clara kanal
değişikliğinin etkisini ölçmez; kapsamı PAM çizer, PCA ölçer.

**3. CLARA SAHAYI TAKİP EDER, ÇALIŞMAYANI NOT ALIR.** Teşhis etmez —
bulgu biriktirir, fabrikaya taşır.

## Neden bu kural gerekliydi — bugün ölçüldü

Bugün 0.8.0 (OY) ve 0.9.0 (WS) sahaya indi. Goat ekibi üç saat çalıştı ve
Clara iki kez *"bakayım mı"* diye sordu — oysa iş bitmemişti.

**Yarım oturumu ölçmenin iki arızası var:**

- **Bulgu eksik çıkar.** Agent henüz o adıma gelmemiştir; *"yapmadı"*
  sanılır, oysa *"sırası gelmedi"*dir.
- **Ölçüm gürültü üretir.** `idle` görünen bir agent bekliyor da olabilir,
  bitirmiş de olabilir, takılmış da olabilir. Üçünü ayıran şey **tamamlanmış
  transkript.**

Bu, `CLA-WAIT-FOR-THE-END`'in saha karşılığı: *"bir şeyin sonucunu, o şey
bitmeden okumazsın."* Bugün 2026-08-04'te ölçülmüş aynı arıza tekrarlanmak
üzereydi — UID kanalı kurulur kurulmaz ölçülmüş, boş görülmüş, *"sessiz
başarısızlık"* diye raporlanmıştı; agent hâlâ çalışıyordu.

## Ayıran soru

**Transkript doldu mu?**

- Dolduysa → ölçülür, bulgu çıkarılır
- Dolmadıysa → **beklenir**; `ListAgents` durumu bir tamamlanma sinyali
  DEĞİLDİR

## Sınır — bu kural neyi yasaklamıyor

**Takip yasak değil.** Clara sahayı izler, ne olduğunu görür, çalışmayan
şeyi not eder. Yasak olan **ölçüm ve teşhis** — yani *"şu kural tutmadı"*
hükmü vermek.

Not almak ile bulgu üretmek ayrı: not bir gözlem, bulgu bir iddiadır ve
iddia tamamlanmış transkriptten çıkar.
