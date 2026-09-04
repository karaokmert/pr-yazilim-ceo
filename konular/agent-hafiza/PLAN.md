# Agent hafızası — kurulum planı

Tarih: 2026-09-04 · Durum: Mert onayı bekliyor
Zemin kararı: Coolify (bkz. `konular/altyapi/kararlar/2026-09-04-arac-sunucusu-zemini-coolify.md`)

---

## Aşama 1 · Sunucu kurulumu — Coolify paneli (birlikte)

**1.1** Coolify'da "hafiza" için yer açılır (proje/environment).

**1.2 Qdrant kurulur** — resmi image (`qdrant/qdrant`), kalıcı disk bağlanır
(kayıtlar container silinse de yaşar), API anahtarı konur.
*Doğrulama:* VPN içinden sağlık ucu cevap veriyor mu.

**1.3 Çevirmen kurulur** — TEI image (CPU sürümü), model:
`intfloat/multilingual-e5-base`. Kalıcı disk bağlanır — model bir kez iner,
yeniden başlatmada tekrar inmez (bilgisayardaki cache derdinin sunucuda
tekrarlanmaması bu satıra bağlı).
*Doğrulama:* tek istekle "merhaba" gönderilir, sayı listesi dönüyor mu.

**1.4** İki servis de dışa kapalı — erişim yalnız VPN içinden.

Tahmin: yarım saatlik panel işi. İkimiz birlikte: sen panelde, ben adım adım.

---

## Aşama 2 · Fork düzeltmesi — `karaokmert/qdrant-mcp` (birlikte)

**2.1** Çevirmen adresi ayarlanabilir yapılır — bugün OpenAI'ye sabitlenmiş
(`embeddings/openai.py:37`); env değişkeni eklenir, bizim sunucuyu gösterir.

**2.2** e5 işaretleri eklenir — kaydederken metnin başına `passage: `,
ararken `query: `. Konmadan da çalışır ama arama kalitesi sessizce düşer;
o yüzden bu adım atlanamaz.

**2.3** `.env.example` yeni ayarlarla güncellenir.

İş bölümü: ben yazarım → değişikliği satır satır sana gösteririm → push senin.

---

## Aşama 3 · Uçtan uca doğrulama

**3.1** Bilgisayardan MCP ile bir cümle kaydedilir, **farklı kelimelerle**
aranır — anlam araması testi (örn. "fatura kesemedim" kaydet, "ödeme belgesi
düzenlenemedi" ile ara).

**3.2** Kanıtın kapsamı yazılır: çevirinin sunucuda koştuğu ayrıca doğrulanır
(bilgisayarda model yok — asıl vaat bu).

---

## Aşama 4 · "Hafızaya ne yazılacak" kararı — ayrı konuşma

Kutu boş başlar. Hangi agent, hangi koleksiyona, neyi, ne zaman yazar/okur —
bu Mert'le ayrı bir masada. Geçen Qdrant denemesi bu soru cevapsız kaldığı
için ölmüştü; bu sefer kurulumdan sonra ilk iş bu.

---

## Bu planda OLMAYANLAR

- K8s / altyapı değişikliği — ayrı karar, kapandı (Coolify kalıyor).
- Müşteri projelerine dokunuş — yok.
- Agent kanonlarına "hafızayı kullan" kuralı — Aşama 4'ten önce yazılmaz.
