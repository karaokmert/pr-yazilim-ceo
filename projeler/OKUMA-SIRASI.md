# projeler/ — ne nerede

Bu klasör iki tür bilgi taşıyor:

**`envanter.md`** — projelerin **künyesi** (2026-08-03). Hangi repo, hangi
teknoloji, canlı mı, sahibi kim. Dosya sisteminden çıkarıldı. Seyrek değişir.

**`agent-dagitim-yapisi.md`** — agent'ların diskteki dağıtımı (2026-08-03).

**`{proje}/DURUM.md`** — projenin **ClickUp'taki iş durumu**. Ne bitti, ne açık,
ne bloke, ne sahipsiz. ⚠️ Bir hafta içinde eskir; tarihi dosyanın başında yazılı.

---

## Klasörler

**Yoğun projeler:** `liston` · `goat` · `wupdoc` · `keba-erp` · `tpws`

**Orta:** `egeli` · `pr-studio` (üç müşteri: Tedrik, KaraokYMM, Efranca) ·
`gazi` · `pr-yazilim`

**Küçük / az kayıtlı:** `bt-products` · `platin` · `pr-template` · `tezcanun` ·
`marwell-alesta` · `adalya` · `websites`

---

## Bilinmesi gereken eşlemeler

Google Sheets'teki haftalık tablo ile ClickUp aynı adları kullanmıyor:

- **WD** = Wupdoc (ayrı proje değil)
- **TP** = TPWS, Keba folder'ının altında yürüyor (ayrı folder yok)
- **KebaTP** = ClickUp'ta böyle bir önek yok; iş TPWS adıyla yürüyor
- **Keba** folder'ında **iki ürün** var: KebaAI/ERP (Mert) ve TPWS (Didem)
- **Alesta** = Marwell folder'ında (marka dönüşümü sürüyor)
- **Marketing** folder'ı diye ayrı bir şey yok — o Gazi Hastanesi'nin kendisi
- **PR Studio** folder'ında üç müşteri var: Tedrik, KaraokYMM, Efranca
- **Adalya** folder'ı yok; işleri "Creative Projeleri" ve "Websites"e dağılmış

---

## 2026-09-02 ölçümünün ana bulgusu

**Haftalık plan ClickUp'tan bağımsız yaşıyor.** Sprint 7'nin 42 iş kaleminden
ClickUp'ta gerçek bir iş kaydı olarak duran üç tane: PRY-18084 (PR Template mobil
provision), PRY-18082 (GWS UI Düzenlemeleri), PRY-18046 (Efranca Revizeler).

Geri kalanı ya hiç yok, ya boş kabuk (Buse'nin dört başlığı: task var, açıklama
boş), ya da başka bir task'ın metninde (Wupdoc'un beş başlığı).

**Sprint listeleri boş** — ClickUp'ta Sprint 3'ten 8'e altı liste var, hiçbirinde
task yok. Sprint kaydı tutulmuyor; işler proje folder'larında yaşıyor.

**Sistemik sorunlar:** statü hijyeni bozuk ("completed" ≠ kapanmış, `date_closed`
boş) · kopya task birikiyor (Gazi'de altı kopya, ListON'da beş çift) · yüksek
öncelikli işlerin çoğu atanmamış · şemsiye task'lar altındaki bugfix'lere bağlı değil.

**Bu ölçümde yapılmayanlar:** task açıklamaları tek tek okunmadı (yalnız başlık,
statü, atama, tarih ve seçili birkaç açıklama) · koda bakılmadı (bir işin bitip
bitmediği ClickUp statüsünden okundu, commit’ten değil) · sprint eşlemesi
yapılamadı (listeler boş olduğu için "son 2-3 sprint" son güncellenme tarihinden
çıkarıldı — bu bir yaklaşım, sprint etiketi değil) · blokelerin sebebi
araştırılmadı.
