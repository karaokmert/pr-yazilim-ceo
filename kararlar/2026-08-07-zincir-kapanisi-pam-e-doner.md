# Karar: Zincir kapanışı PAM'e döner — döküman düzeltmesi ve push sırası

**Tarih:** 2026-08-07
**Karar veren:** Mert
**Kapsam:** `agent-project` fabrikası — ve emsal olarak diğer ekipler

## Karar

Denetim bittiğinde zincir PAM'e döner. Sıra:

```
PAM  → gereksinim yazar
PAD  → uygular, commit'ler
PQA  → denetler, bulguları PAD'e döndürür (döngü)
PQA  → onaylar ve PAM'e bilgi verir: "son hâl bu"
PAM  → dökümanlarını düzeltir, commit'ler
PAM  → PQA'ya push için onay verir
PQA  → son commit'i de inceler → push
Mert → push onayı
```

Mert'in cümlesi: *"PQA commitleri inceledi onayladı, PAM'a bilgi verir 'son hâl bu'
diye. PAM dökümanlarını düzeltir, commitler, PQA'ya push için onay verir. PQA son
gelen commiti de inceleyip pushlar hale getirelim."*

**PAM yalnız dökümanlara dokunabilir** — kanon dosyalarına (agent body'si, skill,
kural indeksi) değil.

## Neden — ölçülmüş boşluk

**PAM'e dönüş yoktu ve bunun iki bedeli ölçüldü (2026-08-07, `Task` kaldırma işi):**

**Birincisi — dökümanı yanlış kalıyor.** PAM cascade alanını *"beş yer"* diye ölçtü.
Gerçekte **altı iz daha** çıktı, beş ek turda. PAM'in `gereksinim.md`'sinde hâlâ
"beş yer" yazıyor ve PAM bunu bilmiyor. Yarın o dökümanı okuyan yanlış bilgi alır.

**İkincisi ve daha pahalısı — yöntemi düzelmiyor.** PAM bir sonraki cascade'i yine
kendi eski yöntemiyle planlayacak, çünkü yönteminin yetmediğini görmedi. Hata **işin
başında** oluyor ve zincirin tamamına yayılıyor.

Zincir şöyleydi: `PAM → PAD → PQA → (PAD ↔ PQA döngüsü) → Mert`. PAM ilk adımdan
sonra hiçbir şey görmüyordu.

## Push neden PQA'da kaldı

İlk düşünce push'u PAM'e vermekti. Ama kanonda bugün yazılan `ISD-COMMIT-THEN-PUSH`
şöyle diyor: *"Ürettiğini PAD commit'ler, denetimden geçeni PQA push eder"* ve
gerekçesi *"kapıyı üreten açarsa denetim atlanabilir hale gelir."*

PAM üretmiyor ama zinciri o başlatıyor — ve PAM body'sinde bugün yazılan cümle
tam bunu söylüyor: *"İşi sen iletiyorsun ama yayın kapısı sende değil."*

Mert'in çözümü kuralı değiştirmedi, **bir adım ekledi**: PAM döküman commit'ini atar
ve PQA'ya push için onay verir; PQA o son commit'i de denetler ve push'lar. Yayın
kapısı denetleyende kalıyor, ve PAM'in kendi commit'i de denetimsiz geçmiyor.

## Ne değişiyor, ne değişmiyor

**Değişmiyor:** `ISD-COMMIT-THEN-PUSH` — push PQA'da, onay kullanıcıda.

**Ekleniyor:** denetim sonrası PAM'e bilgi verme adımı · PAM'in döküman düzeltme ve
commit yetkisi (yalnız `docs/` altı) · PAM'in push onayı · PQA'nın son commit'i de
denetlemesi.

## Uygulama

Bu karar henüz kanona yazılmadı. `docs/fabrika/` altında bir iş olarak açılacak.
Sıradaki iş **PAM'in analiz eksikliği** (Mert'in kararı) — ikisi aynı kökten,
birlikte ele alınabilir.
