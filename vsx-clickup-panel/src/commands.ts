import * as vscode from 'vscode';
import type { AuthService } from './auth/authService';
import { ClickUpApi, type ClickUpTask } from './clickup/api';
import type { TaskNode, TaskTreeProvider } from './views/taskTree';

/** QuickPick ogesi + secilen statuyu tasiyan alan. */
interface StatusPick extends vscode.QuickPickItem {
  status: string;
}

/**
 * Komut kayitlari. contributes.commands ile bu dosya TEK bir
 * is birimidir — birine ekleyip digerini unutmak sessiz arizadir.
 */
export function registerCommands(
  context: vscode.ExtensionContext,
  auth: AuthService,
  taskTree: TaskTreeProvider
): void {
  const api = new ClickUpApi(() => auth.getToken());

  const register = (id: string, handler: (...args: never[]) => unknown): void => {
    context.subscriptions.push(
      vscode.commands.registerCommand(id, async (...args: never[]) => {
        try {
          await handler(...args);
        } catch (err) {
          // Token gecersizse oturum temizlenir ve kullaniciya ayri mesaj gider;
          // ikinci bir hata balonu gostermeye gerek yok.
          if (await auth.clearIfAuthError(err)) {
            taskTree.refresh();
            return;
          }
          void vscode.window.showErrorMessage(
            `ClickUp: ${err instanceof Error ? err.message : String(err)}`
          );
        }
      })
    );
  };

  register('clickupPanel.signIn', async () => {
    await auth.signIn();
  });

  register('clickupPanel.signOut', async () => {
    await auth.signOut();
    void vscode.window.showInformationMessage('ClickUp oturumu kapatildi.');
  });

  register('clickupPanel.refresh', () => {
    taskTree.refresh();
  });

  /**
   * Task detayi. Salt-okunur bir Markdown belgesi olarak acilir.
   *
   * API SECIMI: webview yerine sanal belge. Detay statik metin —
   * webview bir tarayici baglami, CSP yonetimi ve mesaj koprusu
   * getirirdi; karsiliginda hicbir sey kazanmiyorduk. Markdown
   * onizlemesi editorun kendi yeteneklerini (arama, kopyalama,
   * tema uyumu) bedavaya verir.
   */
  register('clickupPanel.showTask', async (taskIdOrNode?: string | TaskNode) => {
    const taskId = resolveTaskId(taskIdOrNode);
    if (!taskId) {
      return;
    }

    const task = await vscode.window.withProgress(
      { location: vscode.ProgressLocation.Window, title: 'ClickUp task yukleniyor...' },
      () => api.getTask(taskId)
    );

    const doc = await vscode.workspace.openTextDocument({
      content: renderTaskMarkdown(task),
      language: 'markdown',
    });
    await vscode.window.showTextDocument(doc, { preview: true });
  });

  /**
   * Statu degistirme.
   *
   * Statuler task'in bagli oldugu LISTEDEN okunur — ClickUp rastgele
   * string kabul etmez. Kullaniciya serbest metin yazdirmak yerine
   * gecerli secenekleri sunuyoruz; yanlis statu 400 ile geri donerdi.
   */
  register('clickupPanel.changeStatus', async (nodeOrId?: TaskNode | string) => {
    const taskId = resolveTaskId(nodeOrId);
    if (!taskId) {
      void vscode.window.showInformationMessage('Once bir task secin.');
      return;
    }

    // Liste bilgisi agactaki kayitta yoksa detay cagrisi ile alinir.
    let task = taskTree.getTask(taskId);
    if (!task?.list?.id) {
      task = await api.getTask(taskId);
    }
    const listId = task.list?.id;
    if (!listId) {
      throw new Error('Task’in bagli oldugu liste bulunamadi, statu degistirilemiyor.');
    }

    const statuses = await vscode.window.withProgress(
      { location: vscode.ProgressLocation.Window, title: 'Statuler yukleniyor...' },
      () => api.listStatuses(listId)
    );
    if (statuses.length === 0) {
      throw new Error('Bu listede tanimli statu bulunamadi.');
    }

    const current = task.status.status;
    const items: StatusPick[] = statuses.map((s) => {
      const item: StatusPick = { label: s.status, status: s.status };
      // exactOptionalPropertyTypes: alani undefined ATAMAK yerine hic koymuyoruz.
      if (s.status.toLowerCase() === current.toLowerCase()) {
        item.description = '(mevcut)';
      }
      return item;
    });

    const picked = await vscode.window.showQuickPick<StatusPick>(items, {
      title: `Statu sec — ${task.name}`,
      ignoreFocusOut: true,
    });
    if (!picked) {
      return; // ESC: iptal, hata degil
    }
    if (picked.status.toLowerCase() === current.toLowerCase()) {
      return; // degisiklik yok, gereksiz PUT atma
    }

    await vscode.window.withProgress(
      { location: vscode.ProgressLocation.Notification, title: `Statu guncelleniyor: ${picked.status}` },
      () => api.updateTaskStatus(taskId, picked.status)
    );

    taskTree.refresh();
    void vscode.window.showInformationMessage(`Statu guncellendi: ${picked.status}`);
  });
}

/**
 * Komut hem agac ogesinden (menu) hem de string id ile (tree item command)
 * cagrilabilir. Ikisini de kabul et — bir komutun neden cagrildigina dair
 * varsayim yapmak, palet uzerinden calistirildiginda patlayan koddur.
 */
function resolveTaskId(input: unknown): string | undefined {
  if (typeof input === 'string' && input) {
    return input;
  }
  if (input && typeof input === 'object' && 'taskId' in input) {
    const id = (input as { taskId: unknown }).taskId;
    return typeof id === 'string' && id ? id : undefined;
  }
  return undefined;
}

function renderTaskMarkdown(task: ClickUpTask): string {
  const lines: string[] = [`# ${task.name}`, ''];
  lines.push(`- **Statu:** ${task.status.status}`);
  if (task.list?.name) {
    lines.push(`- **Liste:** ${task.list.name}`);
  }
  if (task.priority?.priority) {
    lines.push(`- **Oncelik:** ${task.priority.priority}`);
  }
  if (task.assignees?.length) {
    lines.push(`- **Atananlar:** ${task.assignees.map((a) => a.username).join(', ')}`);
  }
  if (task.due_date) {
    lines.push(`- **Bitis:** ${formatEpoch(task.due_date)}`);
  }
  lines.push(`- **ID:** \`${task.id}\``);
  lines.push(`- **ClickUp:** ${task.url}`);
  lines.push('');
  lines.push('---');
  lines.push('');
  lines.push(task.description?.trim() ? task.description : '_Aciklama yok._');
  return lines.join('\n');
}

/** ClickUp tarihleri epoch-ms'i STRING olarak doner. */
function formatEpoch(value: string): string {
  const ms = Number(value);
  if (!Number.isFinite(ms)) {
    return value;
  }
  return new Date(ms).toLocaleString();
}
