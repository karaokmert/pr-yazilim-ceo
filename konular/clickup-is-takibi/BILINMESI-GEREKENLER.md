# ClickUp — iş takip düzeni — bilinmesi gerekenler

> Bu konuda bir iş geldiğinde **önce bu dosya okunur.**
> Hepsi sahada fiilen çarptı; hiçbiri tahmin değil.

Bu işe girmeden önce okunacak beş şey. Hepsi sahada **fiilen** çarptı.

**1. Süre kaydı iki farklı yerde, biri YANLIŞ.**
`current_status.total_time_minutes` ile `status_history[in progress]` **aynı adı taşır,
farklı şeyi ölçer.** Ölçüldü: biri **1 dakika**, diğeri **326 dakika** gösteriyordu —
**326 kat fark.** Yanlış satır okunursa sessizce yanlış sayı yazılır, hata vermez.
→ Doğrusu: `get_task_time_in_status` → `status_history` içinde `status=='in progress'`.

**2. Ve o sayı bile işi ölçmüyor** — iki yönden yanılır:
- **Şişirir:** duvar saatini sayar. Task gece açık kalırsa gece de süreye yazılır
  (326 dk kayıtlı / ~12 dk fiilî çalışma).
- **Eksiltir:** revize turları `revise`/`test` statüsünde geçer, `in progress` yalnız
  **ilk** turu ölçer. İki kez RED alıp düzelten iş **1 dakika** görünür.
→ Sonuç: kayıt **kaliteyi ters ölçüyor.** Metrik olarak kullanılırsa yanlış kişiyi
ödüllendirir. *Karar Mert'te — hangi satır(lar) toplanmalı.*

**3. `since` başlangıç DEĞİL** — "o statüye **en son** geçiş anı". Revize turu yaşandıysa
toplamla tutarsız olur. `start` toplam süreden geri sayılarak üretilir.

**4. Timer kullanılmaz** — ClickUp'ta aynı anda tek timer, ve timer **kullanıcıya** bağlı.
Paralel agent'larda ikincisi hata alır (ölçüldü).

**5. Yazma çağrısının DÖNÜŞÜ ölçüm değildir.** İki yanlış alarm ölçüldü: sub task
açılışında `description` boş göründü (doluydu), `custom_id` null geldi (atanmıştı).
→ Düzeltmeye koşmadan **önce oku.**

**6. API kotası yazma katmanını da keser.** Vuruldu (2026-08-12): *"796 dakika
bekleyin."* Önce yalnız `add_time_entry`, dört dakika sonra **yorum yazma da** kapandı.
→ Bu düzen ClickUp yorumunu *kalıcı kayıt* olarak kullanıyor; kota vurulduğunda
**kalıcı kayıt katmanı tamamen kapanır.** O an üretilen kayıt repoya yazılır
(`bekleyen/` altına), kota açılınca taşınır.

**7. Yatay çizgi (`---`) kullanma.** MCP markdown dönüşümünde `undefined` olarak
basılıyor (ölçüldü: bir yorumda 6 adet). Başlık ya da boş satırla ayır.
