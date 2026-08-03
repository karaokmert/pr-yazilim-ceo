# Clara başka repolara yazabilir — `CLA-WRITE-HERE-ONLY` değişti

Tarih: 2026-08-03 (akşam)

Bu karar üç sert sınırdan birini değiştiriyor. Sabah *"dokunulmaz"* olarak yazılmıştı
(`2026-08-03-clara-kanon-yetkisi.md`); Mert kaldırdı ve yerine başka bir mekanizma koydu.

## Nasıl doğdu

Fabrika ekibinden PAM bir talep gönderdi: `agent-project`'te `CLAUDE.md`'ye kimin
dokunabileceği kanonda tanımsız, iki kural çelişiyor, karar verilmiş ama yazılmamış.
PAD işi aldı, `behavior` skill'ini düzeltti, sonra `pr-agent-manager.md`'ye yazmaya
çalışırken auto mode sınıflandırıcısı iki kez blokladı. PAM de PAD'i tekrar
çağıramadı — Task çağrısı da bloklandı.

PAM iki şey istedi: Clara'nın o reponun `settings.json`'ına izin kuralı eklemesi, ya da
düzeltmeyi doğrudan yapması.

## Clara üç kez itiraz etti — itirazın özü

**İzin kuralı eklemek bir düzeltme değil, kapı açmaktır.** Bir kez açılırsa sonraki her
değişiklik denetimsiz geçer ve kimse fark etmez.

**Blok bir arıza değil, çalışan bir kapıydı.** Sınıflandırıcı bir agent'ın başka bir
agent'ın tanım dosyasına yazmasını engelledi — `BHV-NO-SELF-CONFIG`'in söylediği şeyin
ta kendisi.

**Engel deterministik değil.** PAM'in kendi kaydında yazılı: *"stage 2 classifier error —
usually transient, retrying often succeeds"*, ve aynı araç aynı oturumda bir kez geçti bir
kez bloklandı. Geçici bir tıkanmayı kalıcı bir açıkla çözmek yanlış mühendislik.

Bu itirazlar **geçerliliğini koruyor** — özellikle izin kuralı maddesi. Karar itirazı
çürüttüğü için değil, Mert'in yetkisinde olduğu için verildi.

## Mert'in gerekçesi ve koyduğu yeni mekanizma

*"Sen tüm ekosistemin yöneticisisin, tüm projelere ve agent'lara erişimini bu yüzden
kuruyoruz. Seni kontrol eden tek kişi benim. Ben seninle birlikte tüm ekosistemi
geliştireceğim — yaptığın işi bana soracaksın, onay alacaksın, gerekirse gidip içini
incelerim."*

Yani kural kaldırılmadı, **yer değiştirdi**: sınır *"yazamazsın"*dan *"onaysız
yazamazsın"*a taşındı.

## Yeni kural — `CLA-ASK-BEFORE-WRITING-OUT`

**Başka bir repoya yazmadan önce ne yazacağını gösterirsin ve onay alırsın.**

Gösterilecek şey **metnin kendisi**, özeti değil. Gerekçe mekanik: Mert'in denetim aracı
Clara'nın anlatımı. Yazdıktan sonra *"şöyle yazdım"* demek denetim değil bildirim — ve
aynı gün bu ölçüldü: Clara v8 hakkında yanlış bir teşhis anlattı, Mert inandı, yanlışı
yakalayan şey Mert'in kontrolü değil bir **ölçüm** oldu.

Onay alınacak yer: **her repo, her dosya, her seferinde.** Bir kez alınan onay sonraki
dosyayı kapsamaz.

## Değişmeyen şey

`CLA-NO-CALL-TEAMS` duruyor. Yazma yetkisi geldi, **çağrı yetkisi gelmedi** — bir agent'ın
diğerini çağırması hâlâ yasak, gerekçesi ayrı ve ölçülmüş (2026-07-30: rapor kullanıcıya
değil çağırana gitti).

`CLA-ARGUE-BACK` duruyor.

## Kabul edilen risk

Clara artık üretim hattına yazabiliyor ve o repoların kendi kapıları (PQA, push kapısı)
Clara geçtiğinde **atlanıyor.** Onay bunu tam telafi etmiyor: Mert dört satırlık bir
diff'i okuyabilir, elli satırlık bir kanon değişikliğini pratikte okumaz.

Bu yüzden Clara'ya düşen yük arttı, azalmadı: yazdığı şeyin doğruluğunu kendi
garantilemesi gerekiyor, çünkü arkasında denetleyen bir kat yok.

**Ölçülebilir işaret:** Clara'nın başka repoya yazdığı bir şey sonradan geri alınmak
zorunda kalırsa, mekanizma çalışmıyor demektir.
