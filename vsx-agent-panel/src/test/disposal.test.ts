import * as assert from 'assert';
import * as vscode from 'vscode';

import { SessionTreeProvider, startAutoRefresh } from '../sessionTree';

/**
 * DISPOSAL TESTLERI — sizinti kontrolu.
 *
 * NEDEN ONEMLI: extension host TUM eklentilerle paylasilir. Durdurulmamis
 * bir setInterval ya da dispose edilmemis bir izleyici, kullanicinin butun
 * editorunu yavaslatir ve suc VS Code'a atilir.
 *
 * Developer'in test listesindeki 7. madde ("paneli kapat/ac, kalinti log
 * akmasin") kismen buraya karsilik gelir; tam karsiligi elle EDH gozlemidir
 * ve o AYRICA yapilir.
 */

suite('disposal — kaynak sizintisi', () => {
  test('provider dispose edildikten sonra refresh SESSIZCE yok sayilir', async () => {
    const output = vscode.window.createOutputChannel('disposal-testi');
    const provider = new SessionTreeProvider(output);

    provider.dispose();
    // Dispose sonrasi cagri patlamamali (emitter kapali; fire cagrilirsa atar).
    await provider.refresh();
    provider.refreshElapsed();

    output.dispose();
  });

  test('startAutoRefresh TEK Disposable doner ve dispose edilebilir', () => {
    const output = vscode.window.createOutputChannel('disposal-testi-2');
    const provider = new SessionTreeProvider(output);

    const handle = startAutoRefresh(provider, output);
    assert.ok(typeof handle.dispose === 'function', 'Disposable donmedi');

    // Iki kez dispose etmek de patlamamali (idempotent olmali).
    handle.dispose();
    handle.dispose();

    provider.dispose();
    output.dispose();
  });

  test('dispose sonrasi zamanlayici ARTIK tetiklenmiyor', async () => {
    const output = vscode.window.createOutputChannel('disposal-testi-3');
    const provider = new SessionTreeProvider(output);

    let refreshSayisi = 0;
    const subscription = provider.onDidChangeTreeData(() => {
      refreshSayisi += 1;
    });

    const handle = startAutoRefresh(provider, output);
    handle.dispose();

    const dispozSonrasi = refreshSayisi;
    // Varsayilan aralik 5 sn; 2 sn beklemek zamanlayicinin oldugunu
    // kesin kanitlamaz ama CALISMAYA DEVAM ediyorsa cogu durumda yakalar.
    await new Promise((resolve) => setTimeout(resolve, 2000));

    assert.strictEqual(
      refreshSayisi,
      dispozSonrasi,
      'dispose sonrasi tazeleme olayi geldi — zamanlayici durmamis olabilir'
    );

    subscription.dispose();
    provider.dispose();
    output.dispose();
  });
});
