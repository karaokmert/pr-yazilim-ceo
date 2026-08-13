# test-engineer | 2026-08-13 01:01:39

KENDINI DEGERLENDIR — TE (dort baslik)

═══ 1) BODY ═══
BULANIK: body "Uc modun var — gelen ise gore biri acilir" diyor ama MOD SECIMI KIMDE
belirsiz. Bugun carptim: is geldiginde modu ben mi seciyorum, PA mi soyluyor? Body
"gelen ise gore" diyor (pasif), is-akisi reference'i "Ilk soru: elimdeki test isi mi,
bug mu, veri isi mi" diyor (aktif, bende). Ikisi ayni sey degil.
ONERI (body §Is akisin, ilk cumle): "Modu SEN secersin — gelen isin turunu ANLA
adiminda kendin siniflandirirsin; PA mod adi vermez, is verir."
FAZLA: bulamadim. NE EKSIK: asagida (4. baslik) — DISCOVERY yoklugu.

═══ 2) OMURGA ═══
ALET CANTASI EKSIGI — YOK, harita bugun tuttu (dev-environment dahil dogru yonlendirdi).
GEREKCESIZ KURAL — YOK; dordu de gerekcesini tasiyor (TE-DATA-VIA-UI-OR-API'nin "audit
alanlari/queue tetikleri atlanir" gerekcesi ozellikle iyi, kural ezberlenmiyor anlasiliyor).
YANLIS YER: TE-PERF-BASELINE-FIRST repro-diagnosis'te. Ama performans sikayeti E2E
turunda da geliyor ("modul bitti, test et" → bir ekran yavas). Mod 2'deyken o kural
elimde OLMUYOR. ONERI: kural omurgaya (`test-engineer`) tasinsin, iki mod da gorsun.

═══ 3) REFERENCE ═══
BUGUN ACMADIGIM ama acmaliydim: `is-akisi/references/test-engineer-is-akisi.md`.
Body ozet veriyor, "yeterli" hissi verdigi icin acmadim — sonra actim, icinde body'de
OLMAYAN sey vardi (mod secim sorusu, CA/QA ikizi degilim ayrimi). Klasik BEHAVIOR-
REFERENCE-NOT-AUTOLOADED tuzagi: ozet varken derinlik atlaniyor.
GOVDEYE CIKMALI: `perf-olcum.md`daki "PROD'dan 7 kat yavas" VAKASI degil ama
**"tek ortam olcumu yanilticidir"** hukmu — cunku reference acilmazsa o kural kaybolur
ve tek-ortam olcumu en dogal reflekstir. Hukum govdede, vaka reference'ta kalsin.
SISIREN: bulamadim.

═══ 4) ⚠️ CELISKI — DISCOVERY YOKLUK DALI TANIMSIZ ═══
`e2e-verification`: "DISCOVERY.md oku (ZORUNLU) ... DISCOVERY'siz senaryo YASAK" +
"Platform kararini DISCOVERY'den cikar, KULLANICIYA SORMA".
`proje-dosya-duzeni` DOC-TASK-FOLDER: discovery.md **task-folder icinde**, PA uretir —
yani her iste VAR OLMAYABILIR (yeni proje, devralinan proje, dokumansiz modul).
CELISKI: dosya yoksa kural beni DURDURUYOR ama alternatif VERMIYOR; ustelik ayni
cumlede kullaniciya sormak da yasaklanmis. Iki cikis da kapali → dal tanimsiz.
Bugun fiilen carptim: bu repoda DISCOVERY yok; E2E isi gelseydi kuralim beni kilitlerdi.
ONERI (e2e-verification, DISCOVERY maddesinin altina):
"DISCOVERY YOKSA senaryo uydurulmaz ve is sessizce atlanmaz: (a) PA'dan discovery
iste — gereksinim PA'nin isi; (b) PA yoksa/uretilemiyorsa kapsami KULLANICIYA
onaylatarak cikar (bu durumda platform sorusu mesrudur, yasak yalniz DISCOVERY
varken gecerlidir); (c) ikisi de yoksa isi baslatma, eksigi bildir."
Bu T4'te uc agentin buldugu "arac yoksa ne olur" sinifiyla ayni: **girdi yoksa ne olur**.

⚠️ Ikinci sinif ornegi (ayni aile, daha kucuk): TE-MCP-ASK-INSTALL "kur de" diyor,
kullanici KURAMAZSA ne olacagi tanimsiz — is bekler mi, kismi mi kosulur, PA'ya mi doner?
