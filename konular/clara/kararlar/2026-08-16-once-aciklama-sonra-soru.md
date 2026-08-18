# Karar — her sorunun önüne açıklama konur

**Tarih:** 2026-08-16 20:45 · **Karar mercii:** Mert

## Mert'in cümleleri

İlki, oturumun ortasında (ilk soruyu açıklamasız sorduktan sonra):

> *"Sorularını önce açıklama yaparak sonra ask question u kullanarak yürütmemiz
> gerekiyor — bu önemli bir kural Clara."*

İkincisi, oturum sonunda kuralı kalıcılaştırırken:

> *"Soruları sorma şeklini skill ine ekler misin Clara. Ayrıca her seferinde
> böyle ilerle."*

## Kural

**Soru sorulmadan önce açıklama gelir. İstisnasız.**

```
1. AÇIKLAMA (düz metin)  → ne okudum · ne gördüm · çelişki nerede
2. AskUserQuestion        → seçenekler ve sonuçları
```

Açıklamanın üç parçası:

| | |
|---|---|
| **Ne okudum** | Hangi dosya, hangi satır, hangi cümle — kaynağı adıyla |
| **Ne gördüm** | Bugünkü kanonda ne yazıyor, alıntısıyla |
| **Çelişki nerede** | Neden çatışıyor, ve bu *mekanik* mi *tercih* mi |

## Nereye yazıldı

- **`onay-brief` skill'i** — kuralın gövdesi, "açıklama ne DEĞİLDİR" bölümü,
  ayıran test. Description da güncellendi: artık *"soru sorulacak her durumda aç"*
  diyor (eskiden yalnız onay istenirken açılıyordu — soru sorma tetiği yoktu).
- **Clara kanonu** (`.claude/agents/clara.md`, onay-brief bölümü) — kural özeti +
  ayıran test + skill'e atıf.

İkisine birden yazıldı çünkü skill tetiklenmezse kural görünmez kalırdı.

## Gerekçe

**Seçenek metni bir kararın dayanağını taşıyamaz.** Bir-iki cümlelik seçenek
etiketine ne okunduğu, kanonda ne yazdığı ve neyin çatıştığı sığmıyor. Açıklama
olmadan Mert seçeneklere bakıp *"bu ne demek"* diye sormak zorunda kalıyor — soru
bir tur kaybettiriyor.

**Daha sinsi zarar: açıklamasız soru, sorunun kendisini gizler.** Üç seçenek
sunmak *"burada bir karar var"* demek; ama **neden** karar gerektiğini
göstermiyorsa Mert seçeneği değil, Clara'nın çerçevesini onaylamış oluyor.

## Ayıran test

**Mert bu kutuyu okumadan önceki paragrafı okumasa, kararı verebilir miydi?**

- Verebiliyorsa → açıklama gereksizdi, soru zaten kendine yetiyordu
- Veremiyorsa → açıklama zorunlu, atlanırsa karar eksik bilgiyle veriliyor

## Bu kural sahada nasıl işledi (aynı oturum)

Kuraldan sonra sorulan yedi sorunun hepsi bu düzende gitti ve **üçünde Mert
seçeneklerimin dışında bir cevap verdi:**

- Sprint modu → *"iki ayrı skill olur, handoff modu söyler"* (a+b birleşimi)
- Doküman commit'i → *"kural değil, ara karar"* (üç seçenek de kural öneriyordu)
- Toplu tarama → *"her agent kendi katmanını kontrol eder"* (üçünden de iyisi)

Yani açıklama seçenekleri **aşmayı** mümkün kıldı: durumu görünce Mert kendi
çözümünü üretti. Açıklamasız sorulsaydı üç seçenekten biri seçilirdi.

## Sınır

Açıklama **özet değil** (Mert'in söylediğini ona geri anlatmak),
**anlatı değil** (hangi grep çekildi, kaç dosya açıldı),
**savunma değil** (kendi tercihini öne çıkarmak — tercih varsa seçeneğin
içinde "(Önerilen)" olarak durur).
