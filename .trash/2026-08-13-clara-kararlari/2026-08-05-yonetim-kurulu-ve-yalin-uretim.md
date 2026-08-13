# Yönetim kurulu konumu ve yalın üretim felsefesi

**Tarih:** 2026-08-05
**Karar veren:** Mert
**Etkilediği kanon:** `.claude/agents/clara.md` — "Nerede duruyorsun" bölümü eklendi,
"Olmayan probleme çözüm önermezsin" kuralı eklendi

## Şirket yapısı

```
MERT + CLARA        → yönetim kurulu
FABRİKA EKİBİ       → üretici (agent-project: PAM/PAD/PQA/PCA)
BİRİMLER            → Özel Yazılım · Websitesi · (ileride) e-ticaret,
                      marketing, oyun, finans
```

Clara ve insan ekip doğrudan Mert'e bağlı. Fabrika ekibi Clara'ya bağlı — Clara
fabrikayı yönetir, fabrika birimlerin agent takımlarını üretir. `agent-project` takım
havuzudur.

## Nasıl çalışıyor

Zincir kapalı bir döngü:

**İhtiyaç netleşir** (yönetim kurulu) → **fabrika ekip üretir** → **ekip sahada
çalışır** → **davranış izlenir** (yönetim kurulu) → **fabrikaya döner** → **agent
iyileşir**

Yönetim kurulunun iki durağı var: başta ihtiyacı netleştirmek, sonda sahayı izleyip
bulguyu fabrikaya taşınabilir hâle getirmek.

## Yalın üretim (Yangi) felsefesi kabul edildi

**İhtiyaç doğmadan kapasite kurulmaz.** Her personel bir giderdir — agent'ın kendisi
değil ama üretim süresi maliyet, bakımı maliyet, bağlamda tuttuğu yer maliyet.
Gereksiz personel gereksiz yük.

Mert'in cümlesi: *"6 fabrika kurulmadan kontrolcü alır mıydın işe? Sahayı biz
izliyoruz, şu anlık yetiyoruz. Yetemezsek işe birini alırız."*

## Bu karar neyi düzeltti

Clara vizyonu değerlendirirken *"ölçüm zinciri kopuk, fabrikaya koordinatör gerekir"*
dedi. İtiraz yapısal olarak tutarlıydı ama **olmayan bir problemi çözüyordu:**

- Altı birimin biri bile kurulmamıştı
- Hiçbiri aynı anda çalışmıyordu
- Bugünün gerçek yükü tek kişiyle taşınıyordu

Yani öneri bugünün yükü için değil, hayali bir yük için harcama öneriyordu — muda.

Aynı oturumda ikinci kez tekrarlandı: birinci sprint işinin amacı Mert'e sorulmuşken
cevap beklenmeden amaç uyduruldu. İki olayın ortak arızası aynı — **eldeki durumu
değil, hayalindeki durumu çözmek.**

## Ama israfı kesmek yeter değil

Yalın üretimin diğer yarısı: kapasiteyi *tam zamanında* eklemek ancak "artık
yetmiyor" sinyali varsa mümkün. Toyota gereksiz stok tutmaz ama hattı durduran kordonu
her istasyona koyar.

Bugün o sinyal yok. Örnek: bir webhook işi **42 saat**, PLATIN SSL promptu **~48 saat**
bekledi ve ikisi de hiçbir yerde "askıda" görünmedi. O bekleme yetememe miydi, normal
ritim mi — bilinmiyor, ölçü yok.

**Sonucu:** doğru hareket personel önermek değil, **eşiği ölçmek.** Sprintin 7. işi
("takip ve iş yönetim mekanizması") bu yüzden bir yan iş değil — asıl işi ilerlemeyi
göstermek değil, **ne zaman personel alınacağını söylemek.** Adı bu yüzden "kapasite
sinyali" olarak düşünülmeli.

## Kanona neyin girmediği

Vizyonun kendisi ve yalın üretim felsefesi **kanona yazılmadı**, buraya yazıldı.
Sebebi mekanik: kanona yazılan şey bir sonraki turda "doğru" olarak değil "ben" olarak
taşınır — yani sorgulanamaz. Şirket felsefesi Mert'in kararıdır ve değişebilir;
sorgulanamaz hâle gelmemeli.

Kanona yalnız ikisi girdi: **konum** (yönetim kurulu üyesi — altitüdü belirliyor) ve
**davranış** (olmayan probleme çözüm önermeme).
