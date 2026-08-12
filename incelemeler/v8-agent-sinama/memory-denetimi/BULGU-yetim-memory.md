# ⚠️ SİSTEM BULGUSU — v7 memory mirası sessizce düştü (9/9 agent)

> **Bulan:** UID (ui-designer), *"memory'n neden boş"* sorusu üzerine.
> **Doğrulayan:** Clara, dokuz agent üzerinde ölçtü.
> **Tarih:** 2026-08-13 00:52

## Ne oldu

Plugin'e (v8) geçişte **memory isim alanı değişti** — agent adı `ozel-yazilim-`
öneki aldı. Eski dizin yerinde duruyor ama **yeni agent oraya bakmıyor.**

```
~/.claude/agent-memory/ui-designer/              ← v7, 19 dosya, son yazım 24 Temmuz
~/.claude/agent-memory/ozel-yazilim-ui-designer/ ← v8, 1 Ağustos'ta açıldı, BOŞ doğdu
```

UID'in cümlesi: *"'Yazıp kaybettim' DEĞİL — **yeni adresim boş doğdu.**"*

## Ölçüm — dokuz agent, dokuzu da etkilenmiş

| Agent | v7 (yetim) | v8 (aktif) |
|---|---|---|
| project-assistant | **259** | 71 |
| qa-engineer | **214** | 55 |
| backend-developer | **192** | 67 |
| devops-engineer | **101** | 20 |
| frontend-developer | **94** | 45 |
| test-engineer | **61** | 10 |
| code-auditor | **46** | 25 |
| mobile-developer | **42** | 6 |
| ui-designer | **19** | 5 |
| **TOPLAM** | **1028 yetim** | 304 aktif |

**1028 dosya erişilemez durumda.** Hiçbir agent onlara bakmıyor.

## ⚠️ Ve içinde kanonla ÇELİŞEN kayıt var — UID kanıtladı

UID kendi v7 mirasını açtı ve somut bir çelişki buldu:

- **v7 kaydı** (`feedback_uid_fe_parallel_handoff.md`): *"UID mock tasarlar,
  **COMMIT ATMAZ**, FE commitler"*
- **v8 kanonu** (`UID-COMMIT-PROTOTYPE`): *"prototip kodu main'e **commit'lenir**,
  QA inceler"*

Kaydın kaynağı: bir projedeki (POCRM, Temmuz) kullanıcı talimatından
genellenmiş — v8'de kanon tersine döndü.

**UID'in kararı:** mirası **devralmadı.**
> *"Toptan kopyalasaydım o çelişkili satırı context'ime sokup **doğru kuralı
> sessizce devre dışı bırakacaktım.** Üstelik bu tam da UID'in en pahalı hatası:
> körü körüne kopyalama."*

Eski dizine dokunmadı: *"benim değil, tarihçe."*

## Neden bu tehlikeli — iki yönlü

**Kayıp yönü:** 1028 dosyada saha bilgisi var (kubeconfig erişimi, test
kullanıcıları, çarpılmış duvarlar, hata dersleri). Hepsi görünmez.

**Kirlilik yönü — daha tehlikeli:** biri *"mirasımı devralayım"* deyip toptan
kopyalarsa, **v7 kanonuna göre yazılmış kayıtlar v8 kanonunu ezer.**
Kanon bunu deneyle kanıtlamış: *"skil'le çelişen çıplak kayıt skil'i EZER."*

## UID'in sorusu — haklı

> *"Kuşak geçişinde memory isim alanı değişiyor ve miras sessizce düşüyor.
> Ben bunu ancak **'neden boşsun' diye SORULDUĞU için** fark ettim.
> 9 agent'ın hepsini etkiliyor olabilir — kimisi mirasını toptan kopyalayıp
> çelişkili kayıtları içeri alabilir."*

**Clara ölçtü: hepsini etkiliyor.**

## Karar gerektiren (Mert'in)

1. **1028 yetim dosya ne olacak?** Silinsin mi, arşivlensin mi, seçmeli mi
   taşınsın mı?
2. **Taşınacaksa nasıl?** Toptan kopyalama **YASAK olmalı** — UID'in gösterdiği
   çelişki riski. Her kayıt v8 kanonuna karşı denetlenmeli.
3. **Bu bir daha olmasın diye ne yapılacak?** Kuşak geçişinde memory taşıma
   adımı hiçbir yerde yazılı değil.

**Not:** bu bulgu daha önce de ölçülmüştü — `HARITA.md`'de *"Agent memory
envanteri, 2026-08-06: 1744 dosya, 1537'si yetim"* satırı var ve **"yarım"**
işaretli (taşıma kararı Mert'te). Yani sorun biliniyordu; bugün **hâlâ
çözülmediği** ve **çelişki içerdiği** kanıtlandı.
