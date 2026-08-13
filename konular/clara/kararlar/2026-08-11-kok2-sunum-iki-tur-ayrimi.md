# Kök 2 (sunum) — tek eşikli kural iki tur tipine ayrıldı

> **Karar tarihi:** 2026-08-11 · **Karar:** Mert
> **Kanıt:** bu oturumun kendi transcript ölçümü
> **Bağlı:** `incelemeler/proje-claralari/kayit.md` (D8, D5, D6, D4)

## Problem — ve iki yanlış teşhis

Kök 2: Mert'in 17 düzeltmesinden dördü sunumla ilgiliydi. En serti D8 —
*"Ben senin yönetiminden çok zorlanıyorum Clara, çok hikâye ve karışık
anlatıyorsun."*

**Birinci teşhis (yanlış): "kural eksik."** Ölçüldü, tersi çıktı — kural
**fazla**: aynı davranış gövdede 8 yerde, 4 memory kaydında
(`cevap_uzunlugu`, `secenek_sunma`, `mert_e_anlatim_bicimi`,
`bulgu_yukari_tasima_olcutu`), 2 skill'de yazılı.

**İkinci teşhis (yanlış): "tetikleme sorunu, kural yazarken devreye girmiyor."**
Bu da çürüdü — aşağıdaki ölçüm gösterdi ki kural bu oturumda hiç tetiklenmedi
**ve Clara fark etmedi**; yani kuralı ihlal ederken kuralın neden ihlal edildiğini
analiz ediyordu.

## Ölçüm — kendi çıktısı üzerinde

Kaynak: `~/.claude/projects/-Users-karaok-p-pr-yazilim-ceo/f9d6179c-*.jsonl`
Kapsam: bu oturumun asistan metin blokları. **300 karakterin altındakiler
elendi** — onlar araç çağırmadan önce yazılan ara cümleler, cevap değil.

- Toplam metin bloğu: **61** → ara cümle **34**, asıl cevap **27**
- Kural (≤3 paragraf **ve** ≤1 soru) ihlali: **25/27 = %92**
- Ortalama uzunluk: **2104** karakter · en uzun **4043** · medyan **2284**
- D8'de Mert'in kestiği mesaj **1803**, onayladığı **434** karakterdi
- Bu oturumda **17/27** cevap 1803'ün üstünde
- Kuralı tutturan 2 cevabın ikisi de kısa ara cevaptı (471 ve 640) — yani kural
  **rastgele** tutuyor, disiplinle değil

**Mert bu oturumda uzunluk için bir kez bile kesmedi.**

## Mert'in iki cevabı — kuralı düzelten

**Uzunluk:** *"Zorluyor ama dediğin gibi detaylı konuşulması gereken konular vardı."*
**Yapı:** *"Bölümlere ayrılmasını seviyorum, özellikle insight plugini sonrasında
çok iyi geldi."*

İkisi birlikte okununca: **yapı sorun değil, hacim sorun — ama her turda değil.**

## Karar — iki tur tipi

> **Ayıran test: bu tur bir şeyi BİLDİRİYOR mu, bir şeyi mi KURUYOR?**

**Bildirim turu** (ölçüm sonucu, durum, bir soruya cevap)
→ bir bulgu · üç paragraf · bir soru. Mevcut kalıp burada doğru.

**Düşünme turu** (konu birlikte açılıyor, karar üretiliyor)
→ uzun ve başlıklı olabilir. **Tek kısıt: her bölüm bir iş yapar.**
Aynı şeyi iki kez söyleyen bölüm, tekrar eden gerekçe, süs başlığı çıkarılır.
**Uzunluk sınırı yok** (Mert: *"sınır koyma, her bölüm bir iş yapsın yeterli"*);
**tekrar** yasak.

## Neden kural değişti, davranış değil

`CLA-FIX-THE-CAUSE`: bir kural **%92 oranında ve haklı olarak** çiğneniyorsa sorun
uygulamada değil, kuralın kendisindedir. Tek eşikli kural iki farklı iş tipine
uygulanınca ya sürekli ihlal edilir ya işi bozar — bugün birincisi oldu.

Eski kuralın istisnası vardı ama **yanlış tetikle**: *"Mert ayrıntı istediyse."*
Bugün Mert ayrıntı istemedi; **konu** ayrıntı gerektirdi. Tetik yanlış yerdeydi.

## ⚠️ İstismar riski — kayda geçiyor

Aynı ölçümde 27 cevabın 17'si 1803'ün üstündeydi ve **hepsi düşünme turu değildi.**
Bir bildirim turunu *"konu derin"* diye uzatmak bu ayrımın istismarıdır. Ayrım bir
izin değil, bir sınıflandırma.

**Sonraki ölçüm:** aynı script birkaç oturum sonra tekrar koşulur. Bildirim
turlarının ihlal oranı düşmediyse ayrım işe yaramamış demektir.

## Nereye işlendi

- `.claude/agents/clara.md` — "Nasıl konuşursun" bölümü, iki tur ayrımı + istismar uyarısı
- `.claude/agent-memory/clara/feedback_cevap_uzunlugu.md` — kural, gerekçe, uygulama
