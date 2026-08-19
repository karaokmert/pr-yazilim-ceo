# Degisiklik Gunlugu

Bu projenin kayda deger tum degisiklikleri bu dosyada belgelenir.
Bicim [Keep a Changelog](https://keepachangelog.com/) esas alinir ve
surumleme [Semantic Versioning](https://semver.org/) kurallarina uyar.

## [0.1.0] — 2026-08-18

Ilk calisan surum. Ic kullanim icin dagitilir (pazar yerinde yayinlanmaz).

### Eklendi
- **ClickUp Personal API Token ile giris** — `ClickUp: Token Gir` komutu. Token
  saklanmadan once `GET /user` ile dogrulanir; gecersiz token kaydedilmez.
  Token yalnizca `context.secrets` icinde tutulur.
- **Atanmis task paneli** — Activity Bar'da "ClickUp" gorunumu; size atanmis
  acik task'lari listeler. Sub task'lar tek API cagrisiyla alinip `parent`
  alanindan agac olarak kurulur.
- **Task detayi** — bir task'a tiklayinca salt-okunur Markdown belgesi acilir
  (statu, liste, oncelik, atananlar, bitis tarihi, aciklama).
- **Statu degistirme** — satir ici `$(arrow-swap)` eylemi. Gecerli statuler
  task'in bagli oldugu listeden okunup secim olarak sunulur; ayni statu
  secilirse istek gonderilmez.
- **Workspace secimi** — `clickupPanel.teamId` ayari bossa ve birden fazla
  workspace varsa secim sorulur, secim ayara yazilir.
- **Oturum temizleme** — `ClickUp: Token'i Sil` komutu; ayrica 401/403 alindiginda
  oturum otomatik temizlenip kullaniciya tekrar giris yapmasi bildirilir.

### Bilinen sinirlar
- Task listesi ilk sayfayla sinirli (ClickUp sayfa basina 100 task doner).
  100'den fazla acik task'i olan kullanici eksik liste gorur.
- Ust task'i baskasina atanmis sub task'lar kok seviyede gosterilir.
- Otomatik guncelleme yok: `.vsix` ile kurulan eklentiler kendini guncellemez.
