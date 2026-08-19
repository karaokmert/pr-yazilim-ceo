import * as vscode from 'vscode';
import { SessionTreeProvider, folderFromNode, startAutoRefresh } from './sessionTree';

/**
 * Eklenti giris noktasi.
 *
 * DISPOSAL DESENI — Architect'in kurdugu kural surdurulur:
 * uretilen her Disposable ayni satirda context.subscriptions'a itilir.
 * Extension host tum eklentilerle PAYLASILIR; sizinti yalniz bizi degil
 * kullanicinin butun editorunu yavaslatir.
 *
 * activate() HIZLI kalir: burada disk OKUNMAZ. Ilk tarama tetiklenir
 * ama beklenmez (void) — agac "Yukleniyor…" gosterir, sonuc gelince tazelenir.
 */
export function activate(context: vscode.ExtensionContext): void {
  const output = vscode.window.createOutputChannel('Agent Durum Paneli');
  context.subscriptions.push(output);

  output.appendLine('Agent Durum Paneli etkinlestirildi.');

  // --- Veri saglayici ----------------------------------------------------
  const provider = new SessionTreeProvider(output);
  context.subscriptions.push(provider);

  // createTreeView (registerTreeDataProvider degil): gorunum nesnesine
  // ROZET icin ihtiyacimiz var. Rozet kenar cubugu ikonunda, PANEL
  // KAPALIYKEN de gorunur; asil aranan bilgi (unutulmus oturum sayisi)
  // boylece paneli acmadan fark edilir.
  const view = vscode.window.createTreeView('vsxAgentPanel.sessions', {
    treeDataProvider: provider,
    showCollapseAll: true,
  });
  context.subscriptions.push(view);
  provider.attachView(view);

  // --- Komut kayitlari ---------------------------------------------------
  // Her komutun package.json > contributes.commands icinde karsiligi VARDIR.
  // Kod ve manifest girdisi TEK is birimidir.

  context.subscriptions.push(
    vscode.commands.registerCommand('vsxAgentPanel.refresh', async () => {
      await provider.refresh();
      output.appendLine('Yenile komutu calisti.');
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand('vsxAgentPanel.openFolder', async (node?: unknown) => {
      // YOKLUK NORMAL BIR DURUMDUR: komut palet uzerinden argumansiz da
      // cagrilabilir (manifest'te when:false ile gizli, ama baska bir
      // eklenti executeCommand ile cagirabilir).
      const folder = folderFromNode(node);
      if (!folder) {
        vscode.window.showWarningMessage('Acilacak dizin bulunamadi.');
        return;
      }

      const uri = vscode.Uri.file(folder);

      // Dizin gercekten var mi — silinmis bir dizini acmaya calismak
      // sessiz bir bos pencere uretir.
      try {
        const stat = await vscode.workspace.fs.stat(uri);
        if ((stat.type & vscode.FileType.Directory) === 0) {
          vscode.window.showWarningMessage(`Bir dizin degil: ${folder}`);
          return;
        }
      } catch {
        vscode.window.showWarningMessage(`Dizin bulunamadi: ${folder}`);
        return;
      }

      // Zaten acik olan bir dizini yeniden acmak pencereyi bosuna yeniler.
      const alreadyOpen = vscode.workspace.workspaceFolders?.some(
        (workspaceFolder) => workspaceFolder.uri.fsPath === uri.fsPath
      );
      if (alreadyOpen) {
        vscode.window.showInformationMessage('Bu dizin zaten acik.');
        return;
      }

      output.appendLine(`Dizin aciliyor: ${folder}`);
      // forceNewWindow: mevcut pencereyi kapatmaz — kullanici izlemeye
      // devam edebilsin (panelin amaci bu).
      await vscode.commands.executeCommand('vscode.openFolder', uri, {
        forceNewWindow: true,
      });
    })
  );

  // --- Tazeleme ----------------------------------------------------------
  // Dosya izleyici + periyodik yoklama; ikisi de tek Disposable altinda.
  context.subscriptions.push(startAutoRefresh(provider, output));

  // Ilk tarama — beklenmez, aktivasyon hizli kalir.
  void provider.refresh();
}

/**
 * context.subscriptions'in ifade edemedigi temizlik BURAYA yazilir.
 * Su an oyle bir kaynak yok; disposable olan her sey yukarida kayitli.
 */
export function deactivate(): void {
  // Bilerek bos.
}
