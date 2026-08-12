# qa-engineer | 2026-08-12 21:46:31

DENETIM RAPORU — goat 680109a0

Commit ID: 680109a0 — fix(menu): menude iki grubun birden secili gorunmesi
Yazar: mert@pryazilim.com (agent-yazimi olabilir — emsal olarak supheyle bakilir)

Kisa Ozet: Menude bir sayfaya girince iki grubun birden secili gorunmesi
duzeltilmis. Sebep: sayfa menude baska bir gruba tasinmis ama adresi eski
grubun altinda kalmis; menu yalniz adrese bakinca ikisini birden yakiyordu.
Cozum "sahiplik": sayfa hangi grupta acikca listeliyse o grup sahiplenir.

Teknik Ozet:
- Panel: uc panel (admin-v2, sponsor-v2, streamer) — ayni dosya adi, ayri kopyalar
- Degisen: yalniz Menu.tsx x3 (90 ekleme / 24 silme), sizinti YOK (commit atomik)
- Tablo/Handler/Cache/Yan etki/SQL: YOK (saf FE gorsel mantik)
- Calisma agaci: bu uc dosyada commit sonrasi degisiklik yok

OKUDUGUM DOSYA SAYISI: 5 dosya tam/hedefli okuma
  1. web-admin-v2/.../Menu.tsx      (860 satir — tam tarama + 488-556 govde)
  2. web-sponsor-v2/.../Menu.tsx    (661 satir)
  3. web-streamer/.../Menu.tsx      (431 satir)
  4. web-sponsor-v2/lib/route.ts    (yol sabitlerini cozmek icin)
  5. web-admin-v2/lib/route.ts      (ayni)
  + commit oncesi surumler (git show 680109a0^) — degisimin yonunu dogrulamak icin

Denetim: Diff disi TAM okuma yapildi ve iki yerde diff'in gostermedigi sey
cikti (asagida #1 ve #2). Uc akis kontrolu: olu kod YOK (eski isActive'in
tuketicisi 0 — olculdu), producer-consumer tutarli, paylasilan kod yok
(uc panel bagimsiz kopya, ortak modul degil). Teknik borc SIFIR
(TODO/console.log/debugger taramasi uc dosyada temiz). Sahiplik kurali
mantigi dogru kurulmus; commit mesajindaki "ilk tasarim geri alindi"
notu durustluk gostergesi.

Revize / Dikkat (etki sirasina dizili):

#1 | DIKKAT — Sahiplik kurali YANLIS listeyi tariyor (admin)
   Ne: Menude cizilen liste yetkiye gore filtrelenmis olan, ama sahiplik
   taramasi filtrelenmemis ham liste uzerinde donuyor.
   Bugun zarar: YOK — olctum, 6 senaryo (2 sayfa x 3 yetki profili),
   hicbirinde fark cikmadi. Sebep: sahiplenen grup her iki izinden birine
   sahip olan herkese gorunuyor, yani "sahiplenen gorunmez" hali olusmuyor.
   Yarin zarar: VAR — sahiplenen grup dar bir izne baglanirsa, yetkisi
   olmayan kullanici sayfadayken menude HICBIR sey secili gorunmez.
   Simule ettim: gorunen=['Sponsorlar'], mevcut kod=[], olmasi gereken=
   ['Sponsorlar']. Duzeltilen bug'in (iki grup yaniyor) simetrik tersi.
   Neden onemli: commit'in kendi savundugu sey gelecek korumasi ("bugun
   cakisan yol yoktu ama ileride..."). Ayni gerekcenin burada uygulanmamasi
   ic tutarsizlik. Bugun korunmasi YAPISAL degil, tesadufi.

#2 | DIKKAT — "Uc panelde de ayrac" iddiasi iki panelde yarim
   Ne: Commit mesaji "Yol karsilastirmalari ortak isUnderPath'e alindi
   (uc panelde de)" diyor. Admin'de gercekten oyle. Sponsor ve streamer'da
   ise alt ogenin GORSEL vurgusu hala pathname.includes(sub.path) —
   commit bu satirlara hic dokunmamis. includes ayracsiz startsWith'ten
   daha zayif: yolun ortasinda bile eslesir.
   Bugun zarar: YOK — olctum, 22 sayfa x 14 alt oge kombinasyonu,
   yanlis eslesme 0, ayni oneki paylasan alt oge cifti 0.
   Not: streamer'da submenu HIC yok, oradaki satir fiilen olu.
   Neden onemli: kanit degeri degil, iddia-gerceklik farki. Mesaj
   "uc panelde de duzeltildi" diyor, iki panelde ayni sinif karsilastirma
   duruyor. Sonraki okuyan kapandi saniyor.

#3 | BILGI (bu commit'in bulgusu DEGIL — repo seviyesi, devralinan)
   .claude/settings.local.json git'te TAKIPLI. Kanonum bunu ismen yasakliyor
   (QA-NO-PROJECT-AGENT-CONFIG): agent yapilandirmasi global scope'ta yasar,
   proje kopyasi cift kaynaktir. Bu commit'e karismamis (0 dosya) — o yuzden
   commit'i bloke ETMEZ (CR-BLOCKER-LEVEL: yeni sapma bloke, eski borc bilgi).
   SILMEDIM — silme geri donussuz, karar kullanicida.

DISCOVERY uyumu: Karsilastirilamadi. goat'ta bu ise ait DISCOVERY bulamadim;
kapsam degerlendirmem commit mesajinin kendi beyanina dayaniyor. Isaretliyorum
— kapsam kapisini (QA-DISCOVERY-GATE) tam calistiramadim.

BUILD: Commit mesaji "uc panel de next build yesil (hata izi 0, basari izi 6)"
diyor. Bu beyani KENDIM KOSTURMADIM — kosturmam gerekseydi onay oncesi sart
olurdu (CODE-BUILD-GREEN). Bu bir denetim tatbikati oldugu ve "dosya
degistirme/kapi degil" dendigi icin build'i tetiklemedim. Isaretliyorum:
gercek bir onay kapisinda bu beyani teyit ederdim.

→ KARAR: ONAY (iki DIKKAT notuyla) — RED DEGIL.

Gerekce (QA-METRIC-SPLIT etki testi: "RED etmezsem prod'da bedeli var mi?"):
Bulgularin ikisi de bugun fiili hata URETMIYOR ve bunu tahminle degil
simulasyonla olctum. Kanon ihlali de yok. Duzeltmenin kendisi dogru: kok
neden dogru teshis edilmis, ilk asiri-duzeltme geri alinmis (mesajda acikca
yazili — bu iyi muhendislik), gerileme dusunulmus. RED etmek bu commit'i
bekletirdi ve karsiligi olmayan bir sertlik olurdu.
Ama #1 gercek bir yapisal kirilganliktir ve KAPANMADAN gecmemelidir —
bugun tesadufen korunuyor. Bunu "sonraki ise" degil, sahibine bildiriyorum.

Kapsam (kullanici dili): Menu duzeltmesi saglam ve dar kapsamli — yalniz
menunun secili gosterme mantigina dokunuyor, veri/API/kayit tarafina hic
girmiyor. Iki not birakiyorum: biri menunun yetki filtresiyle ilgili bir
gelecek riski (bugun zarar vermiyor, olctum), digeri commit mesajinin
"uc panelde de yapildi" dedigi bir isin iki panelde yarim kalmasi.

⚠️ HUKUM VERILDI, UYGULANMADI: Talimatin geregi goat'ta hicbir seye
dokunmadim — push/merge yok, statu degismedi, dosya degismedi. Onay
"atomik kapanis" olarak ISLETILMEDI (QA-APPROVE-ATOMIC normalde ClickUp
sub task + developer kapanis handoff'u + PA bilgisi ister; bu bir olcum
oldugu icin uygulamadim).

BEKLEDIGIM: Bu bir tatbikatsa geri bildirim. Gercek akista olsaydi:
#1 ve #2 icin FE'ye DIKKAT handoff'u, #3 icin kullaniciya karar sorusu.
