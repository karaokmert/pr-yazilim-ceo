# devops-engineer | 2026-08-13 01:01:45

KENDINI DEGERLENDIRME — devops-engineer (4 baslik)

═══ 1) AGENT BODY ═══

BULANIK — "Seni QA kapatmaz (kendin kapanir / PA toparlar)".
Bugun carptim: kapanis kimde belirsiz. "kendin kapanir" ile "PA toparlar" iki
farkli senaryo, hangisi ne zaman yazmiyor. Detay 4. baslikta (celiski).
ONERI: "DO'nun kapanisini kullanici ya da PA acar; kapanis sinyali YOKKEN
kendiliginden kapanma — sinyal gelmezse kullanicidan SOR (askida kalma yasak)."

EKSIK — body "kurulum sonrasi QA'ya saglik dogrulama IS" diyor ama QA'ya
GITMEYEN kurulumda (panel/proje) kapanis adresi yok; "PA'ya BILGI" veriyorum,
sonra ne? Yukaridaki cumle bunu da kapatir.

═══ 2) OMURGA SKIL ═══

HARITA ETIKETI YANILTICI — alet cantasi `deploy-release`i "Git akisi / push-merge
sahipligi / deploy rol paylasimi" diye tanitiyor. Bugun olctum: o skilde DO'nun
YEDI prod kurali var (PRECHECK-7 · PRODUCTION-TAG · MERGE-COMMIT-ONLY ·
NO-ROLLBACK-MISSING · SUCCESS-NOT-COMPLETE · PROD-DIFF · BRANCH-ENV) — hicbiri
"git akisi" degil. DO-NO-DEV-GIT "dev git isin yok" dedigi icin bu etiket
"bana degil" diye okunabilir ve prod kapisi sessizce atlanir.
ONERI: satiri degistir -> "**Production deploy kapisi (7 pre-check, tag, rollback,
merge stratejisi) + git akisi/push-merge sahipligi** -> `deploy-release`"

═══ 3) REFERENCE ═══

BUGUN ACMADIGIM ama ACMALIYDIM: memory-management/references/ (3 dosya).
Ilk refleksim govdeyle denetlemekti; govde 7 turu ad+tek cumle veriyor, AYIRT
ETME olcutu (hangi tur hangisi) reference'ta. Actim, denetim degisti.
ONERI: SKILL.md'de tur listesinin ustune tek satir -> "⚠️ Bir kaydi
SINIFLANDIRIYORSAN `references/icerik-turleri.md` ACILMADAN karar verme."

IYI DURUM (degistirilmesin): REL-DO-PRECHECK-7'nin 7 kalemlik listesi GOVDEDE,
reference'a inmemis. Dogru tercih — reference acilmayabilir, o liste kritik.

═══ 4) ⚠️ CELISKI — "kapanis dali tanimsiz" (T4 ile ayni sinif) ═══

`HANDOFF-CLOSE-AUTO-FINISH`: "kapanis handoff'u YOKKEN kendiliginden kapanmak
YASAK — kapiyi tutan rol acar."
`MEMORY-NO-SELF-CLOSE-WRITE`: "kullanici/handoff tetiklemeden pozitif kapanis
kaydi YASAK."
BODY: "Seni QA kapatmaz — kendin kapanir."

Ucu birlikte IMKANSIZ: DO'nun kapisini tutan rol TANIMLI DEGIL (QA kapatmiyor,
PA "toparliyor" — bu bir sinyal mi belirsiz). Yani "kendin kapan" deniyor ama
kendiliginden kapanmak iki kuralla yasak. DAL YOK: sinyal hic gelmezse ne olur
yazmiyor. Developer'da bu dal kapali (QA kapatir), DO'da acik.
ONERI (tek cumle, uc yere de uyar): "Kapanis sinyali olmayan rollerde (DO)
kapanisi KULLANICI acar; sinyal gelmediyse agent kendiliginden kapanmaz,
kullanicidan kapanis teyidi ISTER."

BASKA CELISKI ARADIM, BULAMADIM. DO-NO-RUN ile PRECHECK-7 celisir gibi duruyor
(kontrol et ama calistirma) ama degil: pre-check "komutu yaz, kullanici kossun"
ile uyumlu, dal tanimli. Uydurmuyorum — bu ikisi temiz.
