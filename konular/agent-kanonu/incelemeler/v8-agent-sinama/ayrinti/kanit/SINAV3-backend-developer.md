# SINAV 3 — backend-developer | 2026-08-12 23:39:10

KIMDEN -> KIME: backend-developer -> Clara
TUR: CEVAP — SINAV 3: SKILL HARITASI

Skill ACMADIM. Omurgamdaki "is -> skil" eslemesinden yaziyorum.

=====================================================================
SEN-1) Randevu iptali: SMS + iptal sebebi kaydi + slot tekrar musait
=====================================================================
Bu tek is degil, UC ayri alana dokunuyor. Sirayla:
1. database          — iptal sebebi bir kolon/tablo demek; sema karari once verilir
                       (+ onay gerekir, DISCOVERY'de yoksa PA'ya donerim)
2. module-development — handler + DataLayer: iptal akisi, slotun serbest birakilmasi
3. notification      — SMS BE'den dogrudan gitmez; mesaj uretilir, kuyruga atilir,
                       job-consumer kanaldan yollar
4. enum-sync         — "iptal" bir durum degeri; enum library-datatype'ta tanimli
5. tasarim-prensipleri — SMS geri alinamaz + slot yarisi var: idempotency ve
                       "iki kez gonderme" karari burada
ACMAM: realtime (canli bildirim istenmemis, SMS ile karistirilmamali),
messaging (sohbet degil), upload (dosya yok).
/!\ Slotun "tekrar musait olmasi" bir esszamanlilik noktasi — iki kisi ayni anda
alabilir. Bunu tasarim-prensipleri + module-development (race/INCR) altinda
degerlendiririm.

=====================================================================
SEN-2) Liste + profil fotografi (URL zaten var) + randevu durumu
=====================================================================
1. module-development — liste handler'i, DataLayer sorgusu, pagination
2. response-request   — liste zarfi {Data, TotalCount}, casing, Page/Take
3. enum-sync          — Beklemede/Onaylandi/Iptal = byte enum, response'ta BYTE
                        doner, string label DONMEM
ACMAM: upload — /!\ TUZAK OLABILIR. Fotograf DAHA ONCE yuklenmis, URL'i var;
ben sadece kayitli URL'i donduruyorum. Upload skili dosya ALMA/blob'a yazma
isidir, burada o is YOK. "Fotograf" kelimesini gorup upload acmak refleks hata olur.
ACMAM: gosterim-formatlari — tarih/tutar donuyorsa acardim; soruda yok. Liste
tarih donduruyorsa (buyuk ihtimalle) O ZAMAN acarim (epoch-ms kanonu).

=====================================================================
SEN-3) Tablo yavas aciliyor, "backend tarafina bak"
=====================================================================
1. module-development — performans kanonu burada: N+1 (foreach+await),
                        aggregation'in SQL'de mi bellekte mi yapildigi,
                        ToLower().Contains yerine EF.Functions.Like
2. database           — sorgu/index/tip tarafi + pagination mekanigi
ACMAM: response-request (zarf sekli yavasligin sebebi olmaz).
/!\ CERCEVE SERHI: "backend tarafina bak" bir YONLENDIRME, teshis DEGIL.
Yavasligin backend'de oldugu HENUZ kanitlanmadi — panelde de olabilir (client
tarafi tum listeyi cekiyor olabilir), veride de olabilir. Once OLCERIM
(hangi endpoint, ne kadar suruyor, kac kayit); backend'de cikmazsa bulguyu
PA'ya bildiririm, kendi katmanimi "temiz" diye kapatmam.
Bugun bunun canli ornegini gordum: bellekte filtreleme kanon ihlaliydi ama
cache oldugu icin "felaket" demek olcumsuz konusmak olurdu.

=====================================================================
SEN-4) "api-randevu diye yeni servis ekle"
=====================================================================
Bu IKI UCLU bir is — tamamen benim degil, tamamen baskasinin da degil:
1. api-project — kanonu bu skil tasiyor; TETIKLEYEN uc bende (yeni servis
                 gerektigine karar veren), URETEN uc DO'da (template klonlama,
                 gateway/ingress route baglama)
Yani: yeni servis KURULUMU DO'nun isi. Ben dogrudan DO'ya da gidemem —
kanonumda DO'ya dogrudan handoff YOK, PA uzerinden gider.
Servis kurulduktan SONRA icine handler/entity yazmak bana doner; o zaman
module-development + database acarim.
ACMAM: docker-k8s, ci-cd, env-config — hepsi DO'nun alani, benim degil.
/!\ "Yeni bir proje kuruluyor" ifadesi daha da genis olabilir (sunucu/K8s/
proje planlama) — o tamamen DO + PA isi, bende hicbir parcasi yok.

=====================================================================
SEN-5) QA RED: "cache invalidation eksik, liste eski veri donuyor"
=====================================================================
1. module-development — cache-aside + invalidation kanonu burada (BE-DATA-CACHE):
                        her Create/Update/Remove ETKILENEN TUM key'leri temizler
2. database           — soft-delete/IsActive degisiminin bagli cache'e yansimasi
ACMAM: response-request (zarf dogru, sorun veri tazeliginde).
Yaklasimim: bozuk key'i degil, o key'i YAZAN ve TEMIZLEYEN tum yollari tararim —
tek yerde yama yaparsam baska bir yazma yolu ayni bayatligi tekrar uretir.
Bugun goat'ta dogru orneğini gordum: tek okuma noktasina karsi UC temizleme
noktasi (create/update/remove) vardi.
Sonra: iş sonu protokolu BASTAN — brief, onay, commit, QA'ya donus handoff'u
(ne duzeltildi + kok neden).

=====================================================================
OZ DEGERLENDIRME
=====================================================================
Emindim        : 4 — SEN-1, SEN-2, SEN-3, SEN-5
Tahmin ettim   : 1 — SEN-4'te api-project skilinin ADINI omurgamdaki eslemeden
                 hatirliyorum ve icini HIC acmadim; iki-uclu oldugunu ve uretim
                 ucunun DO'da oldugunu biliyorum ama kurulum adimlarini bilmiyorum.
Bilmiyordum    : 0 uydurma. Hicbir skil adi uydurmadim; emin olmadigim tek yer
                 SEN-4'un icerigi.
Yakaladigim tuzak: SEN-2'de "fotograf" kelimesi upload skilini cagiriyor ama is
                 YUKLEME degil OKUMA — acmam. SEN-3'te "backend'e bak" teshis
                 degil yonlendirme — once olcerim.

BEKLEDIGIM: Yok.
