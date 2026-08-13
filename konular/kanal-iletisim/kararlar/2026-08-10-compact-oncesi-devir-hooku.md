# Compact öncesi devir hook'u — Mert'in kararı

**Tarih:** 2026-08-10 11:47 · **Karar:** Mert · **Durum:** karar verildi, üretilmedi

---

## Karar

**Compaction'a girmeden önce tetiklenen bir hook yazılacak. Agent compaction'a
girdiğinde işi kesip devir dokümanına geçecek.**

Yani compaction bir **kayıp anı** değil, bir **kapanış sinyali** olarak kullanılacak.

---

## Gerekçe — Mert'in cümlesi

> *"Uzun oturumlar olmasın diye agent'ları bu kadar bölüyoruz zaten."*

Bu, bugün kapatılan compaction tartışmasının doğru çerçevesi. Ben *"kanon eşiğe
sığmıyor, ne yapalım"* diye sordum ve üç seçenek sundum — üçü de **kanonu** değiştirmeye
bakıyordu (böl · eşiği kabul et · yeniden yükle).

**Mert dördüncü yolu gösterdi: oturumu değiştir.** Kanon eşiğe sığmıyorsa sorun kanonda
değil, **oturumun o kadar uzamasında.** Ve ekip zaten bu yüzden dokuz role bölünmüş —
her rol kendi işini yapıp devrediyor, tek bir agent baştan sona koşmuyor.

---

## Ne çözüyor

**Bir — kesilen kural sorunu ortadan kalkıyor.** Bugün ölçülen arıza şuydu: `behavior`
20.032 karakter, eşik ~16.000, ve **düşen bölümler tam da işin sonunda lazım olanlardı**
(memory, devir, iş sonu raporu). Zamanlama ters çalışıyordu — kural, ihtiyaç duyulacağı
anda kayboluyordu.

Hook devreye girerse **compaction hiç olmuyor**: agent o noktaya gelmeden devri yazıp
kapanıyor.

**İki — devir disiplinini mekanik hâle getiriyor.** Bugün `dizin-uret.py` için bulduğum
zayıflığın aynısı burada da vardı: talimat yazılı ama **çalıştırılması hatırlamaya
bağlı.** Hook hatırlamayı ortadan kaldırıyor.

**Üç — `URT-HOOK-WHEN-DETERMINISTIC`'e uyuyor.** Fabrikanın kendi kuralı: deterministik
bir olay hook'a aday. *"Context şu eşiğe geldi"* deterministik bir olaydır.

---

## Üretim öncesi ölçülecekler — cevabı bende yok

**Böyle bir tetik var mı?** Claude Code'un compaction öncesi bir hook noktası sunup
sunmadığı **ölçülmedi.** `SessionStart`, `UserPromptSubmit` gibi kayıtlar biliniyor;
`PreCompact` benzeri bir kayıt var mı bakılacak.

**Eşik nereden okunacak?** Hook'un *"compaction yaklaşıyor"* bilgisini nereden alacağı
belirsiz — context doluluğu agent'a görünüyor mu, yoksa dışarıdan mı ölçülecek.

**Devir dokümanı nereye yazılacak?** Kanal kutusuna mı, `docs/` altına mı, ikisine de mi.
Ve **yarım kalan iş** devrinde ne yazılacağı normal kapanıştan farklı — *"iş bitti"*
değil *"iş burada kaldı"*.

**Kim üretecek:** fabrika (PAD). Bu bir hook ve hook üretimi `dagitim`/`uretim`
kanonuna tabi.

---

## Sınırı

**Bu karar bugün üretilmiyor.** Pilot rol tamamlandı ve denetimden geçti; bu kalem
**kalan sekiz rolle birlikte** ya da ayrı bir iş olarak ele alınacak.

**Ve bugünkü compaction kararını geçersiz kılmıyor:** `behavior`'ın 6 kimliği kesme
noktasının dışında kalıyor ve bu **bilinçli kabul edilmiş** bir maliyet olarak duruyor.
Hook geldiğinde o maliyet de düşer — ama hook gelene kadar kabul edilmiş durumda.
