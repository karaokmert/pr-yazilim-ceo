import * as assert from 'assert';
import * as fs from 'fs/promises';
import * as os from 'os';
import * as path from 'path';

import {
  AgentSession,
  formatDuration,
  isStale,
  scanSessions,
  silentMinutes,
  sortSessions,
} from '../sessions';

/**
 * VERI KATMANI TESTLERI.
 *
 * sessions.ts vscode namespace'ini import ETMEDIGI icin dogrudan cagrilabilir.
 * Gercek ~/.claude/sessions'a DOKUNULMAZ: her test sahte bir HOME kurar,
 * os.homedir() oraya yonlendirilir, test bitince geri alinir.
 *
 * NEDEN GERCEK VERIYE KARSI KOSMUYORUZ: gercek dizin her koseyi icermez
 * (bozuk JSON, olu PID, gelecege ait damga) ve her kosumda degisir —
 * test tekrarlanabilir olmaz.
 */

let tempHome: string;
let originalHome: string | undefined;

/**
 * Sahte HOME kurar.
 *
 * OLCULDU: os.homedir() salt-okunur bir getter — dogrudan atanamiyor
 * ("Cannot set property homedir"). Ama process.env.HOME degistirildiginde
 * os.homedir() yeni degeri donduruyor (bu makinede dogrulandi). Yonlendirme
 * bu yuzden env uzerinden yapilir.
 */
async function useFakeHome(): Promise<string> {
  tempHome = await fs.mkdtemp(path.join(os.tmpdir(), 'vsx-panel-test-'));
  originalHome = process.env.HOME;
  process.env.HOME = tempHome;
  const sessionsDir = path.join(tempHome, '.claude', 'sessions');
  await fs.mkdir(sessionsDir, { recursive: true });
  // Yonlendirmenin gercekten tuttugunu DOGRULA: tutmadiysa test gercek
  // ~/.claude/sessions'a karsi kosar ve yanlis bir guven uretir.
  assert.strictEqual(os.homedir(), tempHome, 'sahte HOME yonlendirmesi tutmadi');
  return sessionsDir;
}

async function restoreHome(): Promise<void> {
  if (originalHome === undefined) {
    delete process.env.HOME;
  } else {
    process.env.HOME = originalHome;
  }
  if (tempHome) {
    await fs.rm(tempHome, { recursive: true, force: true });
  }
}

/** Canli bir PID: kendi surecimiz. isProcessAlive(kendi pid) daima true. */
const LIVE_PID = process.pid;

/** Olu PID uretir: cok yuksek, kullanilmayan bir deger. */
const DEAD_PID = 4194303;

async function writeSession(dir: string, pid: number, body: unknown): Promise<void> {
  const content = typeof body === 'string' ? body : JSON.stringify(body);
  await fs.writeFile(path.join(dir, `${pid}.json`), content, 'utf8');
}

suite('sessions — tarama ve dogrulama', () => {
  let sessionsDir: string;

  setup(async () => {
    sessionsDir = await useFakeHome();
  });

  teardown(async () => {
    await restoreHome();
  });

  test('dizin yoksa "no-directory" doner, patlamaz', async () => {
    await fs.rm(path.join(tempHome, '.claude'), { recursive: true, force: true });
    const result = await scanSessions(Date.now());
    assert.strictEqual(result.kind, 'no-directory');
  });

  test('bos dizin: ok + sifir oturum', async () => {
    const result = await scanSessions(Date.now());
    assert.strictEqual(result.kind, 'ok');
    if (result.kind !== 'ok') { return; }
    assert.strictEqual(result.sessions.length, 0);
    assert.strictEqual(result.skipped, 0);
  });

  test('gecerli canli oturum okunur', async () => {
    const now = Date.now();
    await writeSession(sessionsDir, LIVE_PID, {
      pid: LIVE_PID,
      name: 'QA oturumu',
      agent: 'vscode-ext-qa-publisher',
      cwd: '/tmp',
      status: 'busy',
      startedAt: now - 600_000,
      updatedAt: now - 60_000,
    });

    const result = await scanSessions(now);
    assert.strictEqual(result.kind, 'ok');
    if (result.kind !== 'ok') { return; }
    assert.strictEqual(result.sessions.length, 1);
    assert.strictEqual(result.sessions[0].name, 'QA oturumu');
    assert.strictEqual(result.sessions[0].status, 'busy');
    assert.strictEqual(result.sessions[0].cwd, '/tmp');
  });

  test('TUZAK SETI: bozuk kayitlar elenir, hicbiri patlatmaz', async () => {
    const now = Date.now();
    // Gecerli olan tek kayit
    await writeSession(sessionsDir, LIVE_PID, { pid: LIVE_PID, name: 'saglam', updatedAt: now });
    // Bozuk JSON
    await writeSession(sessionsDir, 900001, '{ bozuk json');
    // null
    await writeSession(sessionsDir, 900002, 'null');
    // dizi (obje degil)
    await writeSession(sessionsDir, 900003, '[1,2,3]');
    // bos dosya
    await writeSession(sessionsDir, 900004, '');
    // olu PID
    await writeSession(sessionsDir, DEAD_PID, { pid: DEAD_PID, name: 'olu', updatedAt: now });
    // json olmayan dosya — hic aday sayilmamali
    await fs.writeFile(path.join(sessionsDir, 'notes.txt'), 'bu bir oturum degil', 'utf8');

    const result = await scanSessions(now);
    assert.strictEqual(result.kind, 'ok');
    if (result.kind !== 'ok') { return; }
    assert.strictEqual(result.sessions.length, 1, 'yalniz saglam kayit kalmali');
    assert.strictEqual(result.sessions[0].name, 'saglam');
    assert.ok(result.skipped >= 5, `elenen sayisi beklenenden az: ${result.skipped}`);
  });

  test('gelecege ait updatedAt elenir (negatif sessizlik uretmez)', async () => {
    const now = Date.now();
    await writeSession(sessionsDir, LIVE_PID, {
      pid: LIVE_PID,
      name: 'gelecekten',
      updatedAt: now + 3_600_000,
    });
    const result = await scanSessions(now);
    assert.strictEqual(result.kind, 'ok');
    if (result.kind !== 'ok') { return; }
    assert.strictEqual(result.sessions[0].updatedAt, undefined);
    assert.strictEqual(silentMinutes(result.sessions[0], now), undefined);
  });

  test('adi olmayan kayit PID etiketine duser, bos string olmaz', async () => {
    const now = Date.now();
    await writeSession(sessionsDir, LIVE_PID, { pid: LIVE_PID, name: '   ', updatedAt: now });
    const result = await scanSessions(now);
    assert.strictEqual(result.kind, 'ok');
    if (result.kind !== 'ok') { return; }
    assert.strictEqual(result.sessions[0].name, `PID ${LIVE_PID}`);
  });
});

suite('sessions — siralama ve sunum', () => {
  const now = Date.now();

  function session(over: Partial<AgentSession> & { pid: number }): AgentSession {
    return {
      name: `oturum-${over.pid}`,
      agent: undefined,
      cwd: undefined,
      status: undefined,
      startedAt: undefined,
      updatedAt: undefined,
      ...over,
    };
  }

  test('unutulmus oturum listenin BASINDA olur', () => {
    const taze = session({ pid: 1, name: 'taze', updatedAt: now - 60_000 });
    const unutulmus = session({ pid: 2, name: 'unutulmus', updatedAt: now - 20 * 60_000 });
    const sorted = sortSessions([taze, unutulmus], now, 15);
    assert.strictEqual(sorted[0].name, 'unutulmus');
  });

  test('iki unutulmus varsa en uzun sessiz olan once gelir', () => {
    const a = session({ pid: 1, name: 'a', updatedAt: now - 20 * 60_000 });
    const b = session({ pid: 2, name: 'b', updatedAt: now - 40 * 60_000 });
    const sorted = sortSessions([a, b], now, 15);
    assert.strictEqual(sorted[0].name, 'b');
  });

  test('damgasi olmayan oturum unutulmus SAYILMAZ', () => {
    const bilinmiyor = session({ pid: 1, name: 'bilinmiyor' });
    assert.strictEqual(isStale(bilinmiyor, now, 15), false);
  });

  test('esik degisince unutulmusluk degisir (ayar gercekten etkili)', () => {
    const s = session({ pid: 1, updatedAt: now - 10 * 60_000 });
    assert.strictEqual(isStale(s, now, 15), false, '15 dk esikte unutulmus degil');
    assert.strictEqual(isStale(s, now, 5), true, '5 dk esikte unutulmus');
  });

  test('sure bicimleri', () => {
    assert.strictEqual(formatDuration(0), 'az once');
    assert.strictEqual(formatDuration(12), '12 dk');
    assert.strictEqual(formatDuration(125), '2 sa 05 dk');
  });
});
