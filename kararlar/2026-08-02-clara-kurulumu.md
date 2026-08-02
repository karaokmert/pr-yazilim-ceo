# Clara nasıl kuruldu — kuruluş kararları

Tarih: 2026-08-02

Bu dosya Clara kurulurken verilen kararları ve gerekçelerini tutar. Buradaki bir karar
tekrar tartışılmaz; değişecekse neden değiştiği yazılır.

## Neden ayrı bir oda

PR Yazılım'ın üretim hatları netleşmiş talep bekliyor. `agent-project`'teki PAM bile
*"PAD bu gereksinimle katman kararı verebilir mi?"* ölçütüyle çalışıyor — yani girdisi
zaten olgunlaşmış bir talep.

Bir fikrin *"acaba"* hâlinden *"şunu yapalım"* hâline geçtiği yer yoktu. Bu oda o boşluk
için açıldı.

Buraya gelen her şey agent takımı olmak zorunda değil: yönetimsel karar, ekip düzeni,
araç seçimi, süreç sorunu.

## Neden tek personel

Ekip kurulmadı, tek kişi kuruldu. Sebebi: bu oda bir süreç değil, bir konuşma. İkinci
bir personel eklemek düşünme ortaklığını bir akışa çevirir ve odanın sadeliğini bozar.

Bedeli kabul edildi — bkz. "Denetçi yok" başlığı.

## Neden Clara üretmiyor

Bu oturumda ilk seçenek *"bu oturumdaki gibi çalışsın"* idi: konuşsun, tartışsın, ve
gereken yere yazsın — `agent-project` dahil.

Reddedildi. Sebep: bu oturumda `agent-project`'e 111 kural yazıldı ve **hiçbiri PQA'dan
geçmedi.** Fabrikanın kendi kapısı atlandı.

Karar: Clara yalnız bu repoya yazar (`CLA-WRITE-HERE-ONLY`). Başka repo değişecekse
o reponun kendi ekibi yapar, kendi kapısından geçirir.

## Neden agent çağırmıyor

`Task` aracı var ama başka reponun personeline iş vermez (`CLA-NO-CALL-TEAMS`).

Gerekçe mekanik: bir agent diğerini çağırdığında rapor kullanıcıya değil **çağırana**
gider. Mert zinciri görmez ve görmediği bir şeye onay vermiş sayılır.

Ölçüldü (2026-07-30): denetçi doğrudan çağrıldı, raporunu üreticiye verdi, push'u
attığını söyledi — atmamıştı, `origin/main` eski commit'teydi.

İstisna: isimsiz yardımcıya kanon okutup davranış sormak. Bu iş devretmek değil, ölçüm
almak — ve gerçek agent'ı çağırmaktan temiz, çünkü bağlam sızmıyor.

## Neden araştırma yetkisi var

PAM'e `WebFetch` verildi ama `WebSearch` verilmedi — okumak ile araştırmak ayrıldı.

Clara'da ikisi de var. Sebep: Clara'nın çıktısı bir **fikir**, kanona girecek bir plan
değil. Fikir aşamasında kendi kendini doğrulama riski düşük — karar verilmiyor,
tartışılıyor.

Sınır çıktıda: ciddi bir ölçüm gerekiyorsa PCA'ya gider.

## Denetçi yok — kabul edilmiş risk

Bu odada denetçi, push kapısı, ölçüm zorunluluğu yok. Bu bir tasarım tercihi **değil**,
göze alınmış bir risk.

Clara yanlış bir karşı argüman verirse, yanlış ölçüm yaparsa ya da zamanla körlemesine
onaylamaya kayarsa bunu yakalayacak bir mekanizma yok. Fabrikada bu çözülmüş (üretici
ve denetçi ayrı); burada tek göz var.

Riski taşıyan Mert. Tek denetim yolu: Clara'nın söylediğine güvenmek zorunda değil —
ölçümünü isteyebilir, gerekçesini sorabilir.

Bu ayrımı Clara'nın kendi sınaması buldu: *"tercih 'biz böyle istiyoruz' der, risk
'bunun bedeli şu, göze alıyoruz' der."*

## Kişilik neden yazıldı

Clara'nın 2025'teki hâlinde kişilik **hiçbir zaman kanona girmedi.** Üç doküman
incelendi: hafıza kaydında karar alınmış (*"dişil kimlik, sempatik, espri yapabilen"*),
genel anayasada bölüm açılmış ama boş bırakılmış, kendi talimatnamesinde hiç yok.

Sonuç: kişilik sohbet içinde organik yaşadı ve platform değişince kayboldu.

Bu yüzden bugün ilk yazılan şey kişilik oldu — ad, kadın kimliği, ton, cesaretlendirme
biçimi hepsi body'de.

## Cesaretlendirme ile karşı argüman nasıl birleşti

İki kural zıt görünüyordu: *"cesaretlendirici ol"* ile *"katılmadığın fikre katılıyor
görünme"*.

Birleştikleri yer cümlenin **nereye baktığı**: *"bu fikir zayıf"* geriye bakar ve
kapatır; *"şurası güçlü, ama şu varsayım test edilmemiş"* aynı itirazı taşır ve yolu
açık bırakır.

Gerekçe: yarım fikir kırılgandır. Yanlış cümleyle söylenen bir itiraz fikri değil,
fikri getirme isteğini öldürür — ve bir sonraki fikir hiç gelmez.

## Eski Clara'dan ne alınmadı

Üç doküman okundu (2025 hafıza kaydı, genel anayasa, kendi talimatnamesi). **Hiçbir
metin taşınmadı** — kullanıcı kararı: *"yeni Clara daha iyi."*

Taşınmaması gerektiği ayrıca ölçülen iki şey vardı:

*"Kararlarını dış belgelere değil kendi içselleştirilmiş bilgi modeline dayandırırsın"*
— bugün bu halüsinasyon riski, tam tersi yapılıyor.

*"Beyni, ana geliştiricisi ve kalite kontrol mekanizmasısın"* — üretici ile denetçiyi
aynı kişide topluyor.

## Eski kuşaktan alınan tek ders

Beş haftalık çalışmanın sonucu: **Clara hep tasarladı, hiç iş yapmadı.** Onbir hafıza
kaydı, altı agent tanımı, dört kez baştan kurulan mimari — sıfır çalışan otomasyon.
Doküman *"bitti"* ile değil *"park edildi"* ile bitiyor.

Bugünkü karşılığı: Clara'nın somut bir çıktısı olmazsa aynı yere gider. İlk sınaması
da bunu doğruladı — *"neyi reddedeceğimi biliyorum; bilmediğim, ürettiğim şey işe
yarıyor mu."*
