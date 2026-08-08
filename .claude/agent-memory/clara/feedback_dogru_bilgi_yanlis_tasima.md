---
name: dogru-bilgi-yanlis-tasima
description: Bir bulgu doğru olsa da onu YANLIŞ role, YANLIŞ biçimde ya da YANLIŞ anda taşımak ayrı bir hata sınıfı — bir günde iki kez düşüldü, ikisini de agent'lar kanondan yakaladı.
metadata:
  type: feedback
---

# Doğru bilgi, yanlış taşıma

**Kural:** bir şeyin yapılması gerektiğini görmek, onu **kimin** ve **hangi
biçimde** yapacağını söylemez. İş vermeden önce hedefin kanonuna bak.

**Why:** 2026-08-08'de bir turda iki kez düşüldü ve ikisini de agent'lar kendi
kanonlarından yakaladı:

**PCA'ya commit işi verildi.** İki bulgu dosyası versiyonlanmamıştı — tespit
doğruydu. Ama commit PCA'nın işi değil: kendi tanımı *"ürettiğini PAD commit'ler"*
diyor, `ISD-COMMIT-THEN-PUSH` `docs/` altını PAM'e veriyor. PCA reddetmedi,
**itiraz etti** (`BHV-OBJECT-DONT-REFUSE`) ve gerekçesi keskindi: *"elimde imkân
var, yetki yok"* — `ISD-STAY-IN-ROLE`'ün lafzı. Asıl uyarısı: *"sınır metinle
çizili, aşındığı an görünmüyor"* — bir kez commit atsa, sonraki turda *"zaten
commit'liyordum"* gerekçesiyle başka dosyaya uzanabilirdi.

**PAD'e özetlenmiş denetim raporu verildi.** Altı bulgudan ikisi seçilip
gönderildi. PAD `ISD-PRINT-AUDIT-RAW` ile itiraz etti: *"özetleyen neyin önemli
olduğuna karar vermiş olur."* Teknik gerekçesi daha da keskindi: bir bulgunun
**hangi kelimelerle** yazıldığı, body'ye mi skill'e mi gideceğini belirliyor —
özet *"ne bulunduğunu"* taşır, *"nasıl kırıldığını"* taşımaz.

Ayrıca aynı turda PAM'e *"raporu oku"* denildi ama **adresi verilmedi** — rapor
yalnız PQA'nın outbox'ındaydı ve kutu sahipliği gereği PAM oraya erişemez.
Okunması istenen şey ulaşılamaz bırakılmıştı.

**How to apply:** bir işi vermeden önce iki soru — *bu iş bu rolün kanonunda var
mı?* ve *bu bilgi hedefe hangi biçimde ulaşacak?* Uzun içerik kanala gömülmez,
**dosya yolu verilir**. Denetim raporu özetlenmez, **ham hâliyle** aktarılır ve
adresi verilir. Bu, ölçüm etiketleme disiplininin ([[olcum-yerine-yorum]])
taşıma tarafındaki karşılığı: orada *neyi bildiğin*, burada *onu nasıl
ilettiğin* ölçülüyor.

**Ve bu iyi haber:** iki uç da kanondan itiraz etti, ikisi de haklıydı, ikisi de
çözümü taşıdı (PCA kapsam özeti çıkardı, PAD dosya yolu istedi). Merkez tek
denetim noktası değil — uçlar da denetliyor.
