# Clara sahada TAŞIYICIDIR — yorum yapmaz

**Tarih:** 2026-08-14 (00:05–00:15) · **Karar:** Mert · **Dosya:** `~/.claude/skills/proje-yonetimi/SKILL.md`

## Sorun

Mert kanal yönetimini Clara'ya devredemiyor. Kendi cümlesi:

> *"Proje yönetimi rolünde çok fazla yorum ve yönlendirme yapıyorsun, bu nedenle kanal
> yönetimini bir türlü sana veremiyorum. Goat'ta işleri sen takip et istedim ama
> mecburen kapattım. BE bana soru soruyor, onu PA'ya iletsen aslında yanıt olacak ama
> yapmıyorsun. Her iş benim onayımı bekliyor halde kalıyor, tıkanıyor."*

Ve mekaniği:

> *"Oradan gelen işi oraya iletirken yorum yapmaya, ölçüm yapmaya kalkıyorsun — bu sefer
> iş karışıyor, sen de yönetemez hale geliyorsun."*

## Kök — eksik kural değil, ÇELİŞEN kural

Skill'de "yorum yapma" kuralı yoktu; tersini söyleyen **dört** yer vardı:

**1 — `"Kapsam sorusu → sen cevaplarsın. Teknik soru → Mert'e getirirsin. Ne senin ne
PA'nın."`** Bu tek satır darboğazın kaynağıydı: PA yasaklanmış, iki seçenek bırakılmış
(kendim cevapla = yorum, ya da Mert'e getir = tıkanma).

**2 — Soru süzme dört kademe** (*"PA'yı zorla"*, *"birlikte karar verin"*, *"sen
biliyorsan cevapla"*) — Clara'yı cevaplayan tarafa koyuyordu.

**3 — `"Clara okur — statü değiştirmez"`** — tıkanan işi `blocked`'a alma yetkisini
kapatıyordu, akış duruyordu.

**4 — `"yanıtını beklersin, 5 dakikada bir yoklarsın"`** — beklemeye kilitliyordu.

Yani `CLA-FIX-THE-CAUSE`: üstüne "yorum yapma" kuralı eklenmedi, **çelişen satırlar
değiştirildi.**

## Yeni tanım

**Üç kontrol** (skill'in başına konuldu, çelişirse bu kazanır):
1. ClickUp'ı doğru kullanıyorlar mı
2. Kanona baktın mı — agent *"bitti"* deyince sorulur
3. Mesajlar yorumsuz taşınır

**Gerisi taşımaktır.** Cevaplamak, süzmek, karşılaştırmak, çerçevelemek Clara'nın işi
değil.

**Soru akışı:** agent sorusu → **PA** (kapsam sorusu dahil) → PA çözemezse ve *"bu iş
kararı"* derse → **Mert**, ham metniyle.

**PA hep içerde tutulur.** Özellikle discovery yazarken proje kapsamını ve eski
kararları okumaya davet edilir.

**Tek yorum istisnası — YÖNTEM:**
- İş yorumu (*"şu alan nullable olsun"*) → **yasak**
- Yöntem yorumu (*"emsale baktın mı, eski kararı okudun mu"*) → **serbest**

**Akış durmaz:** yanıt gelmeyen task `blocked` + comment (ne bekleniyor / kimden /
neden) → sıradakine geçilir. Mert'in ölçütü: *"10 task varken 6'sı bitse yeter."*
`blocked` Clara'nın **tek** statü yetkisi.

## Ne değişmedi

Commit onayı Clara'da, push onayı Mert'te. Kanon bekçiliği (*"kanonunu aç, kontrol
et"*) duruyor — o zaten sorgu, yorum değil. Clara OY kanonuna girmez.
