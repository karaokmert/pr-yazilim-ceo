# test-engineer | 2026-08-13 00:52:06

MEMORY DENETIMI — BITTI (TE)

DENETLENEN: 8 dosya (index + kapanis-index + kapanis-notu + 4 kazanim + 1 proje bilgisi).
Hepsinin GOVDESI okundu, beyanla yetinilmedi. Kanon tarafinda memory-management SKILL.md
+ icerik-turleri.md + kapanis.md REFERANSLARI fiilen acildi (reference kendiliginden
yuklenmez — acmadigim kural beni baglar ama bende olmaz).

═══ BULGULAR (2 celiski, ikisi de duzeltildi) ═══

1) TUR ALANI YANLIS — 4 dosyada. kazanim_odeme-tipi-repro / nextjs-ssr-hata-olcutu /
   arac-iddiasi-degil-sonuc / intercept-ayirt-edici-test dosyalarinda frontmatter
   "type: project" ya da "type: feedback" diyordu; icerik ise kanonun #5 turu
   (Hata+Kazanim). Etiket kanonu uc turun adinin SABIT oldugunu, esanlamli kullanmanin
   terfi koprusunu kirdigini soyluyor (tarama ADA bakiyor) — yani bu kayitlar terfi
   taramasinda gorunmeyecekti. DUZELTILDI: dordu de type: kazanim.
   Ek: odeme-tipi-repro'nun govdesinde zaten [QA-pattern-gozlemi] etiketi vardi ama
   frontmatter "project" diyordu — etiket ile tur birbirini tutmuyordu.

2) INDEX'TE TUR KARISMASI — uc kazanim dosyasi "Proje bilgileri" basligi altinda
   listelenmisti. Kazanim proje bilgisi degil. DUZELTILDI: basliklar ayrildi.

Emin olmadigim icin SILMEDIGIM sey: kapanis-notu-goat-boost-lifecycle-test.md.
Icinde GOAT'a dair "su an gecerli degil olabilir" iddialar var (veri engeli, duran uc
bulgu). Ama bu bir DEVIR KOPRUSU ve kanon (KAPANIS-DEVRAL-TEMIZLE) onun ancak
DEVRALINIRKEN temizlenmesini soyluyor — GOAT isi acilmadan silmek bilgi kaybi olur.
Dokunmadim, ACIK birakildi.

═══ EKLENEN (2 yeni dosya, ikisi de POINTER — kural govdesi kopyalanmadi) ═══

3. madde (her iste lazim) → kazanim_te-her-iste-gecerli.md
   Rol sinirim 4 yasak (TE-SCENARIO-NOT-STATIC / TE-FINDING-NOT-GATE /
   CODE-NO-WRITE-ON-AUDIT / BEHAVIOR-NO-INFRA-CMD + curl istisnasi), kosum araci
   (TE-E2E-MCP, TE-MCP-ASK-INSTALL), veri kanali (TE-DATA-VIA-UI-OR-API),
   teshis sirasi (ucuzdan zora, kod EN SON).

4. madde (gozden kacabilecek) → kazanim_te-sessiz-arizalar.md
   Sessiz arizalar: tek oturumda sirayla ≠ cok kullanicili test (eszamanlilik hatasini
   GIZLER, test yesil yanar); dev domain eski kod calistirabilir; arac raporu ≠ sonuc;
   iOS+Android ayri kosum; kanitsiz "calismiyor" yasagi.
   Sira kurallari: senaryo listesi ONCE onaylatilir; DISCOVERY'siz senaryo yasak;
   perf sikayetinde olcmeden yorum yasak (≥5 olcum, cold/warm ayri, esik 2x);
   E2E'de kirilan senaryo ayri is degil, repro'nun girdisi.
   Refleks tuzaklari: "yalniz su tipte calismiyor" / "sayfa aciliyor demek ki saglam" /
   alan yoklugunda null-mu degil anahtar-var-mi.

VAR OLANA EKLEME: 0 yeni konu mevcut kayitlara sigmadi — mevcut dort kazanimim SAHA
olcumleri (olcum/ortam tuzaklari), eklenenler ise ROL SINIRI + MOD SIRASI. Farkli sinif,
ayri dosya. Ama iki dosyada topladim, alti ayri dosya acmadim (index sismesin).

═══ OLCUM ═══
· Denetlenen kayit: 8 · Celiski: 2 (ikisi de duzeltildi) · Silinen: 0
· Yeni dosya: 2 · Var olana eklenen: 0 · Yetim dosya: 0 (dogrulandi)
· INDEX: 11 satir → 17 satir (tavan 200). Index SAF pointer kaldi — kural metni
  ICERMIYOR, cunku index context'e OTOMATIK giriyor ve oraya yazilan cumle pasif not
  degil DAVRANIS TALIMATI oluyor (MEMORY-INDEX-IS-CONTEXT).

═══ SANA SORUM (1 tane) ═══
Yazdigim iki yeni kayit SKIL POINTER'i tasiyor (kural ID + tek satir ozet).
MEMORY-POINTER-ONLY bunu mesru sayiyor ama iki kosulla: (1) atif BASLIKLA verilir —
uydum, satir numarasi kullanmadim; (2) "AG taramasinda skille capraz dogrulanir".
Ikinci kosul benim yapabilecegim bir sey degil. Bu kayitlar bir sonraki AG taramasina
girmeli mi, yoksa boyle birakilip skil degisince benim tazelemem mi bekleniyor?
Skil degisirse pointer'im sessizce bayatlar — bunun bir sahibi var mi?
