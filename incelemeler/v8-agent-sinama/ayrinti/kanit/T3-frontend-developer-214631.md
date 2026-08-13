# frontend-developer | 2026-08-12 21:46:31

SINAMA T3 — KANON UYUM DENETIMI (frontend-developer)
Repo: /Users/karaok/p/ozel-yazilim/goat · panel: src/web-admin-v2 · branch main
YAZMA YAPILMADI — yalniz okuma. Hicbir dosya degistirilmedi.

═══ ACTIGIM SKILLER ═══
Bu oturumda FIILEN actiklarim (Skill araciyla, govdeleri elimde):
  cekirdek (6): behavior · handoff · memory-management · is-akisi ·
                pr-yazilim-oy-envanteri · frontend
  bu is icin (2): data-access · component

ACMADIKLARIM ve NEDEN — bunu kusur olarak degil KAPSAM SINIRI olarak yaziyorum:
  · style  — ACMADIM. Asagida S3 bulgusunu (text-error) ham CSS olcumune
             dayandirdim, kanon alintisina degil. Yani o bulgunun KANITI saglam,
             ama "hangi kural kodu ihlal edildi" kismini omurgamdaki cache'ten
             (CODE-STYLE-TOKEN) veriyorum, kaynak govdeden degil.
  · list   — ACMADIM. Table/staticData/take yorumlari kodda FE-LIST-* kural
             kodlarina atif veriyor; ben bu kodlari DOGRULAYAMADIM (govde elimde
             degil). Asagida bunu acikca isaretledim.
  · form   — Bu dikey kesitte form YOK (LabelCard salt-okunur gosterim).
             Gereksiz skil acmadim.
Bu sinir onemli: denetim raporunda "uydu/uymadi" hukmu verirken hangi hukmun
kanon govdesine, hangisinin ham olcume dayandigini ayirmazsam rapor guvenilmez
olur.

═══ SECIM: NEDEN BU EKRAN ═══
Sectigim: SearchIndex dikey kesiti
  components/Pages/SearchIndex/SearchIndexTable.tsx   (152 satir)
  components/Pages/SearchIndex/SearchIndexDetail.tsx  (238 satir)
  + dokundugu katman: lib/query.ts · services/ApiService.ts · lib/hooks/*

Uc gerekce:
1. TEK EKRANDA DORT EKSEN BIRDEN VAR: veri katmani (useQuery+useMutate+QUERY_KEYS),
   component (Table/Button/Badge/Modal), stil (token siniflari), liste (DataTable
   + take + staticData). Istenen dort olcutu ayni kesitte olcebiliyorum.
2. EN TAZE KOD: 21e17c92 (2026-08-12, bugun). Kanon en cok taze kodda test edilir;
   eski kod zaten devralinmis borc tasir.
3. YAZAR KONTROLU YAPTIM ve bu SECIMIN SEBEBI OLDU:
   git log --format="%ae" -> son commitlerin TAMAMI mert@pryazilim.com = AGENT
   yazimi. Kanonum (pr-yazilim-oy-envanteri) agent ciktisini emsal olarak
   supheyle almami soyluyor. Emsal almiyorum, DENETLIYORUM — ve denetlenecek en
   dogru hedef tam da agent yazimi kodtur. Insan kodunu (burcu@, 2025-11) secseydim
   olcum "agent kanonu tutturuyor mu" sorusuna cevap vermezdi.

═══ UYDU ═══

[V1] FE-DATA-WRAPPER-ONLY — UYDU.
  Kanon: "TanStack useQuery/useMutation DIREKT import YASAK; custom wrapper zorunlu."
  Kanit: SearchIndexTable.tsx:8 -> `from "@/lib/hooks/useQuery"`
         SearchIndexDetail.tsx:10-11 -> useQuery + useMutate, ikisi de lib/hooks'tan.
  Ikisinde de @tanstack/react-query DIREKT import YOK.
  Istisna dogrulandi: lib/hooks/useQuery.ts:6 ve useMutate.ts:4 TanStack'i import
  ediyor — bu kanonun ACIKCA izin verdigi sarmalayici dosyalar.

[V2] FE-DATA-APISERVICE — UYDU.
  Kanon: "Tek ApiService/baseFetch giris noktasi; component'te ham fetch YASAK."
  Kanit: Table:32, Detail:47/54/72 -> hepsi ApiService.X() uzerinden.
  Iki dosyada da ham fetch(/axios YOK (grep ile dogrulandi).

[V3] FE-DATA-QUERY-KEYS (tek kaynak ekseni) — UYDU.
  Kanit: query.ts:244-247'de dort anahtar tanimli; ikisi de QUERY_KEYS'ten
  okunuyor (Table:31, Detail:46/51/68). Cagri yerinde string template ile
  dinamik key URETIMI YOK — parametre dizinin AYRI elemani olarak giriyor:
  Detail:46 -> [QUERY_KEYS.GET_SEARCH_INDEX_STATUS_DETAIL, String(indexType)]
  Bu tam kanonun istedigi bicim ("stabil-ID gibi dusun: string sabit kalir,
  degisken disarida"). Cakisma taramasi yaptim: dort deger de benzersiz.

[V4] FE-DATA-LOADING-GUARD — UYDU (ve incelikli).
  Kanit: Table:118 -> isPending iken Spinner, veri gelince Table mount ediliyor.
  Detail:105-118 -> data?. zinciri + ?? varsayilanlari; undefined .map/.length'e
  sokulmuyor. Detail:225 ErrorMessageList.map ONCESINDE :223 guard var.

[V5] FE-CMP-REUSE-FIRST — UYDU.
  Kanon: "Native HTML yerine proje ortak component'i."
  Kanit: Button/Badge/Table/Card/CardSection/PageTitle/LabelCard/Spinner —
  hepsi @/components altindan. Native <button>/<input>/<table> HIC YOK.
  Tek native kullanim <div>/<span>/<p> (yerlesim + metin) ki bu mesru.

[V6] FE-CMP-MODAL — UYDU.
  Kanon: "Modal/Toast tek Provider ustunden; her component'te ayri instance YASAK."
  Kanit: Detail:9 useModal context'ten; :153 ve :185 openModal cagrisi.
  Ayri modal instance kurulmamis.

[V7] FE-CMP-NAMING — UYDU.
  PascalCase dosya+isim eslesiyor. Ic-ice (inner) component tanimi YOK —
  columns dizisindeki render fonksiyonlari component TANIMI degil, JSX
  donduren fonksiyon (bu kanonun yasakladigi sey degil).

[V8] CODE-STYLE-TOKEN (ham deger ekseni) — UYDU.
  Kanit: grep ile ham hex (#rrggbb) ve px degeri aradim -> SIFIR.
  Tum stil semantik sinif uzerinden (text-md-medium, text-primary...).
  ⚠️ Ama bu ekseni "tam uydu" diye kapatmiyorum — S3'e bak.

[V9] Sozlesme-alan uyumu — UYDU (ve iyi yapilmis).
  Detail:69-72'de yorumla isaretlenmis: bir uc IndexName (metin) alirken
  digeri IndexType (sayi) aliyor. Bu asimetri fark edilmis, guard konmus
  (:151 disabled={!data?.IndexName}). Bu benim en cok deger verdigim sinif —
  cunku bu hatayi derleme YAKALAMAZ.

═══ UYMADI / BULGU ═══

[S1] QUERY_KEYS DEGER BICIMI — kanona UYMADI, ama borc DEVRALINMIS.
  Kanon (FE-DATA-QUERY-KEYS, gövdeden): "anahtar SCREAMING_SNAKE_CASE, deger
  saf sabit string (kebab-case)".
  Bulgu: query.ts:244-247 -> deger de SCREAMING:
     GET_SEARCH_INDEX_STATUS_LIST: "GET_SEARCH_INDEX_STATUS_LIST"
  Kanona gore "get-search-index-status-list" olmaliydi.

  OLCTUM (bu kismi onemsiyorum): 166 anahtarin
     142'si kebab-case  ('get-system-parameter-list')
      24'u SCREAMING    ("GET_COUNTRY_LIST")
  Yani panelin COGUNLUK deseni kebab = kanonla ayni yonde.

  KIM BASLATTI: git log -S ile olctum ->
     SCREAMING'i baslatan: 07c9a68e burcu@pryazilim.com 2025-11-14 (INSAN)
     SearchIndex anahtarlari: 21e17c92 mert@pryazilim.com 2026-08-12 (AGENT)
  HUKUM: agent yeni bir sapma ICAT ETMEDI, mevcut azinlik desenini takip etti.
  Ama kanonum tam bu durum icin acik: BEHAVIOR-CANON-OVER-EMSAL — "Projedeki
  emsal kanonla celisiyorsa kanon uygulanir, emsal kopyalanmaz." Yani
  "emsalde boyleydi" bir savunma DEGIL. Bu bir ihlal, agirligi dusuk (islevsel
  etkisi yok, cunku degerler benzersiz ve cakismiyor).
  SINIF: teknik borc / tutarlilik. Islevsel risk: yok.

[S2] `SEARCH_INDEX_PAGE_SIZE` KULLANIMDAN SONRA TANIMLI — kucuk ama gercek.
  Kanit: SearchIndexTable.tsx:138 kullaniyor, :152 tanimliyor.
  const TDZ'ye tabidir; burada patlamiyor cunku degeri render sirasinda
  okunuyor (modul zaten yuklenmis olur). Yani CALISIR — ama okuyanı yaniltir
  ve dosyayi yukaridan asagi okunamaz kilar. Sabitin evi dosyanin BASI.
  SINIF: okunabilirlik. Islevsel risk: yok (bu haliyle).

[S3] `text-error` TOKEN'I TANIMSIZ — ISLEVSEL BULGU, en ciddi olan.
  Kanit zinciri (uc adimda olctum):
    1. SearchIndexDetail.tsx:226 -> className="text-sm-regular text-error"
    2. styles/colors.css icinde 'error' gecen DEGISKEN: SIFIR
       (--color-error tanimi YOK; --color-primary/secondary/tertiary VAR)
    3. Panel Tailwind v4 @theme deseni kullaniyor (colors.css:1 "@theme {")
       yani text-X sinifini --color-X degiskeni URETIR. Degisken yoksa sinif
       da uretilmez.
  SONUC: text-error bir CSS sinifi uretmiyor -> hata mesajlari renksiz
  (varsayilan metin renginde) basiliyor. Kirmizi gorunmesi beklenen uyari
  gorsel olarak sessiz kaliyor.

  ⚠️ ONEMLI: bu SearchIndex'in ICAT ETTIGI bir hata DEGIL. Ayni sinif panelde
  4 yerde kullaniliyor: Dropzone.tsx, SearchIndexDetail.tsx, SiteUserTicketDetail.tsx,
  SponsorTicketDetail.tsx. Yani SISTEMIK — token setinde eksik var, ekranlar
  onu var sanip kullaniyor.
  SINIF: islevsel (gorsel). Bu bulgu kapsamimin DISINA tasar -> asagiya bak.

  DURUSTLUK NOTU: bu bulguyu `style` skilini ACMADAN uretttim. Olcum ham CSS
  uzerinde yapildi ve saglam; ama kural kodunu (CODE-STYLE-TOKEN) omurgamdaki
  ozet bloktan aliyorum — omurgam kendisi "Bu blok CACHE'tir, kaynak degil"
  diyor. Hukum vermeden once style skilini acmam gerekirdi; acmadim cunku
  bulgu tarama sirasinda ciktı. Bunu kusur olarak isaretliyorum.

═══ DOGRULAYAMADIGIM (govde elimde degil) ═══
Kodda su kural kodlarina atif veren yorumlar var:
  Table:115 "FE-LIST-STATIC-GUARD"  ·  Table:130 "FE-LIST-STATIC-SEARCH"
Bu kodlarin GERCEK govdesini goremedim (list skilini acmadim). Yorumlarin
anlattigi davranis mantikli ve kodla tutarli gorunuyor (veri gelmeden Table
mount edilmiyor; staticData modunda arama kapatilmis; take acikca verilmis).
Ama "bu kural gercekten boyle diyor mu" DOGRULAMASINI YAPMADIM.
Bunu "uydu" diye YAZMIYORUM — dogrulanmamis birakiyorum. Kanit olmadan
hukum vermek, denetimin kendisini bozar.

═══ GENEL HUKUM ═══
Bu ekran kanona BUYUK OLCUDE UYUYOR. Sekiz eksende temiz; ikisi teknik borc
(biri devralinmis), biri sistemik gorsel bulgu.

Dikkat cekici bulduğum sey: kodun yorumlari savunma degil GEREKCE tasiyor —
"neden boyle yapildi" + hangi saha bulgusundan dogdugu yazili (Detail:59-61
modalin hata durumunda kapanmamasi; :207-210 Azure indeksleme gecikmesi
olculmus: "anlik 42, ~5 sn sonra 47"). Bu, benim de uydugum bir kanonun
(gerekce yazma) fiilen uygulanmis hali.

SISTEMIK BULGU YONLENDIRMESI (kanonuma gore):
S3 (text-error) benim yazdigim kod DEGIL ve tek ekrani asiyor (4 tuketici).
Kanonum bu durumda kok neden teshisi yapmami degil, YAPILANDIRILMIS RAPORLA
PA'ya yonlendirmemi soyluyor. Yani: bu bulguyu duzeltmeye kalkmam; PA triyaj
eder, gerekirse TE repro eder, sonra bana doner. Burada yalniz raporluyorum.

BEKLEDIGIM: Bu rapor uzerine hukmun. S3 icin PA'ya yonlendirme istersen
handoff blogunu yazarim.
