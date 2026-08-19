import * as vscode from 'vscode';
import type { AuthService } from '../auth/authService';
import { ClickUpApi, type ClickUpTask } from '../clickup/api';

/**
 * Task agaci. Kok = atanmis task'lar, cocuk = sub task'lar.
 *
 * VERI SEKLI: ClickUp'tan subtasks=true ile TEK cagrida hem ust hem alt
 * task'lar duz bir liste olarak gelir; hiyerarsiyi `parent` alanindan
 * biz kurariz. Alternatif (her task icin ayri sub task cagrisi) N+1
 * istek demekti — 30 task'lik bir listede 31 cagri.
 */
export class TaskTreeProvider
  implements vscode.TreeDataProvider<TaskNode>, vscode.Disposable
{
  private readonly changed = new vscode.EventEmitter<TaskNode | undefined>();
  readonly onDidChangeTreeData = this.changed.event;

  private readonly api: ClickUpApi;

  /** taskId -> o task'in dogrudan cocuklari. Her refresh'te yeniden kurulur. */
  private childrenByParent = new Map<string, ClickUpTask[]>();
  /** Kok seviye task'lar (parent'i olmayan ya da parent'i listede olmayan). */
  private roots: ClickUpTask[] = [];
  /** taskId -> task. Detay/statu komutlari agaci taramadan erisir. */
  private readonly taskIndex = new Map<string, ClickUpTask>();

  /** Ayni anda tek yukleme; yeni refresh oncekini iptal eder. */
  private inFlight: AbortController | undefined;
  private loaded = false;
  private loadError: string | undefined;

  constructor(private readonly auth: AuthService) {
    this.api = new ClickUpApi(() => this.auth.getToken());
  }

  refresh(): void {
    this.loaded = false;
    this.loadError = undefined;
    // Devam eden istek varsa gercekten durdur — sonucu atmak yetmez.
    this.inFlight?.abort();
    this.inFlight = undefined;
    this.changed.fire(undefined);
  }

  getTreeItem(element: TaskNode): vscode.TreeItem {
    return element;
  }

  /** Komutlarin agaci taramadan task'a erismesi icin. */
  getTask(taskId: string): ClickUpTask | undefined {
    return this.taskIndex.get(taskId);
  }

  /**
   * Ilk ag cagrisi burada olur — aktivasyonda degil.
   * Giris yapilmamissa bos donulur; viewsWelcome token girisi baglantisini gosterir.
   */
  async getChildren(element?: TaskNode): Promise<TaskNode[]> {
    if (!(await this.auth.isSignedIn())) {
      return [];
    }

    if (element) {
      const children = this.childrenByParent.get(element.taskId) ?? [];
      return children.map((t) => this.toNode(t));
    }

    if (!this.loaded) {
      await this.load();
    }

    if (this.loadError) {
      return [TaskNode.forMessage(`Yuklenemedi: ${this.loadError}`)];
    }
    if (this.roots.length === 0) {
      return [TaskNode.forMessage('Size atanmis acik task yok.')];
    }
    return this.roots.map((t) => this.toNode(t));
  }

  private async load(): Promise<void> {
    const controller = new AbortController();
    this.inFlight = controller;

    try {
      const teamId = await this.resolveTeamId(controller.signal);
      if (!teamId) {
        this.loadError = 'Workspace (team) secilmedi.';
        this.loaded = true;
        return;
      }

      const user = await this.auth.getCurrentUser();
      if (!user) {
        this.loadError = 'Oturum bulunamadi.';
        this.loaded = true;
        return;
      }

      const tasks = await this.api.listAssignedTasks(teamId, user.id, controller.signal);
      this.index(tasks);
      this.loaded = true;
    } catch (err) {
      if (controller.signal.aborted) {
        return; // yeni bir refresh devrald: bu sonucu sessizce birak
      }
      if (await this.auth.clearIfAuthError(err)) {
        this.loadError = 'Token gecersiz.';
      } else {
        this.loadError = err instanceof Error ? err.message : String(err);
      }
      this.loaded = true;
    } finally {
      if (this.inFlight === controller) {
        this.inFlight = undefined;
      }
    }
  }

  /**
   * Duz task listesini kok/cocuk agacina cevirir.
   *
   * Yetim sub task onemli bir kenar durum: bir sub task atanmis ama
   * ust task'i BASKASINA atanmissa liste sub task'i icerir, ustunu
   * icermez. Onu gizlemek yerine kok seviyeye cikariyoruz — kullanici
   * kendine atanmis isi gormeli.
   */
  private index(tasks: ClickUpTask[]): void {
    this.childrenByParent = new Map();
    this.taskIndex.clear();
    for (const t of tasks) {
      this.taskIndex.set(t.id, t);
    }

    const roots: ClickUpTask[] = [];
    for (const t of tasks) {
      if (t.parent && this.taskIndex.has(t.parent)) {
        const siblings = this.childrenByParent.get(t.parent) ?? [];
        siblings.push(t);
        this.childrenByParent.set(t.parent, siblings);
      } else {
        roots.push(t);
      }
    }
    this.roots = roots;
  }

  /**
   * teamId once ayardan okunur (kullanim noktasinda, aktivasyonda
   * onbelleklenmez — ayar degisince yeniden okunsun). Bos ise
   * kullaniciya erisebildigi workspace'ler sorulur.
   */
  private async resolveTeamId(signal: AbortSignal): Promise<string | undefined> {
    const configured = vscode.workspace
      .getConfiguration('clickupPanel')
      .get<string>('teamId', '')
      .trim();
    if (configured) {
      return configured;
    }

    const teams = await this.api.listTeams(signal);
    if (teams.length === 0) {
      return undefined;
    }
    if (teams.length === 1) {
      return teams[0]?.id;
    }

    const picked = await vscode.window.showQuickPick(
      teams.map((t) => ({ label: t.name, description: t.id, teamId: t.id })),
      { title: 'ClickUp Workspace secin', ignoreFocusOut: true }
    );
    if (!picked) {
      return undefined;
    }

    // Secimi kalici kil, her acilista tekrar sorma.
    await vscode.workspace
      .getConfiguration('clickupPanel')
      .update('teamId', picked.teamId, vscode.ConfigurationTarget.Global);
    return picked.teamId;
  }

  private toNode(task: ClickUpTask): TaskNode {
    const hasChildren = (this.childrenByParent.get(task.id)?.length ?? 0) > 0;
    return TaskNode.forTask(task, hasChildren);
  }

  dispose(): void {
    this.inFlight?.abort();
    this.changed.dispose();
  }
}

export class TaskNode extends vscode.TreeItem {
  private constructor(
    readonly taskId: string,
    label: string,
    collapsibleState: vscode.TreeItemCollapsibleState
  ) {
    super(label, collapsibleState);
    if (taskId) {
      this.id = taskId;
    }
  }

  static forTask(task: ClickUpTask, hasChildren: boolean): TaskNode {
    const node = new TaskNode(
      task.id,
      task.name,
      hasChildren
        ? vscode.TreeItemCollapsibleState.Collapsed
        : vscode.TreeItemCollapsibleState.None
    );
    node.description = task.status.status;
    node.tooltip = buildTooltip(task);
    // contextValue menulerin hedefi: yalnizca gercek task'larda statu
    // degistirme eylemi gorunsun, mesaj satirlarinda gorunmesin.
    node.contextValue = 'clickupTask';
    node.iconPath = new vscode.ThemeIcon('circle-filled', statusColor(task.status.type));
    node.command = {
      command: 'clickupPanel.showTask',
      title: 'Task detayini goster',
      arguments: [task.id],
    };
    return node;
  }

  /** Bos liste / hata gibi durumlar icin tiklanamaz bilgi satiri. */
  static forMessage(text: string): TaskNode {
    const node = new TaskNode('', text, vscode.TreeItemCollapsibleState.None);
    node.contextValue = 'clickupMessage';
    return node;
  }
}

function buildTooltip(task: ClickUpTask): vscode.MarkdownString {
  const md = new vscode.MarkdownString();
  md.appendMarkdown(`**${escapeMarkdown(task.name)}**\n\n`);
  md.appendMarkdown(`Statu: ${escapeMarkdown(task.status.status)}\n\n`);
  if (task.list?.name) {
    md.appendMarkdown(`Liste: ${escapeMarkdown(task.list.name)}\n\n`);
  }
  md.appendMarkdown(`ID: \`${task.id}\``);
  return md;
}

/**
 * Task adi ClickUp'tan gelen kullanici icerigidir — Markdown olarak
 * yorumlanmamali. MarkdownString.isTrusted acilmadigi icin komut
 * calistirilamaz, ama yine de bicim bozulmasin diye kacisliyoruz.
 */
function escapeMarkdown(text: string): string {
  return text.replace(/[\\`*_{}[\]()#+\-.!|]/g, '\\$&');
}

function statusColor(type: string | undefined): vscode.ThemeColor {
  switch (type) {
    case 'closed':
      return new vscode.ThemeColor('charts.green');
    case 'open':
      return new vscode.ThemeColor('charts.blue');
    default:
      return new vscode.ThemeColor('charts.yellow');
  }
}
