# project-assistant | 2026-08-12 21:46:23

CEVAPLARIN USTUNDE DURDUM — UC TANESI YENI SORU ACTI. Son tur, kisa.

Yedi cevap KAPALI (S1, S2, S4, S5, S6, S9, S10 — uzerlerine soru acilmadi,
dogrudan kabul kriterine ceviriyorum). Uc tanesi acti:

═══ T1 (S3'ten) — 10 DAKIKALIK KILIT KIMIN ICIN? ═══

"Eski slot secim sirasinda kilitli kalir, 10 dk islem yapilmazsa cozulur" dedin.
Kilidin cozulmesi ERTELEMEYI de iptal ediyor mu, yoksa yalniz kilidi mi birakiyor?

Iki farkli sonuc var:
(a) Kilit cozulur, randevu ESKI HALINDE kalir -> hasta hicbir sey kaybetmez.
    (Cevabinda bunu yaziyorsun, sanirim kastin bu.)
(b) Ama o 10 dakika icinde ESKI slot baskasina kapali kaldi. Yani bir hasta
    erteleme ekranini acip kapatmadan birakirsa, o slot 10 dk boyunca kimseye
    verilmez. Kotu niyet gerekmez — sekmeyi kapatmak yeter.

SORU: Bu kabul edilebilir mi, yoksa kilit daha kisa mi olmali? Ve kilit
kimin gozunde "dolu" gorunur — takvimde DOLU mu, KAPALI mi gorunur?
(PRC-26'da UC durum var: bos/dolu/kapali. Bu gecici kilit hangisi?
Cevaplanmazsa FE ekranda ne gosterecegini bilemez.)

═══ T2 (S8'den) — EN KRITIGI: "HASTA ADINA" BIR SECIM MI? ═══

Dedin ki: sekreter ekraninda "hasta adina" secili ise 2 saat kurali uygulanir,
"klinik karari" secili ise uygulanmaz.

Bu cok onemli bir sey soyluyor: sekreter, kendi ekraninda bir SECIM yaparak
2 saat kuralini KENDISI DEVRE DISI BIRAKABILIYOR.

SORU: Bu bilincli mi? Cunku pratikte sunu dogurur — sekreter her zaman "klinik
karari" secer ve kural hic calismaz. Kural fiilen sekreterin insafina kalir.

Uc secenek goruyorum, karar senin:
(a) Oyle kalsin — sekreter zaten yetkili, guveniyoruz. (Kayitta kim/ne sectigi
    duruyor, denetim sonradan yapilir.)
(b) "Klinik karari" secmek SEBEP zorunlu kilsin (neden kural disina cikildi).
(c) "Klinik karari" yalniz belirli rollerde (or. klinik admin) acik olsun.

Bu bir yetki tasarimi karari ve BENIM veremem — is kurali.

═══ T3 (S1'den) — KAYBEDEN TARAFA NE YAZILIR, NEREDE GORUR? ═══

"Kaybeden tarafa NE OLDUGU yazilir (hasta bu randevuyu 14:32'de iptal etti)"
dedin — iyi kural. Ama S8'e gore HASTA ARAYUZU YOK.

Yani "hasta iptal etti" cumlesindeki hasta, fiilen SEKRETER'in hasta adina
yaptigi islem. Cakisma su hale geliyor: doktor erteliyor + sekreter (hasta adina)
iptal ediyor. Ikisi de PANEL kullanicisi.

SORU: Kaybeden taraf (doktor) bunu NEREDE gorur?
· Ekranda aninda mi (o an aciksa), yoksa
· Randevu detayinda bir gecmis/log satiri olarak mi?
Bu bir EKRAN gereksinimi ve yazilmazsa FE ne yapacagini bilemez.
(PRC-26 dersi: "bir kural EKRANDA ne demek oldugu AYRI bir maddedir".)

═══ NOT ═══

T2 kapsam/yetki karari oldugu icin cevaplanmadan discovery'yi KAPATAMAM
(`PA-DISC-RISK-CLOSE` — acik risk kalirsa kapanmaz). T1 ve T3 daha kucuk ama
ikisi de EKRAN gereksinimi dogurur; cevapsiz birakirsam FE'ye belirsizlik
tasirim.

Beklediğim: T1, T2, T3 cevaplari. Sonra discovery'yi yazip ClickUp'a serhli
yorum olarak geciyorum, statuyu completed'a cevirip sure kaydini giriyorum.
