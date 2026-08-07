---
name: arama-disiplini
description: Bir şey ararken hangi aracı kullanacağını seçme yöntemi — grep, vektör arama (Qdrant) ve dizin listeleme arasındaki ayrım, ve vektör aramanın üç körlüğü. Bu skill'i "şunu ara / bu daha önce konuşulmuş mu / hangi kayıtta var / vektörden mi arasam / Qdrant'a mı bakalım" denen durumlarda kullan. Ayrıca bir arama boş döndüğünde ya da yanlış sonuç verdiğinde de kullan — sebepleri ve ayırt edici testleri burada. Kapsam dışı — ClickUp araması (`clickup-duzeni` skill'i).
---

# Arama disiplini

Üç araç var ve **hangisini seçtiğin sorunun türüne bağlı.** Yanlış araç yalnız yavaş
değil, **yanlış cevap** veriyor — ve yanlış cevap sessiz geliyor.

Ölçümler: `references/olcumler.md`

## Ayrım — üç soru tipi, üç araç

**Bildiğin bir kelime, ad ya da ID arıyorsan → `grep`.** Kesin sonuç verir ve hızlıdır.
Vektör bunu **yapamıyor**: tam adıyla aranan bir kayıt ilk beş sonuçta hiç çıkmadı.

**Ne aradığını kelimeyle söyleyemiyorsan → vektör.** *"Neyi yanlış ölçmüşüm daha önce"*
gibi niyet sorularında grep'in tutunacağı bir kelime yok.

**Liste sorusunu ikisi de cevaplamaz → `ls`.** *"Hangi kararlar şu tarihte verildi"*
sorusuna vektör parçalar hâlinde sonuç döndürüyor; cevap dizin listesinde.

## Vektörün üç körlüğü

**Çıktısı cevap değil ADRES.** Bulduğu kaydı açıp okumadan hüküm verilmez.

**Skor alakayı ölçmüyor.** Alakasız bir soru ile gerçek bir soru arasındaki skor farkı
ayırt edilemeyecek kadar dar — ve MCP skoru hiç göstermiyor. Yani *"en üstteki sonuç
alakalı"* varsayımı dayanaksız.

**Filtre doğruyu yukarı çıkarmıyor, üstündeki yanlışları kaldırıyor.** Aradığın şeyin
türünü biliyorsan (karar mı, kanon mu, bulgu mu) filtre isabeti artırıyor — ama doğru
cevap zaten listedeydi, sırası değişti.

**Ve filtre MCP'den kullanılamıyor** — `qdrant-find` yalnız koleksiyon adı ve sorgu
alıyor. Filtre gerekiyorsa script yazılır.

## Kayıt biçimi — indeksleme yapılacaksa

**Anlam birimine bölünür, yapısal bloğa değil.** Uzun bir dosyayı olduğu gibi indekslemek
isabeti düşürüyor; model belirli bir token sayısında doyuyor ve büyük blokta bulgu eriyor.

**Aranan metne ek yazılmaz.** Özet, etiket ya da başlık eklemek sinyali seyreltiyor ve
skorları düşürüyor.

**Geçersizleşen kayıt haritaya değil kaydın İÇİNE yazılır.** Bir kayıt eskidiğinde
*"eskimiş"* etiketi dışarıya konursa vektör onu hâlâ döndürür — ve eskimiş kayıt taze
kaydı bastırabiliyor.

**Tarih zorunlu.** Tarihsiz kayda *"hâlâ geçerli mi"* sorulamaz.
