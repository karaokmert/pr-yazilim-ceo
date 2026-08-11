---
name: cerceve-olcumden-belirleyici
description: Bir alt role verilen çerçeve, onun ölçümünden daha belirleyici — yanlış çerçeve doğru ölçümü boşa çıkarır (2026-08-11)
metadata:
  type: feedback
---

Bir agent'a iş verirken **çerçeve** (bu iş nedir, hangi kutuya girer, kime aittir)
onun **ölçümünden daha belirleyicidir.** Ölçüm doğru olsa da yanlış çerçeve sonucu
bozar.

**Why:** 2026-08-11'de Goat'ta PA'ya *"envanterde sprint dışı bir iş bulursan bana
bildir, kapsam kararı Mert'in"* diye çerçeve verildi. PA envanteri **doğru** çıkardı,
ayrımı **doğru** yaptı, çelişkiyi **görüp sordu** — ama sonuç yanlış kutuya girdi:
Buse'nin **teslim edilmiş işi** Mert'e *"kapsam genişletmesi onayı"* olarak sunuldu.
Oysa incelenmesi gereken bir teslimdi.

Yanlış olan tek şey Clara'nın verdiği çerçeveydi. Doğru ölçüm, yanlış kutu.

**How to apply:** bir agent'a iş verirken çerçevenin kendisini de ölç. Ayıran soru:
**bu işin ne olduğunu BİLİYOR muyum, yoksa VARSAYIYOR muyum?** Varsayıyorsan çerçeveyi
agent'a dayatma — ham durumu ver, sınıflandırmayı sor. Agent kodu okuyor; sen envanteri
okuyorsun.

⚠️ **Ve bunun tersi de doğru:** bir agent'a *"şunu ölç"* demek yerine *"şu ölçütü
kullan"* demek de bir çerçevedir — ve ölçüt zayıfsa ölçüm zayıf çıkar. Aynı gün ölçüldü:
Clara *"net negatif = zaman geri sarma riski"* ölçütünü verdi; FE iki deliğini buldu
(yanlış pozitif + yanlış negatif), PA iki delik daha buldu. Ölçüt **dört turda**
keskinleşti ve her iyileştirme bir **karşıt testten** çıktı, tahminden değil.

**Örüntü aynı gün beş kez tekrarlandı** ve her seferinde ölçüm kazandı: Clara'nın üç
çıkarımı (Buse'nin rolü · paket bölme ölçütü · net negatif) · PA'nın kendi envanteri
(ortak dosya 11 sanıldı, ölçümle 7) · BE'nin bir iddiası ("iki catch düzelttim", 8
duruyordu).

Genel kural: **mantıksal olarak temiz görünen bir çerçeve, fiziksel gerçeği ölçmez.**
Kod okumayan taraf çerçeve dayatmaz.

Bkz. [[ekip-disi-sanma]] — aynı vakanın kimlik tarafı.
Bkz. [[isi-dogrula-kodu-degil]] — rol çizgisi: teknik bulgu agent'ın, akış Clara'nın.
Bkz. [[iddiayi-tasima-olc]] — beyan taşımanın kardeş hatası.
