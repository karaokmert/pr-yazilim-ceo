---
name: agent-sinama
description: Bir agent'ın davranışını ölçme yöntemi — kanonu okuyup okudu mu, kuralı uyguluyor mu, bir arıza kural ihlali mi mekanik mi. Bu skill'i "şu agent'ı sına / kanonu okuyor mu / bu davranış doğru mu / agent kuralı çiğnedi mi / şu takımın çıktısını incele" denen durumlarda kullan. Ayrıca bir agent beklenmedik davrandığında, o davranışın sebebini ÖLÇMEK için bir test kurulacaksa da kullan — mekanik arızaları kural ihlalinden ayıran testler burada. Kapsam dışı — agent üretimi ve kural yazımı (`agent-project`, PAD'in işi); ve sahada geçmiş bir anı kaydetmek (`saha-monitorluk`) — sınama bir test KURAR, monitörlük olanı KAYDEDER.
---

# Agent sınama

Bir agent'ın davranışını yorumlamadan önce **iki mekanik arıza** kontrol edilir. Yoksa
mekanik bir sorun kural ihlali sanılır ve yanlış yere müdahale edilir.

Ölçümler: `references/mekanik-arizalar.md`

## İlk soru: kural elinde miydi

**Bir agent kuralına uymuyorsa ilk soru *"kuralı çiğnedi mi"* değil, *"kural elinde
miydi"* olmalı.**

Sebebi: `skills:` frontmatter alanı skill gövdesini agent'ın context'ine **enjekte
etmiyor.** Agent elinde yalnız description bulur ve kanonun orada olduğunu sanır. Yani
kural dosyada var, agent'ta yok — ve ihlal **sessiz.**

Bir açılış hook'u bunu telafi edebilir (agent'a skill'lerini kendisinin yüklemesini
söyler) ama hook her ortamda çalışmıyor. **Sınama yaparken agent'ın kanonu gerçekten
okuyup okumadığı ölçülür, varsayılmaz.**

Ölçme yolu: agent'ın oturum kaydında `Skill` çağrısı var mı, ve skill gövdesi context'e
girdi mi. *"Yüklendim"* demesi kanıt değil.

## İkinci soru: kendisi hakkında bir bilgiye mi dayanıyor

**Agent kendi frontmatter'ını göremez.** Body'sinin metnini görür ama `skills:`,
`tools:`, `model:` alanları ona ulaşmaz.

İki sonucu var:

**Bir agent'a *"tanımında ne yazıyor"* diye sorulmaz** — cevabı tahmin olur.

**Ve bir talimat, agent'ın kendisi hakkındaki bir bilgiye dayanamaz.** O bilgi dışarıdan
verilir. Aksi hâlde agent tahmin eder, yanlış yükler, **ve yüklediğini sanır.**

## Sınamanın sınırı — davranış mı hüküm mü

*"Şu durumda ne yaparsın"* bir **davranış** sorusudur — ölçüdür, kullanılır.
*"Bu kanona uygun mu"* bir **hüküm** sorusudur — ve hüküm denetçinin işi.

Ayıran test: **bu çağrı bir kapıyı kapatıyor mu?** Denetim, onay, kapanış kararı →
kapatır, yasak. Yalnız bir davranış gösteriyorsa → serbest.

## Sınarken niyet taşınmaz

Yardımcıya *"bu kural şunu demek istiyor"* dersen ölçtüğün şey kural olmaktan çıkar,
**senin açıklaman** olur. Yalnız dosya verilir, durum sorulur.

## Başkasının raporundaki mekanik iddia ölçüm değildir

Bir agent *"şu araçla kurdum"*, *"şu mekanizma çalışıyor"* dediğinde bu bir **beyan**.
Aktarmadan önce kendin ölç.

Sebebi: zincir uzadıkça iddia güçleniyor ama dayanağı zayıflıyor. Bir agent'ın raporuna
güvenip kendi doğru gözlemini geri almak ölçülmüş bir hata.

## Aynı dosyanın kaç kopyası var — hangi kaynağa baktığını doğrula

Bu ekosistemde aynı dosyanın onlarca kopyası var: plugin cache'inde sürümler, emekli
kuşaklar, proje repolarında kalıntılar. `grep` yolu değil **içeriği** getirir.

**Okuduğun şeyin yürürlükte olduğunu sen doğrularsın.** Hangi yolun yürürlükte olduğu
`projeler/agent-dagitim-yapisi.md`'de yazılı.

İki kural: **bir arama birden fazla sonuç döndürüyorsa hangisini kullandığını söyle.**
Ve **bir alanı aramak karşıtını aramamak demek değil** — bir kısıt arıyorsan hem izin
listesini hem yasak listesini ara.
