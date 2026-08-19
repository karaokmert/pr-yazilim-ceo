import * as assert from 'assert';
import * as vscode from 'vscode';

/**
 * ENTEGRASYON TESTLERI — gercek, indirilmis bir VS Code icinde kosar.
 *
 * Burada olculen sey "kod calisiyor mu" degil, "MANIFEST ve KOD ANLASIYOR MU":
 * bir komut manifest'te yazili ama kayitli degilse palet'te patlar; kayitli
 * ama manifest'te yoksa palet'te hic gorunmez. Ikisi de SESSIZ arizadir ve
 * yalniz gercek editor icinde yakalanir.
 */

const EXTENSION_ID = 'pryazilim.vsx-agent-panel';

suite('eklenti — aktivasyon', () => {
  test('eklenti bulunuyor', () => {
    const ext = vscode.extensions.getExtension(EXTENSION_ID);
    assert.ok(ext, `${EXTENSION_ID} bulunamadi`);
  });

  test('aktive olabiliyor ve aktivasyon HATASIZ tamamlaniyor', async () => {
    const ext = vscode.extensions.getExtension(EXTENSION_ID);
    assert.ok(ext);
    await ext!.activate();
    assert.strictEqual(ext!.isActive, true, 'eklenti aktif degil');
  });
});

suite('eklenti — komutlar', () => {
  suiteSetup(async () => {
    const ext = vscode.extensions.getExtension(EXTENSION_ID);
    await ext?.activate();
  });

  test('manifest komutlarinin HEPSI kayitli', async () => {
    const registered = await vscode.commands.getCommands(true);
    const ext = vscode.extensions.getExtension(EXTENSION_ID);
    const declared: string[] = (ext?.packageJSON?.contributes?.commands ?? []).map(
      (c: { command: string }) => c.command
    );

    assert.ok(declared.length > 0, 'manifest hic komut bildirmiyor');
    for (const command of declared) {
      assert.ok(
        registered.includes(command),
        `manifest'te bildirilen komut kayitli degil: ${command}`
      );
    }
  });

  test('refresh komutu HATA ATMADAN calisir', async () => {
    // Donus degeri yok; olculen sey "patlamiyor mu".
    await vscode.commands.executeCommand('vsxAgentPanel.refresh');
  });

  test('openFolder argumansiz cagrilinca patlamaz (yokluk normal durumdur)', async () => {
    // Manifest'te palet'ten gizli ama baska bir eklenti executeCommand ile
    // cagirabilir. Uyari gosterip sessizce donmeli.
    await vscode.commands.executeCommand('vsxAgentPanel.openFolder');
  });

  test('openFolder gecersiz dizinle cagrilinca patlamaz', async () => {
    await vscode.commands.executeCommand(
      'vsxAgentPanel.openFolder',
      '/olmayan/bir/dizin/vsx-test'
    );
  });
});

suite('manifest — bildirilen ile gercek uyusuyor mu', () => {
  test('ayar anahtarlari manifest\'te tanimli', () => {
    const ext = vscode.extensions.getExtension(EXTENSION_ID);
    const props = ext?.packageJSON?.contributes?.configuration?.properties ?? {};
    assert.ok(
      'vsxAgentPanel.refreshIntervalSeconds' in props,
      'refreshIntervalSeconds manifest\'te yok — Ayarlar arayuzunde gorunmez'
    );
    assert.ok(
      'vsxAgentPanel.staleThresholdMinutes' in props,
      'staleThresholdMinutes manifest\'te yok'
    );
  });

  test('ayarlar okunabiliyor ve varsayilanlari manifest ile ayni', () => {
    const config = vscode.workspace.getConfiguration('vsxAgentPanel');
    assert.strictEqual(config.get<number>('refreshIntervalSeconds'), 5);
    assert.strictEqual(config.get<number>('staleThresholdMinutes'), 15);
  });

  test('capabilities BEYANI kodla tutarli: calisma alanina dokunulmuyor', () => {
    const ext = vscode.extensions.getExtension(EXTENSION_ID);
    const caps = ext?.packageJSON?.capabilities ?? {};
    assert.strictEqual(
      caps.untrustedWorkspaces?.supported,
      true,
      'untrustedWorkspaces beyani degismis — kodla birlikte yeniden degerlendirilmeli'
    );
    assert.strictEqual(
      caps.virtualWorkspaces?.supported,
      false,
      'virtualWorkspaces beyani degismis — Node fs kullanimi bu beyana dayali'
    );
  });

  test('gorunum kapsayicisi ve gorunum bildirilmis', () => {
    const ext = vscode.extensions.getExtension(EXTENSION_ID);
    const views = ext?.packageJSON?.contributes?.views?.vsxAgentPanel ?? [];
    assert.ok(
      views.some((v: { id: string }) => v.id === 'vsxAgentPanel.sessions'),
      'vsxAgentPanel.sessions gorunumu bildirilmemis'
    );
  });
});
