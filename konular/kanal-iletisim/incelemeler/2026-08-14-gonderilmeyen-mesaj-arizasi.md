# Ölçüm — gönderilmeyen mesaj arızası ve rol bazında görünürlüğü

**Tarih:** 2026-08-14 · **Ölçen:** Clara (tetik) + PAM/PAD/PQA/PCA (cevap)

## Olay

PAM iki cevabı da **yazdı**, ikisini de **SendMessage ile göndermedi.** Ekranında
durdular, kimseye ulaşmadılar. **Yedi saat kayboldu** (11:27 → 18:40).

Kaybolan iki şey: PQA'nın denetim raporu (c7dd3d3 GEÇMEDİ, iki bulgu) ve
QA/CA/TE ölçüm kapsamı + tur görüşü.

## Ölçüm — arıza kimde

Dört personele soruldu: *"ne ürettin, kime gönderdin, ne zaman?"*

| Rol | Gönderdi mi | Kanıt |
|---|---|---|
| PAD | **evet** | 07:34 + 11:19, ikisi de `success` · bağımsız doğrulama: devri ulaşmasaydı 11:27'de denetim bitmiş olamazdı |
| PQA | **evet** | 07:34 + 11:27, msg_id `4c2857e8` |
| PCA | **evet** | 07:34, msg_id `52c50f4d` |
| **PAM** | **HAYIR** | iki cevap yazıldı, gönderilmedi |

**Arıza tekildi ve kaynağı görünür oldu** — PAM örtmedi, kendi üstlendi.

## ⚠️ ASIL BULGU — PQA'nın notu

> *"Bir denetçinin çıktısı bulgudur, ve **gönderilmemiş bir bulgu ile hiç bulunmamış
> bir bulgu dışarıdan aynı görünür** — ikisi de sessizdir. Sende arıza en azından
> 'cevap gelmedi' diye fark edilebiliyordu; bende **'demek temiz çıkmış'** diye
> okunurdu."*

**Aynı arıza rolüne göre farklı görünürlükte:**

| Rol | Arıza olursa dışarıdan nasıl görünür |
|---|---|
| Planlayıcı (PAM) | *"cevap gelmedi"* → **fark edilir**, sorulur |
| Üretici (PAD) | *"üretim gelmedi"* → **fark edilir** |
| **Denetçi (PQA)** | *"demek temiz çıkmış"* → **FARK EDİLMEZ** |
| Ölçümcü (PCA) | *"ölçüm çıkmadı"* → kısmen fark edilir |

Denetçide arıza **sessizliğin sessizliği**: bulgu üretilmedi mi, üretilip
gönderilmedi mi — dışarıdan ayırt edilemiyor. Ve *"temiz"* varsayılan okuma olduğu
için kimse sormuyor.

## Kural adayı — HENÜZ DEĞİL

**Ölçüm tek:** bugün bir kez oldu, PAM'de oldu, PQA'da olmadı. PQA'nın söylediği
bir **risk tarifi**, gerçekleşmiş bir arıza değil.

Ölçülmemiş kural kanona girmez. Bu kayıt bir **kural değil, bir işaret**: aynı arıza
bir kez daha görülürse ve denetçide görülürse, o zaman kural konuşulur.

**Ne aranacak:** bir denetim turunda *"temiz çıktı"* sanılan ama aslında rapor
gönderilmemiş bir tur.

## Yan bulgu — kanal kendiliğinden kapandı

PCA ölçtü: 10:17:48–10:18:09 arasında `skill-project` altındaki **dokuz kutunun
tamamı** arşive taşındı, `live-channel.json` boşaltıldı. Sabah *"şimdilik silme"*
denen beş kutu da bu turda kapandı. **Veri kaybı yok** (`archive-log.json` üç kayıtla
doğrulandı, PCA'nın outbox mesajı arşivde duruyor).

Kim yaptı bilinmiyor — PAM yapmadı, PCA yapmadı. PCA nedensellik iddia etmedi, yalnız
SendMessage akışına geçişle zamanlamanın örtüştüğünü not etti.

**Sonuç:** *"beş kutu arşivlenemiyor"* kalemi kendiliğinden kapandı.
