# `SendMessage` ölçümü — PAM neden 10 handoff taşıyor

Tarih: 2026-08-04

Mert'in şikâyeti: *"PAM'a diğer agent'ları çağırıp yönetmesi görevini verdim, istediğim
senkronda değil — çünkü bir skill düzenlemesinde 10 kere handoff taşımak istemiyorum."*

Fabrika ölçümünde (`incelemeler/fabrika-olcutu/saha-davranisi.md`) sebep hipotez olarak
görünmüştü: PAM `SendMessage` çağırdı, *"exists but is not enabled in this context"*
döndü, her turda **yeni agent** açmak zorunda kaldı. Bu dosya o hipotezi ölçüyor.

## Yöntem

Bu repoda geçici bir deney agent'ı yazıldı (`test-sendmessage`, ölçüm sonrası silindi) ve
`general-purpose` ile iki turlu bir konuşma kuruldu:

1. Birinci tur: agent'a bir işaret verildi (`ZEYTIN-4471`), taze context'le başladığı
   doğrulandı.
2. İkinci tur: **başka bir agent'a** `SendMessage` ile aynı agent'a mesaj yollatıldı —
   *"az önce verdiğim işaret neydi? Hatırlamıyorsan tahmin etme."*

Ölçüm bilinçli olarak dolaylı yapıldı: Clara doğrudan `SendMessage` çağırsa yalnız
kendi kanalını ölçmüş olurdu; asıl soru **bir agent'ın başka bir agent'la konuşmayı
sürdürebilmesi.**

## Bulgu bir — `SendMessage` çalışıyor

Mesaj gitti, agent işareti doğru döndürdü (`ZEYTIN-4471`), iki tur **aynı context'te**
birleşti.

Ama bir ayrıntı var: `SendMessage` başlangıçta araç listesinde **yok**, deferred tool.
Çağıran agent önce `ToolSearch("select:SendMessage")` ile şemasını yüklemek zorunda
kaldı. Yani araç var ama **kendiliğinden görünmüyor** — bir agent onu arayacağını
bilmiyorsa bulamaz.

**PAM'in aldığı hata bu yüzden olabilir.** *"Exists but is not enabled in this context"*
bir yasak değil, yüklenmemiş bir şema mesajı olabilir. Bu bir çıkarım, ölçülmedi.

## Bulgu iki — ölü agent transcript'ten canlandırılıyor

Gönderim sonucu birebir:

> *"Agent had no active task; **resumed from transcript** in the background with your
> message."*

Yani agent'ın işi bitmiş, görevi kapanmış — buna rağmen mesaj ulaştı ve **bağlamı
korunmuş** hâlde devam etti. Bu yeni bir spawn değil, gerçek bir devam.

Agent'ın kendi ayrımı önemli: *"Bunu hatırlamadım — birinci turun tamamı hâlâ bu
oturumun bağlamında duruyor, oradan okudum. Bu test oturum-içi bağlam sürekliliğini
ölçüyor, kalıcı memory'yi değil."*

Yani mekanizma **transcript devamı**, hafıza değil. Aynı oturum içinde çalışır.

## Bulgu üç — dönüş kanalı yok, yukarı mesaj gitmiyor

En kritik bulgu. Çağrılan agent cevabını `SendMessage` ile geri yollamayı denedi ve
başarısız oldu:

> `No agent named 'general-purpose' is reachable. Check the spelling, or use the agent
> ID from a background agent's spawn result.`

Agent'ın kendi teşhisi: *"Jenerik tip adı yönlendirilebilir bir adres değil. Bir peer'a
ulaşmak için gerçek agent adı ya da spawn sonucundaki `agentId` gerekiyor. Ben onun
tarafından açıldığım için elimde böyle bir ID yok — **aşağı doğru mesaj çalışıyor,
yukarı çalışmıyor.**"*

Cevabı ancak çağıran agent **çıktı dosyasını okuduğu için** öğrenildi.

**Bu, `CLAUDE.md`'deki bulguyu keskinleştiriyor.** Orada yazılı olan: *"bir agent
diğerini çağırdığında rapor kullanıcıya değil çağırana gider."* Ölçüm daha kötüsünü
gösterdi: **rapor çağırana bile gitmeyebilir** — çağıran dosyayı okumazsa kaybolur.

## Bulgu dört — peer mesajı güvensizlik uyarısıyla geliyor

Gelen mesaj `<agent-message from="general-purpose">` sarmalayıcısı içinde, yanında sabit
bir uyarı bloğu ile teslim ediliyor: bir peer yetki yükseltemez, izin onaylayamaz.

Uyarı **koşulsuz** — zararsız bir test mesajında bile tetiklendi. Yani platform
seviyesinde agent-agent zincirine karşı bir koruma var ve bu odanın
`CLA-NO-CALL-TEAMS` gerekçesiyle aynı yönde.

## Bulgu beş — yeni agent oturum içinde tanınıyor (gecikmeli)

Deney agent'ı yazıldıktan hemen sonra çağrıldı: `Agent type 'test-sendmessage' not
found`. **Ama birkaç dakika sonra tanındı ve çalıştı.**

Yani agent listesi oturum içinde güncelleniyor, sadece anında değil. Clara ilk denemede
*"restart gerekiyor"* dedi, **yanlıştı ve geri çekildi.**

Bunun PAM'in `90eeb9a2` oturumundaki `Task` arızasıyla ilişkisi belirsiz: orada PAD
frontmatter'a `Task` ekledi, PAM *"frontmatter değişikliği çalışan oturumda etkili
olmuyor"* dedi ve o oturum boyunca hiç düzelmedi. **Ayrı bir mekanik olabilir —
ölçülmedi.**

## Bulgu altı — agent kendi frontmatter'ını göremiyor (üçüncü kez)

Deney agent'ına *"adın ne"* soruldu. Cevap: *"Bir ad verilmedi — tanımımda isim yok."*
Oysa frontmatter'da `name: test-sendmessage` yazılı.

Body'sindeki kritik kuralı (`TST-NO-INVENT`) doğru aktardı — yani gövdeyi görüyor,
frontmatter'ı görmüyor. `YT-AGENT-CANT-SEE-SELF` üçüncü kez doğrulandı.

## PAM'in derdine cevap

**On handoff'un sebebi tasarım değil, araçtı.** `SendMessage` çalışıyor ve bir agent'la
konuşmayı sürdürebiliyor. PAM o gece bunu kullanamadı ve her düzeltme turunda yeni bir
PAD açtı — her yeni PAD taze context, her turda baştan anlatma.

**Ama tam çözüm değil, çünkü dönüş kanalı yok.** PAM PAD'e mesaj yollayabilir; PAD
PAM'e yollayamaz. Yani revize döngüsünde her dönüş yine PAM'in bir hamlesini gerektirir.
Fark şu: PAM aynı PAD'e döner (bağlam korunur), yeni PAD açmaz.

Beklenen kazanç: beş turluk döngüde PAD'e beş kez baştan anlatmak yerine bir kez
anlatıp dört kez *"şunu düzelt"* demek.

**Ölçülmeyen:** PAM'in aldığı hatanın sebebi gerçekten deferred-tool yüklemesi mi, yoksa
başka bir kısıt mı. Bunu PAM'in kendi oturumunda denemesi gerekiyor.

## Not — turları azaltmak hedef değil

Fabrika ölçümü şunu gösterdi: beş turun dördü PQA'nın **gerçek bulgusuyla** döndü, biri
push öncesi commit eksiğini yakaladı ve o olmasaydı sahaya bayat kural inecekti.

Yani hedef *"10 handoff'u 1'e indirmek"* değil, **aynı turları tek konuşma içinde
döndürmek.** Turları azaltmak denetimi azaltır; konuşmayı sürdürmek azaltmaz.
