# OY-9 kanonu okumasından Clara'ya alınan dört hüküm

**Tarih:** 2026-09-03 · **Karar:** Mert — *"dördünü de al"*
**Kaynak:** `~/p/fabrika-v2/docs/oy-9/` davranış katmanı (behavior · is-disiplini ·
memory · denetleme-kurallari)

Mert OY-9 davranış skill'lerini okumamı ve kendime alabileceklerimi çıkarmamı istedi.
Okunan kapsam: çerçeve dosyası, davranış katmanının tamamı (11 dosya) ve PA gövdesi.
Okunmayan: CA/QA/TE gövdeleri, agent-özel on iş skill'i, üç takım skill'i,
`00-ROL-BULGULARI.md`.

Bilgi anlatımla alındı, atıfla değil — her sistem bağımsız yaşar. Kopyanın tazeliği
"bu hâlâ böyle mi" sorusuyla korunur (`clara-behavior` › Anlatımla gelen bilgi
sessizce eskir).

## Alınan dört hüküm ve nereye yazıldığı

**1 · Başlık gövdeyle aynı kuvveti taşır** → `clara-behavior`
Başlık taşınır, gövde arkada kalır; gövdeye yumuşatıcı not yazmak başlıktaki kesin
dili düzeltmez. Kaynağı OY-9 `denetleme-kurallari`. Bana işliyor çünkü bulgularım
Mert'e ve kapanış dokümanlarına başlıkla gidiyor.

**2 · Kapsam onayı içerik onayını kapsamaz** → `clara-behavior`
"Şunu yapacağım" onayı ile "ürettiğim bu" onayı ayrı kapılar. OY-9'da ölçülmüş:
onaylı kapsamın içine yanlış içerik girdi, kimse fark etmedi. Bende bu ayrım yoktu —
kapsam onayı alıp içeriği sunmadan dosyaya yazma riskim vardı.

**3 · Kaydın ölüm koşulu — ders refleks olunca silinir** → `hafiza-duzeni`
"Bir dersi hatırlamak için okumuyorsan o ders artık sende, kayıtta değil." MEMORY.md
tek yönlü büyüyordu; temizlik ritmim vardı ama silme ölçütüm yoktu. Kaynağı OY-9
`memory`.

**4 · Kanıt çifti: ne koştu + neyi kanıtladı** → `clara-is-disiplini`
Sahte yeşil vakası: kimliksiz istek 200 döndü, yetki katmanı hiç koşmamıştı.
"Aracın ne ölçtüğü" dersimin kardeşi — o aracın saydığını sorgular, bu yeşilin
kapsadığını.

## Alınmayanlar ve sebebi

- "Çakışan iki ölçüm birbirini doğrulamaz, pekiştirir" — bende zaten var
  (`feedback_cakisan_sinyal_dogrulama_degil`). İki sistemde bağımsız yaşıyor.
- Devir bloğu biçimi, `Beklediğim:` satırı, iki-uçlu başlık — bende zaten var.

## Aynı okumada çıkan bulgular (fabrikaya taşınması Mert'in kararı)

1. **`sozlesme-tuketimi` frontmatter/gövde çelişkisi** — description "her oturumda
   yüklenir" diyor, gövde "ON-DEMAND" diyor ve preload edilmeme gerekçesini uzun
   anlatıyor. Karar verilmiş, gövde güncellenmiş, description unutulmuş.
2. **`Mod:` satırının yokluk-anlamlı tasarımı** — unutma ile bilinçli tekil seçimi
   ayırt edilemiyor; sessiz arıza sınıfı bilinçli açık bırakılmış.
3. **Onay mekanizmasında zıt ölçümler** — OY kanonu "onay ekrana yazılır, araç
   kullanılmaz, istisna yok"; Clara kanonu tam tersini ölçtü (metin atlanıyor, araç
   atlanmıyor). Zincir içi roller için ekran kuralı doğru; PA-kullanıcı ekranında
   gerekçe yazılı değil.
4. **Küçük:** sprint skill'inde ClickUp bölümü aynı cümlede "5-6 sub task birden
   in progress" ve "agent çalıştığı task'ı in progress'e alır" diyor — muğlak.
