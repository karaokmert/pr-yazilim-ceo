import * as vscode from 'vscode';
import { ClickUpApi, ClickUpApiError, type ClickUpUser } from '../clickup/api';

/** context.secrets anahtari. globalState/settings ASLA kullanilmaz. */
const TOKEN_KEY = 'clickupPanel.accessToken';

/**
 * ClickUp oturumunun sahibi — Personal API Token ile.
 *
 * KARAR (Mert, 2026-08-18): OAuth degil Personal API Token.
 * ClickUp'in OAuth token degis-tokusu client_secret zorunlu kilar ve
 * PKCE desteklemez; bir .vsix zip dosyasidir ve icine gomulen sir
 * sir degildir. Kullanici kendi token'ini girer.
 *
 * KURAL: token YALNIZCA context.secrets icinde yasar.
 * globalState diskte sifrelenmemis durur, settings.json baska
 * makinelere senkronlanir ve hata raporlarina yapistirilir.
 */
export class AuthService implements vscode.Disposable {
  private readonly disposables: vscode.Disposable[] = [];
  private readonly sessionChanged = new vscode.EventEmitter<void>();
  readonly onDidChangeSession = this.sessionChanged.event;

  /** Token dogrulandiginda sahibinin kimligi — listAssignedTasks icin sart. */
  private cachedUser: ClickUpUser | undefined;

  private readonly api: ClickUpApi;

  constructor(private readonly context: vscode.ExtensionContext) {
    this.disposables.push(this.sessionChanged);
    this.api = new ClickUpApi(() => this.getToken());
  }

  async isSignedIn(): Promise<boolean> {
    return (await this.getToken()) !== undefined;
  }

  async getToken(): Promise<string | undefined> {
    return this.context.secrets.get(TOKEN_KEY);
  }

  /**
   * Oturum sahibinin ClickUp kullanicisi.
   *
   * Onbelleklenir: her task cekiminde /user cagrisi yapmak gereksiz.
   * signOut() onbellegi temizler, boylece bayat kimlik kalmaz.
   */
  async getCurrentUser(): Promise<ClickUpUser | undefined> {
    if (this.cachedUser) {
      return this.cachedUser;
    }
    if (!(await this.isSignedIn())) {
      return undefined;
    }
    this.cachedUser = await this.api.getCurrentUser();
    return this.cachedUser;
  }

  /**
   * Token girisi: kullanicidan token alir, ClickUp'a karsi DOGRULAR,
   * ancak gecerliyse saklar.
   *
   * Dogrulamadan saklamak kotu bir takas olurdu: yanlis token sessizce
   * kaydedilir, kullanici "giris yaptim" saniir ve arizayi ancak task
   * listesi bos gelince fark ederdi.
   */
  async signIn(): Promise<void> {
    const token = await vscode.window.showInputBox({
      title: 'ClickUp Personal API Token',
      prompt: 'ClickUp > Settings > Apps > API Token bolumunden kopyalayin',
      placeHolder: 'pk_...',
      ignoreFocusOut: true,
      password: true,
      validateInput: (value) => {
        const trimmed = value.trim();
        if (!trimmed) {
          return 'Token bos olamaz.';
        }
        if (!trimmed.startsWith('pk_')) {
          return 'Personal API Token "pk_" ile baslar.';
        }
        return undefined;
      },
    });

    // undefined = kullanici ESC'ledi. Iptal bir hata degildir, sessizce cik.
    if (token === undefined) {
      return;
    }

    const trimmed = token.trim();

    const user = await vscode.window.withProgress(
      { location: vscode.ProgressLocation.Notification, title: 'ClickUp token dogrulaniyor...' },
      async () => {
        // Henuz saklamadik — dogrulama icin token'i dogrudan veren gecici istemci.
        const probe = new ClickUpApi(async () => trimmed);
        return probe.getCurrentUser();
      }
    );

    await this.context.secrets.store(TOKEN_KEY, trimmed);
    this.cachedUser = user;
    this.sessionChanged.fire();

    void vscode.window.showInformationMessage(`ClickUp: ${user.username} olarak giris yapildi.`);
  }

  async signOut(): Promise<void> {
    await this.context.secrets.delete(TOKEN_KEY);
    this.cachedUser = undefined;
    this.sessionChanged.fire();
  }

  /**
   * Token gecersizlestiginde (401/403) oturumu temizler.
   * Cagiran taraf ClickUpApiError.isAuthError gordugunde buraya doner —
   * boylece kullanici "neden bos" diye bakmak yerine tekrar giris yapar.
   */
  async handleAuthFailure(): Promise<void> {
    await this.signOut();
    void vscode.window.showWarningMessage(
      'ClickUp token gecersiz ya da suresi dolmus. Lutfen tekrar giris yapin.'
    );
  }

  /** Token gecersizse oturumu temizleyip true doner. */
  async clearIfAuthError(err: unknown): Promise<boolean> {
    if (err instanceof ClickUpApiError && err.isAuthError) {
      await this.handleAuthFailure();
      return true;
    }
    return false;
  }

  dispose(): void {
    this.disposables.forEach((d) => d.dispose());
    this.disposables.length = 0;
  }
}
