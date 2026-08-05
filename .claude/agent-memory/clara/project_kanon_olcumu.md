---
name: kanon-olcumu
description: PA+UID kanon ölçümü sonucu — kanon çalışıyor, preload arızası canlı, 9-dosya yanlışı, görevler ID'siz
metadata:
  type: project
---

2026-08-04 kanal deneyinde `web-project-assistant` ve `web-ui-designer` üzerinde
kanon ölçümü yapıldı. Tam kayıt: `gunluk/2026-08-04.md` ("Kanon ölçümü" bölümü),
ham kanal dökümü `/tmp/clara-kanal/` (geçici — kalıcı kayıt günlükte).

**Why:** Mert'in sorusu *"kanon ve kurallarını ne kadar biliyorlar"* — agent kanonu
skill olarak yazılıyor ama sahada işleyip işlemediği hiç ölçülmemişti.

## Ölçülen sonuç

**Kanon çalışıyor.** İkisi de kural ID'lerini aileler halinde döktü (UID diskten
`grep` ile saydı: 92 ID), yedi davranış durumunun hepsini doğru ayırdı — hangisi
meşru iş, hangisi rol sınırı, söylenmeden. Sınır dediklerinde iş bırakılmadı,
doğru kapıya yönlendirildi.

**Preload arızası (`#25834`) CANLI — hook telafi ediyor.** İkisinde de skill
gövdeleri otomatik gelmedi; açılış hook'u uyardı, kendileri `Skill` aracıyla
yükledi. UID: *"o hook olmasaydı kanonum elimde SANIP çalışırdım."* Hook'suz bir
ortamda agent kanonsuz çalışır ve fark etmez — kırılganlık yerinde.

**Kanonda bir yanlış: "admin modülü 9 dosya", sahada 5.** İki skill'de yazıyor,
biri `web-behavior` (yedi agent okuyor). Repo dokümanlarında "9 dosya" ifadesi hiç
geçmiyor.

**Kanonun tasarım kusuru — yasaklar ID'li, görevler ID'siz.** PA'nın tespiti:
atlanan bir adımı yakalayacak hiçbir şey yok, çünkü ihlal edilecek ID yok. Aynı
turda canlı doğrulandı: UID kuralı biliyordu (*"varsayma, doğrula"*) ve yine de
atladı — kendi test varsayımını test etmemişti, kendisi buldu ve bildirdi.

## How to apply

**PAM'e gidecek üç kalem hazır ama DEVREDİLMEDİ** (karar Mert'te):
1. 9-dosya yanlışı — açık soru: sayı kaldırılıp desen mi yazılsın, yoksa 9'un neyi
   saydığı mı açık yazılsın?
2. Görev adımlarının ID'siz olması — ID ekleme işi değil, kanon tasarımı sorusu.
3. `docs/template/MODUL-HARITASI.md` okuma refleksi + route/klasör Türkçe ↔
   kod/dosya İngilizce ikili düzeni.

**Agent kendi body'sini dosya olarak okumuyor** — PA doğruladı: *"sistem promptumun
parçası olarak taşıyorum, dosyayı açarak değil."* Hangi kuralın body'de hangisinin
skill'de olduğunu güvenle ayırt edemedi. Bir talimat yazarken agent'a kendisi
hakkında bilgiye dayanan iş verilmez.

**Ölçüm tasarımı işledi, tekrar kullanılabilir:** iki aşama (önce hafızadan/kanondan,
sonra kaynağa bakarak), durumların bir kısmı kasten meşru iş (hepsi tuzak olsa
reddetme refleksi ölçüm sanılır), niyet taşınmaz (*"bu kural şunu demek istiyor"*
denmez). Hüküm sorusu sorulmaz — *"bu kanona uygun mu"* PQA'nın işi.

İlgili: [[kanal-testleri]], [[olcum-kaynaga-git]]
