# Arama disiplini: grep mi vektör mü, ve vektörün üç körlüğü

**Tarih:** 2026-08-06
**Karar:** Clara (ölçüme dayalı), Mert'in tetiğiyle
**Kanona giren yer:** `.claude/agents/clara.md` → "Kayıtlar" bölümü + yeni "Ararken"
alt bölümü

## Neden bu kanon değişikliği yapıldı

Mert'in tarifi: *"sen hepsini dosya gibi atarsan olmaz, kendine göre anlamlı
gruplayarak ve kategori ederek yüklemen lazım... doğru kayıt yöntemini bulana kadar
kayıt etmen lazım ki en iyi indekslediğini netleştirip kurala çevirelim."*

Yani ölçümün amacı baştan kural üretmekti. Beş kayıt biçimi, dört ayrı ölçüm koşuldu;
ölçümün tamamı `incelemeler/qdrant-kayit-bicimi/kayit.md`'de.

## Kanona giren üç şey

**1. Bir kayıt geçersizleştiyse durum bilgisi kaydın İÇİNE yazılır.**

Haritaya yazmak yetmiyor. Ölçüldü: `skill-preload-bulgusu` `HARITA.md`'de *"eskimiş
olabilir"* etiketliydi ve vektör aramada **birinci** geldi (0.670); çözümün yazılı
olduğu taze kayıt ikinci kaldı (0.651). Etiket haritadaydı, kaydın metninde değildi.

Sebep yapısal: benzerlik anlamı ölçer, doğruluğu ölçmez. Eskimiş kayıt soruya daha
benzer çünkü sorunu ayrıntılı anlatıyor.

**Bu kanondaki mevcut kuralın boşluğunu kapatıyor.** Kanon zaten *"eskimiş olabilir
bir kayda dayanmadan önce kontrol edilir"* diyordu — ama o kuralın işlemesi için
etiketin görünmesi gerekiyor ve aramada görünmüyordu.

**2. grep / vektör ayrımı.**

- **Bilinen kelime, ad, ID → grep.** Beş arama 0.041 sn. Vektör bunu yapamıyor:
  *"preload arızası"* tam adıyla arandı, ilk beşte o dosya hiç çıkmadı.
- **Kelimeyle söylenemeyen niyet sorusu → vektör.** *"Neyi yanlış ölçmüşüm daha
  önce"* — grep'in tutunacağı kelime yok.
- **Liste sorusu → ikisi de değil.** *"Hangi kararlar 5 Ağustos'ta verildi"* → beş
  sonuç üç dosyadan, parçalar halinde. `ls kararlar/` cevaplar.

**3. Vektör çıktısı cevap değil ADRES; sıralamaya güvenilmez, daraltılır.**

Skor alakayı ölçmüyor. İki kanıt:

- Alakasız soru (*"2024 Formula 1 şampiyonu kim"*) **0.507**, gerçek soru
  (*"preload arızası nedir"*) **0.564**. Aralık 0.057, ve MCP skoru hiç göstermiyor.
- Filtre ölçümünde doğru cevap **0.534**, üstündeki yanlış **0.581**.

Filtre isabeti 5/7'den 7/7'ye çıkardı ama **doğruyu yukarı çıkarmadı — üstündeki
yanlışları kaldırdı.** Bu ayrım önemli: çözüm sıralamayı iyileştirmek değil, arama
alanını daraltmak.

## Kayıt biçimi kuralları (ölçülmüş, kanona girmedi — inceleme dosyasında)

Bunlar kanona yazılmadı çünkü Qdrant kalıcı kullanılacak mı henüz karar değil. Karar
verilirse kanona ya da bir skill'e taşınır.

- **QK-1** anlam birimine böl, 1400 karakter üstünü paragraf sınırından ayır, her
  parça kendi başlığını taşır (model 514 token'da doyuyor). Ölçüm: 4/10 → 9/10.
- **QK-2** aranan metne ek yazma; kategori/tarih/konu payload'a gider. İki bağımsız
  ölçüm aynı sonucu verdi (öz ekleme ve kategori ekleme, ikisi de düşürdü) —
  mekanizma sinyal seyreltmesi.
- **QK-3** türü biliyorsan filtre koy (5/7 → 7/7).

## Açık kalem — Mert'in kararı bekliyor

Filtre tek işe yarayan iyileştirme ama **MCP desteklemiyor** (`qdrant-find` yalnız
`{collection_name, query}` alıyor). Üç yol:

**(a)** Artımlı indeksleme yazılır, arama script'ten yapılır; MCP yalnız yazma için.
**(b)** Filtre destekleyen başka bir MCP sunucusu bulunur (araştırılmadı).
**(c)** Vektör bırakılır; grep + `HARITA.md` yeter — bu odada günde ~5-10 arama var.

Ek olarak: **473/797 kayıt tarihsiz**, yani tarih filtresi bugün yarım çalışıyor ve
filtre koyulduğunda o kayıtlar sessizce düşüyor.

## İlgili kayıtlar

- Ölçümün tamamı: `incelemeler/qdrant-kayit-bicimi/kayit.md`
- Dünkü boyut kararı: `kararlar/2026-08-05-qdrant-mcp-ayri-alan.md`
- Aynı gün kanona giren ikinci değişiklik:
  `kararlar/2026-08-06-plan-task-kosum-sirasi.md`
