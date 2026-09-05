# Kayıt yöntemi deneyi — en iyi hafıza kayıt biçimini bulmak

Tetik: Mert, 2026-09-04 — "türlü türlü kayıt yap: dokümanı full kaydet, parçala,
cümle cümle yap; yüzlerce sına, doğruyu bul." Önceki hüküm-vs-blok ölçümü 16 soru
ve iki yöntemle dardı; kayıt biçimi burada sistematik yarışır.

## Korpus

149 hükmün kaynak adreslerinden repo'da mevcut **52 dosya** (~173 KB).
Bulunamayan 20 adres deney dışı (not: çoğu muhtemelen taşınmış/başka repo —
ayrı iş).

## Yöntemler (koleksiyon = yöntem, hepsi mE5-large, 1024, Cosine)

- `y-dokuman` — dosya olduğu gibi tek kayıt
- `y-paragraf` — boş satırdan bölünmüş saf paragraflar
- `y-paragraf-baslik` — paragraf + "dosya başlığı › bölüm başlığı" öneki
- `y-cumle` — cümle cümle
- `y-parca` — ~800 karakter + 150 bindirme (klasik RAG parçası)
- `y-hukum` — hafiza-large'dan, kaynağı bu 52 dosya olan hüküm kayıtları
  (vektörler kopyalanır, yeniden embed edilmez)

Her kaydın payload'unda `kaynak_adres` zorunlu — skorlama buna dayanır.

## Soru seti

Hükümleri HİÇ GÖRMEYEN ayrı bir agent, 52 dosyayı okuyarak üretir:
dosya başına 2–3 soru (~130 soru) + cevabı korpusta olmayan ~15 negatif kontrol.
Karışım: belirti dili / doğal kullanıcı dili / doğrudan bilgi / birkaç İngilizce
/ birkaç tek kelime. Soru dosya adını ya da yolunu İÇEREMEZ.
Çıktı: `sorular.jsonl` — {soru, beklenen_dosya|null, tip}.

Tuzak notu: sorular hükümden üretilirse hüküm yöntemi hileli kazanır —
soru üreticisi ile yöntem koşucusu ayrı eller.

## Ölçüm (kaynak bazlı — parça boyları farklı, kayıt bazlı kıyas adil değil)

Soru başına her koleksiyonda ilk 5 sonuç:
- hit@1, hit@5: doğru dosyadan gelen kayıt 1. sırada / ilk 5'te mi
- MRR (doğru dosyanın ilk görüldüğü sıranın tersi, ortalama)
- negatif sorularda ilk skor dağılımı (eşik bandı için)
- maliyet: koleksiyon kayıt sayısı + ilk-5 sonucun ortalama metin hacmi

## Görevler

- [x] Plan yazıldı
- [x] A: soru üretimi — 164 soru (59 belirti, 60 doğal, 24 anahtar, 6 İng, 15 negatif)
- [x] B: parçalama + yükleme — y-dokuman 52 · y-paragraf 833 · y-paragraf-baslik 833 · y-cumle 2521 · y-parca 268 · y-hukum 129
- [x] C: koşum + ham sonuç — kosum-sonuc.json / skor-sonuc.json; paragraf kazandı
      (hit@1 0.79 / hit@5 0.97), doküman sonuncu, hüküm keskin-ama-dar
- [x] Clara: hakemlik + sentez → ../TASARIM.md; bulgular clara-analiz koleksiyonunda (13 hüküm)
- [ ] Base-vs-large kapanış ölçümü: y-paragraf base ile yeniden kur, 164 soruyu koş
      (TASARIM.md model kararı bunu bekliyor — y-* koleksiyonları O YÜZDEN duruyor)
- [ ] Temizlik: y-* + clara-1/2 + test-hafiza koleksiyonları, base ölçümü bitince

## Dokunulmayan

`hafiza` (base, canlı) ve `hafiza-large` koleksiyonlarına yazılmaz;
y-hukum onlardan yalnız OKUR.
