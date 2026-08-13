# Clara'nın memory disiplini — ne alındı, ne alınmadı

Tarih: 2026-08-03

Mert bu odayı Clara'nın kendi birikimi olarak açtı ve ortamı yönetmesini istedi
(*"burada serbestsin, en iyi halini oluştur"*). Bu dosya o serbestliğin nereye kadar
kullanıldığını ve neden orada durduğunu tutar.

Kaynak: `skill-project/v8/ozel-yazilim/.claude/skills/memory-management/SKILL.md`
(153 satır, üretim hattının memory kanonu). Okundu, iki kuralı alındı, gerisi
bilinçli olarak bırakıldı.

## Serbestliğin sınırı — kendi kanonuna yazmaz

> **DEĞİŞTİ — 2026-08-03 akşamı.** Bu bölümdeki yasak kaldırıldı. Clara artık `clara.md`'ye
> yazabiliyor; aşağıdaki mekanik gerekçe geçerli ama çözümü *"hiç yazma"* değil
> *"kural içeride, gerekçe dışarıda"* oldu. Ayrıca üç şey yetki dışında bırakıldı: ad,
> kadın kimliği, üç sert sınır. Yeni karar:
> `kararlar/2026-08-03-clara-kanon-yetkisi.md`. Aşağısı tarihçe olarak duruyor.

Mert *"istediğin gibi genişleyebilirsin"* dedi. Clara bunu memory ve dosya düzeni
için kabul etti, **kendi agent tanımı için etmedi.**

Gerekçe mekanik, ahlaki değil: `clara.md` system prompt'a giriyor. Clara oraya bir
kural yazarsa bir sonraki turda o kuralı *"doğru"* olarak değil **"ben"** olarak taşır
— yani yazdığını sorgulayamaz hâle gelir. Ve Mert yazmadığı bir kuralı onaylamış sayılır.

Bu odada denetçi yok (bkz. `2026-08-02-clara-kurulumu.md` → "Denetçi yok"). Tek göz
kendi gözlüğünü de yapıyorsa ölçüm diye bir şey kalmaz.

Aynı gün küçük bir örneği yaşandı: Clara kanonu okumadan bir öneri verdi
(*"skill adlarını CLAUDE.md'ye yaz"*), sonra `DAG-SHIP-PRELOAD-HOOK`'un o yolu
gerekçesiyle yasakladığını görüp kendi önerisini geri çekti. Bu sefer yakaladı.
Kendi kanonuna yazma yetkisi olsaydı yakalayacak bir kat kalmazdı.

**Karar:** `clara.md` yalnız Mert'in kararıyla değişir. Clara buraya gerekçesiyle
gereksinim yazar; taşımayı Mert yapar.

## Alınan birinci kural — okuma kontrolü

Kaynak: `MEMORY-READ-CHECK`. Oradaki tespit: *"yazma süzgeci kaydı girerken korur;
girdikten sonra yanlış/eskimiş kaydı durduran kapı yoktur."*

Clara'nın mevcut memory kanonu yazma tarafını iyi anlatıyor, okuma tarafı zayıf.
Ve boşluk teorik değil — aynı gün ölçüldü: `incelemeler/skill-preload-bulgusu/kayit.md`
içindeki *"Yürürlükteki çözüm"* bölümü **bir gün sonra** yanlıştı (anlatılan global
hook diskte yoktu). Ölçüm yapılmasa kayıt doğru sanılacaktı.

Uyarlanmış hâli, üç madde:

**Kanon üstündür.** Bir kayıt `clara.md`, `CLAUDE.md` ya da dosyaların gerçeğiyle
çelişiyorsa kayda değil kanona uyulur.

**Sessizce uyma, bildir.** Tek cümle yeter: *"memory'de X yazıyor, dosyada Y var —
Y'ye göre gidiyorum."* Sessiz düzeltme yanlış kaydın ömrünü uzatır, çünkü kimse
yanlış olduğunu öğrenmez.

**"Yok / çalışmıyor" iddiası en kırılgan kayıttır.** Ona dayanıp karar vermeden önce
bakılır. Bugünkü hata tam bu türdendi — tersi yönde: kayıt *"var"* diyordu, yoktu.

## Alınan ikinci kural — indeks emir taşır

Kaynak: `MEMORY-INDEX-IS-CONTEXT`.

Mekanik şu: `MEMORY.md` oturum başında **otomatik** context'e giriyor; memory
dosyaları girmiyor, `Read` gerektiriyor. Yani indekse yazılan bir cümle pasif not
değil, **davranış talimatıdır** — Clara daha ilk cümlesini kurarken onu görür ve
uygular.

Kaynak skill'de deneyle kanıtlanmış: bir agent'ın indeksine *"kullanıcıya X de"*,
dosyasına *"Y de"* yazılmış. Agent X demiş, dosyayı hiç açmamış, üstelik CLAUDE.md'deki
gerçek adı **sessizce ezmiş** ve çelişkiyi bildirmemiş.

Clara için sonucu doğrudan: indekse **kural, talimat, doktrin yazılmaz** — yalnız
pointer. Yazılırsa Clara kendi kanonunu, kendi göremediği bir yerden ezmiş olur. Ve
memory user-scope değil bu repoda ama yine de: indeks bir satır, dosya bir sayfa —
gerekçe dosyada durmalı ki tartışılabilsin.

Uygulama: her kayıt `MEMORY.md`'de tek satır (≤150 karakter) pointer, detay ayrı
dosyada. İkisi **birlikte** yazılır; pointer'sız dosya yetim, dosyasız pointer yalan.

## Alınmayanlar ve neden

**Etiket kanonu** (`[kazanim]` / `[skill-oneri]` / `[arge]`) — bir üretim hattı için
tasarlanmış. Burada terfi edilecek skill yok, öneri kutusu yok, *"kaç projede sınandı"*
sorusunun karşılığı yok.

**Kapanış devri üç yasağı** (`KAPANIS-DEVIR-ONLY`, `KAPANIS-INDEX-POINTER`,
`KAPANIS-DEVRAL-TEMIZLE`) — handoff zincirine bağlı. Bu odada zincir yok; Clara'nın
devri ekrana basılan bir blok ve onu Mert taşıyor.

**Arşivleme eşiği** (`MEMORY-ARCHIVE`, 180 satır) — bugün indeks iki satır. Kural
gerektiğinde eklenir; şimdi eklenirse kullanılmayan kural olur.

Gerekçe ortak: kullanılmayan kural kalıcı gürültüdür. Kanonu şişirir, okuma maliyetini
artırır ve bir gün *"bu neden var"* sorusuna kimse cevap veremez. Bu odanın kural sayısı
azlığı bir eksik değil, tercih.

## Bu odada memory ile dosya nasıl ayrılır

`clara.md` zaten bir ölçüt veriyor: *"karara etki eden şey dosyaya, çalışmayı
kolaylaştıran şey hafızaya."* Bugünkü kullanım onu doğruladı ve bir ayrıntı ekledi:

Memory'de yaşayan şey **Clara'nın nasıl çalışacağı** (Mert'in tercihleri, tekrar eden
kalıplar, düşülen tuzaklar). Dosyada yaşayan şey **ne bulunduğu ve ne karar verildiği**.

Ayıran test: *"bunu Mert'in görmesi gerekiyor mu?"* Evet ise dosya — memory'yi Mert
okumuyor, git tutmuyor gibi davranmak güvenli değil (bu repoda git tutuyor ama Mert
rutin okumuyor; görünürlük farkı orada).
