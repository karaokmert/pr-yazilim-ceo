# SINAV 3 — qa-engineer | 2026-08-12 23:39:33

SINAV 3 — SKILL HARITASI. Skill ACMADIM, alet cantasindan hatirladigim.

SEN-1) BE commit: yeni tablo + handler + endpoint
ACACAKLARIM (sirayla):
 1. commit-review — inceleme akisinin kendisi (6 adim, CR-* tetikleyicileri)
 2. database — yeni TABLO var: EntityBase 6 alan, tip kanonu, DATETIME2/
    NVARCHAR, tekil ad, elle-SQL migration
 3. module-development — HANDLER var: adlandirma, GetOptions/CheckAccess
    yetkisi, handler tek is (validate->DataLayer->response), N+1
 4. response-request — ENDPOINT var: zarf sekli, sayfali liste, Page/Take
 5. code-quality — jenerik esik + teknik borc (TODO/magic/olu kod)
 + kosullu: enum-sync (commit'te enum varsa), tasarim-prensipleri (sessiz
   yutma / idempotency supheliyse)
ACMAYACAKLARIM: frontend/mobile (BE commit'i, o katman yok) · production-audit
 (canliya cikis degil) · deploy-release (push istenmedi).

SEN-2) Modul kapanisi, bes commit, tum yuzey
ACACAKLARIM:
 1. module-audit — is turu BU: tek diff degil modulun tum yuzeyi + yapisal
    uyum skoru
 2. commit-review (toplu-mod) — bireysel commit OK ≠ push'a hazir; modul
    butunlugu + commit-arasi tutarlilik (BE yeni sozlesme gonderirken FE
    eskisini mi tuketiyor)
 3. ilgili katman kanonlari — modulde ne varsa (backend/frontend/mobile +
    alt skilleri); denetim olcutu orada
 + qa-denetim-lensi (quality reference'i) — degisen yapiyi kanona eslerken
   "neye bakilacak" listesi
ACMAYACAKLARIM: escaped-bug-analysis (kacan hata yok) · production-audit
 (canliya cikis ayri mod).
NOT: cross-module diff buyukse CA'ya reaktif etki analizi tetiklerim
 (QA-IMPACT-REACTIVE-TRIGGER) — skil degil, handoff.

SEN-3) "Dev'de hata cikti, senin kapindan gecmisti"
ACACAKLARIM:
 1. escaped-bug-analysis — is turu tam BU: kacan hata, oz elestiri,
    hangi kontrol atlandi, ders sonraki incelemeye nasil tasinir
 2. ilgili katman kanonu — hatanin dustugu yer neresiyse (kural gercekten
    var miydi, ben mi atladim yoksa kanonda bosluk mu)
 + kacirma deseni tekrar ediyorsa [QA-pattern-gozlemi] olarak isaretlerim
SINIR — bu is BENIM ama TAMAMI degil: hatanin TEDAVISI developer'in,
 dinamik REPRO'su TE'nin, derin statik kok-neden CA'nin. Ben "neden
 kacti"yi uretirim, fix'i degil. Savunma degil oz elestiri uretilir.

SEN-4) Canliya cikis, "taramayi baslat"
ACACAKLARIM:
 1. production-audit — is turu BU; 3 asama atlanamaz (altyapi+SQL /
    model-veri: dolu tabloya NOT NULL-FK-enum cakismasi + backfill /
    etki: silinen-imzasi degisen endpoint + kontrat daralmasi + shared
    lib tuketicileri)
 2. database — prod SQL'in sahibi QA; kaynak KOD (MODUL-BILGI degil)
 3. deploy-release — branch->ortam, merge stratejisi (squash prod-only
    commit'leri SILER), kimin neyi yaptigi
ACMAYACAKLARIM: commit-review (tekil diff modu degil).
SINIRIM: tararim + GO veririm; SQL'i CALISTIRMAM, prod'da MERGE ETMEM
 (merge kullanicida), prod CURL yapmam (DO'da).

SEN-5) SQL migration + entity'de yeni alanlar — tipleri nasil kontrol ederim
ACACAKLARIM:
 1. database — TEK kaynak: canonical tip kanonu, DATETIME2 (DATETIME yasak),
    NVARCHAR (VARCHAR yasak), byte enum, {Action}Date adlandirmasi,
    ModifiedUser/UpdateDate NOT NULL YASAK (ikisi de blokor)
 2. commit-review — CR-SQL-DIFF tetigi (.sql diff'te gorunuyorsa)
 + enum-sync (yeni alan enum ise: byte, 1-tabanli, tek kaynak library-datatype)
YONTEM (skil degil): SQL ile entity'yi YAN YANA okurum — kolon tipi ile
 C# property tipi eslesiyor mu, nullability iki tarafta ayni mi.
⚠️ DURUSTLUK: database govdesi su an bende YOK. Yukaridaki alti kural
 quality omurgamdaki OZET bloktan; tam tip tablosu (hangi alan hangi tip)
 database'de ve onu ACMADAN kesin hukum veremem.

═══ OZ DEGERLENDIRME ═══
EMINDIM: 4 senaryo (SEN-1,2,3,4) — is turu -> skil eslemesi alet
 cantasinda net, hepsi orada yazili.
TAHMIN ETTIGIM: SEN-5'in ikincil kalemleri — CR-SQL-DIFF'in tam tetigi
 ("BLOKE" diyordu ama kapsamini ozet duzeyinde biliyorum) ve enum-sync'in
 devreye girip girmeyecegi alanin turune bagli.
BILMEDIGIM: 0 senaryo. Ama iki BOSLUK isaretliyorum:
 · database / module-development / response-request / enum-sync /
   code-quality govdeleri su an bende YOK — adlarini ve ne icin
   acilacaklarini biliyorum, KURALLARIN TAM METNINI bilmiyorum.
   Gercek iste bunlari ACARAK denetlerim; hafizadan denetim kapiyi deler.
 · "76 skil" dedin — ben yalnizca kendi alet cantamdakileri sayabildim.
   Listede olup benim gormedigim bir skil varsa onu bilmiyorum.

BEKLEDIGIM: Yok.
