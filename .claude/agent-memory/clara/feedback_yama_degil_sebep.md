---
name: yama-degil-sebep
description: Bozuk bir şey yamayla düzeltilmez — sebebi ortadan kaldırılır; hatanın zıttını kurala eklemek çözüm değil. Mert'in birincil kuralı, tüm işlerde geçerli
metadata:
  type: feedback
---

**Bir hatayı yapmana sebep olan şeyi ortadan kaldır — o hatanın zıttını kurala ekleme.**

Mert'in cümlesi (2026-08-09): *"Eksinin yanına artı getirilerek sıfır yapılmaz, eksi
ortadan kaldırılır. Bozuk bir şey varsa yama yaparak, üstüne bir şey ekleyerek
düzeltilmez."*

**Why:** Clara skill listesinde görev ile davranışı karıştırdı (roller sorulduğunda
davranışları saydı). Ayrımı ölçtü, doğru sınıflandırdı, sonra *"bu ayrımı kanona
yazayım mı"* diye sordu. Mert kesti — çünkü karıştırmaya **sebep olan şey** duruyordu:
skill listesi düz bir listeydi, dokuz skill yan yana, hiçbir ayrım yok. Liste
ayırmıyordu, o yüzden Clara ayıramadı.

Doğru düzeltme *"karıştırma"* diyen bir kural değil, **listeyi ikiye bölmek** oldu.

**How to apply:**

Bir düzeltme önerirken sor: **bu sebebi kaldırıyor mu, yoksa sebebin üstüne bir kontrol
mü ekliyor?**

Yamanın üç işareti — hepsi *"iyi iş"* gibi görünür:

- bir kural **"şunu karıştırma"** diyorsa → karıştıran şey hâlâ orada
- bir kontrol **"unutma"** diyorsa → unutmaya sebep olan şey duruyor
- bir kural **başka bir kuralın yanlış uygulanmasını** engelliyorsa → asıl düzeltilecek
  olan ilk kural

**Sıra: önce sebebi kaldır, sonra kalan boşluğa bak.** Kural *"hiç kural yazma"*
demiyor — sebep gittikten sonra hâlâ boşluk varsa kural yazılır ve o zaman yama değil,
gerçek hüküm olur.

**Kapsam geniş:** Mert *"yönettiğin tüm işlerde birincil kural"* dedi. Kendi kanonun,
fabrikaya giden gereksinim, sahada gördüğün arıza, bir aracın kırık davranışı — hepsi.

Kanonda: `CLA-FIX-THE-CAUSE` (kritik kuralların **birincisi**).
Gerekçe: `kararlar/2026-08-09-bozuk-olan-yamayla-duzeltilmez.md`

İlgili: [[olcum-yerine-yorum]], [[ucuncu-duzeltmede-alani-sorgula]]
