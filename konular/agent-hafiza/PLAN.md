# Agent hafızası — kurulum planı (v2)

Tarih: 2026-09-04 · Resim Mert onaylı ("aynen süperiz")
Kimlik: **PR Venture Studio'nun ilk AI altyapı servisi** — `rag.prventurestudio.com`
Gereksinim ve ufuk: `BILINMESI-GEREKENLER.md` · Zemin: Coolify/EX44 (karar dosyası altyapı konusunda)

---

## Aşama 1 · Servisleri ayağa kaldırmak (Mert panelde, Clara yanında)

**1.1 Qdrant** — katalog şablonundan kuruldu/kuruluyor. Kontroller:
- Image `latest` değil sabit sürüm: `qdrant/qdrant:v1.19.0` (wg-easy dersi:
  şablon + latest ikilisi sessiz kırılma üretir).
- Volume `/qdrant/storage` ✓ · `QDRANT__SERVICE__API_KEY` ✓ (değer 1Password'e).
- **Adres:** `rag.prventurestudio.com` — Mert'in kararı: servis domain'le açılır,
  VPN-only değil.

**1.2 DNS + SSL** — tools.pryazilim.com dersi uygulanır:
- A kaydı `rag.prventurestudio.com` → 65.109.150.95, önce **DNS-only** (gri bulut).
- Coolify domain alanına `https://rag.prventurestudio.com` → Let's Encrypt
  sertifikayı kendisi alır.
- Cloudflare proxy'si sonradan açılacaksa önce SSL modu **Full (strict)**.
- HTTPS geldiğinde "API anahtarı şifresiz gidiyor" riski kapanır.

**1.3 Çevirmen (TEI)** — ikinci servis: `text-embeddings-inference` (CPU imajı,
v1.9.3), model `intfloat/multilingual-e5-base`, model cache'i için volume.
Anahtar: TEI'nin kendi `API_KEY` env'i var (Bearer token ister) — 2026-09-04'te
README'den doğrulandı; Clara'nın "anahtar desteği yok" ön bilgisi YANLIŞTI,
düzeltildi. Domain'le açılır + anahtar zorunlu.

**1.4 Sağlık testleri** — Qdrant: `/healthz` · TEI: tek cümle çevirisi.
Her testte neyin kanıtlandığı yazılır.

⚠️ **AÇIK İŞ (Mert'in kararı):** güvenlik sıkılaştırma (VPN/erişim daraltma)
kurulumlar bitince. Kapanınca buraya KAPANDI notu düşülür.
Güncelleme 2026-09-04 12:48: HTTPS + API anahtarı devreye girdikten sonra
Mert gerçek kayıtlarla (Clara'nın karar/hafıza içeriği) büyük test kararı
verdi — bilinçli risk kabulü; hassas olmayan iç know-how sınıfı veri.

---

## Aşama 2 · Fork düzeltmesi — `karaokmert/qdrant-mcp` (birlikte)

- Çevirmen adresi env'den (bugün `embeddings/openai.py:37` OpenAI'ye sabit).
- e5 önekleri: kayıtta `passage: `, aramada `query: `.
- `.env.example` güncellenir.
- İş bölümü: Clara yazar → satır satır gösterir → push Mert.

---

## Aşama 3 · Uçtan uca doğrulama

- Bir cümle kaydet, FARKLI kelimelerle ara (anlam testi).
- Çevirinin sunucuda koştuğu ayrıca kanıtlanır (bilgisayarda model yok).

---

## Aşama 4 · Pilot: Clara

- Clara'ya koleksiyon açılır; hibrit düzen: `MEMORY.md` indeks lokalde
  (hızlı kayıtlar + koleksiyon işaretleri + arama kuralları), gövdeler merkezde.
- Kural sistemi OY `memory-management` skill'inden uyarlanır.
- Beğenilirse → **fabrikaya talep:** memory-management + settings skill'lerinin
  merkezi hafızaya uyarlanması, agent'lara yayılması (plugin kurulumunda API
  key + kendi koleksiyonunu açma akışı).

---

## Aşama 5 · Değer ölçümü

Bir ay kullanım: kim ne aradı, buldu mu, işe yaradı mı → devam / büyüt / kapat.
Ufuk: ürün altyapısı — ilk test adayı Keba AI bağlantısı (o gün tasarlanır,
bugün kurulmaz; Qdrant'ın anahtar+koleksiyon modeli kapıyı açık tutuyor).

---

## Bu planda OLMAYANLAR

- K8s / altyapı değişikliği (kapandı — Coolify kalıyor)
- Müşteri projelerine dokunuş
- Multi-tenant ürün altyapısı (kapı açık, inşaat yok)
- Agent kanonlarına hafıza kuralı (fabrika devrinden önce yazılmaz)
