// Headless end-to-end check at phone size (390x844) using the Chrome DevTools Protocol directly.
// Usage: node verify/e2e.mjs <chrome-headless-shell path> <site url> <screenshot dir>
// Blocks gc.zgo.at so test visits are never counted.
import { spawn } from 'node:child_process';
import { mkdirSync, writeFileSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const [chrome, site, outDir] = process.argv.slice(2);
mkdirSync(outDir, { recursive: true });
const port = 9333;
const proc = spawn(chrome, [
  '--headless', '--disable-gpu', `--remote-debugging-port=${port}`, '--window-size=390,844',
  '--host-resolver-rules=MAP gc.zgo.at 127.0.0.1', `--user-data-dir=${mkdtempSync(join(tmpdir(), 'adsp-e2e-'))}`, 'about:blank',
], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

let targets;
for (let i = 0; i < 50; i++) { try { targets = await (await fetch(`http://127.0.0.1:${port}/json`)).json(); break; } catch { await sleep(200); } }
const page = targets.find((t) => t.type === 'page');
const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener('open', r));
let id = 0; const pending = new Map(); const errors = [];
ws.addEventListener('message', (ev) => {
  const m = JSON.parse(ev.data);
  if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
  if (m.method === 'Runtime.exceptionThrown') errors.push(m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text);
});
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const ev = async (expr) => (await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true })).result?.result?.value;
const shot = async (name) => { const r = await send('Page.captureScreenshot', { format: 'png' }); writeFileSync(join(outDir, name), Buffer.from(r.result.data, 'base64')); };

await send('Runtime.enable'); await send('Page.enable');
await send('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 1, mobile: true });
await send('Network.enable');
await send('Network.setUserAgentOverride', { userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1' });
const results = {};
const go = async (hash) => { await send('Page.navigate', { url: `${site}${hash}` }); await sleep(2500); };

// home: measure time until the first screen is rendered
const t0 = Date.now(); await send('Page.navigate', { url: `${site}#/` });
for (let i = 0; i < 100 && !(await ev(`!!document.querySelector('#app h1')`)); i++) await sleep(100);
results.firstRenderMs = Date.now() - t0;
await ev(`window.__ev = []; window.goatcounter = { count: (o) => window.__ev.push(o.path) }; true`);
results.homeButton = await ev(`!!document.querySelector('a[href="#/diagnose"]')`);
await ev(`document.getElementById('installClose')?.click(); true`);
await shot('e2e_1_home.png');

// diagnosis: start, answer 10 questions (always the first choice), then result
await go('#/diagnose');
await ev(`document.getElementById('go').click(); true`);
await sleep(400);
results.subjects = [];
for (let k = 0; k < 10; k++) {
  results.subjects.push(await ev(`document.querySelector('.tag')?.textContent.slice(0, 3)`));
  if (k === 0) await shot('e2e_2_question.png');
  await ev(`document.querySelector('.choice').click(); true`); await sleep(150);
  await ev(`document.getElementById('next').click(); true`); await sleep(250);
}
results.resultTitle = await ev(`document.querySelector('h1')?.textContent`);
results.resultScore = await ev(`document.querySelector('.score')?.textContent`);
results.resultNote = await ev(`document.querySelector('.card .small b')?.textContent`);
await shot('e2e_3_result.png');
// story card: capture the generated image instead of downloading
results.card = await ev(`(async () => { let url = null; const orig = HTMLAnchorElement.prototype.click;
  HTMLAnchorElement.prototype.click = function () { if (this.download) url = this.href; else orig.call(this); };
  document.getElementById('share').click(); await new Promise((r) => setTimeout(r, 1500));
  HTMLAnchorElement.prototype.click = orig;
  if (!url) return null; const img = new Image(); img.src = url; await img.decode(); return { w: img.width, h: img.height, url }; })()`);
if (results.card?.url) { writeFileSync(join(outDir, 'e2e_4_card.png'), Buffer.from(results.card.url.split(',')[1], 'base64')); results.card = `${results.card.w}x${results.card.h}`; }

// mock list, then mock 3 starts with timer and 50 cells; report-click tracking
await go('#/mock');
results.mockList = await ev(`[...document.querySelectorAll('#app .card b')].map((b) => b.textContent)`);
await go('#/practice/1/%EC%A0%84%EC%B2%B4');
await ev(`document.querySelector('.choice').click(); true`); await sleep(200);
await ev(`(() => { const a = document.querySelector('[data-track="report_click"]'); a.removeAttribute('href'); a.click(); return true; })()`);
await go('#/mock/m3');
results.mockCells = await ev(`document.querySelectorAll('.palette button').length`);
results.mockTimer = await ev(`document.getElementById('timer')?.textContent`);
await shot('e2e_5_mock.png');
await ev(`window.confirm = () => true; document.getElementById('submit').click(); true`); await sleep(500);
results.mockResult = await ev(`document.querySelector('.score')?.textContent + ' / ' + document.querySelector('.card p b')?.textContent`);
await shot('e2e_6_mock_result.png');

// study pages, review queue, difficulty feedback, survey
results.pages = {};
for (const h of ['#/freq', '#/compare', '#/formulas', '#/d7', '#/map', '#/review', '#/survey', '#/verify', '#/notes/3']) {
  await go(h, 1200);
  results.pages[h] = await ev(`(document.querySelector('#app h1')?.textContent || 'NO H1') + ' | ' + document.querySelectorAll('#app table tr, #app li, #app .maprow').length`);
}
await go('#/practice/2/%EC%A0%84%EC%B2%B4');
await ev(`document.querySelector('.choice').click(); true`); await sleep(200);
await ev(`document.querySelector('[data-diff="hard"]').click(); true`); await sleep(100);
results.diffDisabled = await ev(`[...document.querySelectorAll('[data-diff]')].every((b) => b.disabled)`);
results.srsCount = await ev(`Object.keys(JSON.parse(localStorage.getItem('adsp:v1')).srs || {}).length`);

// share preview tags
results.events = await ev(`window.__ev`);
results.og = await ev(`['og:title','og:description','og:image'].map((p) => document.querySelector('meta[property="' + p + '"]')?.content)`);
results.errors = errors;
console.log(JSON.stringify(results, null, 1));
ws.close(); proc.kill();
process.exit(errors.length ? 1 : 0);
