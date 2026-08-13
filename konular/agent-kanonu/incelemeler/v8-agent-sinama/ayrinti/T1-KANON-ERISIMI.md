# T1 — Kanon erişimi ölçümü

> Soru: agent'lar kanonlarına **tam erişebiliyor mu?** (Mert'in 2. maddesi)
> Yöntem: beyan değil **alıntı** istendi; alıntılar gerçek dosyalarla karşılaştırıldı.
> Kaynak: `~/.claude/plugins/cache/pryazilim-agents/ozel-yazilim/0.7.0/`

## Sonuç: EVET — ama otomatik değil, telafi ile

Beş agent (PA · BE · FE · QA · CA) test edildi. **Beşi de** omurga skill'inden
kelimesi kelimesine alıntı yapabildi ve alıntıların **hepsi gerçek dosyada doğrulandı.**

### Doğrulanan alıntılar (uydurma YOK)

| Agent | Alıntıladığı kural | Dosyada | Doğrulama |
|---|---|---|---|
| QA | `QA-STATIC-GATE` | quality/SKILL.md:108 | birebir |
| QA | `QA-STANDARD-MATCH` | quality/SKILL.md:131 | birebir |
| QA | `BEHAVIOR-REFERENCE-NOT-AUTOLOADED` | behavior/SKILL.md:18 | birebir |
| CA | `CA-NO-DIRECTIVE` | code-auditor/SKILL.md:21 | birebir |
| CA | `CA-STATIC-NO-REPRO` | code-auditor/SKILL.md:28 | birebir |
| FE | `FE-MOTION-DOM-PIN` | frontend/SKILL.md | birebir |

CA ayrıca dört skill'in **satır sayısını** verdi: 56 / 67 / 77 / 152.
Ölçtüm — **dördü de doğru.** Yani CA gerçekten diske baktı, hatırlamadı.

## Ama mekanizma bozuk — telafi ile ayakta

FE'nin bildirimi (ve doğrulandı):

> *"Preload mekanizması bu ortamda çalışmıyor. Tanımındaki `skills:` alanında
> listelenen skill'lerin GÖVDESİ context'ine girmedi — elinde yalnız description var."*

**Bu bilinen bir Claude Code arızası** ve fabrika bunu biliyor. `hooks/hooks.json`:

> *"Preload boşluğu telafisi: `skills:` frontmatter'ı plugin agentlarında sessizce
> çalışmadığı için (anthropics/claude-code#15178) açılışta skil yükleme talimatı enjekte eder."*

Telafi düzgün tasarlanmış: `preload-skills.py` agent dosyasını **tek kaynak** kabul
ediyor, listeyi script'e gömmüyor, bug düzelince kaldırılabilir.

### Kalan risk — telafi agent disiplinine bağlı

Hook bir **talimat** basıyor; yüklemeyi agent yapıyor. Bugün beşi de yaptı.
Yapmayan bir agent "skillerim yüklü" sanır ve elinde yalnız description olur —
**ve bu sessizdir.** Ölçüm yapılmadan fark edilmez.

## Üç katman ayrımı — FE'nin katkısı

FE sorumu düzeltti ve haklıydı: iki değil **üç** katman var.

1. **Gövdesi elde** — omurga + çekirdek skill'ler (6-7 tane, elle yüklenmiş)
2. **Yalnız ad/tarif** — öz skill'ler (~120 tane), işe girerken açılır
3. **Reference dosyaları** — HİÇBİRİ elde değil, atıfla açılır

Üçüncü katmanı üç agent bağımsız bildirdi (QA · CA · FE) ve üçü de aynı kuralı
gösterdi: `BEHAVIOR-REFERENCE-NOT-AUTOLOADED`. Yani kanon bu sınırı **kendisi
söylüyor** ve agent'lar okumuş.

QA'nın kendi cümlesi: *"'diskte var' ile 'elimde var' farklı iki şey. Ayırt ediyorum."*

## QA'nın kendi bildirdiği açık

> *"En sık yaptığım iş COMMIT İNCELEME ve o işin skill'i (`commit-review`) şu an
> gövdesiz. 6 adımlı inceleme akışı orada. Bir commit gelirse ÖNCE onu açmam gerekir."*

Bu doğru davranış (on-demand tasarım) ama **bir riski görünür kılıyor**: en sık
yapılan işin skill'i varsayılan olarak elde değil.
