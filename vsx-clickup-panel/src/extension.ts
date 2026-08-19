import * as vscode from 'vscode';
import { AuthService } from './auth/authService';
import { registerCommands } from './commands';
import { TaskTreeProvider } from './views/taskTree';

/**
 * Aktivasyon: ucuz olmali. Burada yalnizca kayit yapilir.
 * Ag cagrisi YOK — task cekme, view ilk kez gorunur oldugunda
 * TaskTreeProvider.getChildren() icinden tetiklenir.
 *
 * Dispose deseni: olusturulan her Disposable ayni satirda
 * context.subscriptions'a itilir. Bu iskelet taklit edilerek
 * buyuyecek — yeni bir kayit eklerken deseni bozma.
 */
export async function activate(context: vscode.ExtensionContext): Promise<void> {
  const auth = new AuthService(context);
  context.subscriptions.push(auth);

  const taskTree = new TaskTreeProvider(auth);
  context.subscriptions.push(taskTree);

  context.subscriptions.push(
    vscode.window.registerTreeDataProvider('clickupPanel.tasks', taskTree)
  );

  // NOT: burada bir registerUriHandler YOK ve bu bilincli.
  // Personal API Token akisinda tarayicidan donen bir callback olmadigi
  // icin URI handler'a gerek kalmadi; manifest'teki "onUri" aktivasyon
  // olayi da ayni gerekceyle kaldirildi. Ikisi tek is birimidir —
  // biri kaldirilip digeri birakilirsa kod "URI handler var, calisiyor
  // olmali" diye yanlis okunur.
  registerCommands(context, auth, taskTree);

  // Giris durumu menu gorunurlugunu (when: clickupPanel.signedIn) surer.
  context.subscriptions.push(
    auth.onDidChangeSession(() => {
      void syncSignedInContext(auth);
      taskTree.refresh();
    })
  );
  await syncSignedInContext(auth);
}

async function syncSignedInContext(auth: AuthService): Promise<void> {
  const signedIn = await auth.isSignedIn();
  await vscode.commands.executeCommand('setContext', 'clickupPanel.signedIn', signedIn);
}

/**
 * context.subscriptions'in ifade edemedigi temizlik burada yapilir.
 * Su an oyle bir sey yok; dispose edilebilir her sey yukarida sahiplenildi.
 */
export function deactivate(): void {
  // bilerek bos
}
