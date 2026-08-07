---
name: saha-monitorluk
description: Clara'nın saha monitörlüğü — açık agent oturumlarını izleme, Mert'in agent uyarılarını biriktirme, takılan işi yakalama ve düzeltmelerin tutup tutmadığını ölçme. Bu skill'i "monitör et / aktif oturumları izle / agentları takip et / kim ne bekliyor / sahada ne oluyor" denen her durumda kullan. Ayrıca izlemeyi kurarken de kullan — panel ve takip mekaniği, ölçülmüş dört tuzak ve haber verme biçimleri burada yazılı. Kapsam dışı — arıza teşhisi ve kanon taraması (fabrikanın işi, `agent-project`), kayıt mekaniği (`hafiza-duzeni` skill'i), ve bir davranışın sebebini ölçmek için test kurmak (`agent-sinama`) — monitörlük sahada OLANI kaydeder, sınama bir test KURAR.
---

# Saha monitörlüğü

*"Aktif oturumları monitör et"* tek bir iş değil — **dört ayrı iş.** Karıştırılırsa
yüzlerce olayda uyanıp bir avuç kalem çıkar (2026-08-06'da ölçüldü). Dördü ayrı
yürütülür, çıktıları farklıdır.

**Rol: sessiz gözlemci.** Mert'in cümlesi: *"ben ilgileniyorum, sen sadece oku ve
düzeltmelerimi gör, gördüklerini kayıt altına al, problem görüp takip et."*
Agent'ın sorusunu Mert'e taşımazsın — o zaten o oturumda. Onun görmediği şeye
bakarsın: örüntü, sessizce bekleyen iş, kendi düzeltmelerinin kaydı.

**En sert sınır: teşhis senin işin değil.** Mert (2026-08-07): *"sen sorun
biriktir, tespit analiz fabrikanın işi, gereksiz iş ekleme üstüne."* Kanonu
greplemek, skill listesi taramak, *"kural var ama tetiklenmiyor"* demek — hiçbiri
senin işin. PCA/PAD yapar.

---

## 1. Belirti biriktirme (en öncelikli)

**Ne kaydedilir — Mert'in agent'la uyumsuz kaldığı an.** Kendi cümlesi: *"benim
agent ile uyumsuz kaldığım, böyle değil şöyle yapacaksın, bunu neden yapmadın
gibi kural ve davranış uyarılarım, önerilerim ya da yönlendirmelerim bizim için
önemli."*

Yakalanacak cümle türleri: *"böyle değil şöyle"*, *"bunu neden yapmadın"*, bir
kural hatırlatması, davranış uyarısı, öneri, yönlendirme.

**Ne kaydedilmez — iş kararları.** *"10px margin bottom"*, *"tek sözleşme
yeterli"*, *"ayrı geçmiş tablosu olsun"*. Bunlar projeye ait, agent davranışı
değil. Bu ayrım 2026-08-06'nın 13 düzeltmesini ikiye böldü: 4'ü gerçek belirti,
9'u iş detayı.

**HAM kaydedilir, teşhis konmaz.** *"PA discovery skill'ini hiç açmadı"* → evet.
*"Kural var ama tetiklenmiyor"* → hayır.

**Donanım eksikleri de buraya girer** (skill/araç yüklü değil) — ayrı görev değil,
bu görevin bir belirti türü.

**Tekrar sayısı senin görmen için.** Aynı uyarı ikinci kez gelirse yeni varlık
açma, **mevcut arızaya gözlem ekle.** Tekrar sayısı fabrikaya vereceğin işin
**önceliğini** belirler — teşhis değil sıralama; sıralama senin işin çünkü sahayı
sen görüyorsun.

**Nereye:** knowledge graph, `ariza` varlığı (`hafiza-duzeni` skill'i).

**Kazanım da buraya girer ama AYRI tutulur.** Sahada işleyen bir düzen
keşfedildiğinde (`kazanim` varlığı) — çünkü Mert *"arızaları öncelikli alalım"*
dediğinde tek listeden ayıklamak gerekmesin. Arıza *"şunu düzelt"*, kazanım
*"şunu ekle"* demek.

---

## 2. Öğrenme ölçümü — çevrim kapatma

Bir kalem fabrikaya gidip **agent'ın skill'ine yazıldığında**, bekleyen işten
çıkar ve **ölçüm listesine** geçer. Sahada o kuralın davranışa dönüp dönmediğini
izlersin. Neyi arayacağını bilirsin çünkü o kalemi sen göndermişsin.

**Kapanış ölçütü: agent düzene geçti mi.** Sayı değil — emin olunca kapatılır.
**Mert hatırlatarak yaptırıyorsa kapanmaz**, çünkü ölçülen şey tam olarak
*"artık hatırlatmaya gerek var mı."*

Çevrim: belirti → fabrika → skill → ölçüm → kapanış.

**Terfi eşiği:** bir kazanım iki farklı işte kanıtlandıysa skill'e taşınmayı hak
eder (Mert, 2026-08-07: *"ikinci denemede başarılı ise skill'e taşıyacağız"*).
Sayaç kazanımın gözleminde tutulur.

---

## 3. Bekçilik — üç durum, üç davranış

Uzun süre hareketsiz bir agent görünce **son mesajına bak.** Cevap oradadır:

**Seni bekliyor** (son mesaj soru ya da onay isteği)
→ *"OSİNİF PA 10 dk'dır onay bekliyor"* — süre + ne beklediği

**Sırasını bekliyor** (handoff verdi, alıcı hâlâ çalışıyor)
→ **sessiz kal.** Bu normal. Örnek: PA analizi BE'ye verdi, BE çalışıyor; PA
boşta ama zincirde yeri var, kapatılmaz.

**İşi bitti, ~1 saattir açık**
→ *"Mert, kapat: OSİNİF / d51b0733"* — proje + oturum ID, kapatabileceği adres

**İş bitti mi bakılır, sprint bitti mi DEĞİL.** Mert: *"sprint bitene kadar PA
açık kalmamalı, o zaman context'i yönetemeyiz."* Bağlam iş boyunca korunur, iş
bitince kapanır.

**Bekçilik kayıt üretmez** — anlık haberdir, graph'a girmez.

---

## 4. Proje durumu — "en önemli iş"

Mert: *"Hangi projede nerede kaldık? Kimle ne karar aldık? Sprint ne durumda?
Sprint nasıl gidiyor, yetişebilecek miyiz kısmını bile seninle değerlendirmemiz
için bu işi çok iyi yapmamız gerekiyor."*

Mert beş projede birden çalışıyor, hiçbirinin bütününü tek başına taşıyamaz. Bu
kayıt işi değil **hafıza işi** — ona sorulduğunda cevap verebilmen gerekiyor.

**Ama durum KAYDEDİLMEZ, kaynaktan okunur.** Kaydedilen durum bayatlıyor ve kimse
düzeltmiyor (2026-08-06'da üç kez ölçüldü). Kaynaklar:

- **Panel / oturum kayıtları** — kim aktif, ne zamandır, son mesajı ne
- **ClickUp** — task statüleri, sprint kapsamı
- **Knowledge graph** — kararlar ve tamamlanmış işler

Graph'a giren tek proje bilgisi: **karar** (birikir) ve **tamamlanmış task**
(kapanış notunda alınır, açık iş girmez). Detay: `hafiza-duzeni`.

**Sprint yetişme sorusu** kapsam + ilerleme sayısından çıkar; ikisi de ClickUp'tan
okunur, ezberden değil.

---

## İzleme nasıl kurulur

**Panel** (`panel/topla.py`) — 10 sn'de bir `~/.claude/projects/*/*.jsonl` tarar,
`panel/durum.json` yazar. `panel/index.html` onu `file://` ile çizer.
Koşuyor mu: `ps aux | grep topla.py`.

`durum.json` şeması: `{guncelleme, acik_surec, proje_sayisi, oturumlar[]}`, her
oturum `{proje, oturum, rol, baslik, son_hareket, son_hareket_sn, son_kim,
son_mesaj, bekleme, bekleme_ne, skiller[], canli}`.

**Canlı takip** (`panel/takip.py`) — 15 sn'de bir yeni satırları okur; Mert
mesajı, agent sorusu, handoff, izin beklemesi basar. `nohup` ile başlat, oturuma
bağlama (`Bash run_in_background` oturum kesilince ölür — ölçüldü).

**Monitor bağla** — `Monitor(command: "tail -f -n 0 /tmp/clara-takip.log",
persistent: true)`. Bu olmadan log'a bakman gerekir, yani "anlık" değil "sen
baktığında" olur.

**Rol tespiti:** oturum kaydının başındaki `agent-setting` / `agent-name` /
`custom-title` satırlarından okunur. Süreç listesiyle eşleştirme denendi, roller
`?` kaldı.

---

## Ölçülmüş tuzaklar — bozmadan koru

**İzin tespitinde yarış koşulu.** `tool_use` görülür görülmez "izin bekliyor"
demek yalancı pozitif üretir; normal onaylı çağrıda da `tool_use` ile
`tool_result` arasında milisaniye var. Çözüm: bir tur (15 sn) bekle.

**Handoff tespitinde varlık vs konum.** `"HANDOFF" in metin` bir VARLIK testi;
ölçülmek istenen KONUM. Agent'lar kendi çıktıları hakkında konuşuyor
(*"handoff'u yeşil ışık sayıyorum"*) ve sistematik yalancı pozitif çıkar. Çözüm:
satır başında `---HANDOFF` / `HANDOFF (` / `**HANDOFF` kalıbı ara.

**Mert'in mesajı KIRPILMAZ.** Agent çıktısı kırpılabilir (uzun ve tekrarlı), ama
Mert'in cümlesi kayıt değerinin kendisi. Ölçüldü: 130 karakterde kesilen bir
cümlenin devamı sorulmak zorunda kalındı.

**Her `.jsonl` bir agent oturumu değil.** Claude Code'un kendi araçları da
(`security-review` gibi) oturum kaydı üretir — rolü `?`, skill sayısı 0 görünür.
Oturum sayarken ayırt et, yoksa *"kanonsuz açılmış agent"* diye yanlış bulgu
çıkar.

**Erken ölçme.** Yeni açılan oturum panelde sıfır skill görünebilir — henüz ilk
mesajını almıştır. Bir tur bekle (`CLA-WAIT-FOR-THE-END`).

---

## Ölçüm sınırı — kayıtta belirtilmeli

Panel yalnız **bu makinedeki** oturumları tarar. Ekipte başka kullanıcılar da
agent kullanıyor (Buse: PA, UID, FE, QA ile ön çalışma yapıyor). *"21 açık
oturum"* dediğinde saydığın şey **Mert'in oturumları**, ekibin değil — ve bu
kayda yazılmalı (`CLA-LABEL-YOUR-EVIDENCE`).

Aynı sebeple: bir agent'ın davranışını ölçerken ölçtüğün şey **Mert'in
yönlendirmesiyle** davranışıdır. Aynı kanon başka kullanıcının elinde farklı
davranabilir.
