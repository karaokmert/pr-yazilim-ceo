# "Bensiz çalıştırdığımda ClickUp'a hazırlar mı?"

> Mert'in sorusu. Ölçüldü — çünkü bugün ClickUp düzenini agent'lar **Clara'nın
> gönderdiği brief'ten** öğrendi. Kanonlarında ne kadarı var?
> Kaynak: `cache/pryazilim-agents/ozel-yazilim/0.7.0/`

## Cevap: KISMEN — temel düzen var, üç şey yok, bir mekanik boşluk var

## ✅ Kanonda VAR (bugünkü brief'imin çoğu)

`clickup` skill'i (161 satır) şunları zaten söylüyor:

- **Sahiplik ayrımı:** *"Her agent kendi sahip olduğu task'a yazar; ana task ve
  backlog project-assistant'ın."* — brief'imin 2. maddesi
- **Statü seti:** `CLICKUP-STATUS-SET` — *"PR Yazılım statüleri sabit,
  sorgulanmaz; genel ClickUp statüsü ('To Do'/'Done') YASAK"*
- **Kanıt zorunluluğu:** *"'Bitti' bir beyandır, kayıt değildir: bir işin hangi
  aşamada olduğu ClickUp'taki statüden okunur, bir agent'ın beyanından değil."*
- `revise` akışı · task ID'nin handoff'la taşınması

**Yani brief geçmesem de temel düzeni bilirlerdi.**

## ❌ Kanonda YOK — üç şey

| Ne | Ölçüm |
|---|---|
| **Süre kaydı mekaniği** (`get_task_time_in_status`, `current_status` tuzağı) | **hiçbir skill'de 0 eşleşme** |
| *"Bittim, sıradaki ne"* → PA'ya sor, havuzdan iş alma | `clickup`'ta 0 |
| **Paylaşılan çalışma ağacı** (`git add .` yasağı, pathspec, `--cached` doğrulama) | **hiçbir skill'de yok** |

**En tehlikelisi süre kaydı:** `current_status` tuzağı kanonda yazmadığı için
**her yeni oturumda yeniden düşülebilir** — ve sessizce yanlış sayı yazar.
Bugün ölçüldü: 1 dk vs 326 dk, **326 kat fark.**

## ⚠️ Mekanik boşluk — `clickup` hiçbir preload listesinde yok

| Agent | preload'da `clickup` | omurgada atıf |
|---|---|---|
| PA | ❌ | ✅ *"Task açma / statü / backlog → `clickup`"* |
| BE | ❌ | ❌ |
| FE | ❌ | ❌ |
| QA | ❌ | ❌ (agent tanımında 2 geçiş var) |
| CA | ❌ | ❌ |

**Sonuç:**
- **PA düzeni bulur** — omurgasında adres yazılı, işe girerken açar
- **BE/FE/CA ise ClickUp'a dokunması gerektiğini kendi kanonundan öğrenemez.**
  Bugün Clara'nın brief'inden öğrendiler.

Bu, Sınav 3'te CA'nın kendi söylediğiyle örtüşüyor:
> *"ClickUp düzeni çok detaylı anlatıldı ama bana hiç sub task verilmedi —
> o talimatın tamamı boşa okundu. **Verilmeyen işin kuralı gürültüdür.**"*

Tersi de doğru: **verilmeyen kuralın işi yapılamaz.**

## Fabrikaya öneri (karar Mert'in)

1. **Süre kaydı mekaniğini kanona yaz** — `current_status` tuzağı dahil.
   Bugün 326 kat fark ölçüldü; kanonda olmadığı için tekrarlanabilir.
2. **`clickup` atıfını developer omurgalarına ekle** — en azından
   *"kendi sub task'ının statüsü → `clickup`"* satırı.
3. **Paylaşılan çalışma ağacı kurallarını** bir yere bağla (git disiplini
   `behavior`'da var ama çok-agent senaryosu yok).

⚠️ Ve S7 hatırlatması: süre kaydı kanona yazılmadan önce **ne ölçeceği**
kararlaştırılmalı — bugünkü kural revize alan işi 1 dakika gösteriyor.
