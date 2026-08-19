import * as assert from 'assert';

import { displayName } from '../sessionTree';

/**
 * BASARIM / DAYANIKLILIK TESTI — ad ayristirma.
 *
 * NEDEN VAR: v0.2'de yeni bir yuzey acildi. NAME_PATTERN duzenli ifadesi
 * GUVENILMEZ girdi isliyor (oturum adini baska bir surec yaziyor) ve
 * displayName HER TAZELEMEDE her satir icin cagriliyor.
 *
 * OLCULDU (QA, v0.2): kalip eslesmeyen uzun girdilerde surenin girdi
 * uzunluguyla KUADRATIK buyudugu gorulur - bosluk sayisi iki katina
 * cikinca sure ~3.6-4.1 kat artiyor. Pratikte zararsiz (gercek adlar
 * 15-41 karakter, ~50k karakterde fark edilir gecikme basliyor) ama
 * kayda gecti ve buyume bir sinira baglandi.
 *
 * BU TEST BIR GERILEME KAPISIDIR: kalip ileride degistirilirse ve
 * daha kotu bir geri-izleme davranisi gelirse burada yakalanir.
 */

suite('basarim — ad ayristirma dayanikligi', () => {
  test('gercek boyuttaki adlar ihmal edilebilir surede islenir', () => {
    const gercek = 'Clara · CEO Asistani -  - pr-yazilim-ceo';
    const t0 = Date.now();
    for (let i = 0; i < 1000; i += 1) {
      displayName(gercek);
    }
    const gecen = Date.now() - t0;
    assert.ok(gecen < 200, `1000 cagri ${gecen} ms surdu — beklenen: 200 ms alti`);
  });

  test('ASIRI uzun bozuk ad panelı KILITLEMEZ', () => {
    // 20.000 boslukluk, kalibi eslesmeyen bir ad: en kotu durum sekli.
    const kotu = 'A' + ' '.repeat(20_000) + '-';
    const t0 = Date.now();
    const sonuc = displayName(kotu);
    const gecen = Date.now() - t0;

    // Kirpma yine de calismali (arıza gorunur kalir ama satir kisalir).
    assert.ok(sonuc.length <= 32, 'kirpma uygulanmamis');
    // 1 saniye USTU bir sure kullanicinin hissedecegi bir donma olur.
    assert.ok(gecen < 1000, `asiri uzun ad ${gecen} ms surdu — 1000 ms ustu kabul edilemez`);
  });

  test('kalibi eslesen uzun ad hizli islenir (geri izleme yok)', () => {
    const eslesen = 'R'.repeat(5000) + ' - 0818-21:24 - proje';
    const t0 = Date.now();
    displayName(eslesen);
    const gecen = Date.now() - t0;
    assert.ok(gecen < 100, `eslesen uzun ad ${gecen} ms surdu`);
  });
});
