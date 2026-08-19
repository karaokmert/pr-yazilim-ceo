import * as fs from 'fs/promises';
import * as os from 'os';
import * as path from 'path';

/**
 * VERI KATMANI — ~/.claude/sessions/<PID>.json okuma ve dogrulama.
 *
 * Bu dosya vscode namespace'ini BILEREK ic ice almaz: saf veri katmani,
 * editorden bagimsiz test edilebilir kalir. VS Code'a bagli her sey
 * (TreeItem, ikon, komut) sessionTree.ts icindedir.
 *
 * NODE fs KULLANIMI BILINCLI: okunan dizin kullanicinin ev dizinidir,
 * calisma alani DEGILDIR — sanal/uzak dosya sistemi ihtimali yoktur ve
 * manifest zaten virtualWorkspaces=false, browser girdisi yok (masaustu hedef).
 * workspace.fs burada bir sey kazandirmaz, Node fs dogru aractir.
 */

/** sessions/<PID>.json dosyasinin ham sekli. Her alan opsiyoneldir:
 *  disk uzerindeki JSON bizim sozlesmemiz degil, baska bir surecin ciktisi. */
interface RawSessionFile {
  pid?: unknown;
  sessionId?: unknown;
  cwd?: unknown;
  startedAt?: unknown;
  version?: unknown;
  kind?: unknown;
  name?: unknown;
  agent?: unknown;
  updatedAt?: unknown;
  status?: unknown;
}

/** Ayristirilmis, dogrulanmis ve canli oldugu teyit edilmis oturum. */
export interface AgentSession {
  pid: number;
  /** Gorunen ad. Dosyada yoksa PID'e duser — asla bos string olmaz. */
  name: string;
  /** Agent tipi (ornek: vscode-ext-developer). Bilinmiyorsa undefined. */
  agent: string | undefined;
  /** Calisma dizini. Bilinmiyorsa undefined — "dizini ac" o zaman kapalidir. */
  cwd: string | undefined;
  /** busy | idle | bilinmiyorsa undefined. Dosyadan HAZIR gelir. */
  status: string | undefined;
  /** epoch ms. Gecersizse undefined — "kac dakikadir sessiz" hesaplanamaz. */
  startedAt: number | undefined;
  /** epoch ms. Gecersizse undefined. */
  updatedAt: number | undefined;
}

/** Okuma sonucu. Yokluk bir HATA DEGIL, normal bir durumdur —
 *  cagiran taraf anlamli bir bos-durum gosterebilsin diye ayirt edilir. */
export type SessionScan =
  | { kind: 'ok'; sessions: AgentSession[]; skipped: number }
  | { kind: 'no-directory'; directory: string }
  | { kind: 'unreadable'; directory: string; reason: string };

/** Oturum dosyalarinin bulundugu dizin. */
export function sessionsDirectory(): string {
  return path.join(os.homedir(), '.claude', 'sessions');
}

/**
 * Surecin gercekten yasadigini dogrular.
 *
 * KEMER + ASKI: dosyanin varligi surecin yasadigini KANITLAMAZ — cokmus bir
 * surecin dosyasi diskte kalir. signal 0 sinyal GONDERMEZ, yalnizca surecin
 * var olup olmadigini ve erisilebilirligini sinar.
 *
 * EPERM = surec YASIYOR ama baska kullaniciya ait; olu saymak yanlis olur.
 */
function isProcessAlive(pid: number): boolean {
  try {
    process.kill(pid, 0);
    return true;
  } catch (error) {
    return (error as NodeJS.ErrnoException)?.code === 'EPERM';
  }
}

/** Sonlu, pozitif bir sayi mi — NaN, Infinity ve string'i eler. */
function finitePositive(value: unknown): number | undefined {
  return typeof value === 'number' && Number.isFinite(value) && value > 0
    ? value
    : undefined;
}

/** Bos olmayan bir metin mi — bos string undefined'a duser. */
function nonEmptyString(value: unknown): string | undefined {
  if (typeof value !== 'string') {
    return undefined;
  }
  const trimmed = value.trim();
  return trimmed.length > 0 ? trimmed : undefined;
}

/**
 * Zaman damgasini dogrular ve GELECEK degerleri eler.
 *
 * OLCULDU: bozuk bir kayit sacma bir updatedAt tasiyabiliyor ve gecen sure
 * hesabi anlamsiz cikiyor (29 milyon dakika). Gelecege ait bir damga da
 * negatif sessizlik uretir; ikisi de undefined'a dusurulur.
 */
function timestamp(value: unknown, now: number): number | undefined {
  const parsed = finitePositive(value);
  if (parsed === undefined) {
    return undefined;
  }
  // Bir dakikalik saat kaymasi paylari birakilir.
  return parsed > now + 60_000 ? undefined : parsed;
}

/**
 * Tek bir dosyanin icerigini oturuma cevirir.
 * Gecerli degilse undefined doner — cagiran taraf onu SAYAR, patlamaz.
 */
function parseSession(raw: string, fallbackPid: number, now: number): AgentSession | undefined {
  let data: RawSessionFile;
  try {
    data = JSON.parse(raw) as RawSessionFile;
  } catch {
    return undefined;
  }

  if (data === null || typeof data !== 'object') {
    return undefined;
  }

  // PID dosya icinden okunur; yoksa dosya adindaki degere duser.
  const pid = finitePositive(data.pid) ?? fallbackPid;
  if (!Number.isInteger(pid)) {
    return undefined;
  }

  return {
    pid,
    name: nonEmptyString(data.name) ?? `PID ${pid}`,
    agent: nonEmptyString(data.agent),
    cwd: nonEmptyString(data.cwd),
    status: nonEmptyString(data.status),
    startedAt: timestamp(data.startedAt, now),
    updatedAt: timestamp(data.updatedAt, now),
  };
}

/**
 * Oturum dizinini tarar, bozuk kayitlari eler, olu surecleri suzer.
 *
 * `now` disaridan verilir: ayni tarama icindeki tum sessizlik hesaplari
 * tek bir ana gore yapilsin (ve test edilebilir kalsin).
 */
export async function scanSessions(now: number = Date.now()): Promise<SessionScan> {
  const directory = sessionsDirectory();

  let entries: string[];
  try {
    entries = await fs.readdir(directory);
  } catch (error) {
    const code = (error as NodeJS.ErrnoException)?.code;
    // YOKLUK NORMAL: dizin hic olusmamis olabilir.
    if (code === 'ENOENT') {
      return { kind: 'no-directory', directory };
    }
    return {
      kind: 'unreadable',
      directory,
      reason: code ?? (error instanceof Error ? error.message : String(error)),
    };
  }

  // Ayni dizinde .key dosyalari da var; yalniz <PID>.json alinir.
  const candidates = entries.filter((entry) => /^\d+\.json$/.test(entry));

  const results = await Promise.all(
    candidates.map(async (entry) => {
      const fallbackPid = Number.parseInt(entry, 10);
      try {
        const raw = await fs.readFile(path.join(directory, entry), 'utf8');
        return parseSession(raw, fallbackPid, now);
      } catch {
        // Tarama sirasinda silinmis ya da okunamayan dosya: sayilir, patlatmaz.
        return undefined;
      }
    })
  );

  // PID'e gore tekillestirilir: bir surece ait birden fazla dosya kalmis
  // olabilir (artik/bozuk kayit). OLCULDU: ayni oturum aksi halde listede
  // birden cok kez gorunuyor. En taze updatedAt kazanir.
  const byPid = new Map<number, AgentSession>();
  let skipped = 0;

  for (const session of results) {
    if (!session) {
      skipped += 1;
      continue;
    }
    // CANLILIK: dosya diskte kalabilir, surec olmus olabilir.
    if (!isProcessAlive(session.pid)) {
      skipped += 1;
      continue;
    }
    const existing = byPid.get(session.pid);
    if (existing) {
      skipped += 1;
      if ((existing.updatedAt ?? 0) >= (session.updatedAt ?? 0)) {
        continue;
      }
    }
    byPid.set(session.pid, session);
  }

  return { kind: 'ok', sessions: [...byPid.values()], skipped };
}

/** Son aktiviteden bu yana gecen dakika. Damga yoksa undefined. */
export function silentMinutes(session: AgentSession, now: number): number | undefined {
  if (session.updatedAt === undefined) {
    return undefined;
  }
  return Math.max(0, Math.floor((now - session.updatedAt) / 60_000));
}

/**
 * Oturum "unutulmus" mu — esikten uzun suredir sessiz mi.
 * Damga bilinmiyorsa unutulmus SAYILMAZ: bilmemek ile sessizlik ayni sey degil.
 */
export function isStale(session: AgentSession, now: number, thresholdMinutes: number): boolean {
  const minutes = silentMinutes(session, now);
  return minutes !== undefined && minutes >= thresholdMinutes;
}

/** Insan okunur sure: "az once", "12 dk", "2 sa 05 dk". */
export function formatDuration(totalMinutes: number): string {
  if (totalMinutes < 1) {
    return 'az once';
  }
  if (totalMinutes < 60) {
    return `${totalMinutes} dk`;
  }
  const hours = Math.floor(totalMinutes / 60);
  const minutes = totalMinutes % 60;
  return `${hours} sa ${String(minutes).padStart(2, '0')} dk`;
}

/**
 * Siralama — MERT'IN ONCELIGI: unutulmus oturum en ustte.
 * 1) Unutulmus olanlar once
 * 2) Icinde: en uzun sessiz olan once
 * 3) Esitse: ada gore (liste her taramada ayni sirada kalsin, zipilamasin)
 */
export function sortSessions(
  sessions: AgentSession[],
  now: number,
  thresholdMinutes: number
): AgentSession[] {
  return [...sessions].sort((a, b) => {
    const aStale = isStale(a, now, thresholdMinutes);
    const bStale = isStale(b, now, thresholdMinutes);
    if (aStale !== bStale) {
      return aStale ? -1 : 1;
    }
    const aSilent = silentMinutes(a, now) ?? -1;
    const bSilent = silentMinutes(b, now) ?? -1;
    if (aSilent !== bSilent) {
      return bSilent - aSilent;
    }
    return a.name.localeCompare(b.name, 'tr');
  });
}
