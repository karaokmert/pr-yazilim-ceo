# Kanal — agent iletişimi — bilinmesi gerekenler

> Bu konuda bir iş geldiğinde **önce bu dosya okunur.**
> Hepsi sahada fiilen çarptı; hiçbiri tahmin değil.

**1. Monitörler oturumla ölür.** Oturum kapanınca `Monitor` task'ı gider ama dizin
durur, `STATUS.md` `OPEN` yazar, mesajlar yerinde — **hiçbir şey arızalı görünmez.**
Yeni oturumda kanal varsa monitör **yeniden kurulur.**

**2. `PID` canlılık kanıtı DEĞİL.** Tek geçerli sinyal: kutunun **kendi son yazım
zamanı** (PCA ölçümü).

**3. Kanal TAŞIYICIDIR, kayıt değil.** Oturum kapanınca arşive gömülür. Ölçüldü —
iki bağımsız vaka aynı gün: QA'nın RED raporu ve bir karar cevabı kanalda kalıp
kayboldu, ertesi gün PA aradı bulamadı.
→ Üretilen rapor/karar **kalıcı katmana** (ClickUp yorumu / repo) geçer.

**4. Arşivleme okunmamış mesajı REDDEDER** — `--force` kaybı sessizleştirir, son çare.
Önce `read.py`, sonra `archive.py`.

**5. `send.py` tip adları sabit:** `TASK|INFO|QUESTION|CLOSE`. Başka tip `rc=1` döner
ve mesaj **gitmez** (Clara bir kez düştü, PA iş beklerken bekledi).

**6. Boru hattı çıkış kodunu yutar.** `python3 send.py ... | tail -3` yazarsan `$?`
**tail'in** kodudur. Ölçüldü: bir agent bu yüzden `send.py`'ye yanlış arıza atfetti.
