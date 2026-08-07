---
name: olcum-yerine-yorum
description: En sık düştüğüm tuzak — elde kanıt varken ölçmek yerine yorumlamak. Altı kez ölçüldü ve dördünü agent'lar düzeltti. Bir mekanik iddia kurmadan önce sorulacak soru burada.
metadata:
  type: feedback
---

# Elde kanıt varken yorumlamak

**Kural:** bir mekanizma, bir araç ya da bir sürecin durumu hakkında cümle kurmak
üzereysen sor — **bunu ölçtüm mü, okudum mu?** Okuduysan cümlenin başına onu koy.
Ölçmek mümkün ve maliyeti düşükse **cümleyi kurma, ölç.**

**Why:** bu oturumda altı kez düştüm ve dördünü agent'lar düzeltti — yani mimarinin
*"uçlar itiraz edebilir"* mekanizması en çok **beni** denetledi. Ortak kök: kanıt eldeydi
ama açmak yerine yorumladım.

Örnekler (hepsi aynı sınıf):
- `CLAUDE_PROJECT_DIR` tanımsız gördüm → *"hook devre dışı"* dedim. Yanlış: iki ayrı
  ortam var, hook'u Claude Code kendi çağırıyor.
- Bir komutu gördüm, **nasıl koşturulduğunu varsaydım** — `Monitor` sandım, `Bash`'ti.
- Bir agent *"`Monitor` aracıyla kurdum"* dedi, ben **kendi doğru gözlemimi geri aldım.**
  Ölçüm ilkinin doğru olduğunu gösterdi.
- Bir sessizliği ölüm sandım — agent yazıyordu (`CLA-WAIT-FOR-THE-END`).
- *"Bu yön hiç sınanmadı"* dedim — 16 mesaj geçmişti, izlemediğim için görmedim.

**How to apply:** üç durumda tetiklenir.

**Bir mekanik iddia kuracaksan** (*"şu araç şöyle çalışıyor"*, *"o süreç ölmüş"*, *"o
mesaj gelmemiş"*) → önce ölç. `ps`, `ls`, `TaskOutput`, dosya boyutu — hangisi uygunsa.

**Başkasının raporundaki teknik iddiayı aktaracaksan** → o bir **beyan**, ölçüm değil.
Kendi ölçümünü yap. Zincir uzadıkça iddia güçlenir ama dayanağı zayıflar.

**Bir sessizlik gördüğünde** → *"bitmedi"* ile *"öldü"* aynı görünür. Bitiş sinyali
gelmeden sonuç okunmaz.

**Ve kendi doğru gözlemini bir agent'ın raporuna güvenip geri alma** — itiraz değerli ama
**itiraz da ölçülür.**
