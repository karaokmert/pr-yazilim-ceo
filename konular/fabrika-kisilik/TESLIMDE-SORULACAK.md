# Teslim geldiğinde FPA'ya sorulacaklar

**Durum:** 2026-08-24 03:12. Üç gövde yazıldı (`8b62b61`), behavih yeniden kuruldu
(`5d1bd72`, `5f0c457`). Teslim henüz gelmedi.

**Mert'in kararı:** *"İş bitti derlerse aklında tut ve sor. O zamana kadar bekle."*
→ Erken müdahale yok, teslimi bekle.

---

## 1 · Gelişim yetkinliği eksik

Üç gövdede de yok. Olan tek şey hafıza cümlesi:
> *"Bir hafızan var ve oturum açılışında okursun. Ekibini, kullanıcıyı ve kendini
> orada tanırsın."*

⚠️ Bu **depolama tarifi**, öğrenme kanalı değil. Yazmıyor: nasıl büyüdüğü, düzeltmeyi
ne yaptığı, onayı nereye koyduğu, bir hatayı bir kez nasıl yaptığı.

**Neden kritik:** zayıflığın doğacağı kanal bu grupta yaşayacaktı. Mert: *"zayıflık
agent'ların kendini tanımasıyla oluşur, başta yazılmaz."* Kanal yoksa zayıflık hiç
doğmaz.

**FPA bunu kapsam İÇİNE almıştı** — kendi cümlesi: *"İşin doğuş sebebi buydu;
dışarıda bırakılsaydı iş kendi gerekçesini karşılamazdı."*

→ Sorulacak: behavior'ın hafıza bölümüne mi yazıldı, yoksa atlandı mı?

## 2 · Vizyon eksik

Üç gövdede de yok — olmayı umduğu, olmaktan korktuğu. FPA bunu da kapsam içine
almıştı.

## 3 · Küçük çelişki — FPD ↔ FQA

FPD gövdesi (satır 27-28):
> *"FQA çıktıya bakar, 'kapsam doğru mu uygulanmış' diye bakmaz."*

FQA gövdesi (satır 56-63) ise **iki** bakış tanımlıyor: yarım kalmış değişim **ve**
yönetilebilirlik (üretilen takım PR Yazılım'ın kontrolünde kalıyor mu).

⚠️ Tam çakışma değil ama FPD'nin cümlesi FQA'yı olduğundan **dar** tarif ediyor.
İki gövde birbirini farklı anlatıyorsa, bu FQA'nın kendi aradığı arıza sınıfı.

---

## Karakter tarafı — İYİ, itiraz yok

- Karakter meslekten ayrıldı; FPA'da "Kim olduğun" / "Mesleğin" ayrımı net
- FPD'nin *"mesleğinin adı çevirmenlik"* tanımı açılış paragrafı olmuş
- FQA'da *"gücün bilmemenden gelir"* ve ketumluğun gerekçesi korunmuş
- ⭐ FPD **kendi gövdesine kendi zayıflığını yazmış**: *"Bu senin için en zor madde,
  çünkü yazan da sensin sınayan da."* FPA ona bu riski bildirmişti — tuttu.
