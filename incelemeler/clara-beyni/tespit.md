# Clara'nın beyni — ilk tespit

Tarih: 2026-08-03

Mert Clara'nın "yaşayan ve gelişen" bir agent olmasını istedi ve önce mevcut durumun
çıkarılmasını istedi. Bu dosya o tespiti tutar — ölçülmüş hâliyle.

## Kaynak ve yöntem

Tüm repo tarandı: 31 dosya, 1474 satır (`.git` hariç, `.remember/tmp` dahil).
Git geçmişi 8 commit, tamamı 2026-08-02 ve 08-03. Ölçüm `find` + `wc -l` +
`git ls-files` ile yapıldı; içerik okundu.

## Beynin üç katı

**Kanon** — `.claude/agents/clara.md`, 386 satır. Kim olduğu, üç sert kural, konuşma
kalıbı. Sınandı ve davranış ürettiği ölçüldü (`incelemeler/clara-ilk-sinama/kayit.md`).
Tamamı Mert'in elinden çıktı; Clara'nın yazdığı tek satır yok — ve yazması yasak
(`kararlar/2026-08-03-clara-memory-disiplini.md`, gerekçe: system prompt'a giren şeyi
sorgulayamaz).

**Kayıt** — `kararlar/` 2 dosya, `incelemeler/` 3 dosya, `fikirler/` 1 dosya.
Toplam ~600 satır. Yazma disiplini işliyor (her oturumda üretildi), ama **haritası
yoktu**: bir konuya dönmek için klasörü listelemek ve dosya adından tahmin etmek
gerekiyordu. 5 dosyada tolere edilebilir, 50 dosyada kaybolur.

**Hafıza** — `.claude/agent-memory/clara/`, 4 kayıt + indeks.

## Bulgu bir — hafıza yalnız düzeltmelerden oluşmuş

Dört kaydın **dördü de** `feedback` tipinde. Bir tane `user`, `project` ya da
`reference` kaydı yok.

Yani hafızanın tamamı *"Clara şunu yanlış yaptı, tekrarlamasın"* biçiminde. Mert'i
tanıyan tek kayıt yok — nasıl çalıştığı, hangi kararı neden verdiği, neye tahammülü
olmadığı hiçbir yerde durmuyor.

Sonucu: Clara hata tekrarlamaz ama Mert'i tanımaz. "Yıllarca çalışacak arkadaş"
hedefinde bu ters yön — düzeltme birikimi savunma üretir, tanıma birikimi öngörü
üretir.

## Bulgu iki — `.remember` git dışı

`.remember/.gitignore` içeriği tek satır: `*`. `git ls-files .remember/` boş döndü.

Yani oturum özetleri (`today-*.md`, `now.md`, `logs/`) yalnız bu bilgisayarda.
Repo'ya giren şey Mert'in commit'leri ve Clara'nın yazdığı dosyalar; çalışma akışının
kendisi girmiyor.

Bu bir arıza değil, remember plugin'inin varsayılanı — ama bilinmesi gerekiyor:
**oturum kaydına dayanan bir hatırlama repo'da taşınmaz.** Kalıcı olması gereken şey
`kararlar/`, `incelemeler/`, `fikirler/` ya da `agent-memory/` altına yazılmalı.

## Bulgu üç — büyüme mekanizması hiç yoktu

Kanon *"sonucu yazarsın"* diyor, *"kendini yazarsın"* demiyor. `CLA-WRITE-BEFORE-CLOSE`
işin sonucunu emrediyor; Clara'nın kendi öğrenmesini kimse emretmiyor.

Ölçülebilir sonucu: 8 commit boyunca hafızaya 4 kayıt girdi ve **hepsi Mert'in
düzeltmesinden sonra** girdi. Clara kendiliğinden bir kayıt açmadı.

Yani engel bir yasak değil, bir **eksik**. Yetki vardı, tetikleyici yoktu.

## RAG / Obsidian MCP — bugün gerekmiyor

Mert ikisini de teklif etti. Reddedildi, gerekçe ölçüye dayalı:

İkisi de bir **arama** problemi çözüyor. Bugünkü hacim 31 dosya / 1474 satır — grep
tüm repoyu bir saniyede tarıyor, kaybolan bir kayıt yok. Çözülmesi gereken problem
arama değil **yazma disiplini**: ne zaman, nereye, hangi biçimde.

Bugün araç eklenirse boş bir kütüphaneye tasnif sistemi kurulur; sonuç hem kayıt
disiplini olmayan hem de bakımı olan bir katman.

**Eşik konuldu** (`kararlar/2026-08-03-clara-buyume-duzeni.md`): kayıtlar grep'le
bulunamaz hâle geldiğinde — kabaca 100+ kayıt dosyası, ya da bir konuyu bulmak iki
denemeden fazla sürdüğünde — araç yeniden konuşulur.

## Ne yapıldı

`HARITA.md` açıldı (kayıt haritası, oturum başında bakılan yer) ve büyüme düzeni
karara bağlandı — bkz. `kararlar/2026-08-03-clara-buyume-duzeni.md`.
