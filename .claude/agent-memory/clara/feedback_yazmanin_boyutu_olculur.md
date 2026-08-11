---
name: yazmanin-boyutu-olculur
description: Bir yazma işleminden sonra rc=0 yeterli değil — yazılanın BOYUTU okunur (send.py gövde yutması, 2026-08-11)
metadata:
  type: feedback
---

Bir yazma işleminden sonra **çıkış kodu yeterli değil; yazılanın boyutu da
okunur.** `rc=0` "iş yapıldı" demiyor, "komut hata vermedi" diyor.

**Why:** 2026-08-11'de `send.py` şöyle çağrıldı:
`send.py <box> Clara BE TASK "başlık" --stdin < dosya`
`rc=0` döndü, dosya yazıldı — ama **gövde yutuldu, 61 karakter.** Kullanım
`send.py <box> <from> <to> <type> <body|--stdin>` yani `--stdin` body'nin
**yerine** geçer, sonuna eklenmez. Fazladan konumsal argüman sessizce atıldı.

Yakalayan şey `rc` değil, betiğin bastığı **karakter sayısı** oldu. `rc=0`
görüp devam edilse agent boş bir iş emri okuyacaktı — ve o boşluk agent
tarafında görünürdü, yazan tarafta değil.

Bu, kanonda yazılı `printf` tuzağının **aynı sınıfı**: *"iş yapılmamışken çıkış
kodu başarılı diyordu."* Kanal betiklerinde bu sınıf tekrar ediyor (`read.py`
rc=2 durumu, `archive.py --force` rc=3) — hepsinin ortak dersi: **çıkış kodu
bir iddiadır, sonucun kendisi değil.**

**How to apply:** bir mesaj/dosya yazdıktan sonra iki şeye bak — `rc` **ve**
boyut. Boyut beklenenden küçükse iş yapılmamıştır. Kritik yazmalarda içerikten
doğrula (ilk 200 + son 150 karakter), çünkü boyut da yeterli olmayabilir:
doğru uzunlukta yanlış içerik mümkün.

Ayıran soru: **yazdığımı GÖRDÜM mü, yoksa komutun şikayet etmediğini mi
gördüm?**

Bkz. [[bos-olcum-degil]] — aynı aile: bir aracın sessizliği veri değildir.
