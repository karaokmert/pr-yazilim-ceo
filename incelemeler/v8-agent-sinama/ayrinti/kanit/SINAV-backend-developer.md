# BILGI SINAVI — backend-developer | 2026-08-12 23:13:42

KIMDEN -> KIME: backend-developer -> Clara
TUR: CEVAP — BILGI SINAVI

Skill ACMADAN yazdim. Not: bu oturumda module-development/database/
response-request'i zaten acmistim, govdeleri context'imde duruyor — yani bu
"ezberden" degil "bugun okudugumdan" geliyor. Bunu avantaj olarak isaretliyorum,
saklamiyorum. Sonradan da hicbir sey acmadim, kontrol etmedim.

=====================================================================
S1) skip hesabi + Take ust siniri
=====================================================================
skip = (Page - 1) * Take. Page 1-TABANLI (0-tabanli YASAK). Handler skip'i
hesaplar, DataLayer imzasi (int skip, int take) alir — EF'in Skip/Take'ine 1:1.
Take'e ust sinir KOYARIM: maksimum 50. Neden: client kontrati bozsa bile BE
korumak zorunda; tavansiz Take tum tabloyu supurur. Guard ikili:
  Take <= 0 || Take > 50 -> CheckVal("1-50 arasinda olmalidir")
  Page ?? 1 ve Page <= 0 -> hata (?? 1 yalniz NULL'i korur, SIFIRI korumaz;
  Page=0 negatif skip uretir)
Ek: "hepsini getir" ihtiyaci Take'i buyuterek COZULMEZ — Take'siz ayri lookup
endpoint'i acilir (dropdown, TotalCount dondurmez).
EMINIM. Bugun bu kuralin sahada 65 handler'dan 1'inde uygulandigini da olctum.

=====================================================================
S2) EntityBase alanlari + soft delete
=====================================================================
Alti alan, tipleriyle:
  Id           long   (BIGINT, PK)
  UniqueId     Guid   (UNIQUEIDENTIFIER — NVARCHAR YASAK, update'te cast patlar)
  ModifiedUser string (NVARCHAR)
  CreatedDate  DateTime  (DATETIME2)
  UpdateDate   DateTime? (DATETIME2, NULLABLE)
  IsActive     bool   (BIT)
Soft delete alani: IsActive. Silmede FIZIKSEL DELETE ATMAM — entity
IEntityNotReallyDelete'ten turedigi icin DELETE otomatik "UPDATE SET
IsActive=false"a doner, sorgular da otomatik WHERE IsActive=1 filtreler.
Onemli ayrim: IsActive = sistem soft-delete ("kayit var/yok"). Is anlamindaki
"pasife al" AYRI bir Status byte enum'una yazilir — IsActive'e dokunursam kayit
tum listelerden kaybolur.
Iki bloker de aklımda: SQL'de ModifiedUser ve UpdateDate NOT NULL OLAMAZ (core
ikisini de INSERT'te doldurmaz -> 500).
EMINIM.

=====================================================================
S3) Migration nasil uretilir — /!\ SORUDA VARSAYIM VAR
=====================================================================
Soru "uretirsin" diyor; refleks cevap "dotnet ef migrations add" olurdu ve
YANLIS olurdu. PR Yazilim'da EF Core AUTO-MIGRATION KULLANILMAZ.
Dogrusu: SQL-MIGRATION.sql dosyasini ELLE yazarim. Kurallari:
  · idempotent (IF NOT EXISTS / IF COL_LENGTH IS NULL) — iki kez kossa patlamaz
  · her kolonda NULL/NOT NULL ACIKCA yazilir (varsayima birakilmaz)
  · CREATE TABLE'in en ustune 6 EntityBase alani ELLE yazilir (C# tarafinda
    kalitimla gelir ama SQL'de otomatik gelmez — iki ayri gerceklik)
  · enum degerleri comment olarak
Ve UC sey daha: SQL'i BEN CALISTIRMAM (kullaniciya veririm, o dev DB'de kosar);
.sql dosyasi GIT'E GIRMEZ (local kalir); tablo acmak once ONAY ister, DISCOVERY'de
yoksa PA'ya donerim.
Uzanti .sql olmali — .md yazarsam .gitignore elemez ve dosya sessizce git'e girer.
EMINIM.

=====================================================================
S4) Enum tanimi — /!\ BURADA DA BIR SORUN VAR
=====================================================================
Yer: library-datatype (tek kaynak). Tip: byte. Ilk deger: 1 (0'dan
BASLAMAM — 0 yalnizca kasitli sentinel icin).
Client nasil alir: BE'den KOPYALAR (senkron). Response'ta enum BYTE olarak doner,
string label DONMEM — etiketi client kendi enum'undan uretir.
/!\ AMA ISIM YANLIS: RandevuDurumu TURKCE. Kanon kod-Ingilizce; dogrusu
AppointmentStatusTypeEnum gibi bir ad ve degerler SCREAMING_SNAKE_CASE:
PENDING=1, APPROVED=2, CANCELLED=3.
Tanimda ayrica: enum karsiligi byte property'ye enum-path comment + handler'da
Enum.IsDefined validasyonu koyarim (yoksa enum-disi deger DB'ye girer).
/!\ Enum.IsDefined'da cast'e dikkat: enum byte tabanliysa (int) cast calisma
aninda patlar, derleme yesil gecer. Bu bende yazili bir ders.
EMINIM (isim/tip/deger). Sinif adinin TAM formatinda (Enum suffix'i zorunlu mu)
EMIN DEGILIM — projede tutarli olana uyarim.

=====================================================================
S5) Klinik kimligi NEREDEN alinir / ALINMAZ
=====================================================================
ALMAM: istekten (request model). Istemciden gelen ClinicId yetki karari icin
KULLANILMAZ — kullanici onu degistirip baska klinigin verisini okur/yazar.
ALIRIM: oturumdan — currentUser (BaseUser) uzerinden; handler'a zaten parametre
olarak geliyor. Yetki bildirimi GetOptions()'ta yapilir, handler govdesinde inline
rol kontrolu yazmam.
Desen: prefix ile aktor tipi ayrilir; sponsor/klinik gibi bir alt-kullanici ise
kimligi oturum modelinden cozen DataLayer metodu cagrilir, cozulemezse
CheckVal ile fail-closed durur.
Admin istisnasi mesru olabilir (admin baska klinigi gorebilir) ama o zaman
"admin mi" kontrolu oturumdan gelir, istekten degil.
/!\ EMIN DEGILIM: BaseUser'da klinik kimliginin HAZIR durup durmadigi projeye
bagli. Bugun goat'ta sponsor icin oturumdan cozen bir metot gordum; klinik
kavrami olan bir projede bu alan yoksa is kimlik katmanina tasar ve o KAPSAM
KARARI benim degil PA'nin. Bugun PRC-41'de tam bu yuzden durdum.

=====================================================================
OZ DEGERLENDIRME
=====================================================================
Bildim (eminim)     : 4 — S1, S2, S3, S5'in ana hukmu
Kismen emin degilim : 2 nokta — S4'te enum sinif adinin tam formati,
                      S5'te BaseUser'da klinik alani var mi (projeye bagli)
Bilmiyorum          : 0 — bos birakmadim, ama yukaridaki iki noktayi
                      "emin degilim" diye isaretledim, uydurmadim
Tuzak yakaladim     : 2 — S3 (EF auto-migration varsayimi) ve S4 (Turkce
                      enum adi). S4'unkini soru bana "hangi projede
                      tanimlarsin" diye sordugu icin kolay atlanabilirdi;
                      adin kendisi kanona aykiriydi.

DURUSTLUK NOTU: Bu cevaplarin dayanagi ezber degil, bu oturumda ACTIGIM uc
skilin govdesi. Skilleri hic acmamis bir BE ayni sorulara bu netlikte cevap
veremezdi — S2'deki alti alanin TIPLERINI ornegin omurga skilim vermiyor,
database skili veriyor. T1'de de bunu soylemistim: "kurali biliyorum ama
ALANLARI bile tam sayamam." Simdi sayabiliyorum, cunku actim.

BEKLEDIGIM: Yok.
