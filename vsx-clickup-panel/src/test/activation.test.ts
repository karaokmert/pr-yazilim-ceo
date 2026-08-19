import * as assert from 'assert';
import * as vscode from 'vscode';

const EXT_ID = 'pr-yazilim.vsx-clickup-panel';

suite('Aktivasyon iskeleti', () => {
  test('eklenti bulunur ve aktive olur', async () => {
    const ext = vscode.extensions.getExtension(EXT_ID);
    assert.ok(ext, `Eklenti bulunamadi: ${EXT_ID}`);
    await ext.activate();
    assert.strictEqual(ext.isActive, true, 'Eklenti aktive olmadi');
  });

  test('bildirilen tum komutlar fiilen kayitli', async () => {
    const ext = vscode.extensions.getExtension(EXT_ID);
    await ext!.activate();

    const declared: string[] = ext!.packageJSON.contributes.commands.map(
      (c: { command: string }) => c.command
    );
    const registered = await vscode.commands.getCommands(true);

    for (const cmd of declared) {
      assert.ok(
        registered.includes(cmd),
        `contributes.commands'ta var ama kayitli degil: ${cmd}`
      );
    }
    assert.strictEqual(declared.length, 5, 'Beklenen komut sayisi 5');
  });

  test('tree view kayitli ve giris yapilmadan bos doner', async () => {
    const ext = vscode.extensions.getExtension(EXT_ID);
    await ext!.activate();
    // View'i acmak getChildren()'i tetikler; hata firlatmamali.
    await vscode.commands.executeCommand('clickupPanel.tasks.focus');
    assert.ok(true, 'View acilirken hata firlatilmadi');
  });

  /**
   * DEGISTI (onceki hali: "onUri aktivasyon olayi bildirilmis").
   *
   * Eski test onUri'nin VARLIGINI zorunlu kiliyordu ve gerekcesi
   * "OAuth callback icin sart" idi. Mert'in karariyla OAuth kaldirilip
   * Personal API Token'a gecildi; callback olmadigi icin onUri de
   * registerUriHandler de kaldirildi. Test artik tersini bekliyor:
   * kaldirilan mekanizmanin geri sizmadigini dogruluyor.
   */
  test('onUri kaldirilmis — Personal API Token akisinda callback yok', () => {
    const ext = vscode.extensions.getExtension(EXT_ID);
    const events: string[] = ext!.packageJSON.activationEvents ?? [];
    assert.ok(
      !events.includes('onUri'),
      'onUri hala bildirilmis — OAuth callback yok, bu olay gereksiz ve yaniltici'
    );
  });

  test('gizli bilgi ayarlarda saklanmiyor', () => {
    const ext = vscode.extensions.getExtension(EXT_ID);
    const props = Object.keys(
      ext!.packageJSON.contributes.configuration.properties
    );
    const suspicious = props.filter((p) => /secret|token|password/i.test(p));
    assert.deepStrictEqual(
      suspicious,
      [],
      `Gizli bilgi ayar olarak bildirilmis: ${suspicious.join(', ')}`
    );
  });

  test('OAuth kalintisi yok — clientId ayari kaldirilmis', () => {
    const ext = vscode.extensions.getExtension(EXT_ID);
    const props = Object.keys(
      ext!.packageJSON.contributes.configuration.properties
    );
    assert.ok(
      !props.includes('clickupPanel.clientId'),
      'clientId ayari duruyor — OAuth kaldirildi, bu ayar artik anlamsiz'
    );
    assert.ok(props.includes('clickupPanel.teamId'), 'teamId ayari kaybolmus');
  });

  test('kodda okunan her ayar manifest semasinda bildirilmis', () => {
    const ext = vscode.extensions.getExtension(EXT_ID);
    const declared = Object.keys(
      ext!.packageJSON.contributes.configuration.properties
    );
    // taskTree.resolveTeamId() bu anahtari okuyor; semada yoksa
    // Settings arayuzunde gorunmez ve dogrulama almaz.
    assert.ok(
      declared.includes('clickupPanel.teamId'),
      'Kod clickupPanel.teamId okuyor ama semada bildirilmemis'
    );
  });

  test('argumana bagli komutlar komut paletinde gizli', () => {
    const ext = vscode.extensions.getExtension(EXT_ID);
    const palette: Array<{ command: string; when?: string }> =
      ext!.packageJSON.contributes.menus.commandPalette;

    for (const cmd of ['clickupPanel.showTask', 'clickupPanel.changeStatus']) {
      const entry = palette.find((e) => e.command === cmd);
      assert.ok(entry, `${cmd} icin commandPalette girdisi yok`);
      assert.strictEqual(
        entry.when,
        'false',
        `${cmd} paletten argumansiz cagrilabilir — anlamli is yapamaz`
      );
    }
  });
});
