# Qdrant MCP: bu oda ayrı bir vektör alanı kullanır

**Tarih:** 2026-08-05
**Karar:** Mert

## Karar

`pr-yazilim-ceo` odasının Qdrant MCP'si **768 boyutlu, kendi collection'ında** çalışır.
Buradaki notlar sunucudaki mevcut 1024 boyutlu ekosisteme **katılmaz** — ekibin
aramasında çıkmaz, çıkması da istenmiyor.

Bu bir eksiklik değil, düzenin kendisi. Yeni düzen bu.

## Neden bu soru çıktı

Sunucuya (`qdrant.prventurestudio.com`) bağlanınca 43 collection göründü ve
neredeyse tamamı **1024 boyutlu** — isimlerinde bile yazıyor: `pr-clara-1024`,
`pr-backend-1024`, `mert-personal-1024`, `*-personal-1024`. Standardın kaynağı
büyük olasılıkla `pr-yazilim-bge-m3` collection'ında görünen **BGE-M3** modeli.

MCP'nin embedding motoru FastEmbed ve **FastEmbed BGE-M3'ü desteklemiyor** (dense
model listesinde yok, ölçüldü). Yani MCP o ekosisteme teknik olarak katılamıyor.

## Neden 1024'e çıkmak çözüm değil

FastEmbed'in 1024 boyutlu modelleri var (`multilingual-e5-large`, `jina-v3`,
`snowflake-arctic-embed-l`...). Ama **aynı boyut aynı model demek değil.**
Farklı bir modelin ürettiği 1024'lük vektör, BGE-M3'ün vektörüyle aynı uzayda
durmuyor. Sayı uyuşur, anlam uyuşmaz.

Bunun tehlikeli tarafı: bu durumda arama **hata vermez.** Sessizce alakasız
sonuç döner. Uyumsuzluğun görünmez olması, uyumsuzluğun kendisinden kötü.

## Kararın sonuçları

**Kabul edilen:** Buradaki notlar ekibin araçlarından aranamaz. Clara'nın
biriktirdiği şey bu odada kalır.

**Kazanılan:** Ham düşünce ekibin arama sonuçlarını kirletmez. Bu odanın işi
olgunlaşmamış fikri konuşmak; olgunlaşmamış fikrin ekibin önüne çıkması
CLAUDE.md'deki "netleşmeden önce bir yer gerekiyordu" gerekçesine aykırı olurdu.

**Değişirse ne olur:** İleride "Clara'nın notları ekipte de çıksın" istenirse
bu MCP o işi yapamaz. O zaman BGE-M3 üreten sistem bulunur ve ona bağlanılır —
mevcut 1024'lük collection'ları dolduran araç zaten var, kim/ne olduğu
araştırılmadı. Bu karar değişirse buraya neden değiştiği yazılır.

## Kurulumun teknik izi

Yapılandırma `.mcp.json`'da (gitignore'lı — JWT düz duruyor), şablonu
`.mcp.json.example`'da. Kurulum notları şablonun `_kurulum` bloğunda.

Yol boyunca çıkan üç bulgu:

**Model `/tmp`'ye iniyordu.** FastEmbed varsayılanı `tempfile.gettempdir()` —
macOS'ta `/var/folders/.../T`. Reboot'ta silinir, MCP her açılışta 1 GB'ı
~4 dakika yeniden indirir ve bu "sunucuya bağlanamadı" gibi görünür.
`FASTEMBED_CACHE_PATH=~/.cache/fastembed` ile sabitlendi.

**URL'de `:443` şart.** Port yazılmazsa `qdrant-client` varsayılan 6333'e gidiyor;
Cloudflare o portu proxy'lemediği için "No route to host" alınıyor.

**Cloudflare sorun değildi.** `urllib` ile yapılan istekler Cloudflare bot
korumasına takılıp `error code: 1010` alıyordu, ama `qdrant-client` sorunsuz
geçiyor. WAF kuralına ya da proxy kapatmaya gerek olmadı — SSL olduğu gibi kaldı.
İlk teşhis (Cloudflare'ı suçlamak) eksikti; iki istemciyi ayırt etmek gerekiyordu.

**Doğrulama:** Bağlantı kuruldu, geçici bir collection oluşturuldu, 4 Türkçe not
yazıldı, üç farklı soruda üçünde de doğru not birinci sırada geldi (sorular
notların kelimelerini kullanmıyordu). Test collection'ı silindi.

## Açık kalem

Token **2026-08-12** tarihinde doluyor ve ölüşü sessiz olacak — MCP 403 alır,
"bağlanamadı" gibi görünür. Kalıcıya geçilirken süresiz üretilmeli ve yetki
Managed Access'ten **Global Access**'e düşürülmeli: MCP'nin collection
oluşturması gerekiyor (Collection Access yetmiyor) ama silme yetkisine
ihtiyacı yok.
