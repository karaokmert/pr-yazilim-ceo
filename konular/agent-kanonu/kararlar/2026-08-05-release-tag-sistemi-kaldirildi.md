> ⚠️ **BU KARAR SAHADA TUTMAMIŞ — ölçüldü 2026-08-13.**
> Kanon (`deploy-release`, plugin 0.7.0) hâlâ `REL-DO-PRODUCTION-TAG` diyor:
> *"Prod deploy sonrası versiyon TAG'i (`v{x.y.z}`) + not ZORUNLU; atlamak YASAK."*
> Yani karar ya uygulanmamış ya geri alınmış — **hiçbir yerde yazmıyor.**
> DO bugün prod'a çıksa kanona uyup tag atar.
> **Karar Mert'te:** kanon mu düzeltilecek, karar mı geri alınacak?

# Karar — release tag sistemi kaldırılıyor

**Tarih:** 2026-08-05
**Karar veren:** Mert
**Kapsam:** prod release akışı (tüm projeler)

## Karar

Prod çıkışında `vX.Y.Z` release tag'i atılmayacak. Tag adımı akıştan çıkıyor.

Mert'in cümlesi: *"Clara ben bu tag sistemini hiç sevmedim"*, ardından
*"tag sistemini kaldıralım."*

## Gerekçe — bugün ölçüldü

EGELI'de `v1.3.3` tag'i canlı olarak izlendi (2026-08-05, 15:52-16:56):

**Tag prod'a çıktıktan SONRA atıldı.** PR #178 canlıya çıkmıştı; PA sonradan
tag'in atılmadığını fark etti ve DO'ya handoff yazdı. Yani tag *"bu sürümde ne
var"* sorusuna cevap vermiyor — o cevabı PR zaten veriyor.

**Beş adım, sıfır bilgi kazancı.** Mert tag'i istedi → PA kendi yetkisinde olmadığını
görüp DO'ya handoff yazdı → yeni oturum açıldı → DO `git push origin v1.3.3` için
izin bekledi → tag atıldı → DO→PA bilgi handoff'u → Mert onu da taşıdı.

**Tag'in tek gerçek işi rollback'e isim vermek, ama rollback SHA ile de çalışıyor.**
Aynı gün DO ve Mert zaten SHA konuştu (`df9b2ce`). Yani tag, SHA'nın yanına konmuş
ikinci bir isim: bakımı var, karşılığı yok.

## Kaybedilen

GitHub "Releases" sekmesi boş kalır. Sürüm listesi PR geçmişinden okunur.

Bu kabul edildi: PR başlığı + merge tarihi + değişen dosyalar tag'in taşıdığı
bilginin tamamını taşıyor, üstelik ek adım gerektirmeden.

## Yürürlük

Bu karar bu odanın kaydı; **kanon değişikliği değil.** Agent kanonunda (DO ve PA
tarafında) release/tag adımı yazılıysa çıkarılması gerekiyor ve o iş `agent-project`
hattında, PAM üzerinden yapılır. Devir bloğu yazılacak.

## Bağlam

Tag'i ilk isteyen de Mert'ti (aynı gün 15:52: *"tag'i sen at, v1.3.3"*). Yani karar
bir kuralın yanlışlığından değil, kuralın **maliyetinin ölçülmesinden** geldi — istek
verildi, akış izlendi, karşılığı görülmedi.

Ölçümün tam kaydı: `gunluk/2026-08-05.md` (EGELI tag turu).
