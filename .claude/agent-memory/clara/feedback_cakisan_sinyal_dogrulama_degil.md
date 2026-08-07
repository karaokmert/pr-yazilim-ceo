---
name: cakisan-sinyal-dogrulama-degil
description: Çakışan sinyaller doğrulama değildir; bir ölçüt doğru cevabı yanlış nedenle verdiğinde de bozuktur. Ölçüt seçerken sor — bu sinyaller ayrıldığı bir senaryo var mı?
metadata:
  type: feedback
---

# Çakışan sinyal doğrulama değildir

**Kural:** Bir ölçüt seçerken *"kaç sinyal aynı şeyi diyor"* değil, **"bu sinyaller
birbirinden ayrıldığı bir senaryo var mı"** diye sor. Ayrılmıyorlarsa elinde N bağımsız
ölçüm değil, **bir gerçeğin N yansıması** var.

Ve ikinci yarısı: bir ölçüt yalnız yanlış cevap verdiğinde bozuk olmaz — **doğru cevabı
yanlış nedenle** verdiğinde de bozuktur. Bu tür en zor yakalananı, çünkü test her
seferinde geçiyor.

**Why:** 2026-08-07, oturum açılışı. Kanondaki *"önce NEREDEYİM"* adımı ayrımı `pwd` ile
ölçüyordu. Clara `pr-yazilim-ceo`'da **kurulu** bir agent ve her projede çalışabiliyor —
yani `pwd` oturumun konusunu değil **başlatan `cd`'yi** gösteriyor, onun için neredeyse
sabit bir değer. Sabit bir değerle değişken bir soru ölçülmez. Mert kesti: *"pwd sana
orayı verdi, sen orada kurulu bir agentsin, her projede çalışabilirsin."*

Ölçüm yapıldığında beş sinyal (`pwd`, ana oturumun `lsof` cwd'si, başlatma komut satırı,
transcript yolu, yüklenen `CLAUDE.md`) **hepsi aynı yeri** gösterdi. İlk bakışta güçlü
bir doğrulama; değil — beşi de tek bir `cd`'den türüyordu.

O turda `pwd` gerçekten doğru cevabı verdi (oturum `pr-yazilim-ceo`'da açılmıştı). Ölçüt
bu yüzden bozuk: doğruyu yanlış nedenle veriyordu. Arıza sessizdi — her oturumda *"EV"*
diyecekti, yönetim moduna hiç geçmeyecekti ve hiçbir şey arızalı görünmeyecekti.

**How to apply:** Bir ölçüt kanona girerken (ya da bir bulguyu "doğrulanmış" ilan
ederken) iki soruyu sor: *(1)* bu sinyaller hangi senaryoda birbirinden ayrılır — cevap
yoksa tek ölçüm var, *(2)* bu ölçüt yanlış olsa arıza görünür mü — görünmüyorsa sessiz
arıza sınıfındadır ve ek bir kontrol gerekir.

Özellikle **kimlik/konum/ortam** sorularında geçerli: bu tür sinyaller genelde tek bir
başlatma kararından türer, o yüzden hepsi aynı şeyi söyler.

Gerekçe: `kararlar/2026-08-07-mod-ayrimi-pwd-ile-olculmez.md`
İlgili: [[olcum-yerine-yorum]] · [[olcum-kaynaga-git]]
