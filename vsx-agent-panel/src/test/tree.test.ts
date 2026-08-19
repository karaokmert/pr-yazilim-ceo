import * as assert from 'assert';
import * as vscode from 'vscode';

import { AgentSession } from '../sessions';
import {
  Node,
  SessionTreeProvider,
  UNKNOWN_PROJECT_LABEL,
  displayName,
  groupDescription,
  groupSessions,
} from '../sessionTree';

/**
 * SUNUM KATMANI TESTLERI (v0.2 bilgi mimarisi).
 *
 * Uc riski karsilar, ucu de OLCULMUS:
 *  1) Ad ayristirma - acik yedi oturumun %29'u kaliba UYMUYOR ve biri
 *     BOZUK (bos tarih alani + kacak tirnak). Ayristirma tutmazsa ham ad
 *     OLDUGU GIBI gosterilmeli; kacak tirnak SILINMEMELI (ariza gorunur
 *     kalsin - sunum katmani onu gizlerse kimse duzeltmez).
 *  2) cwd'si olmayan oturum ayri bir gruba dusmeli, kaybolmamali.
 *  3) Grup basligi sayimi - unutulmus YOKKEN "unutulmus" ibaresi HIC
 *     gecmemeli (yanlis alarm), varken gecmeli (gruplama unutulmusu
 *     GOMMEMELI kisitinin karsiligi).
 */

const NOW = Date.now();
const THRESHOLD = 15;

function session(over: Partial<AgentSession> & { pid: number }): AgentSession {
  return {
    name: `oturum-${over.pid}`,
    agent: undefined,
    cwd: undefined,
    status: undefined,
    startedAt: undefined,
    updatedAt: NOW - 60_000,
    ...over,
  };
}

suite('sunum - ad ayristirma', () => {
  test('kalip TUTAN adlarda yalniz rol kalir', () => {
    assert.strictEqual(displayName('VSX · Architect - 0818-21:24 - skill-project'), 'VSX · Architect');
    assert.strictEqual(displayName('OY · TE - 0818-21:10 - osinif'), 'OY · TE');
  });

  test('kalip TUTMAYAN ad KIRPILMAZ, oldugu gibi kalir', () => {
    assert.strictEqual(displayName('Agent generator'), 'Agent generator');
  });

  test('BOZUK ad TEMIZLENMEZ - yalniz uzunluktan kirpilir', () => {
    // OLCULDU: bu gercek bir oturum adi. Tarih alani bos, sonda kacak tirnak.
    // v0.2'de bu test "ham haliyle korunur" diyordu; v0.3'te uzunluk kirpmasi
    // eklendi ve bu ad 41 karakter (sinir 32) oldugu icin KIRPILIYOR.
    // DEGISMEYEN sey: hicbir KARAKTER TEMIZLIGI yapilmiyor - kacak tirnak
    // silinmiyor, bos tarih alani kapatilmiyor. Kirpma arizayi gizlemez,
    // yalniz satiri kisaltir; tam ad tooltip'te durur.
    const bozuk = 'Clara · CEO Asistani -  - pr-yazilim-ceo"';
    const label = displayName(bozuk);

    // Bozuk kismin GORUNEN parcasi aynen duruyor: cift tire ve bos tarih alani.
    assert.ok(label.startsWith('Clara · CEO Asistani -  -'), 'bozuk yapi degistirilmis');
    // Kirpilmis ama TEMIZLENMEMIS.
    assert.ok(label.endsWith('\u2026'), 'uzun ad kirpilmamis');
    assert.ok(label.length <= 32);
  });

  test('TEK normalizasyon trim; ic bosluk ve isaretler korunur', () => {
    assert.strictEqual(displayName('  bosluklu ad  '), 'bosluklu ad');
  });

  test('rol BOSSA ham ada duser (kalip tutsa bile)', () => {
    // Bastaki tire disinda rol yok; sadelestirme bos etiket URETEMEZ.
    const label = displayName(' - 0818-21:24 - dizin');
    assert.ok(label.length > 0, 'bos etiket uretildi');
    assert.strictEqual(label, '- 0818-21:24 - dizin');
  });

  test('veri katmaninin PID yedegi bozulmadan gecer', () => {
    assert.strictEqual(displayName('PID 4242'), 'PID 4242');
  });
});

suite('sunum - etiket kirpma', () => {
  /**
   * SINIR OLCULDU: acik oturumlarin ayristirilmis rollerinin en uzunu 15
   * karakter, ham ada dusenlerin en uzunu 41 (bozuk ad). Sinir 32 secildi -
   * 40 secilseydi 41 karakterlik ad tek karakter kirpilir, satir kisalmaz,
   * yalniz cirkinlesirdi.
   */
  const LIMIT = 32;

  test('sinirin ALTINDAKI etiket dokunulmadan gecer', () => {
    const kisa = 'a'.repeat(LIMIT - 1);
    assert.strictEqual(displayName(kisa), kisa);
  });

  test('sinira TAM ESIT etiket kirpilmaz', () => {
    const tam = 'a'.repeat(LIMIT);
    assert.strictEqual(displayName(tam), tam);
  });

  test('siniri ASAN etiket kirpilir ve isaret alir', () => {
    const uzun = 'a'.repeat(LIMIT + 20);
    const label = displayName(uzun);
    assert.strictEqual(label.length, LIMIT, 'kirpilmis etiket siniri asiyor');
    assert.ok(label.endsWith('\u2026'), 'kirpma isareti yok');
  });

  test('KISA ozel ad kirpilmaz (elle adlandirilmis oturum)', () => {
    // 'Agent generator' = 15 karakter; kirpma bu vakaya DOKUNMAMALI.
    assert.strictEqual(displayName('Agent generator'), 'Agent generator');
  });

  test('AYRISTIRILAN rol kirpmadan once cikarilir', () => {
    // Ham ad 44 karakter (sinirin uzerinde) ama rol 15 - kirpma devreye
    // girmemeli. Sira yanlis olsaydi "VSX · Architect - 0818-21..." kirpilirdi.
    const label = displayName('VSX · Architect - 0818-21:24 - skill-project');
    assert.strictEqual(label, 'VSX · Architect');
    assert.ok(!label.endsWith('\u2026'), 'ayristirilan rol gereksiz yere kirpilmis');
  });

  test('BOZUK uzun ad kirpilir ama tooltip icin ham hali degismez', () => {
    const bozuk = 'Clara · CEO Asistani -  - pr-yazilim-ceo"';
    const label = displayName(bozuk);
    assert.ok(label.length <= LIMIT, 'bozuk ad kirpilmamis');
    assert.ok(label.endsWith('\u2026'));
    // displayName GIRDIYI degistirmez; ham ad cagirana ait ve tooltip'e
    // oradan gider (asagidaki tooltip testi bunu ayrica dogrular).
    assert.strictEqual(bozuk, 'Clara · CEO Asistani -  - pr-yazilim-ceo"');
  });

  test('kirpma sonunda bosluk birakmaz', () => {
    const label = displayName('kelime kelime kelime kelime kelime kelime');
    assert.ok(!/\s\u2026$/.test(label), 'kirpma isaretinden once bosluk kalmis');
  });
});

suite('sunum - gruplama', () => {
  test('oturumlar cwd EKSENINDE gruplanir (ad ekseninde DEGIL)', () => {
    const groups = groupSessions(
      [
        session({ pid: 1, cwd: '/a/proje-bir' }),
        session({ pid: 2, cwd: '/a/proje-bir' }),
        session({ pid: 3, cwd: '/b/proje-iki' }),
      ],
      NOW,
      THRESHOLD
    );
    assert.strictEqual(groups.length, 2);
    const labels = groups.map((g) => g.label).sort();
    assert.deepStrictEqual(labels, ['proje-bir', 'proje-iki']);
  });

  test('cwd YOKSA "(dizin bilinmiyor)" grubuna duser, KAYBOLMAZ', () => {
    const groups = groupSessions(
      [session({ pid: 1, cwd: undefined }), session({ pid: 2, cwd: '/a/proje' })],
      NOW,
      THRESHOLD
    );
    const unknown = groups.find((g) => g.label === UNKNOWN_PROJECT_LABEL);
    assert.ok(unknown, 'bilinmeyen dizin grubu olusmadi');
    assert.strictEqual(unknown!.sessions.length, 1);
    assert.strictEqual(unknown!.cwd, undefined);
  });

  test('grup ETIKETI yolun son klasoru olur, tam yol tooltip icin saklanir', () => {
    const [group] = groupSessions([session({ pid: 1, cwd: '/x/y/derin/proje' })], NOW, THRESHOLD);
    assert.strictEqual(group.label, 'proje');
    assert.strictEqual(group.cwd, '/x/y/derin/proje');
  });

  test('GRUP ICI siralama korunur: unutulmus ustte', () => {
    const [group] = groupSessions(
      [
        session({ pid: 1, name: 'taze', cwd: '/p', updatedAt: NOW - 60_000 }),
        session({ pid: 2, name: 'unutulmus', cwd: '/p', updatedAt: NOW - 40 * 60_000 }),
      ],
      NOW,
      THRESHOLD
    );
    assert.strictEqual(group.sessions[0].name, 'unutulmus');
  });

  test('GRUPLAR ARASI siralama: unutulmus TASIYAN grup once', () => {
    const groups = groupSessions(
      [
        session({ pid: 1, cwd: '/temiz', updatedAt: NOW - 60_000 }),
        session({ pid: 2, cwd: '/unutulmus-olan', updatedAt: NOW - 40 * 60_000 }),
      ],
      NOW,
      THRESHOLD
    );
    assert.strictEqual(groups[0].label, 'unutulmus-olan');
  });

  test('iki grupta da unutulmus varsa en uzun sessiz olan grup once', () => {
    const groups = groupSessions(
      [
        session({ pid: 1, cwd: '/yirmi', updatedAt: NOW - 20 * 60_000 }),
        session({ pid: 2, cwd: '/kirk', updatedAt: NOW - 40 * 60_000 }),
      ],
      NOW,
      THRESHOLD
    );
    assert.strictEqual(groups[0].label, 'kirk');
  });
});

suite('sunum - grup basligi sayimi', () => {
  test('unutulmus YOKKEN "unutulmus" ibaresi HIC gecmez', () => {
    const text = groupDescription(3, 0);
    assert.strictEqual(text, '3 oturum');
    assert.ok(!text.includes('unutulmus'), 'yanlis alarm: unutulmus yokken yaziyor');
  });

  test('unutulmus VARKEN sayisiyla birlikte gecer', () => {
    assert.strictEqual(groupDescription(3, 1), '3 oturum · 1 unutulmus');
  });

  test('tek oturumlu grup da normal grup gibi sayilir (ozel durum YOK)', () => {
    assert.strictEqual(groupDescription(1, 0), '1 oturum');
  });
});

suite('sunum - agac kademeleri', () => {
  let output: vscode.OutputChannel;
  let provider: SessionTreeProvider;

  setup(() => {
    output = vscode.window.createOutputChannel('agac-testi');
    provider = new SessionTreeProvider(output);
  });

  teardown(() => {
    provider.dispose();
    output.dispose();
  });

  test('tarama YAPILMADAN kokte tek bir MESAJ dugumu bulunur', () => {
    const roots = provider.getChildren();
    assert.strictEqual(roots.length, 1);
    assert.strictEqual(roots[0].kind, 'message');
  });

  test('MESAJ dugumleri KOKTE kalir, gruba girmez', () => {
    const roots = provider.getChildren();
    const message = roots[0];
    // Mesaj dugumunun cocugu OLMAMALI.
    assert.deepStrictEqual(provider.getChildren(message), []);
  });

  test('grup dugumu TreeItem uretebilir ve acik baslar', () => {
    const [group] = groupSessions([session({ pid: 1, cwd: '/p/proje' })], NOW, THRESHOLD);
    const node: Node = { kind: 'project', group };
    const item = provider.getTreeItem(node);
    assert.strictEqual(item.label, 'proje');
    assert.strictEqual(
      item.collapsibleState,
      vscode.TreeItemCollapsibleState.Expanded,
      'gruplar varsayilan olarak ACIK baslamali'
    );
    assert.strictEqual(item.contextValue, 'vsxAgentPanel.project');
  });

  test('grup dugumunun COCUKLARI o grubun oturumlaridir', () => {
    const [group] = groupSessions(
      [session({ pid: 1, cwd: '/p' }), session({ pid: 2, cwd: '/p' })],
      NOW,
      THRESHOLD
    );
    const children = provider.getChildren({ kind: 'project', group });
    assert.strictEqual(children.length, 2);
    assert.ok(children.every((c) => c.kind === 'session'));
  });

  test('oturum satirinda DIZIN YOK, yalniz sessizlik var', () => {
    const s = session({
      pid: 1,
      name: 'VSX · QA - 0818-21:24 - skill-project',
      cwd: '/Users/x/skill-project',
      updatedAt: NOW - 22 * 60_000,
    });
    const item = provider.getTreeItem({ kind: 'session', session: s });

    assert.strictEqual(item.label, 'VSX · QA', 'label sade rol olmali');
    const description = String(item.description);
    assert.strictEqual(description, '22 dk', 'description yalniz sessizlik olmali');
    assert.ok(!description.includes('skill-project'), 'dizin satirda tekrar ediyor');
  });

  test('tooltip HAM ADI tasir (kisaltilan ad sistemde aranabilsin)', () => {
    const ham = 'VSX · QA - 0818-21:24 - skill-project';
    const s = session({ pid: 1, name: ham, cwd: '/p' });
    const item = provider.getTreeItem({ kind: 'session', session: s });
    const tooltip = item.tooltip as vscode.MarkdownString;
    assert.ok(tooltip.value.includes('Ham ad'), 'tooltip ham ad satiri tasimiyor');
    // Kacislar nedeniyle birebir arama yapilmaz; ayirt edici parca aranir.
    assert.ok(tooltip.value.includes('0818'), 'ham addaki tarih tooltip\'te yok');
  });

  test('KIRPILAN ad tooltip\'te EKSIKSIZ durur (kirpma orada uygulanmaz)', () => {
    const bozuk = 'Clara · CEO Asistani -  - pr-yazilim-ceo"';
    const s = session({ pid: 1, name: bozuk, cwd: '/p' });
    const item = provider.getTreeItem({ kind: 'session', session: s });

    // Satir kirpilmis olmali...
    assert.ok(String(item.label).endsWith('\u2026'), 'satir etiketi kirpilmamis');

    // ...ama tooltip tam adi tasimali: kirpilan kuyruk ('yazilim-ceo')
    // ve kacak tirnak orada gorunmeli.
    const tooltip = item.tooltip as vscode.MarkdownString;
    // Kirpilan kuyruk ('yazilim-ceo') ve kacak tirnak tooltip'te GORUNMELI.
    assert.ok(tooltip.value.includes('yazilim'), 'kirpilan kuyruk tooltip\'te yok');
    // Tooltip BASLIGI da kirpilmamali - kopru orada kuruluyor.
    const baslik = tooltip.value.split('\n')[0];
    assert.ok(!baslik.includes('\u2026'), 'tooltip basligi kirpilmis - kopru koptu');
  });

  test('sessizligi BILINMEYEN oturum "sessizlik bilinmiyor" gosterir', () => {
    const s = session({ pid: 1, updatedAt: undefined });
    const item = provider.getTreeItem({ kind: 'session', session: s });
    assert.strictEqual(String(item.description), 'sessizlik bilinmiyor');
  });

  test('dizini OLMAYAN oturum farkli contextValue tasir (menu gizlensin)', () => {
    const s = session({ pid: 1, cwd: undefined });
    const item = provider.getTreeItem({ kind: 'session', session: s });
    assert.strictEqual(item.contextValue, 'vsxAgentPanel.sessionNoFolder');
    assert.strictEqual(item.command, undefined, 'dizini yokken tiklama komutu olmamali');
  });
});
