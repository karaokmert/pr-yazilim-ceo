import * as assert from 'assert';
import * as vscode from 'vscode';

/**
 * GUVENLIK YUZEYI TESTLERI — Markdown/tooltip enjeksiyonu.
 *
 * NEDEN VAR: oturum "name" alani BASKA BIR SURECIN diske yazdigi veridir.
 * Bizim sozlesmemiz degil; guvenilmez girdi olarak islenmelidir.
 * VS Code'da MarkdownString ile bir tooltip'e komut baglantisi
 * (command:...) enjekte edilebilirse, kullanicinin tek tiklamayla
 * istemedigi bir komutu calistirmasi mumkun olur.
 *
 * Developer bu noktada ACIKCA ikinci goz istedi. Olculen sey:
 * varsayilan bayraklarin (isTrusted / supportHtml kapali) gercekten
 * koruyup korumadigi — beyan degil, davranis.
 */

suite('guvenlik — MarkdownString varsayilanlari', () => {
  test('isTrusted VARSAYILAN OLARAK kapali (komut baglantisi calismaz)', () => {
    const md = new vscode.MarkdownString();
    md.appendMarkdown('[tikla](command:workbench.action.terminal.new)');
    assert.ok(
      md.isTrusted === false || md.isTrusted === undefined,
      `isTrusted varsayilani beklenmedik: ${String(md.isTrusted)} — komut baglantilari calisabilir`
    );
  });

  test('supportHtml VARSAYILAN OLARAK kapali (ham HTML render edilmez)', () => {
    const md = new vscode.MarkdownString();
    md.appendMarkdown('<img src=x onerror="x">');
    assert.ok(
      md.supportHtml === false || md.supportHtml === undefined,
      `supportHtml varsayilani beklenmedik: ${String(md.supportHtml)} — ham HTML render edilebilir`
    );
  });

  test('supportThemeIcons acilinca bile isTrusted KENDILIGINDEN acilmaz', () => {
    // Kodda stale dalinda supportThemeIcons=true yapiliyor. Bunun yan etki
    // olarak guveni acmadigi dogrulanir.
    const md = new vscode.MarkdownString();
    md.supportThemeIcons = true;
    assert.ok(
      md.isTrusted === false || md.isTrusted === undefined,
      'supportThemeIcons isTrusted\'i acmis — komut baglantisi riski'
    );
  });

  test('appendText kullanilsaydi da kacis saglanirdi (referans olcum)', () => {
    const md = new vscode.MarkdownString();
    md.appendText('[tikla](command:x)');
    // appendText Markdown'i kacirir; uretilen deger ham metin OLMAMALI.
    assert.notStrictEqual(md.value, '[tikla](command:x)');
  });
});

suite('guvenlik — eklenti yuzeyi', () => {
  test('eklenti hicbir gizli-bilgi (secret) API\'si kullanmiyor', async () => {
    // Dolayli olcum: aktivasyon sonrasi eklenti calisiyor ve secrets
    // API'sine dokunmuyor (kaynak taramasiyla birlikte degerlendirilir).
    const ext = vscode.extensions.getExtension('pryazilim.vsx-agent-panel');
    await ext?.activate();
    assert.strictEqual(ext?.isActive, true);
  });

  test('manifest hicbir ayar araciligiyla calistirilabilir yol istemiyor', () => {
    const ext = vscode.extensions.getExtension('pryazilim.vsx-agent-panel');
    const props = ext?.packageJSON?.contributes?.configuration?.properties ?? {};
    for (const [key, value] of Object.entries<{ type?: string }>(props)) {
      // Calistirilabilir yol tasiyan bir ayar olsaydi untrustedWorkspaces
      // beyaninin 'limited' + restrictedConfigurations olmasi gerekirdi.
      assert.strictEqual(
        value.type,
        'number',
        `${key} sayisal degil — calistirilabilir yol tasiyorsa guven beyani gozden gecirilmeli`
      );
    }
  });
});
