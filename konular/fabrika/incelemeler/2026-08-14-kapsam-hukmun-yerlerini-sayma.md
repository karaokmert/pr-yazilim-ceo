# Ölçüm — kapsam çizerken hükmün yerlerini saymak

**Tarih:** 2026-08-14 · **Ölçen:** PAM (kendi deseni) · **Kayıt:** Clara

## Desen

PAM'in kendi cümlesi:

> *"Kapsamı çizerken hükmün **KENDİSİNİ** değil, hükmün **BULUNDUĞU YERLERİ** sayıyorum.
> Oysa aynı hüküm kimlik anmadan başka yerlerde de yaşıyor."*

## Üç vaka, aynı gün

| # | Ne oldu | Ne kaçtı |
|---|---|---|
| 1 | Kanal işinde kapsam **iki metinle** çizildi | Üçüncü metin çelişkinin **gerçek tarafıydı** |
| 2 | Body turunda **dokuz body arası** cascade düşünüldü | **Dosya içi** cascade hiç düşünülmedi → Bulgu 2 oradan çıktı |
| 3 | Revizede kapsam *"açılış paragrafı ile On-demand arası"* çizildi | BE satır 64'teki üçüncü iz dışarıda kaldı — PAD buldu |

Üçünde de **ölçüm doğru, kapsam eksik.** Sayılan yerler doğru sayıldı; sayılmayan yer
hiç görünmedi.

## Neden bu sınıf hata sessiz

Kapsam **geniş** yazılırsa: ölçülmemiş alan ölçülmüş sanılır — okuyan bir eksik görmez.
Kapsam **dar** çizilirse: ölçüm sınırlanır ama bu **görünür**, biri fark eder.

Buradaki üç vaka ikinci türden — ve üçünde de fark eden **başkası** oldu (PAD iki kez,
çelişkinin kendisi bir kez). Yani mekanizma çalıştı ama **bir tur maliyetiyle.**

## Kanonda karşılığı var

`ISD-CASCADE-COVERS-DESCRIPTIONS` tam bunu söylüyor: aynı hüküm kimlik anmadan başka
yerlerde yaşayabilir.

⚠️ **Yani eksik olan hükmün varlığı değil, uygulaması.** PAM'in kendi tespiti:
*"Kanonda hüküm zaten var."*

## Kural yazılmadı — gerekçe

Yeni kural yazmak burada **yama** olurdu (`CLA-FIX-THE-CAUSE`): mevcut hüküm doğru,
üstüne ikinci bir hüküm eklemek sebebi kaldırmaz.

**Sebep ne:** kapsam çizilirken sorulan soru *"bu hüküm nerede yazılı?"* — oysa
sorulması gereken *"bu hüküm başka nerede, başka adla yaşıyor olabilir?"*

Birinci soru bir **arama**, ikincisi bir **şüphe**. Arama tarama ile biter, şüphe
okuma ile.

## İzlenecek

Bu desen dördüncü kez görülürse — ve PAM dışında birinde görülürse — kişisel değil
**yapısal** demektir. O zaman hükmün kendisi değil, hükmün **nasıl uygulandığı**
sorgulanır.
