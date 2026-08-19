# Degisiklik Gunlugu

## [0.2.0] - 2026-08-18

Panel proje bazli gruplandi; satirlar sadelesti.

### Eklenen
- **Iki kademeli agac:** oturumlar calisma dizinine (cwd) gore proje
  gruplarinda toplanir. Grup basligi klasor adini, oturum sayisini ve
  varsa unutulmus sayisini gosterir.
- **Kenar cubugu rozeti:** unutulmus oturum sayisi panel KAPALIYKEN de
  gorunur.
- Dizini bilinmeyen oturumlar "(dizin bilinmiyor)" grubunda toplanir.
- Grup basligindan da calisma dizini acilabilir (sag tik).
- Unutulmus oturum tasiyan gruplar listenin basinda; grup basliginda
  sari uyari ikonu.

### Degisen
- **Satirlar kisaldi:** oturum satirinda artik yalniz sade rol adi ve
  sessizlik suresi var. Dizin satirdan cikti (grup basliginda duruyor).
- Oturum adlari ayristirilip sade role indirgeniyor; ayristirma
  tutmazsa ham ad oldugu gibi korunur (arıza gizlenmez).
- Uzun adlar 32 karakterde kirpilir; **tam ad tooltip'te eksiksiz durur.**
- Tooltip'e "Ham ad" satiri eklendi.

### Duzeltilen
- Tooltip basligi kirpilmis adi gosteriyordu; artik tam adi gosteriyor
  (kirpilmis satir ile gercek ad arasindaki koprü kopmuyor).

### Notlar
- Guvenlik yuzeyi degismedi: eklenti yalniz okur, ag cagrisi yapmaz,
  telemetri toplamaz, gizli bilgi saklamaz.
- Veri katmani (`sessions.ts`) bu surumde HIC degismedi.

## [0.1.0] - 2026-08-18

Ilk calisan surum — panel gercek oturum verisini gosteriyor.

### Eklenen
- Kenar cubugunda "Agent Durumu" paneli: acik Claude Code oturumlari canli listelenir.
- Unutulmus oturum (varsayilan 15 dk sessiz) sari uyari ikonuyla listenin en ustunde gosterilir.
- Oturuma tiklayinca calisma dizini yeni pencerede acilir; zaten acik dizin icin bilgi verilir.
- Sag tik menusunde "Oturum Dizinini Ac" — yalniz dizini bilinen oturumlarda gorunur.
- Baslikta "Yenile" komutu.
- Iki ayar: `refreshIntervalSeconds` (varsayilan 5) ve `staleThresholdMinutes` (varsayilan 15).
  Ikisi de yeniden yukleme gerektirmeden etkili olur.
- Oturum kaydi bulunamadiginda ve dizin okunamadiginda anlamli bos-durum satirlari.

### Notlar
- Bozuk, eksik ya da olu surece ait oturum kayitlari sessizce elenir; panel patlamaz.
- Ayni surece ait birden fazla kayit tekillestirilir (en taze kayit kazanir).
- Eklenti yalniz `~/.claude/sessions` dizinini OKUR; yazmaz, silmez, ag cagrisi yapmaz.

## [0.0.1] - 2026-08-18

- Proje iskeleti: manifest, esbuild, tsconfig, .vscodeignore, hata ayiklama yapilandirmasi.
- activate/deactivate yasam dongusu ve disposal deseni kuruldu.
- Veri katmani HENUZ BAGLANMADI (Developer'a devredildi).
