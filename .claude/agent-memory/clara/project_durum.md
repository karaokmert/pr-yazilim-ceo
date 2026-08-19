---
name: project-durum
description: Son kapanış dokümanının adresi ve tek cümlelik durum — her oturum açılışında İLK okunur
metadata:
  type: project
---

**Son iş: fabrika skill temizliği + Clara'nın iletim yetkisi
(EV, `skill-project`, 2026-08-19 17:02–19:05).**

Kapanış: `gunluk/ev/2026-08-19-kapanis-aksam-fabrika-temizligi.md`
⚠️ Aynı günün İKİNCİ kapanışı — birincisi
`gunluk/ev/2026-08-19-kapanis-gece-nobeti-ve-ogrenme-dongusu.md` (16:50'ye kadar).

## BİLMEDEN İŞE BAŞLAMA

**1. Clara artık devir bloğunu KENDİ iletiyor** — Mert'in onayıyla, `SendMessage` ile.
`CLA-NO-CALL-TEAMS` değişti (karar:
`konular/clara/kararlar/2026-08-19-handoff-sendmessage-ile-iletilir.md`).
Sıra sabit: bloğu **önce Mert'e göster**, o "ilet" der, sonra git. Onaysız iletim yok.
⚠️ Ayrım: **saha ağında (OY/WS) hâlâ izleyicisin** — orada merkez PA. Yalnız
**fabrika ağında (PAM/PAD/PQA/PCA)** taşıyıcısın.

**2. Fabrika skill listesi 26 → 5.** Yalnız `behavior`, `is-duzeni`, `uretim`,
`yapi-taslari`, `dagitim` yürürlükte. Kalan 21 `trash/2026-08-19_1754-emekli-fabrika-skilleri/`
altında. Emekli bir skill adı görürsen (`uretim-standardi`, `cascade`, `kanon-sagligi`…)
o artık yok.

**3. Eşzamanlı commit — komut biçimi.** Birden çok agent aynı repoda commit'lerken
İKİ ADIM: `git add <klasör>` sonra `git commit -m "mesaj" -- <klasör>`.
`-m` ÖNCE, `--` SONRA (ters yazılırsa hata verir). Ve `add` atlanırsa **yeni dosya
sessizce düşer** — `-- <yol>` yalnız takip edilen dosyayı alır.

**4. Qdrant KAPALI** (2026-08-16, Mert kapattı). Vektör arama kanondan çıktı.
**`grep -l` kullanma**, satır göster (`-h`) — `-l` dosya adı verir, cevap vermez.

## AÇIK — devam eden

**PUSH BEKLİYOR:** `skill-project` 7 commit `origin/main` önünde (`26c1148` başta).
PQA denetimde, **onay Mert'te**. Bitince PQA'nın kapanışı verilecek.

**RED-2 katman kararı PAD'de:** `docs/fabrika/red2-sinir-isaretleri/gereksinim.md`
— iki çıkarımın (URT-NO-CONTENT şerhi + agent listesi tazelenmesi) nereye yazılacağı.

**`CLAUDE.md` §3 borç bloğu geçersiz** — "iki skill ailesi yan yana" diyor ama emekli
aile bugün temizlendi. Blok kendisi "temizlenince silinir" yazıyor; kimse
görevlendirilmedi.

**`rules-index.json` bakımsız** — bugün 4 kırık atıf temizlendi, sabahki ölçüm 138
eksik referans saymıştı.

## MERT'İN KARARINI BEKLEYEN (16 Ağustos'tan devreden, dokunulmadı)

`/sendmessage` repoya taşınsın mı · `setup.py` PID düzeltmesi (kutu adı dakika
bazlı, aynı dakikada iki agent aynı adı üretiyor) · beş agent'a `clickup` atıfı ·
"tutarlı yazacaklar mı" ikinci ölçümü · fabrika betiklerine yazma izni

**Oturumlar arası görünürlük** — Mert: *"birçok session açıyorum, haberi olmuyor."*
⚠️ Çözüm YENİ DOSYA DEĞİL (Mert defter önerisini reddetti: *"dosyalama sisteminden
sıkıldım"*). Doğru teşhis: **sorgu problemi** — var olan kapanışlar okunsun.
