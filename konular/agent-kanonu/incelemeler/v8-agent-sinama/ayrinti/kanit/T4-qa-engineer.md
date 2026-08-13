# T4 qa-engineer | 2026-08-12 21:57:11

SINAMA T4 — kanon sapmasi avi (qa-engineer)

Yalniz BUGUN FIILEN CARPTIGIM yerleri yaziyorum. Teorik tarama yapmadim —
uydurma sapma olcumu bozar.

═══ S1) CELISKI ═══

C1. QA-USER-LANGUAGE  x  QA-EVIDENCE-NO-DIRECTIVE + commit-review cikti formati
    Ayni ciktida iki zit emir. Alintilar:
    QA-USER-LANGUAGE: "doğrulama kanıtı (kanon-ID listesi, üç-akış adım dökümü,
    TARANAN DOSYA SAYISI) RAPORLANMAZ" ve "'şu dosyanın şu satırında' koordinatı
    girmez".
    QA-EVIDENCE-NO-DIRECTIVE: "Kod kanıtı olmayan bulgu YASAK (dosya:satır/pattern
    ZORUNLU)."
    commit-review cikti sablonu: "#{n} | Bulgu | YER | Neden önemli"
    >> Carptigi an: BUGUN, T3 raporunda. "Yer" alanini doldurursam koordinat
    yasagina, doldurmazsam kanit zorunluluguna giriyorum. Ustelik Clara "kac
    dosya okudugunu" ISTEDI — QA-USER-LANGUAGE onu ismen yasakliyor.
    Cozdugum yol: koordinat yerine YAPI adi yazdim ("admin'de filtrelenmis
    liste"), dosya sayisini istendigi icin verdim. Ikisi de kanonun
    duzenlemedigi bir orta yol — yani kural degil ben karar verdim.
    Not: gerilim sahte degil, "kime giden mesaj" ayrimi kurala YAZILMAMIS:
    kullaniciya ozet / developer'a kanit. Ayrim olsa celiski cozulur.

C2. HANDOFF-REVISE-BLOCK-REQUIRED  x  (rapor dosyasi ureten kural YOK)
    Alinti: "`Oku:` = revizyon maddelerinin yazılı olduğu TEK yer (RAPOR
    DOSYASI/ClickUp task'ı/commit) — maddeleri bloğa dökme."
    Kural bir rapor dosyasinin VAR OLDUGUNU varsayiyor; ama QA'nin o dosyayi
    uretmesini soyleyen kural yok. Ayrica HANDOFF-SCREEN-ONLY handoff'u diske
    yazmayi yasakliyor. Sonuc: maddeleri bloga dokemiyorum, dosyaya da
    yazamiyorum (kural yok), geriye kanal/ekran kaliyor — ve orasi ucucu.
    >> S2'deki bosluga baglaniyor; ayni yaranin iki yuzu.

═══ S2) BOSLUK ═══

B1. QA CIKTISININ KALICI EVI YOK. (En agir bulgum.)
    Bugun uc olcum urettim (T1 kanon envanteri, T2 push reddi gerekcesi,
    T3 denetim raporu + iki simulasyon). UCU DE yalnizca kanalda duruyor.
    Kanal arsivlenince gider.
    Olctum: quality + commit-review + module-audit + production-audit + handoff
    icinde "QA raporunu su dosyaya yaz" diyen TEK kural yok. Kiyas: CA'nin
    AUDIT-REPORT/REMEDIATION ciktisi ADLANDIRILMIS (module-audit:78'de
    ismen geciyor). QA'nin muadili yok.
    Somut kayip: T3'te uc simulasyon kosturdum (6 senaryo yetki, 22x14 yol,
    1 kirilganlik). Ayni commit yarin bir daha denetlenirse bu olcum
    SIFIRDAN tekrarlanir — cunku hicbir yerde yazili degil.
    Not: memory bunun evi DEGIL (MEMORY-POINTER-ONLY: is-kaydi yasak) —
    yani "memory'ye yaz" cevabi da kanon disi. Ev gercekten yok.

B2. "DISCOVERY YOKSA" hali duzenlenmemis.
    QA-DISCOVERY-GATE: "Her commit DISCOVERY kapsamiyla karsilastirilir."
    Bugun goat'ta DISCOVERY bulamadim. Kural "yoksa ne yapilir" demiyor:
    denetim durur mu, kapsam beyanina guvenilir mi, bu tek basina RED mi?
    Kendi kararimla ilerledim ve raporda "kapiyi tam calistiramadim" diye
    isaretledim — ama bu benim tercihim, kanonun cevabi degil.

B3. TATBIKAT/OLCUM MODU yok.
    QA-APPROVE-ATOMIC onayi bolunemez sayar: sub task + kapanis handoff'u +
    PA bilgisi "ayrilamaz". Bugun "hukum ver ama UYGULAMA" dendi — yani
    atomik uculu kasitli olarak bolundu. Kanonda bu mod tanimli degil;
    talimatla kanon arasinda kaldim, uygulamayip raporda ISARETLEDIM.
    Kucuk ama gercek: bir kuralin "istisnasi yok" demesi, tatbikati da
    ihlal gibi gosteriyor.

═══ S3) FAZLALIK / OLU KURAL ═══

Net bir olu kural BULAMADIM — ve bunu uydurmayacagim.
Bugun tetiklenmeyen cok kural oldu (CR-SQL-DIFF, CR-DEPLOY-ENV, CR-BJ...)
ama tetiklenmemek olu olmak degildir: commit'te o desen yoktu, o kadar.
"Bu satir olmasa ne yanlis yapardim" testini gecemedigim bir kural
goremedim.

Tek ZAYIF gozlem (fazlalik degil, konum): QA-METRIC-SPLIT hem quality
omurgasinda hem commit-review "Karar seviyeleri" bolumunde anlatiliyor.
Ikisi celismiyor (biri olcut, oteki uygulama) — bu yuzden sapma DEMIYORUM,
yalnizca not.

═══ KENDI SINIRIM ═══
· Yalniz KENDI kanonuma baktim. Baska agentin kuralina hukum vermedim.
· Isaret (benim isim DEGIL): B1'in ayni yarasi CA/TE'de de olabilir —
  ciktisi rapor olan her rol ayni evsizlikte. Bakmadim, onlarin isi.
· C1'i "celiski" diye yazdim ama iki kural farkli MUHATABI kastediyor
  olabilir (kullanici vs developer) — o zaman celiski degil eksik ifade
  olur. Hangisi oldugundan EMIN DEGILIM, isaretliyorum.
· Govdesi elimde OLMAYAN skillerde (code-quality, database, enum-sync...)
  sapma aramadim — okumadigim metin hakkinda hukum vermem.

BEKLEDIGIM: Yok — dort olcum tamamlandi.
