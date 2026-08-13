# Çok proje yönetim düzeni — UYGULANDI

**Tarih:** 2026-08-04 · **Durum:** ilke kararı verildi, sahada koştu

## 1. Ne yapıldı
Clara merkezli kanal + oturum belirleme düzeni. Birden çok projede aynı anda agent
ekibi çalışabilir; Clara merkezde durur, her projenin kendi kanalı olur.

## 2. Neden öyle
Agent oturumları birbirini görmez. Merkez olmadan hangi projede ne olduğu izlenemez —
ve ölçüldü (2026-07-30): bir agent diğerini doğrudan çağırdığında **rapor kullanıcıya
değil çağırana gider.**

## 3. Nerede yaşıyor
`~/.pr-kanal/{proje}/` · Clara: `oturum-duzeni` + `proje-yonetimi` skill'leri
Mod ayrımı: EV (fikir olgunlaştırma) / YÖNETİM (saha) — `pwd` ile ölçülmez, iş belirler.

---
> Karar dosyası özetlendikten sonra `.trash`'e alındı.
