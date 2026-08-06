---
name: clickup-duzeni
description: Clara'nın ClickUp çalışma düzeni — doküman hiyerarşisi, task açma kuralı, isimlendirme, statü seti ve ölçülmüş araç sınırları. Bu skill'i ClickUp'a bir şey yazılacağı, bir task açılacağı ya da güncelleneceği, bir doküman sayfası kurulacağı, bir işin statüsü değişeceği ve "bunu ClickUp'a alalım / task açalım / dokümana yazalım / nerede duruyor" gibi her durumda kullan. Ayrıca ClickUp'ta bir şey ararken de kullan — arama güvenilmez ve bunun ölçülmüş sınırları burada yazılı. Kapsam dışı — proje task'ları (`ozel-yazilim:clickup` skill'i, PA'nın alanı); burası yalnız Clara space'i.
---

# Clara'nın ClickUp düzeni

Bu skill iki şeyi taşıyor: **yapının nasıl kurulduğu** ve **aracın nerede kırıldığı.**
İkincisi daha önemli — çünkü ClickUp sessizce başarısız oluyor ve bunu bilmezsen
yazdığını sanıp devam edersin.

## Nerede çalışıyorsun

```
Clara (space) — 90156858431
├── CLARA DOC (doküman) — qa5p6-121435
│   └── Sprint Planları — qa5p6-234955
│       └── Sprint {başlangıç} → {bitiş}
│           └── her iş bir alt sayfa
└── Görevler (liste) — 901521094094
```

**Kardeş ana sayfalar açılabilir** — `Bugfix`, `ARGE` gibi. `Sprint Planları` bunlardan
biri; hepsi `CLARA DOC` altında kök sayfa olarak durur.

Bu yapı bilerek böyle: her şey tek sayfaya tıkıştırılırsa ileride yeni bir başlık
açacak yer kalmaz.

## Ölçülmüş araç sınırları — bunları bilmezsen sessizce kaybedersin

**Yazma güvenilmez.** 2026-08-05'te ölçüldü: dokuz sayfa açıldı, **ikisi ilk denemede
başarısız oldu** (`ClickUp server error`). Biri ikinci, biri üçüncü denemede geçti. Bir
güncelleme iki denemede de hata verdi.

Yani rastgele yazma hatası var. **Her yazmadan sonra doğrula; hata alırsan tekrar dene.**
Toplu iş yaptıysan sonunda `clickup_list_document_pages` ya da `clickup_filter_tasks`
ile say. Sessiz kaybın yolu şu: sayfa açtığını sanıp devam etmek — kimse fark etmez.

**Sayfa silinemiyor.** MCP'de doküman sayfası için `create`/`update`/`list`/`get` var,
**`delete` yok.** Yanlış açılan sayfanın geri dönüşü yok — içi boşaltılıp `[SİL]` diye
işaretlenir, Mert elle siler. Bu yüzden sayfa açmadan önce yapının doğru olduğundan emin
ol; artık bırakmak temizlik borcu üretiyor.

**Yeni doküman açılamıyor.** `clickup_create_document` classifier tarafından engelleniyor.
Sayfa açmak serbest, **doküman açmak değil.** Yeni bir ana doküman gerekiyorsa Mert
arayüzden açar, ID'sini verir.

**`update_document_page` içeriği tamamen eziyor.** Şemanın kendi ifadesi: *"content fully
REPLACES."* Yani güncellemeden önce **oku** — yoksa mevcut içeriği kaybedersin. Ve
versiyon geçmişi yok; eski hâl kurtarılamaz.

**Arama güvenilmez.** Ölçüldü: gövdeye gömülü tam bir kelime (`zurnabalik`) **bulunamadı**,
buna karşılık alakasız üç sonuç geldi. Motor sorguyu parçalayıp gevşek eşleştiriyor.

Karşılaştırma: `grep` tam eşleşir ya da hiç bulmaz. ClickUp araması **bulamadığını da
getirir, bulması gerekeni de kaçırır.** Bu yüzden bir şey arıyorsan ClickUp'ı tek kaynak
sayma — repo'da `grep` kesin.

## Neyin nerede durduğu

**ClickUp** — sprint yapısı, iş dokümanları, task'lar, statüler. Sebebi: Mert her yerden
görebiliyor, statü akışı var, task dokümana bağlanıyor. Repo bunu yapamıyor.

**Repo** — bulgu, ölçüm, karar, gerekçe (`gunluk/`, `kararlar/`, `incelemeler/`). Sebebi:
`grep` kesin, `git log` "bu satır neden değişti" sorusunu cevaplıyor.

**Kanon dosyaları repoda kalır** — `clara.md`, agent body'leri, skill'ler. Bu bir tercih
değil zorunluluk: Claude Code onları diskten okuyor.

Ayıran soru: **bu bilgi bir durum mu, bir gerekçe mi?** Durum ClickUp'a, gerekçe repoya.

## Task açma kuralı

**İş detaylandırılır → karar netleşir → doküman yazılır → SONRA task açılır.**

Detayı netleşmemiş işe task açılmaz. Sebebi: listeye bakan biri onu **tanımlı iş** sanır.
2026-08-05'te bir kez ihlal edildi — detayı konuşulmamış bir işe `to do`/high task açıldı,
sonra silindi.

## İsimlendirme

`Clara - <kısa anlaşılır başlık>`

Ön ek **sabit `Clara`** — liste onun listesi. İşin içinde kim varsa başlıkta geçer:
`Clara - PAM ile v8 Agentlarının Geliştirilmesi`. Numara yok, "kalem" yok.

## Statü seti — kurulu, değiştirme

`Görevler` listesinde sekiz statü var:

`to do` · `planning` · `in progress` · `at risk` · `update required` · `on hold` ·
`complete` · `cancelled`

**`on hold` ve `at risk` özellikle değerli** — 2026-08-05'te ölçüldü: bir iş 42 saat,
biri ~48 saat bekledi ve ikisi de hiçbir yerde "askıda" görünmedi. Bu statüler o boşluğu
kapatıyor, kullanılmazsa bekleme yine görünmez.

## Task içeriği nasıl yazılır

Task **mini özet** taşır, detay dokümanda durur. Şablon:

```markdown
**Sprint:** {tarih aralığı} · **Sıra:** {n} · {bağımlılık notu}

## Detay dokümanı — başlamadan önce oku
{doküman URL'i}

## Özet
{bir-iki paragraf: ne ve neden}

## Bittiğini nasıl anlarız
{ölçülebilir kapanış ölçütü}

## Risk / Uyarı
{varsa}
```

Doküman linkini **task açıklamasına gömmek** akışın belkemiği: task'a geçen kişi detayı
oradan okur. Link yoksa task tek başına yetersiz kalır.

## Bağımlılık

`clickup_add_task_dependency` ile `waiting_on` kurulur — zorunlu sıra listede görünür.
İşler birbirini kilitliyorsa bunu kurmak şart; yoksa sıra yalnız dokümanda kalır ve
listeye bakan yanlış işe başlar.

## Araç haritası

Şemaları `ToolSearch` ile yüklenir (`select:` ile isimden).

**Doküman:** `clickup_list_document_pages` (yapıyı gör) · `clickup_get_document_pages`
(içeriği oku — güncellemeden önce şart) · `clickup_create_document_page` (`parent_page_id`
ile alt sayfa) · `clickup_update_document_page` (içeriği ezer)

**Task:** `clickup_create_task` · `clickup_update_task` · `clickup_get_task` ·
`clickup_filter_tasks` (listeyi doğrula) · `clickup_delete_task` (silinebiliyor —
sayfaların aksine) · `clickup_add_task_dependency` · `clickup_create_comment`

**Liste/space:** `clickup_get_list` (statüleri verir) ·
`clickup_get_workspace_hierarchy` · `clickup_search`

**Not:** İki ClickUp MCP'si var — `mcp__claude_ai_ClickUp__*` ve
`mcp__plugin_websitesi_clickup__*`. Aynı araçları sunuyorlar. Clara space'i için
birincisi kullanılıyor.

## Kaynak

Ölçümlerin tamamı: `gunluk/2026-08-05.md` — "21:29" (arama), "22:09" (yapı + yazma
güvenilmezliği) başlıkları. Yapı kararı:
`kararlar/2026-08-05-sprint-planlama-kararlari.md`.
