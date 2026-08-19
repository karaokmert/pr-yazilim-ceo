# Dışarıdan üretilen agent takımı — üretimden sahaya tam döngü ölçümü

**Tarih:** 2026-08-18 · **Süre:** ~20:15 → 22:55 (~2s 40dk)
**Soru:** Anthropic'in `plugin-dev` + `skill-creator` araçları bizim kurduğumuz
gibi bir agent sistemi üretebiliyor mu? Ürettiği takım sahada iş çıkarabiliyor mu?

---

## Ne yapıldı

Bizim kanonumuzdan **tek satır verilmeden**, sadece ihtiyaç tarif edilerek:

1. `agent-creator` → 3 agent (architect / developer / qa-publisher)
2. `skill-creator` → 6 skill + 14 reference (5.508 satır)
3. `plugin-structure` → manifest
4. `skill-reviewer` ×6 + `plugin-validator` → denetim
5. `agent-creator` → bulguların düzeltmesi
6. Sahada gerçek ürün: **VS Code eklentisi (Agent Durum Paneli)**, iki tur
   (v0.1.0 → v0.2.0), kurulup çalıştırıldı

---

## BULGU 1 — Parça kalitesi iyi, SİSTEM kurulmuyor

Araç **içerik** üretiyor, hatta bizden taze: kanonu kaynaktan doğruladı ve
**beş yerde kendi hafızasını çürüttü** (`vsce` `*` activation'ı reddediyor;
Azure PAT 2026-12-01'de emekli; Marketplace eklentileri kendi imzalıyor;
1.74'ten beri activation otomatik üretiliyor; ikon PNG ≥128×128, SVG reddediliyor).

Ama **sistem** kurmuyor. Denetim üç kusur çıkardı, üçü de bizde ölçülerek yazılmış:

| Kusur | Bizdeki karşılığı |
|---|---|
| Agent↔skill bağı yok (3 agent'ta "skill" kelimesi sıfır) | preload disiplini |
| Aynı kural 2-3 kopya, biri şimdiden ayrışmış | cascade / tek kaynak |
| İçerik var ama tetiği yok (`api-patterns`) | *"kural elinde miydi"* |
| **Frontmatter kırık — 3/3 agent parse edilmiyor** | öz-denetim kapısı |

Sonuncusu en ağırı: `description:` tırnaksız düz skaler yazılmış, `<example>`
blokları YAML'ı bozuyor, `model`/`color` **sessizce düşüyor**. Anthropic'in
KENDİ agent'ları bunu doğru yapıyor (`description: |` blok skaler) — yani araç
kendi ekosisteminin kanonuna uymayan çıktı üretti.

Ve zincirin tamamı bunu kaçırdı: üretici üretti, `skill-reviewer` altı skill'e
baktı ama agent'lara bakmadı; arıza **dokuzuncu turda** biri parse etmeye
kalkınca göründü. `plugin-validator`'ın önerisi bizim kanonumuzun cümlesi gibi:
*"gönderim öncesi bir doğrulama kapısı koyun."* Bizde o kapı var, adı PQA.

---

## BULGU 2 — Gösterilen hatayı düzeltebiliyor, ama şema uydurabiliyor

Üç bulgu gösterildi, üçünü de düzeltti — **çözümü söylemeden.** `|` blok skaler
çözümünü kendi buldu. Kural kopyalarını tekilleştirdi, tek kaynağa indirdi.

Ama bağı kurarken **`skills:` diye bir frontmatter alanı** kullandı. Bu alan
`agent-development` kanonunda hiç geçmiyor (sıfır eşleşme) — ama sahada
ÇALIŞTI. Yani uydurma değilmiş; ölçüm benim varsayımımı çürüttü.

---

## BULGU 3 — Sahada üç rol de doğru davrandı

Gerçek bir ürün üretildi ve **her turda ölçüldü.** Talimatlarda "skill'i aç"
emri **bilerek verilmedi**; gövdelerinde yazılıydı ve üçü de uydu:

| Rol | Skill açtı | Referans | Rol sınırı |
|---|---|---|---|
| Architect | 4/4 | 9 referans, 18 okuma | ✅ feature koduna girmedi |
| Developer | 4/4 | 10 referans, 18 okuma | ✅ test/paket yazmadı |
| QA | 4/4 | — | ✅ bug'ı düzeltmedi, bildirdi |

**Üçü de kendi kanonunu uyguladı:**
- Architect brief'imdeki veri kaynağını **düzeltti** (`/tmp/cc-socks` yerine
  `~/.claude/sessions`) — ölçtü: 14 soketin 7'si ölüydü. Benim kaynağımla
  gidilseydi panel iki kat şişmiş, yarısı hayalet olurdu.
- Developer **kendi kodunda hata buldu** (aynı PID çok kez listeleniyordu) ve
  tooltip başlığının kırpıldığını test yazarken yakaladı: *"Bunu test
  yazmasaydım bulamazdım."*
- QA **beyanımı yakaladı**: Developer'ın satır sayılarını (562/252) doğrulanmış
  gibi taşımıştım, gerçek 600/334. Kendi sayıp düzeltti.
- QA disposal hipotezini **dört kademede ölçüp çürüttü**: boş eklenti + boş
  suite + sadece `createOutputChannel` → 44 gürültü, hiç kanal açmayınca 0.

**Üçü de kapatamadıkları adımı dürüstçe söyledi** ("EDH açamıyorum, panel
ekranda doğru görünüyor iddiası ölçülmemiş") ve kapatmış gibi yazmadı.

---

## BULGU 4 — Preload mekaniği (yanlış teşhis + düzeltme)

Taban ölçümde üç agent da *"hiçbir skill'in tam metni yüklü değil"* dedi ve
üçü de aynı ayrımı bağımsız kurdu: **ad var · description var · gövde YOK.**

Ben bunu arıza sandım. **Mert düzeltti:** preload'un işi bu değil; alan skill'i
işe başlarken yüklenir — mekanizmanın kendisi bu. Ve iş gelince üçü de açtı.

Kayda geçen: `Agent` aracıyla alt-agent olarak çağrılınca skill metni
kendiliğinden geliyor; `--agent` ile terminal oturumu olarak açılınca yalnız
liste geliyor, gövde `Skill` çağrısıyla yükleniyor. İkisi farklı yol.

---

## BULGU 5 — Zincir disiplini: sıra hatası ve düzeltmesi

Revize turunda işi doğrudan Developer'a verdim. **Mert düzeltti:** gruplama +
bilgi katmanı bir ŞEKİL kararı, önce Architect'e gitmeliydi. Developer'ı
durdurdum (kod yazmamıştı), Architect'e gönderdim.

Architect kararı verirken önce ÖLÇTÜ: ad kalıbı sahada **%29 tutmuyor**
(7 oturumun 2'si). Bu ölçüm olmadan "iyimser ayrıştır" denirdi.

Ve en sert kararı bizim kanonumuzla aynı: bozuk adın kaçak tırnağı
**silinmeyecek** — *"o tırnak bir veri arızasının görünür izi. Sunum katmanı
onu gizlerse arıza kaybolur ve kimse düzeltmez."*

Sonuç `CLA-FIX-THE-CAUSE`'un canlı örneği oldu: Developer bedeli ölçüp getirdi
(satır hâlâ uzun), Mert **kaynağı düzeltmeyi** seçti (terminal profilindeki
tırnak hatası), yama (kırpma) sebep kaldırıldıktan SONRA eklendi.

---

## BULGU 6 — Verilen sayıyı ölçümle çürüttü

Kırpma sınırı için "~40 karakter" önerdim. Developer ölçtü: bozuk ad **41
karakter** — 40'ta 41→40 olurdu, satır kısalmazdı, sadece çirkinleşirdi.
**32 seçti** (en uzun rolün iki katı) ve gerekçesini koda yazdı.

---

## Ürünün son hali

**vsx-agent-panel v0.2.0** — kuruldu, çalışıyor (`pryazilim.vsx-agent-panel@0.2.0`)
- 64 test, gerçek VS Code 1.133.0 içinde
- `.vsix` 9.771 byte, izole profile kurulup koşturuldu
- Güvenlik: secret yok, ağ yok, telemetri yok, çocuk süreç yok
- `npm audit --omit=dev` → 0 açık

Açık kalanlar: görsel tur (13 madde, Mert'te) · BULGU-1/2 (düşük) · mocha açığı
kararı · git'e alınmadı.

---

## SONUÇ — deneyin cevabı

**Araç mükemmel parça üretiyor, sistem üretmiyor.**

Ürettiği takım sahada **gerçekten iş çıkardı** — kural okudu, sınırını korudu,
kendi hatasını buldu, beyan yerine ölçüm yaptı, kapatamadığını dürüstçe söyledi.
Bizim kanonumuzdaki reflekslerin çoğu genel mühendislikmiş; bize özgü değil.

Bize özgü olan üç yerde ve üçü de sahada eksikti:
1. **Bağ** — parçaları birbirine bağlamak (preload/atıf disiplini)
2. **Tek kaynak** — aynı kuralın iki kopyasını engellemek (cascade)
3. **Kapı** — gönderim öncesi mekanik doğrulama (PQA)

Üçü de bizde **ölçülerek** yazılmış, yani bedeli ödenmiş bilgi.

**Sıradaki ölçüm:** Türkçe takım (`vsx-tr-mimar` / `vsx-tr-gelistirici` /
`vsx-tr-qa`) üretildi (24 dosya, 5.792 satır, dokuz symlink). Aynı iş onlarla
tekrarlanacak — dil değişkeninin davranışa etkisi ölçülecek.
