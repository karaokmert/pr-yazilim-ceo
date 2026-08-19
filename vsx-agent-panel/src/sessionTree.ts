import * as path from 'path';
import * as vscode from 'vscode';
import {
  AgentSession,
  SessionScan,
  formatDuration,
  isStale,
  scanSessions,
  sessionsDirectory,
  silentMinutes,
  sortSessions,
} from './sessions';

/**
 * AGAC KATMANI - veriyi VS Code'un gorebilecegi hale cevirir.
 *
 * Veri okuma/dogrulama sessions.ts'te; burada yalniz SUNUM ve TAZELEME var.
 * Ad ayristirma da BURADADIR: bir sunum kararidir, veri katmani saf kalir.
 *
 * BILGI MIMARISI (Architect karari, v0.2):
 *   KADEME 1  proje grubu - eksen cwd (ad DEGIL: ad %29 kaliba uymuyor)
 *   KADEME 2  oturum satiri - label=rol, description=sessizlik, tooltip=tumu
 * Dizin satirdan CIKTI: grup basliginda duruyor; ayni bilgiyi iki kez
 * gostermek satiri sisiren seydi.
 *
 * TAZELEME NEDEN IKI KAYNAKLI:
 *  - Dosya izleyici: bir agent mesaj aldiginda sessions/*.json yazilir.
 *  - Periyodik yoklama: "22 dakikadir sessiz" bilgisi HICBIR DOSYA
 *    DEGISMEDEN eskir. Izleyici tek basina yeterli degildir.
 */

const CONFIG_SECTION = 'vsxAgentPanel';

/** cwd'si olmayan oturumlarin toplandigi grup. */
export const UNKNOWN_PROJECT_LABEL = '(dizin bilinmiyor)';

/**
 * Oturum adi kalibi: <rol> - <DDMM-SS:DD> - <dizin>
 * Ornek: "VSX . Architect - 0818-21:24 - skill-project"
 */
const NAME_PATTERN = /^(.+?)\s+-\s+\d{4}-\d{2}:\d{2}\s+-\s+.+$/;

/**
 * Satir etiketi icin ust sinir.
 *
 * SAYI OLCULDU, secilmedi: acik oturumlarin ayristirilmis rollerinin en
 * uzunu 15 karakter ("VSX · Architect"), ham ada dusenlerin en uzunu 41
 * ("Clara · CEO Asistani -  - pr-yazilim-ceo" - bozuk ad).
 *
 * 40 yerine 32: 40 secilseydi o 41 karakterlik ad tek karakter kirpilip
 * "..." eklenecekti - satir KISALMAZ, yalniz cirkinlesirdi. 32, roller icin
 * fazlasiyla genis (en uzunun iki kati) ama bozuk/uzun ham adi gercekten
 * kisaltir. Kirpma pratikte YALNIZ ham ada dusen vakalarda devreye girer.
 */
const MAX_LABEL_LENGTH = 32;

/** Kirpma isareti; tek karakterlik ellipsis satirda bir yer tutar. */
const ELLIPSIS = '\u2026';

/**
 * Satirda gosterilecek sade adi uretir.
 *
 * SIRA: once ayristir, tutmazsa ham ada dus, EN SON uzunluga bak.
 * Kirpma en sonda yapilir - once rol cikarilmaya calisilir, cunku
 * ayristirma basarili oldugunda kirpmaya zaten gerek kalmaz.
 *
 * UC KADEMELI YEDEK - hepsi HAM ADA duser:
 *   a) kalip tutmuyorsa            -> ham ad
 *   b) kalip tutuyor ama rol bossa -> ham ad
 *   c) ad zaten yoksa              -> veri katmaninin yedegi ("PID <n>")
 *
 * TEK NORMALIZASYON trim'dir. Baska hicbir temizlik YAPILMAZ - ozellikle
 * kacak tirnak SILINMEZ: o bir veri arizasinin gorunur izidir. Sunum
 * katmani onu gizlerse ariza kaybolur ve kimse duzeltmez. Panelin isi
 * gercegi gostermek, guzellestirmek degil.
 *
 * KIRPMA ARIZAYI GIZLEMEZ, yalniz satiri kisaltir: tam ad tooltip'te
 * ("Ham ad" satiri) EKSIKSIZ durur ve orada KIRPILMAZ.
 */
export function displayName(rawName: string): string {
  const raw = rawName.trim();
  const match = NAME_PATTERN.exec(raw);
  const role = match ? match[1].trim() : '';
  const label = role.length > 0 ? role : raw;
  return truncateLabel(label);
}

/**
 * Etiketi ust sinira kirpar. Sinirin altindaki her sey OLDUGU GIBI kalir -
 * bu yuzden ayristirilmis roller ve kisa ozel adlar ("Agent generator")
 * hic etkilenmez.
 */
function truncateLabel(label: string): string {
  if (label.length <= MAX_LABEL_LENGTH) {
    return label;
  }
  // Kirpilan yerde bosluk kalirsa "abc ..." gibi gorunur; sagdan trim edilir.
  return label.slice(0, MAX_LABEL_LENGTH - 1).trimEnd() + ELLIPSIS;
}

/** Grup basliginda gosterilecek kisa proje adi (yolun son klasoru). */
function projectLabel(cwd: string | undefined): string {
  if (!cwd) {
    return UNKNOWN_PROJECT_LABEL;
  }
  const base = path.basename(cwd);
  return base.length > 0 ? base : cwd;
}

/** Bir proje grubu - ayni cwd'yi paylasan oturumlar. */
export interface ProjectGroup {
  /** Gruplama anahtari: tam cwd, ya da cwd yoksa sabit bir isaret. */
  key: string;
  label: string;
  /** Tam yol; bilinmiyorsa undefined. */
  cwd: string | undefined;
  sessions: AgentSession[];
}

/** Agactaki bir dugum. */
export type Node =
  | { kind: 'project'; group: ProjectGroup }
  | { kind: 'session'; session: AgentSession }
  | { kind: 'message'; label: string; detail?: string; icon?: vscode.ThemeIcon };

/**
 * Oturumlari cwd'ye gore gruplar ve GRUPLARI siralar.
 *
 * Grup siralamasi grup ici siralamayla AYNI onceligi izler
 * (unutulmus > sessizlik > ad): iki kademe farkli davransaydi liste
 * ogrenilmesi gereken iki ayri sisteme donerdi.
 */
export function groupSessions(
  sessions: AgentSession[],
  now: number,
  thresholdMinutes: number
): ProjectGroup[] {
  const groups = new Map<string, ProjectGroup>();

  for (const session of sessions) {
    const key = session.cwd ?? ' unknown';
    let group = groups.get(key);
    if (!group) {
      group = {
        key,
        label: projectLabel(session.cwd),
        cwd: session.cwd,
        sessions: [],
      };
      groups.set(key, group);
    }
    group.sessions.push(session);
  }

  // Grup ici: mevcut sortSessions AYNEN kullanilir (fonksiyona dokunulmaz).
  for (const group of groups.values()) {
    group.sessions = sortSessions(group.sessions, now, thresholdMinutes);
  }

  const staleCount = (group: ProjectGroup): number =>
    group.sessions.filter((s) => isStale(s, now, thresholdMinutes)).length;

  const longestSilence = (group: ProjectGroup): number =>
    group.sessions.reduce((max, s) => Math.max(max, silentMinutes(s, now) ?? -1), -1);

  return [...groups.values()].sort((a, b) => {
    const aStale = staleCount(a) > 0;
    const bStale = staleCount(b) > 0;
    if (aStale !== bStale) {
      return aStale ? -1 : 1;
    }
    const aSilent = longestSilence(a);
    const bSilent = longestSilence(b);
    if (aSilent !== bSilent) {
      return bSilent - aSilent;
    }
    return a.label.localeCompare(b.label, 'tr');
  });
}

/**
 * Grup basligi aciklamasi: "3 oturum . 1 unutulmus".
 * Unutulmus YOKSA "unutulmus" ibaresi HIC gecmez.
 */
export function groupDescription(sessionCount: number, staleCount: number): string {
  const base = `${sessionCount} oturum`;
  return staleCount > 0 ? `${base} · ${staleCount} unutulmus` : base;
}

export class SessionTreeProvider implements vscode.TreeDataProvider<Node> {
  private readonly emitter = new vscode.EventEmitter<Node | undefined>();
  readonly onDidChangeTreeData = this.emitter.event;

  /** Son tarama. getChildren senkron kalsin diye burada tutulur. */
  private scan: SessionScan | undefined;
  /** Tum satirlar tek bir ana gore hesaplansin diye taramada dondurulur. */
  private scannedAt = Date.now();
  private disposed = false;

  /** Rozet guncellemesi icin gorunum; kurulum sonrasi baglanir. */
  private view: vscode.TreeView<Node> | undefined;

  constructor(private readonly output: vscode.OutputChannel) {}

  /** Rozeti guncelleyebilmek icin gorunumu baglar. */
  attachView(view: vscode.TreeView<Node>): void {
    this.view = view;
    this.updateBadge();
  }

  /** Diski yeniden okur ve agaci tazeler. Cakisan cagrilar zararsizdir. */
  async refresh(): Promise<void> {
    if (this.disposed) {
      return;
    }
    const now = Date.now();
    const scan = await scanSessions(now);
    if (this.disposed) {
      return;
    }
    this.scan = scan;
    this.scannedAt = now;
    if (scan.kind === 'unreadable') {
      this.output.appendLine(`Oturum dizini okunamadi (${scan.reason}): ${scan.directory}`);
    }
    this.updateBadge();
    this.emitter.fire(undefined);
  }

  /**
   * Yalniz gecen sureyi tazeler - diski OKUMAZ.
   * Periyodik yoklamanin ucuz yolu: dosyalar degismese de "12 dk"
   * etiketinin "13 dk" olmasi gerekir. Rozet de eskir (bir oturum
   * hicbir dosya degismeden esigi asabilir).
   */
  refreshElapsed(): void {
    if (this.disposed || this.scan === undefined) {
      return;
    }
    this.updateBadge();
    this.emitter.fire(undefined);
  }

  /**
   * Kenar cubugu rozeti = unutulmus oturum sayisi.
   *
   * NEDEN ROZET: rozet PANEL KAPALIYKEN de gorunur. Asil aranan bilgi
   * ("hangi oturum unutulmus") boylece paneli acmadan fark edilir.
   */
  private updateBadge(): void {
    if (!this.view) {
      return;
    }
    const count = this.staleCount();
    this.view.badge =
      count > 0 ? { value: count, tooltip: `${count} oturum unutulmus` } : undefined;
  }

  private staleCount(): number {
    if (this.scan?.kind !== 'ok') {
      return 0;
    }
    const threshold = this.staleThresholdMinutes();
    const now = Date.now();
    return this.scan.sessions.filter((s) => isStale(s, now, threshold)).length;
  }

  getTreeItem(node: Node): vscode.TreeItem {
    if (node.kind === 'message') {
      const item = new vscode.TreeItem(node.label, vscode.TreeItemCollapsibleState.None);
      item.tooltip = node.detail;
      item.iconPath = node.icon;
      item.contextValue = 'vsxAgentPanel.message';
      return item;
    }

    if (node.kind === 'project') {
      return this.projectTreeItem(node.group);
    }

    return this.sessionTreeItem(node);
  }

  private projectTreeItem(group: ProjectGroup): vscode.TreeItem {
    const now = Date.now();
    const threshold = this.staleThresholdMinutes();
    const staleCount = group.sessions.filter((s) => isStale(s, now, threshold)).length;

    // Gruplar VARSAYILAN OLARAK ACIK; tek oturumlu proje icin ozel durum YOK.
    // Sabit yapi akilli yapidan iyidir: aksi halde ayni proje bir oturumla
    // duz satir, ikincisi acilinca grup altina kayar ve goz her taramada
    // yeniden yer arar.
    const item = new vscode.TreeItem(group.label, vscode.TreeItemCollapsibleState.Expanded);
    item.description = groupDescription(group.sessions.length, staleCount);
    item.tooltip = group.cwd ?? 'Bu oturumlarin calisma dizini bilinmiyor.';
    item.contextValue = 'vsxAgentPanel.project';

    // Grup KAPALI olsa bile basligi unutulmus tasidigini soyler -
    // "gruplama unutulmusu GOMMEMELI" kisitinin karsiligi budur.
    item.iconPath =
      staleCount > 0
        ? new vscode.ThemeIcon('warning', new vscode.ThemeColor('list.warningForeground'))
        : new vscode.ThemeIcon('folder');

    // Grup dugumu de id tasir: agac tazelenince acik/kapali hali korunur.
    item.id = `project:${group.key}`;
    return item;
  }

  private sessionTreeItem(node: { kind: 'session'; session: AgentSession }): vscode.TreeItem {
    const { session } = node;
    const now = Date.now();
    const minutes = silentMinutes(session, now);
    const stale = isStale(session, now, this.staleThresholdMinutes());

    // label = SADE ROL (ayristirma tutmazsa ham ad)
    const item = new vscode.TreeItem(
      displayName(session.name),
      vscode.TreeItemCollapsibleState.None
    );

    // description = YALNIZ sessizlik. Dizin buradan CIKTI (grup basliginda).
    item.description = minutes === undefined ? 'sessizlik bilinmiyor' : formatDuration(minutes);

    item.tooltip = buildTooltip(session, now, stale);
    item.iconPath = statusIcon(session, stale);

    // contextValue: menu when-cumleleri buna dayanir; dizini olmayan
    // oturumda "dizini ac" gosterilmemeli.
    item.contextValue = session.cwd ? 'vsxAgentPanel.session' : 'vsxAgentPanel.sessionNoFolder';

    if (session.cwd) {
      item.command = {
        command: 'vsxAgentPanel.openFolder',
        title: 'Oturum Dizinini Ac',
        arguments: [node],
      };
    }

    return item;
  }

  getChildren(element?: Node): Node[] {
    // KADEME 2: bir grubun oturumlari.
    if (element) {
      if (element.kind === 'project') {
        return element.group.sessions.map((session) => ({ kind: 'session' as const, session }));
      }
      return [];
    }

    // KADEME 1: kok. Mesaj dugumleri KOKTE kalir, gruba girmez.
    const scan = this.scan;
    if (scan === undefined) {
      return [
        { kind: 'message', label: 'Yukleniyor...', icon: new vscode.ThemeIcon('loading~spin') },
      ];
    }

    if (scan.kind === 'no-directory') {
      return [
        {
          kind: 'message',
          label: 'Oturum kaydi bulunamadi.',
          detail: `Beklenen dizin: ${scan.directory}\nClaude Code oturumu acildiginda bu dizin olusur.`,
          icon: new vscode.ThemeIcon('info'),
        },
      ];
    }

    if (scan.kind === 'unreadable') {
      return [
        {
          kind: 'message',
          label: 'Oturum dizini okunamadi.',
          detail: `${scan.directory}\nSebep: ${scan.reason}`,
          icon: new vscode.ThemeIcon('warning'),
        },
      ];
    }

    if (scan.sessions.length === 0) {
      const detail =
        scan.skipped > 0
          ? `${scan.skipped} kayit elendi (surec kapanmis ya da dosya bozuk).`
          : 'Su anda acik bir Claude Code oturumu yok.';
      return [
        {
          kind: 'message',
          label: 'Acik oturum yok.',
          detail,
          icon: new vscode.ThemeIcon('circle-slash'),
        },
      ];
    }

    const groups = groupSessions(scan.sessions, this.scannedAt, this.staleThresholdMinutes());
    return groups.map((group) => ({ kind: 'project' as const, group }));
  }

  private staleThresholdMinutes(): number {
    // Aktivasyonda ONBELLEKLENMEZ: kullanici ayari degistirdiginde
    // yeniden yukleme beklemeden etkili olsun.
    const value = vscode.workspace
      .getConfiguration(CONFIG_SECTION)
      .get<number>('staleThresholdMinutes', 15);
    return Number.isFinite(value) && value > 0 ? value : 15;
  }

  dispose(): void {
    this.disposed = true;
    this.view = undefined;
    this.emitter.dispose();
  }
}

function buildTooltip(session: AgentSession, now: number, stale: boolean): vscode.MarkdownString {
  const md = new vscode.MarkdownString();
  // TOOLTIP BASLIGI KIRPILMAZ: tooltip, satirdaki kisaltilmis ad ile
  // sistemdeki gercek ad arasindaki KOPRUDUR. Burada da kirpsaydik
  // kopru koparadi - tam ad hicbir yerde gorunmezdi.
  md.appendMarkdown(`**${escapeMarkdown(session.name.trim())}**\n\n`);

  const rows: Array<[string, string]> = [];
  rows.push(['Durum', session.status ?? 'bilinmiyor']);

  const silent = silentMinutes(session, now);
  rows.push([
    'Son aktivite',
    silent === undefined ? 'bilinmiyor' : `${formatDuration(silent)} once`,
  ]);

  if (session.startedAt !== undefined) {
    const open = Math.max(0, Math.floor((now - session.startedAt) / 60_000));
    rows.push(['Acik suresi', formatDuration(open)]);
  }
  if (session.agent) {
    rows.push(['Agent tipi', session.agent]);
  }
  if (session.cwd) {
    rows.push(['Dizin', session.cwd]);
  }
  rows.push(['PID', String(session.pid)]);

  // HAM AD HER ZAMAN gosterilir - label kisaldiginda kullanicinin gordugu ad
  // ile sistemdeki gercek ad ayrisir; bu satir olmadan biri bir oturumu
  // ararken eslestiremez.
  rows.push(['Ham ad', session.name]);

  for (const [label, value] of rows) {
    md.appendMarkdown(`- ${label}: ${escapeMarkdown(value)}\n`);
  }

  if (stale) {
    md.appendMarkdown('\n$(warning) Uzun suredir sessiz - unutulmus olabilir.');
    md.supportThemeIcons = true;
  }
  return md;
}

/**
 * Ikon secimi. RENK ONCELIGI unutulmusluktadir: aranan bilgi
 * "kim calisiyor" degil, "kim unutulmus".
 */
function statusIcon(session: AgentSession, stale: boolean): vscode.ThemeIcon {
  if (stale) {
    return new vscode.ThemeIcon('warning', new vscode.ThemeColor('list.warningForeground'));
  }
  if (session.status === 'busy') {
    return new vscode.ThemeIcon('sync~spin', new vscode.ThemeColor('charts.blue'));
  }
  if (session.status === 'idle') {
    return new vscode.ThemeIcon('circle-filled', new vscode.ThemeColor('charts.green'));
  }
  return new vscode.ThemeIcon('question');
}

function escapeMarkdown(text: string): string {
  return text.replace(/([\\`*_{}[\]()#+\-.!|])/g, '\\$1');
}

/**
 * Izleyici + periyodik yoklamayi kurar ve TEK bir Disposable dondurur.
 *
 * setInterval Disposable DEGILDIR - sarmalanmazsa eklenti kapandiginda
 * calismaya devam eder. Paylasilan host'ta bu bir sizintidir.
 */
export function startAutoRefresh(
  provider: SessionTreeProvider,
  output: vscode.OutputChannel
): vscode.Disposable {
  const disposables: vscode.Disposable[] = [];

  // 1) Dosya izleyici - bir oturum yazildiginda aninda haber verir.
  const pattern = new vscode.RelativePattern(vscode.Uri.file(sessionsDirectory()), '*.json');
  const watcher = vscode.workspace.createFileSystemWatcher(pattern);
  disposables.push(watcher);

  // Izleyici cok siklikla tetiklenir; her olayda disk okumak israftir.
  let debounce: NodeJS.Timeout | undefined;
  const onChange = (): void => {
    if (debounce) {
      clearTimeout(debounce);
    }
    debounce = setTimeout(() => {
      debounce = undefined;
      void provider.refresh();
    }, 250);
  };
  disposables.push(watcher.onDidChange(onChange));
  disposables.push(watcher.onDidCreate(onChange));
  disposables.push(watcher.onDidDelete(onChange));
  disposables.push({
    dispose: () => {
      if (debounce) {
        clearTimeout(debounce);
        debounce = undefined;
      }
    },
  });

  // 2) Periyodik yoklama - gecen sure hicbir dosya degismeden eskir.
  let timer: NodeJS.Timeout | undefined;
  let pollTick = 0;

  const readInterval = (): number => {
    const value = vscode.workspace
      .getConfiguration(CONFIG_SECTION)
      .get<number>('refreshIntervalSeconds', 5);
    return Number.isFinite(value) && value >= 1 ? Math.min(value, 60) : 5;
  };

  const startTimer = (): void => {
    const seconds = readInterval();
    timer = setInterval(() => {
      pollTick += 1;
      // Her turda etiketleri tazele (ucuz, disk yok).
      provider.refreshElapsed();
      // Yaklasik 30 saniyede bir diski da oku: izleyicinin kacirdigi
      // durumlar (surec cokmesi - dosya degismez, surec olur) icin.
      if (pollTick * seconds >= 30) {
        pollTick = 0;
        void provider.refresh();
      }
    }, seconds * 1000);
  };

  startTimer();

  // Ayar degisince zamanlayici YENIDEN kurulur; yoksa kullanici degeri
  // degistirir ve hicbir sey olmaz (yeniden yukleyene kadar).
  disposables.push(
    vscode.workspace.onDidChangeConfiguration((event) => {
      if (event.affectsConfiguration(`${CONFIG_SECTION}.refreshIntervalSeconds`)) {
        if (timer) {
          clearInterval(timer);
        }
        pollTick = 0;
        startTimer();
        output.appendLine(`Tazeleme araligi guncellendi: ${readInterval()} sn.`);
      }
      if (event.affectsConfiguration(`${CONFIG_SECTION}.staleThresholdMinutes`)) {
        provider.refreshElapsed();
      }
    })
  );

  // setInterval'i Disposable'a sarmala.
  disposables.push({
    dispose: () => {
      if (timer) {
        clearInterval(timer);
        timer = undefined;
      }
    },
  });

  return vscode.Disposable.from(...disposables);
}

/**
 * Bir agac dugumunden dizin cikarir. Komut palet uzerinden argumansiz da
 * cagrilabilir - o yuzden her sekil savunulur.
 */
export function folderFromNode(node: unknown): string | undefined {
  if (typeof node === 'string') {
    return node.trim().length > 0 ? node : undefined;
  }
  if (node && typeof node === 'object' && 'kind' in node) {
    const candidate = node as Node;
    if (candidate.kind === 'session') {
      return candidate.session.cwd;
    }
    // Grup basligindan da dizin acilabilmeli.
    if (candidate.kind === 'project') {
      return candidate.group.cwd;
    }
  }
  return undefined;
}
