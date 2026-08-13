# backend-developer | 2026-08-12 21:46:21

KIMDEN -> KIME: backend-developer -> Clara
TUR: RAPOR — T2 kanon uyum denetimi (goat / GetSponsorSubUserListHandler)

YAZMA IZNI YOK kuralina uydum: goat'ta HICBIR dosyaya dokunmadim, commit atmadim.
Yalniz okudum. Bulgulari RAPORLUYORUM, duzeltmedim.

=====================================================================
ACTIGIM SKILLER (bu isten ONCE, fiilen)
=====================================================================
· module-development  (handler + DataLayer + performans kanonu)
· database            (EntityBase, tip, isimlendirme, cache/soft-delete)
· response-request    (zarf, liste sekli, pagination, Page/Take guard)
Oturum basindaki 6 cekirdek zaten yukluydu (behavior/handoff/memory-management/
is-akisi/pr-yazilim-oy-envanteri/backend).
NOT: references/*.md dosyalarini ACMADIM — bu denetim govde kurallariyla yapildi.

=====================================================================
SECTIGIM HANDLER + NEDEN
=====================================================================
src/api-sponsor/handlers/sponsor-sub-user/GetSponsorSubUserListHandler.cs

Secim rastgele degil, uc olcutle daralttim:

1) SAF INSAN-YAZIMI OLMALI. Kanonum (pr-yazilim-oy-envanteri): agent-yazimi kodu
   emsal almak "dongusel referans" — sapmayi kanon sanirim. Olctum:
     git log --format=%ae -> 14 yazar. mert@pryazilim.com = agent (322 commit).
     Handler DOGURAN commitlerin yazar dagilimi:
       389 ugurgulsevim@hotmail.com (insan, repoyu kuran)
       103 muhammed@pryazilim.com   (insan)
        97 mert@pryazilim.com       (AGENT)
        19 emirhan@pryazilim.com    (insan)
   Sectigim dosyanin HEM dogumu HEM son dokunusu ugurgulsevim = agent eli hic
   degmemis. Yani burada bulacagim sey "agentin hatasi" degil, kanonun sahada
   gercekten tutup tutmadigi.
   /!\ Yan bulgu: insan developer buse@ 44 commit atmis ama HANDLER dosyasina
   0 kez dokunmus (yalniz frontend). Once bos sonuc aldim, kontrol grubuyla
   aracimi test ettim — arac calisiyordu, sonuc gercekten sifirdi.

2) DENETIM YUZEYI GENIS OLMALI. Liste handler'i sectim cunku tek dosyada
   pagination + TotalCount + yetki + N+1 + cache + siralama eksenlerinin HEPSI
   olculebiliyor. Tekil bir Create handler'i secseydim pagination ekseni hic
   olcelemezdi.

3) ZINCIRI OKUNABILIR OLMALI. Handler + DataLayer + entity + model + Program.cs
   kaydinin besini de okudum (diff-disi tam okuma refleksi).

Okuduklarim:
  handler   : GetSponsorSubUserListHandler.cs (119 satir, tamami)
  DataLayer : SponsorDataLayer.cs:1154-1177 (+ GetUserMainSponsorId 5-17,
              + invalidation 1116/1126/1136)
  entity    : SponsorSubUser.cs
  model     : library-datatype/Sponsor/SponsorSubUserListModel.cs
  kayit     : api-sponsor/Program.cs:176

=====================================================================
UYDU — kural / kanit
=====================================================================
BE-HANDLER-NAMING       UYDU. Get+SponsorSubUser+List+Handler; cekirdek CRUD fiili
                        "Get". Program.cs:176 MapPost "/get-sponsor-sub-user-list"
                        — POST-only ve kebab-case. 404 riski yok (kayit dogrulandi).
BE-HANDLER-AUTH         UYDU. Yetki GetOptions()'ta (satir 22-31), handler govdesinde
                        inline rol kontrolu YOK. Dortlu acikca yazilmis
                        (AdminUser=true, SiteUser=false, SponsorUser=true,
                        UnregisteredUser=false) — dordu de EXPLICIT.
                        /!\ Bu benim kendi memory dersimin tersi yonde iyi ornek:
                        varsayilanlar aciktir, yalniz true olani yazmak digerlerini
                        acik birakir. Burada dordu de yazilmis.
BE-HANDLER-RESPONSE     UYDU. SetError(ex: ex, obj: model, url: this.GetType().Name)
                        — satir 114. Named-argument kullanilmis; positional exception
                        (ic hata sizintisi) yok. RESP-BE-SETMETHOD ile de uyumlu.
BE-HANDLER-MODEL-LOC    UYDU. Wrapper modeller handler dosyasinda (1-18), ic model
                        SponsorSubUserListModel library-datatype/Sponsor/ altinda —
                        nested class yok. Satir 16'da enum-path yorumu bile var.
BE-HANDLER-VALIDATE     UYDU. (sponsorId == 0).CheckVal(...) satir 60 — erken cikis.
                        String temizleme model.SearchText.PrTrim() satir 62, ciplak
                        .Trim() degil (core extension). Bir kez, validation asamasinda.
BE-DATA-CACHE           UYDU ve GUCLU. Cache-aside dogru kurulmus (1156 get / 1173 set)
                        ve invalidation UC yerde birden (1116, 1126, 1136 = create/
                        update/remove). Key aspect'li: sponsor:id:{id}:subuser:list.
                        Ayrica grep ile teyit ettim: bu key'e dokunan 5 yer var,
                        3'u temizlik. Yetim cache yok.
DB-ENTITYBASE-AUTO      UYDU. SponsorSubUser : EntityBaseModel, IEntityNotReallyDelete
                        — 6 alan yeniden TANIMLANMAMIS, kalitimla geliyor. Kanon tam.
DB-TABLE-SINGULAR       UYDU. Entity "SponsorSubUser" tekil PascalCase, prefix yok.
                        DbSet de tekil (_db.SponsorSubUser).
DB-COLUMN-NAMING        UYDU. FK "SponsorId" ({Entity}Id), boolean "IsSuperAdmin"/
                        "IsRequiredTwoFactor" (Is{Property}), dosya cifti
                        ProfileFileName+ProfileFilePath yan yana. Kisaltma yok.
BE-DATA-SOFTDELETE      UYDU. Sorgu x.IsActive filtreli (1160). IEntityNotReallyDelete
                        ile fiziksel silme kapali.
RESP-LIST-SHAPE         UYDU. data = { Data, TotalCount } — PascalCase (14-18).
RESP-BE-TOTALCOUNT      UYDU (mantiken). Sira dogru: filtrele (68-98) -> say (102)
                        -> sayfala (104). TotalCount sayfa filtresinden ONCE.
FMT-DATE-EPOCH          UYDU. Tarih tel uzerinde long epoch: ToJSTime() (1165, 1169).
                        Request tarafi da long (satir 8-11), DateTime degil.
BE-PERF-N-PLUS-1        UYDU. Dongu icinde DB cagrisi YOK — tek sorgu, sonra bellekte
                        projeksiyon.

=====================================================================
UYMADI — uc bulgu (agirlik sirasi)
=====================================================================

--- BULGU 1 (YUKSEK) — Take ust siniri dogrulanmiyor -------------------
Kural: RESP-BE-PAGE-GUARD — "Take: Take <= 0 || Take > 50 -> hata (CheckVal
'1-50 arasinda olmalidir')" + RESP-PAGINATION "Take (sayfa boyutu, maksimum 50)".
Kanit: handler satir 45-47 ve 104.
  model.Page = model.Page ?? 1;              <- Page korunmus
  var skip = (model.Page - 1) * model.Take;
  ...
  .Skip(skip ?? 0).Take(model.Take)          <- Take HIC dogrulanmamis
Page icin ?? 1 var ama:
  · Take = 0 gonderilirse -> bos sayfa doner (sessiz yanlis sonuc)
  · Take = 999999 gonderilirse -> tavan YOK, tum liste doner
  · Page = 0 veya negatif gonderilirse -> skip negatif olur; CheckVal yok, yalnizca
    ?? 1 null'i koruyor, SIFIRI korumuyor. Page=0 -> skip = -1*Take (negatif).
Kanonun istedigi ikili guard'in yarisi var, yarisi yok.

/!\ KAPSAM OLCTUM — bu TEKIL hata degil, SISTEMIK:
  grep "Take > 50|Take > 100|1-50" src/api-sponsor/handlers/  -> 0 sonuc
  grep -l "Page ?? 1" src/api-sponsor/handlers/               -> 19 dosya
Yani "Page ?? 1" proje standardi olmus, "Take tavani" hic girmemis. Tek bir
developer'in unutmasi degil, kanonun bu maddesi sahaya HIC inmemis.
Bunu tekil bulgu diye yazsaydim yanlis teshis olurdu.

--- BULGU 2 (ORTA) — filtreleme + sayfalama BELLEKTE, SQL'de degil ------
Kural: BE-PERF-SQL-SIDE — "Aggregation + arama SQL tarafinda. GroupBy/Sum/Count ->
SQL'de (ToListAsync sonrasi C# YASAK, bellek sisir). Metin arama EF.Functions.Like
(ToLower().Contains() YASAK)."
Kanit: DataLayer 1160 tum satirlari cekiyor (ToListAsync), handler 66'da
AsEnumerable() ile BELLEGE aliniyor; 70-72 arama, 75-98 filtreler, 102 sayim,
104 sayfalama — HEPSI bellekte.
  x.UserName.ToLower().Contains(...)   <- kanonun acikca yasakladigi kalip
Iki ayri sonuc:
  · Turkce collation sorunu: ToLower() ile "İ/ı" eslesmesi bozulur (kanon
    Turkish_CI_AI + EF.Functions.Like istiyor).
  · Sponsor alt kullanici sayisi buyudukce tum liste her istekte bellege cekilir.

/!\ AMA BURADA BIR CERCEVE SORUSU VAR — tek tarafli okumak yanlis olurdu:
Bu kod bilincli bir cache tasarimina yaslaniyor. Liste zaten Redis'te tutuluyor
(1156-1173) ve cache-aside dogru kurulmus; yani "her istekte DB'yi supuruyor"
DEGIL, "cache'ten gelen listeyi bellekte filtreliyor". Bu, alt-kullanici sayisinin
kucuk oldugu varsayimi altinda MAKUL bir tercih.
Hukmum: kanon ihlali VAR (ToLower().Contains acikca yasak ve Turkce collation
sorunu cache'ten bagimsiz gercek), ama "performans felaketi" demek olcumsuz
konusmak olur. Sinir: liste buyurse tasarim cokmez, once cache nesnesi sismeye
baslar. Bunu OLCMEDIM (veri yok) — olcmedigim seyi iddia etmiyorum.

--- BULGU 3 (DUSUK / GOZLEM) — cache'lenen listede TTL yok --------------
Kural: BE-DATA-CACHE — "Definition/dropdown tablolari Redis cache (TTL: tanim 60dk,
dropdown 30dk)."
Kanit: DataLayer 1173 -> this._cache.SetAsync(key, result) — TTL parametresi YOK.
Invalidation dogru kurulmus (3 nokta) oldugu icin pratikte bayat veri riski dusuk;
ama invalidation'i atlayan yeni bir yazma yolu acilirsa (baska bir DataLayer'dan
SponsorSubUser guncellenirse) kayit SURESIZ bayat kalir. TTL ikinci savunmadir.
Bunu "ihlal" diye degil GOZLEM diye yaziyorum: kural metni TTL'i tanim/dropdown
tablolari icin sartlandiriyor, bu bir kullanici listesi — kuralin kapsamina girip
girmedigi tartisilir. Emin degilim, isaretliyorum.

=====================================================================
DENETLEYEMEDIGIM (durustluk siniri)
=====================================================================
· Take tavaninin FE tarafindan zorlanip zorlanmadigina bakmadim — panel her zaman
  makul bir Take gonderiyor olabilir. Ama BE kanonu "client kontrati bozsa bile BE
  korur" diyor, yani bu savunmayi gecerli saymam.
· SQL semasini (gercek kolon tipleri/nullability) OKUMADIM — migration dosyasi
  aramadim. DB-MODIFIEDUSER / DB-UPDATEDATE-NULL bloker'larini bu yuzden
  DENETLEMEDIM. Entity C# tarafi temiz, SQL tarafi olculmedi.
· KOSMADIM. Build almadim, curl atmadim (yazma izni yok + telepresence komutunu
  ben calistirmam). Bu STATIK bir okuma; "calisiyor/calismiyor" DEMIYORUM.
· references/*.md acmadim — govde kurallariyla denetledim. self-check.md'de ek
  madde olabilir, gormedim.

=====================================================================
HUKUM
=====================================================================
13 eksende UYDU, 2 gercek ihlal + 1 gozlem. Insan-yazimi bu handler kanonun
buyuk kismini tutuyor; ozellikle yetki bildirimi, model yerlesimi, cache
invalidation ve hata yakalama ORNEK duzeyde.
Iki ihlalin ikisi de AYNI SINIFTAN: "istekten gelen degere guvenmek" (Take
dogrulanmiyor) ve "veriyi bellege alip orada islemek" (filtreleme). Ikisi de
derlemeyi kirmaz, testi patlatmaz — sessiz sinif.
En degerli bulgu tekil ihlal degil, BULGU 1'in SISTEMIK olmasi: Take guard'i
19 handler'lik bir orneklemde HIC yok. Bu bir developer hatasi degil, kanonun o
maddesinin sahaya hic inmemis olmasi. Duzeltilecekse tek dosyada degil, kural
duzeyinde ele alinmali.

BEKLEDIGIM: Yok — olcum raporu teslim edildi. Duzeltme YAPMADIM (olcum, is degil).
