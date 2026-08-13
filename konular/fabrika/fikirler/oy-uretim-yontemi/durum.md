# OY üretim yöntemi — nereden başlanacak

Tarih: 2026-08-03 · **Yarım** — ölçüm yapılmadı, karar verilmedi

> **GÜNCELLENDİ — 2026-08-03 akşamı.** Aşağıdaki iki hipotez (bilgi kaybı / bağlanma
> kaybı) **büyük ölçüde geçersiz.** v8'in *"sahada tutmadı"* sonucunun sebebi bulundu ve
> mekanik: agent'lar `skills:` listesini hiç yükleyemiyordu, yani kanonlarını
> **okumadan** çalıştılar (`incelemeler/skill-preload-bulgusu/kayit.md`). Kural biçimi
> sınanmamıştı — kural elde bile değildi.
>
> Mert bir hook yapısı kurdu ve v8 iki gündür sahada çalışıyor, gözlemi *"mükemmel
> çalışıyor."*
>
> **Açık kalan soru:** preload arızasının çözülmesi kural **biçiminin** doğrulandığı
> anlamına gelmiyor. İki ayrı soru var — *kural elinde miydi* (artık evet) ve *kural
> davranış üretiyor mu* (henüz ölçülmedi). İki günlük gözlem birincisine yeter,
> ikincisine yetmez.
>
> Yani aşağıdaki *"ayıran ölçüm"* hâlâ anlamlı ama sorusu değişti: artık *"v8 neden
> tutmadı"* değil, **"v8 kuralları eline geçtiğinde davranış üretiyor mu"**.

## Durum

Fabrika ekibinin ilk işi OY agent takımını üretmek. Elde iki eski kuşak var ve ikisi de
yetersiz.

**v7** sahada uzun süre çalıştı, iyi işler çıkardı — ama bilgisi azdı ve bakımı çok
zordu. Bir kural değiştirmek günler alıyordu.

**v8** onu düzeltmek için yapıldı. Bakımı kolaylaştı ama sahada tutmadı: agent'lar
kurallara istendiği gibi uymadı.

Yeni OY ikisinin üstüne kurulacak ama hiçbirinin kopyası olmayacak.

## Bulunan boşluk — teşhis asimetrisi

İki kuşağın teşhisi aynı ağırlıkta değil.

v7 için sebep biliniyor: bakım zorluğu yaşandı, ölçüldü, günler harcandı. Somut.

v8 için elde yalnız **sonuç** var: *"sahada tutmadı, kurallara uyulmadı."* Bu bir gözlem,
sebep değil. Ve sebep bilinmeden yeni kuşak aynı hataya düşer.

## İki hipotez — ölçülmedi

v8 neden tutmadı? İki rakip açıklama var ve ikisi farklı sonuç doğurur:

**Bilgi kaybı.** v8 bakımı kolaylaştırmak için kuralları konsolide etti, kısalttı,
referansa taşıdı. Bu sırada davranışı tetikleyen ayrıntı da gitti. Doğruysa çözüm
ayrıntıyı geri getirmek.

**Bağlanma kaybı.** Bilgi duruyor ama kural artık bir ana bağlı değil. v7 adımın içinde
söylüyordu (*"şimdi şu dosyayı aç"*), v8 duran bir yükümlülük olarak yazdı (*"kanona
dayanacaksan aç"*). Doğruysa çözüm bilgiyi çoğaltmak değil, bağlama noktası kurmak.

**Ayıran ölçüm:** her iki kuşaktan aynı kuralı isimsiz bir yardımcıya okutup davranış
sormak. v7 formu davranışa dönüşüyor mu, v8 formu dönüşüyor mu.

## PAM'e ne gidecek — henüz belirsiz

İlk okuma *"PAM'e yöntem lazım"* idi. Clara buna itiraz etti: PAM kıdemli bir üretici,
iki kuşağı okuyup karşılaştırmayı zaten yapabilir. Bilmediği şey yöntem değil, **hangi
tarafın hangi sebeple tuttuğu.**

Yani PAM'e giden şey bir süreç tarifi değil, bir **karar dayanağı** olmalı. O dayanak
şu an hiçbir yerde yazılı değil.

## Açık kalan risk

*"İkisinin üstüne kurulacak ama kopyası olmayacak"* bir hedef değil, bir dilek —
ölçütü yok. İş bittiğinde yeni OY'ye bakıp *"bu gerçekten ikisinin üstünde mi"* diye
sorulacak ve cevap verecek bir şey olmayacak.

Ölçüt konmazsa üçüncü kuşak da aynı yerden döner.

## Sıradaki adım

Ölçüm yapılmadı. Yapılacak olan: v7 ve v8'in kural biçimlerini karşılaştırmak, hangi
hipotezin doğru olduğunu davranış testiyle ayırmak.

Karar bekleyen: ölçümü kim yapacak ve kapsamı ne olacak.
