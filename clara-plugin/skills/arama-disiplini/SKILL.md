---
name: arama-disiplini
description: Bir şey ararken hangi aracı nasıl kullanacağını seçme yöntemi — grep ile dizin listeleme arasındaki ayrım, grep'in eşleşen satırı gösterme disiplini ve aynı soruya farklı bulgu çıkmasının sebebi. Bu skill'i "şunu ara / bu daha önce konuşulmuş mu / hangi kayıtta var / bunu nerede yazmıştık" denen durumlarda kullan. Ayrıca bir arama boş döndüğünde, çok fazla sonuç döndüğünde ya da aynı soru iki kez farklı cevap verdiğinde de kullan — sebepleri ve ayırt edici testleri burada. Kapsam dışı — ClickUp araması (`clickup-duzeni` skill'i).
---

# Arama disiplini

İki araç var: **`grep`** ve **`ls`**. Hangisini seçtiğin sorunun türüne bağlı, ama asıl
mesele seçim değil — **`grep`'i nasıl çağırdığın.** Yanlış çağrı yalnız yavaş değil,
**yanlış cevap** veriyor ve yanlış cevap sessiz geliyor.

Ölçümler: `references/olcumler.md`

## En önemli kural — `-l` değil, SATIR

**`grep -l` dosya adı verir, cevap vermez.** Dosyaların içine bakar ama sana yalnız
hangi dosyada geçtiğini söyler. Sonuç: elinde bir dosya adı listesi kalır, hangisinde
cevap olduğunu **açıp okuyana kadar** bilemezsin.

**Eşleşen satırı gösteren biçim cevabı doğrudan verir.** Ölçüldü (2026-08-16), aynı
soru iki biçimde soruldu:

- `grep -ril` → **11 dosya adı**, hangisinde ne yazdığı belirsiz, 11 dosya açmak gerekir
- `grep -rih` → **47 satır**, ilk 25'i okundu ve **hiçbir dosya açılmadan** cevap çıktı

İkinci aramada çıkan şey yalnız cevap değildi: **iki satırın birbirini kestiği bir
çelişki** de görüldü. Dosya adı listesinde o çelişki görünmüyordu.

**Yani varsayılan `-h` (ya da satır gösteren herhangi bir biçim), `-l` istisna.**

`-l` yalnız şu iki durumda doğru: **kaç dosya etkileniyor** sorusu (sayım) ve
**hangi dosyaları düzenleyeceğim** sorusu (toplu düzenleme girdisi).

⚠️ **Bedeli var:** satırla arama daha çok çıktı üretir. Geniş bir kelime yüzlerce
satır döndürebilir. Sıra: **önce dizinle daralt, sonra satırla bak** — `head` ile kes.

## İkinci kural — aynı soruya farklı bulgu çıkıyorsa sebep KELİME TAHMİNİ

Bir soruyu iki kez arayıp iki farklı sonuç alıyorsan dosyalar değişmedi; **senin
seçtiğin kelime değişti.**

`grep` aradığın **kelimeyi** bulur, aradığın **şeyi** değil. Soruyu kelimeye çevirirken
tahmin yürütüyorsun: *"kanal açılış"* mı, *"açılışta kanal"* mı, *"kanal kurulmaz"* mı?
Her tahmin farklı küme döndürüyor.

Ölçüldü aynı gün: dar arama (tek klasör + dar kalıp) doğru dosyayı **hiç bulamadı** —
oysa dosya tam o klasördeydi. Geniş arama aynı dosyayı buldu ama **sekiz sonucun
içine gömdü.**

**Ayıran hareket: tek kelimeyle ara, kalıpla değil.** Kalıp (`kanal.*acilis`) senin
cümle kurgunu dayatır; tek kelime (`kanal-acilis`) metnin kendi kurgusunu bulur.
Sonuç çok gelirse **ikinci kelimeyle boru hattında daralt**, kalıbı genişletme.

## Üçüncü kural — bir eşleşme o ismin kendisi demek değil

`grep` **alt dizeyi** bulur, adı doğrulamaz. `x` araması `x`i de `önek-x`i de
`x-sonek`i de getirir.

Ölçüldü 2026-08-11: `grep dagitim` çekildi, `- dagitim` satırı görüldü ve yanlış
skill'in yürürlükte olduğu söylendi — `dagitim` ve `plugin-dagitim` iki ayrı şeydi.
**Yanlış bilgi Mert'e taşındı ve bir karar ona dayanarak verildi.**

Eşleşen satırı gördükten sonra **adı tam hâliyle doğrula**: dosyayı aç, sınırlı ara
(`grep -w`, `^ad$`), ya da varlığı `ls` ile sor.

## Dördüncü kural — bir alanı aramak karşıtını aramamak demek

Bir kısıt arıyorsan **hem izin listesini hem yasak listesini** ara. `tools:` arayıp
`disallowedTools:` aramamak, ölçümü yarım bırakır (ölçüldü, Mert yakaladı).

## Liste sorusu → `ls`

*"Hangi kararlar şu tarihte verildi"*, *"bu klasörde ne var"* — bunlar arama değil
**listeleme** sorusu. `grep` bunlara parçalı cevap verir; doğru cevap dizinin kendisidir.

Klasör yapısı bu yüzden haritadır ve ayrıca bir indeks tutulmaz — indeks bayatlar,
dizin listesi kendiliğinden günceldir.

## Tarihçe — vektör arama (Qdrant) KAPATILDI

**2026-08-15 ölçümü:** Qdrant iki katmanda birden düşük — bulut `403 ExpiredSignature`,
yerel `000` (ayakta değil).

**Sebep arıza değil, karar.** Mert: *"Qdrant'ı mantıklı bulmadık ve kullanmadık,
o nedenle kapattım."*

Bu skill eskiden *"niyet sorusu → vektör arama"* diyordu. **O kural yürürlükten kalktı**
— olmayan bir araca yönlendiriyordu. Niyet soruları artık `grep` + dizin gezmeyle
cevaplanır; kelime tahmini sorunu (yukarıda) bunun bedeli.

Vektörün ölçülmüş üç körlüğü tarihçe olarak duruyor — bir gün geri gelirse hatırlanacak:
çıktısı cevap değil **adres**; **skor alakayı ölçmüyor** (alakasız soru ile gerçek soru
arasındaki fark ayırt edilemeyecek kadar dar); ve **eskimiş kayıt taze kaydı bastırıyor**
(benzerlik anlamı ölçer, doğruluğu ölçmez).
