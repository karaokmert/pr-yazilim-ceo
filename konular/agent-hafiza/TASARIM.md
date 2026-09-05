# PR Yazılım Hafıza Sistemi — Tasarım

Yazan: Clara, 2026-09-05. Dayanak: iki günlük iç ölçüm (16-soru model kıyası,
164-soru × 6-yöntem kayıt deneyi, kanal testi) + dört hatlı literatür taraması
(parçalama · güncel tutma · arama kalitesi · Mem0/Letta/Zep). Araştırma raporları
sub-agent çıktısı olarak bu oturumun kaydında; kaynak linkleri raporlarda.

Bu bir seçenek listesi değil tasarımdır — kararlar verilmiştir, her kararın
gerekçesi yanında. İtiraz edilen karar değişir; edilmeyeni uygulamaya alırım.

---

## Mimari: tek koleksiyon, iki katman

Hafıza tek koleksiyonda (`hafiza`) yaşar; kayıtlar `katman` alanıyla ayrışır:

**Hüküm katmanı** (`katman: hukum`) — agent'ın elle damıttığı kısa kayıtlar:
karar, ders, tercih, kapanış. Bugünkü sistem. Keskin ama dar: iç ölçümde bulduğu
soruda hep 1. sırada, kapsamadığı soruda hiç yok.

**Doküman katmanı** (`katman: dokuman`) — repo'daki markdown dokümanların
paragraf bazlı otomatik indeksi. Kapsamayı bu verir: 164-soru deneyinde paragraf
hit@5 0.97 ile tüm yöntemleri geçti. "Memory pointer olmuş" arızasını da kökünden
kapatır — metin hafızanın içinde, dosya yalnız köprü.

Tek koleksiyon kararının sebebi: iki katman aramada doğal yarışır — hüküm varsa
zaten üste çıkar (ölçüldü), yoksa paragraf yakalar. Ayrı koleksiyon her soruya
çift arama maliyeti bindirir ve MCP tek-atış mimarisine ters.

Literatür karşılığı: ham + damıtılmış iki-katman deseni Mem0 (mesaj/olgu),
Zep (episode/entity) ve Letta'da (archival/core) aynen var — sektörün yakınsadığı
yapı bu. Bizim farkımız damıtmanın elle (agent bilinçli) yapılması; Mem0
kayıtlarının %97.8'ini junk bulan kullanıcı denetimi, otomatik damıtmanın kalite
garantisi olmadığını gösteriyor — elle damıtma savunulabilir.

## Yazma metodu

### Doküman katmanı — otomatik indeksleme hattı

**Birim: başlık-bağlamlı paragraf.** Boş satırla bölünen paragraf; başına
`{dosya H1} › {en yakın bölüm başlığı}: ` öneki eklenerek embed edilir.
Gerekçe: paragraf iç ölçümde kazandı (hit@1 0.79; Vectara NAACL-2025 ve
FloTorch-2026 bağımsız aynı sonuçta: ince parçalama isabeti düşürür); başlık
öneki literatürde ölçülmüş kazanç (ECIR 2026: prefix-as-text baseline'ı tutarlı
geçiyor) ve Anthropic Contextual Retrieval'ın sıfır-LLM-maliyetli yaklaşığı.
İç ölçümde saf paragraf hit@5'te önekliyi hafif geçti (0.97/0.93) ama korpus
büyüyüp çapraz-proje olunca "hangi dokümanın parçası" bilgisi ayrıştırıcı olur —
öneki alıyorum.

**Boy kuralı:** 40 karakterden kısa blok öncekine yapışır; ardışık kısa
paragraflar ~400 token'a kadar birleştirilir. (Literatür optimumu ~512 token;
bizim paragraflar küçük kalırsa küçük-chunk tuzağına düşeriz — FloTorch'ta
43-token'lık fragmanlar end-to-end doğruluğu %54'e düşürdü.)

**Önek zinciri:** embed girdisi = `passage: {başlık zinciri}: {paragraf}` —
e5 öneki en dışta, zorunlu (model kartı: öneksiz performans düşer; MCP fork'u
hüküm tarafında bunu zaten ekliyor, indeksleme scripti de ekler).

**Payload:** content (öneksiz paragraf) · kaynak_adres · basliklar (zinciri) ·
katman: dokuman · git_sha · chunk_hash · sira.

**Kapsam:** başlangıçta `pr-yazilim-ceo/konular` + `kararlar` (mevcut 52+
dosya); proje repoları katman kanıtlanınca eklenir.

### Hüküm katmanı — yazma anı disiplini

Bugünkü şema kalır (içerik = belirti dilinde hüküm; metadata: tur, proje,
yazan, tarih, detay, iliskili) + iki değişiklik ve bir düzeltme:

**Düzeltme — `kaynak_adres` yerine `kaynaklar` (liste):** kaydın GERÇEK
dayanakları — iç ölçüm dosyası, dış literatür linki. Üretilen sentez dokümanı
(TASARIM.md gibi) kaynak sayılmaz: o hükümlerden türer, hükümler ondan değil —
döngüsel atıf pointer alışkanlığının geri dönüşüdür (Mert yakaladı, 2026-09-05).

**1. Yazmadan önce komşu kontrolü mekanikleşir** (Mem0'ın ADD/UPDATE/NOOP
deseni, deterministik uyarlama): store'dan önce aynı konuda find; dönen ilk 5'te
mükerrer varsa yazılmaz (NOOP), çelişen varsa yeni yazılır + eski geçersizlenir
(UPDATE), yoksa yazılır (ADD). "Hangisi doğru" kararını LLM'e bırakmama ilkesi
literatürde ölçülü: deterministik seçim +10.8 puan (arXiv 2606.01435).

**2. `detay` alanı zorunlu** — kayıt kendi kendine yetmeli. kaynak_adres köprü,
dayanak değil. (Mevcut 149 detaysız kayıt: doküman katmanı gelince kaynak
paragrafları zaten hafızada olacak — geriye dönük detay dolumu GEREKMİYOR,
katman onun yerini alıyor. Bu, dün planlanan "detay doldurma" işini iptal eder.)

## Güncelleme metodu

**Geçersizleme payload'a taşınır.** Bugünkü içerik-damgası (`[GEÇERSİZ — yerine:
id]`) doğru fikir, yanlış katman — arama vektöre bakıyor, damgayı görmüyor
(ölçüldü: damgalı kayıt aramada yine 1. geldi). Yeni mekanizma: payload'da
`durum: gecersiz` + `yerine: <id>`; MCP find çağrısına varsayılan filtre
`must_not durum=gecersiz` (fork'ta küçük yama). İçerik damgası insan okunurluğu
için kalabilir ama mekanizma filtredir. Literatür karşılığı: Zep/Graphiti'nin
invalidate-don't-delete deseni; Mem0 bile 2026'da "asla üstüne yazma"ya döndü —
"eskiyen doğru silinmez" kararımız sektörün yakınsadığı yön.

**İki tarih tutulur** (Zep bi-temporal'in hafif hâli): `tarih` (kararın/olayın
günü) ve `kayit_tarihi` (yazım anı). "Bu karardan ne zaman vazgeçtik" sorusu
`yerine` zinciri + tarihlerle cevaplanır.

**Doküman katmanı git'le güncel kalır.** Registry (son indekslenen commit SHA —
Qdrant'ta tek meta-point); koşumda `git diff --name-only <SHA> HEAD` değişen
dosyaları verir; dosya içinde chunk_hash karşılaştırması (normalize içerik
SHA256) değişen/yeni/silinen paragrafı ayırır; yalnız değişen embed edilir,
silinen silinir. Literatür: LiveVectorLake deseni — %85-95 yerine %10-15
yeniden-işleme; git zaten içerik-adresli olduğundan bizde maliyeti sıfıra yakın.
Koşum tetiği: commit sonrası elle/hook ya da günlük — Faz 1'de script, tetik
kararı kullanımla.

**Bakım rutini** (Letta sleep-time deseninin bizdeki hâli): periyodik arka-plan
taraması — mükerrer hüküm ikizleri (ölçülmüş sorun: sıralamayı bölüyor),
kapanmış acik-is kayıtları, geçersizleme zinciri kopuklukları. Konuşma turunun
dışında, ayrı oturum/agent'la.

## Okuma metodu

**Tek arama, filtre serbest.** Agent `qdrant_find` ile arar; varsayılan filtre
yalnız `durum != gecersiz`. Katman filtresi zorlanmaz — hüküm ve paragraf
yarışır, en iyi kazanır.

**Skor eşiğiyle "cevap yok" kararı VERİLMEZ — bu kural kanona girer.** Sebep
yapısal: mE5 ailesi temperature=0.01 ile eğitilmiş, skorlar kasıtlı dar banda
sıkışıyor (model sahibinin açıklaması: "mutlak skor değil sıralama önemli").
Bizim ölçüm aynı şeyi gösterdi: doğrular 0.81-0.89, yakın-konu tuzaklar
0.83-0.86 — bant örtüşüyor, eşik imkânsız. Karar: tüketici agent ilk 5 sonucu
OKUR ve yeterliliğe kendisi hükmeder — MCP mimarisinde tüketici zaten LLM,
ayrı bir yargıç çağrısına gerek yok; kural "skora güvenme, içeriğe bak."

**Belirti dili sınırı kabul edilir ve yazma tarafında telafi edilir:** her
yöntemde en zayıf tip belirti diliydi (hit@1 0.64-0.66) — arama tarafında çözümü
yok; hüküm yazma kuralı "belirti diliyle yaz" (dünkü ders) tam bu boşluğu
dolduruyor, doküman katmanının paragrafları da doğal dilde olduğundan kısmi
kapsama veriyor.

## Model kararı

**Beklentim base'e dönüş; karar tek koşumluk ölçümle kapanır.** Large iki iç
ölçümde de base'i geçemedi (16-soru: 13/15 vs 15/15; skor marjı aynı) ve dar-bant
sorunu her iki modelde yapısal. Large'ın maliyeti gerçek: CPU'da yavaş, ~3×
model boyu. Kapanış ölçümü: 164-soru deneyinin paragraf koleksiyonu base ile
tekrar koşulur (~900 embed, ucuz); hit@1/hit@5 farkı anlamlı değilse TEI base'e
döner. (Reranker gelirse ilk-aşama modelinin önemi daha da düşer — literatür.)

## Fazlar

**Faz 1 — şimdi:** indeksleme scripti (başlık-önekli paragraf + git-registry)
· geçersizleme payload+filtre (fork yaması: varsayılan durum filtresi) ·
base-vs-large kapanış ölçümü · kanon güncellemeleri (skor-eşiği yasağı, yazma
öncesi komşu kontrolü, detay zorunluluğu).

**Faz 2 — katman kanıtlanınca:** reranker (bge-reranker-v2-m3, TEI ikinci
instance — literatürde en yüksek yatırım getirisi, ~120ms) · recency decay
(Qdrant formula query, kapanış gibi tarihli sınıflarda) · bakım rutini.

**Faz 3 — ihtiyaç doğarsa:** hybrid BM25 (ancak Türkçe kök/n-gram tokenizasyonla
— öneksiz BM25 aglütinatif dilde değersiz) · çapraz-proje kapsam genişletme.

**Ertelenen/elenen:** late chunking (Jina modellerine özgü, e5'e taşınmaz) ·
semantic chunking (iki bağımsız benchmark: maliyeti kazancı karşılamıyor) ·
HyDE/multi-query (reranker varken kazanç eriyor; MCP tek-atışa ters) · skor
kalibrasyonu (yorumu düzeltir, ayırt ediciliği artırmaz).

## Riskler ve açık uçlar

- Doküman katmanı koleksiyonu ~10-20× büyütür (52 dosya → ~800 paragraf;
  çapraz-proje ile binler). Qdrant'a dert değil; asıl izlenecek şey hüküm/paragraf
  karışımında hükmün üstte kalmaya devam edip etmediği — ilk ay ölçülür.
- Soru setimiz dosyalardan üretildi; doküman-dışı bilgiye giden soruların
  (konuşma hafızası) performansı ölçülmedi — hüküm katmanının asıl değeri orada,
  pilot kullanımda görülecek.
- VPN/güvenlik sıkılaştırma hâlâ bekliyor (Mert'in takvimi) — o kapanana dek
  hassas kayıt sınırı yürürlükte.
