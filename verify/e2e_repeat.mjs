// Headless check of the repeat-study features: diagnosis retake, choice shuffling, practice modes, mock retake history,
// first+latest prediction, backup export/import, and the four resets (confirm dialogs are accepted automatically).
// Usage: node verify/e2e_repeat.mjs <chrome-headless-shell> <site url>
import { spawn } from 'node:child_process';
import { mkdirSync, mkdtempSync } from 'node:fs';
import { join } from 'node:path';

const [chrome, site] = process.argv.slice(2);
const base = 'C:/prie-lab/tmp/adsp_e2e'; mkdirSync(base, { recursive: true });
const port = 9338, sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const proc = spawn(chrome, ['--headless', `--remote-debugging-port=${port}`, '--host-resolver-rules=MAP gc.zgo.at 127.0.0.1', `--user-data-dir=${mkdtempSync(join(base, 'r-'))}`, 'about:blank'], { stdio: 'ignore' });
let t; for (let i = 0; i < 50; i++) { try { t = await (await fetch(`http://127.0.0.1:${port}/json`)).json(); break; } catch { await sleep(200); } }
const ws = new WebSocket(t.find((x) => x.type === 'page').webSocketDebuggerUrl); await new Promise((r) => ws.addEventListener('open', r));
let id = 0; const P = new Map(); const errors = []; const dialogs = [];
const send = (method, params = {}) => new Promise((r) => { const i = ++id; P.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
ws.addEventListener('message', (e) => { const m = JSON.parse(e.data); if (m.id && P.has(m.id)) { P.get(m.id)(m); P.delete(m.id); }
  if (m.method === 'Runtime.exceptionThrown') errors.push(m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text);
  if (m.method === 'Page.javascriptDialogOpening') { dialogs.push(m.params.message); send('Page.handleJavaScriptDialog', { accept: true }); } });
const ev = async (x) => { const r = await send('Runtime.evaluate', { expression: x, awaitPromise: true, returnByValue: true }); if (r.result?.exceptionDetails) throw new Error(r.result.exceptionDetails.exception?.description); return r.result?.result?.value; };
const go = async (h, w = 1200) => { await send('Page.navigate', { url: site + h }); await sleep(w); };
const R = {}; const ok = (k, v) => { R[k] = v; };
await send('Runtime.enable'); await send('Page.enable');
await send('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 1, mobile: true });
await go('#/', 2500);

// 1) diagnosis twice -> different question sets
const diag = async () => { await go('#/', 600); await go('#/diagnose'); await ev(`document.getElementById('go').click(); true`); await sleep(300); const ids = [];
  for (let k = 0; k < 10; k++) { ids.push(await ev(`QS.find((q) => q.q === document.querySelector('.qtext').textContent && [...document.querySelectorAll('.choice span:last-child')].map((e) => e.textContent).sort().join('|') === q.choices.slice().sort().join('|'))?.id`));
    await ev(`document.querySelector('.choice').click(); true`); await sleep(80); await ev(`document.getElementById('next').click(); true`); await sleep(120); }
  return ids; };
const d1 = await diag(), d2 = await diag();
ok('diagRetakeOverlap', d1.filter((x) => d2.includes(x)).length + ' of 10 repeated');

// 2) shuffling: displayed order differs from stored order for some questions; off -> identity
await go('#/practice/3/%EC%A0%84%EC%B2%B4');
let shuffled = 0;
for (let k = 0; k < 8; k++) { shuffled += await ev(`[...document.querySelectorAll('.choice')].map((b) => b.dataset.k).join('') !== '0123' ? 1 : 0`);
  await ev(`document.querySelector('.choice').click(); true`); await sleep(60); await ev(`document.getElementById('next').click(); true`); await sleep(80); }
ok('shuffledOf8', shuffled);
ok('explainNumberMatchesScreen', await ev(`(async () => { location.hash = '#/practice/3/%EC%A0%84%EC%B2%B4'; await new Promise((r) => setTimeout(r, 600));
  const q = QS.find((x) => x.q === document.querySelector('.qtext').textContent && [...document.querySelectorAll('.choice span:last-child')].map((e) => e.textContent).sort().join('|') === x.choices.slice().sort().join('|'));
  document.querySelector('.choice').click(); await new Promise((r) => setTimeout(r, 100));
  const shownPos = [...document.querySelectorAll('.choice')].findIndex((b) => b.classList.contains('right'));
  return document.querySelector('.explain .res').textContent.includes('정답 ' + '①②③④'[shownPos]); })()`));
await go('#/settings'); await ev(`document.getElementById('st-shuffle').click(); true`); await sleep(300);
await go('#/practice/2/%EC%A0%84%EC%B2%B4');
ok('shuffleOffIdentity', await ev(`[...document.querySelectorAll('.choice')].map((b) => b.dataset.k).join('') === '0123'`));
await go('#/settings'); await ev(`document.getElementById('st-shuffle').click(); true`); await sleep(300);
ok('shuffleBackOn', await ev(`JSON.parse(localStorage.getItem('adsp:v1')).shuffle !== false`));

// 3) practice modes
await go('#/practice/3');
ok('modeChips', await ev(`[...document.querySelectorAll('[data-pmode]')].map((b) => b.textContent)`));
await ev(`document.querySelector('[data-pmode="wrong"]').click(); true`); await sleep(400);
await ev(`document.querySelector('#app a.btn.primary').click(); true`); await sleep(500);
ok('wrongModeOnlyWrong', await ev(`(() => { const db = JSON.parse(localStorage.getItem('adsp:v1')); const q = QS.find((x) => x.q === document.querySelector('.qtext').textContent && [...document.querySelectorAll('.choice span:last-child')].map((e) => e.textContent).sort().join('|') === x.choices.slice().sort().join('|')); return !!db.wrong[q.id]; })()`));
await go('#/practice/3'); await ev(`document.querySelector('[data-pmode="all"]').click(); true`); await sleep(300);

// 4) mock retake: two sittings of m1 -> history "1회차 → 2회차"
for (let n = 0; n < 2; n++) {
  await go('#/', 600); await go('#/mock/m1', 1500);
  for (let k = 0; k < 3 + 3 * n; k++) { await ev(`document.querySelector('.choice').click(); true`); await sleep(60); }
  await ev(`document.getElementById('submit').click(); true`); await sleep(500);
}
await go('#/mock');
ok('mockHistory', await ev(`document.querySelector('#app .card p.small').textContent`));
ok('mockRetakeButton', await ev(`document.querySelector('#app .card a.btn').textContent`));

// 5) prediction: a question first wrong then right counts 0.5, not 1
ok('firstPlusLatest', await ev(`(() => { const saved = JSON.stringify(DB); const q = QS.find((x) => x.subject === 1);
  DB.attempts = [{ id: q.id, s: 1, ok: false, t: 1 }, { id: q.id, s: 1, ok: true, t: 2 }, { id: q.id, s: 1, ok: true, t: 3 }];
  const sc = questionScores(1); DB = JSON.parse(saved); return sc.length + ' question, score ' + sc[0].score; })()`));

// 6) backup export -> reset all -> import restores
await go('#/', 500); await go('#/settings');
const before = await ev(`JSON.parse(localStorage.getItem('adsp:v1')).attempts.length`);
const file = await ev(`(async () => { let url = null; const orig = HTMLAnchorElement.prototype.click;
  HTMLAnchorElement.prototype.click = function () { if (this.download) url = this.href; else orig.call(this); };
  document.getElementById('st-export').click(); HTMLAnchorElement.prototype.click = orig; return await (await fetch(url)).text(); })()`);
ok('exportParsed', JSON.parse(file).data.attempts.length === before);
await ev(`document.getElementById('st-all').click(); true`); await sleep(400);
ok('afterResetAll', await ev(`JSON.parse(localStorage.getItem('adsp:v1')).attempts.length`));
await go('#/', 500); await go('#/settings');
await ev(`(() => { const dt = new DataTransfer(); dt.items.add(new File([${JSON.stringify(file)}], 'backup.json', { type: 'application/json' }));
  const inp = document.getElementById('st-import'); inp.files = dt.files; inp.dispatchEvent(new Event('change')); return true; })()`); await sleep(800);
ok('afterImport', `${await ev(`JSON.parse(localStorage.getItem('adsp:v1')).attempts.length`)} (before ${before})`);

// 7) targeted resets
await go('#/', 500); await go('#/settings');
await ev(`document.querySelector('[data-reset-m="m1"]').click(); true`); await sleep(400);
ok('mockResetM1', await ev(`(() => { const db = JSON.parse(localStorage.getItem('adsp:v1')); return db.mocks.filter((m) => m.id === 'm1').length + ' mocks, ' + db.attempts.filter((a) => a.mid === 'm1').length + ' attempts'; })()`));
await go('#/', 500); await go('#/settings');
await ev(`document.querySelector('[data-reset-s="3"]').click(); true`); await sleep(400);
ok('subject3Reset', await ev(`(() => { const db = JSON.parse(localStorage.getItem('adsp:v1')); return db.attempts.filter((a) => a.s === 3).length + ' left in s3, ' + db.attempts.filter((a) => a.s !== 3).length + ' in other subjects'; })()`));
await go('#/', 500); await go('#/settings');
await ev(`document.getElementById('st-wrong').click(); true`); await sleep(400);
ok('wrongCleared', await ev(`Object.keys(JSON.parse(localStorage.getItem('adsp:v1')).wrong).length`));

// 8) progress map rounds
await go('#/map');
ok('mapRounds', await ev(`document.querySelector('.maprow span').innerText.replace(/\\n/g, ' | ')`));
ok('confirmDialogs', dialogs.length);
ok('errors', errors);
console.log(JSON.stringify(R, null, 1));
ws.close(); proc.kill(); process.exit(errors.length ? 1 : 0);
