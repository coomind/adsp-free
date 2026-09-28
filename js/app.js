'use strict';
// ADsP free practice — static SPA. All user data stays in this browser (localStorage).

const CFG = {
  repo: 'coomind/adsp-free',
  site: 'coomind.github.io/adsp-free',
  insta: 'https://www.instagram.com/prie.note/',
};
const KEY = 'adsp:v1';
const $ = (s, el = document) => el.querySelector(s);
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const NUM = ['①', '②', '③', '④', '⑤'];

// ---------- storage ----------
const store = {
  load() {
    try { return Object.assign({ attempts: [], wrong: {}, mocks: [], theme: null, banner: false }, JSON.parse(localStorage.getItem(KEY) || '{}')); }
    catch { return { attempts: [], wrong: {}, mocks: [], theme: null, banner: false }; }
  },
  save(d) { try { localStorage.setItem(KEY, JSON.stringify(d)); } catch { /* private mode: keep in memory */ } },
};
let DB = store.load();
const save = () => store.save(DB);

// ---------- data ----------
let EXAM, QS = [], QMAP = {}, NOTES = {};
async function getJSON(u) { const r = await fetch(u); if (!r.ok) throw new Error(u); return r.json(); }
async function loadData() {
  EXAM = await getJSON('data/exam.json');
  for (const s of EXAM.subjects) {
    try { const qs = await getJSON(`data/questions/s${s.id}.json`); QS.push(...qs); } catch { /* subject not ready yet */ }
  }
  QS.forEach((q) => (QMAP[q.id] = q));
}
const subj = (id) => EXAM.subjects.find((s) => s.id === +id);
const itemName = (iid) => {
  for (const s of EXAM.subjects) for (const it of s.items) for (const sub of it.subs) if (sub.id === iid) return `${s.name} › ${it.name} › ${sub.name}`;
  return iid;
};
const daysLeft = () => {
  const [y, m, d] = EXAM.examDate.split('-').map(Number);
  const now = new Date(); const t = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  return Math.round((new Date(y, m - 1, d) - t) / 86400000);
};
const ddayText = () => { const n = daysLeft(); return n > 0 ? `D-${n}` : n === 0 ? 'D-DAY' : `시험 종료`; };

// ---------- events (GoatCounter; event name only, no personal data) ----------
function track(name) {
  try { if (window.goatcounter && window.goatcounter.count) window.goatcounter.count({ path: `event/${name}`, title: name, event: true }); } catch { /* ignore */ }
}

// ---------- records ----------
function record(q, pick, mode) {
  const ok = pick === q.answer;
  DB.attempts.push({ id: q.id, s: q.subject, ok, t: Date.now(), m: mode });
  if (!ok) DB.wrong[q.id] = Date.now(); else if (mode === 'wrong') delete DB.wrong[q.id];
  save();
  return ok;
}
const solvedSet = (s) => new Set(DB.attempts.filter((a) => a.s === s).map((a) => a.id));

// ---------- router ----------
const routes = [];
const route = (re, fn) => routes.push([re, fn]);
async function render() {
  const h = location.hash.slice(1) || '/';
  const tab = h.split('/')[1] || 'home';
  document.querySelectorAll('.tabbar a').forEach((a) => a.classList.toggle('on', a.dataset.tab === (tab === '' ? 'home' : tab) || (tab === 'today' && a.dataset.tab === 'practice') || (tab === 'wrong' && a.dataset.tab === 'practice')));
  stopTimer();
  // hash routes are invisible to GoatCounter's automatic count, so report each view (skips localhost by default)
  // (the first page load is counted by count.js itself)
  if (render.seen && window.goatcounter && window.goatcounter.count) window.goatcounter.count({ path: location.pathname + location.hash });
  render.seen = true;
  for (const [re, fn] of routes) { const m = h.match(re); if (m) { const app = $('#app'); app.innerHTML = ''; await fn(app, ...m.slice(1)); app.focus({ preventScroll: true }); window.scrollTo(0, 0); return; } }
  location.hash = '#/';
}

// ---------- home ----------
route(/^\/$/, (app) => {
  const wrongN = Object.keys(DB.wrong).length;
  app.innerHTML = `
  <p class="row"><span class="label beta">베타</span><span class="label">자체 제작 예상문제</span></p>
  <div class="card beta-card"><b>베타 공개 중이에요.</b> 틀린 문제를 찾으면 문제 아래 <b>⚑ 오류 신고</b>를 눌러 주세요. 반영되면 원하는 분은 <a href="#/testers">베타 테스터 명단</a>에 이름을 올려 드려요. <a href="#/verify">문제 검증 방법 보기</a></div>
  <h1>ADsP ${esc(EXAM.round)} 대비<br>무료 문제풀이</h1>
  <div class="card"><div class="row" style="justify-content:space-between">
    <div><div class="dday">${ddayText()}</div><div class="small">시험 ${esc(EXAM.schedule.exam)} · 접수 ${esc(EXAM.schedule.apply)}</div></div>
  </div></div>
  <a class="btn primary block" href="#/diagnose">10문제로 지금 합격 가능성 진단</a>
  <p class="small" style="margin:6px 0 12px">실제 시험 비율(1과목 2 · 2과목 2 · 3과목 6)로 10문제를 풀면 바로 예상 점수 범위를 보여줘요.</p>
  <a class="btn block" href="#/today">오늘의 10문제</a>
  <h2>과목별 진도</h2>
  ${EXAM.subjects.map((s) => {
    const total = QS.filter((q) => q.subject === s.id).length; const done = solvedSet(s.id).size;
    const pct = total ? Math.round((done / total) * 100) : 0;
    return `<div class="card"><div class="row" style="justify-content:space-between"><b>${s.id}과목 ${esc(s.name)}</b><span class="small">${done}/${total}문제</span></div>
      <div class="bar" style="margin:10px 0 12px"><i style="width:${pct}%"></i></div>
      <div class="row"><a class="chip" href="#/notes/${s.id}">요약 노트</a>${total ? `<a class="chip" href="#/practice/${s.id}">유형별 풀기</a>` : '<span class="small">문제 준비 중</span>'}</div></div>`;
  }).join('')}
  <div class="grid">
    <a class="btn" href="#/mock">모의고사</a>
    <a class="btn" href="#/wrong">오답노트 (${wrongN})</a>
    <a class="btn" href="#/predict">합격 예측</a>
  </div>
  <p class="small" style="margin-top:16px">시험 ${EXAM.totalQuestions}문항 · ${EXAM.durationMin}분 · 총점 ${EXAM.passTotal}점 이상 합격 · 과목별 ${EXAM.failRatio * 100}% 미만 과락 (출처: 데이터자격시험 공식 안내)</p>`;
});

// ---------- notes ----------
route(/^\/notes\/(\d)$/, async (app, s) => {
  const S = subj(s);
  if (!NOTES[s]) { try { NOTES[s] = await (await fetch(`data/notes/s${s}.html`)).text(); } catch { NOTES[s] = ''; } }
  const tabs = EXAM.subjects.map((x) => `<a class="chip ${x.id === +s ? 'on' : ''}" href="#/notes/${x.id}">${x.id}과목</a>`).join('');
  const toc = S.items.map((it) => `<p class="small" style="margin:10px 0 0"><b>${esc(it.name)}</b></p>` + it.subs.map((sb) => `<a href="#/notes/${s}" data-jump="${sb.id}">${esc(sb.name)}</a>`).join('')).join('');
  app.innerHTML = `<div class="row">${tabs}</div><h1>${S.id}과목 ${esc(S.name)} 요약</h1>
    <p class="small">공식 출제 기준 항목 순서대로 정리했어요.</p>
    <details class="card toc"><summary><b>목차</b></summary>${toc}</details>
    <div class="note">${NOTES[s] || '<p class="muted">노트 준비 중이에요.</p>'}</div>
    ${QS.some((q) => q.subject === +s) ? `<a class="btn primary block" href="#/practice/${s}">${S.id}과목 문제 풀기</a>` : ''}`;
  app.querySelectorAll('[data-jump]').forEach((a) => a.addEventListener('click', (e) => {
    e.preventDefault(); const el = app.querySelector(`section[data-item="${a.dataset.jump}"]`); if (el) el.scrollIntoView({ behavior: 'smooth' });
  }));
});

// ---------- practice ----------
route(/^\/practice$/, (app) => {
  app.innerHTML = `<h1>문제 풀기</h1>
  <a class="btn primary block" href="#/today">오늘의 10문제</a>
  ${EXAM.subjects.map((s) => { const n = QS.filter((q) => q.subject === s.id).length;
    return `<div class="card"><b>${s.id}과목 ${esc(s.name)}</b><p class="small">${n ? `${n}문제` : '준비 중'}</p>${n ? `<a class="btn block" href="#/practice/${s.id}">유형별로 풀기</a>` : ''}</div>`; }).join('')}
  <a class="btn block" href="#/wrong">오답노트 (${Object.keys(DB.wrong).length})</a>`;
});
route(/^\/practice\/(\d)(?:\/(.+))?$/, (app, s, tag) => {
  const S = subj(s); tag = tag ? decodeURIComponent(tag) : null;
  const pool = QS.filter((q) => q.subject === +s);
  const tags = [...new Set(pool.flatMap((q) => q.tags))];
  const items = S.items.flatMap((it) => it.subs).filter((sb) => pool.some((q) => q.item === sb.id));
  if (!tag) {
    app.innerHTML = `<h1>${S.id}과목 ${esc(S.name)}</h1>
      <a class="btn primary block" href="#/practice/${s}/전체">전체 ${pool.length}문제 풀기</a>
      <h2>출제 기준 항목별</h2><div class="row">${items.map((sb) => `<a class="chip" href="#/practice/${s}/${encodeURIComponent('항목:' + sb.id)}">${esc(sb.name)} (${pool.filter((q) => q.item === sb.id).length})</a>`).join('')}</div>
      <h2>유형 태그별</h2><div class="row">${tags.map((t) => `<a class="chip" href="#/practice/${s}/${encodeURIComponent(t)}">${esc(t)} (${pool.filter((q) => q.tags.includes(t)).length})</a>`).join('')}</div>`;
    return;
  }
  let list = pool;
  if (tag.startsWith('항목:')) list = pool.filter((q) => q.item === tag.slice(3));
  else if (tag !== '전체') list = pool.filter((q) => q.tags.includes(tag));
  quiz(app, list, { title: `${S.id}과목 · ${tag.startsWith('항목:') ? itemName(tag.slice(3)).split(' › ').pop() : tag}`, mode: 'practice' });
});
function examMix10() {
  // prefer unsolved, then wrong ones, keep subject mix close to the exam (1:1:3)
  const pick = [];
  const want = { 1: 2, 2: 2, 3: 6 };
  for (const s of EXAM.subjects) {
    const pool = QS.filter((q) => q.subject === s.id); if (!pool.length) continue;
    const done = solvedSet(s.id);
    const ranked = shuffle(pool).sort((a, b) => (done.has(a.id) - done.has(b.id)) || ((DB.wrong[b.id] ? 1 : 0) - (DB.wrong[a.id] ? 1 : 0)));
    pick.push(...ranked.slice(0, want[s.id]));
  }
  // fill to 10 if some subjects are not ready
  const rest = shuffle(QS.filter((q) => !pick.includes(q)));
  while (pick.length < 10 && rest.length) pick.push(rest.pop());
  return shuffle(pick);
}
route(/^\/today$/, (app) => quiz(app, examMix10(), { title: '오늘의 10문제', mode: 'today' }));

// ---------- 10-question diagnosis ----------
// Only these 10 answers count. With 2/2/6 questions per subject the band is deliberately wide (z = 1.64, ~90%).
function diagEstimate(results) {
  const subs = EXAM.subjects.map((S) => {
    const r = results.filter((x) => x.q.subject === S.id); const n = r.length, ok = r.filter((x) => x.ok).length;
    const p = (ok + 1) / (n + 2), se = Math.sqrt((p * (1 - p)) / (n + 2)), z = 1.64, max = S.questions * EXAM.pointsEach;
    return { s: S, n, ok, p, max, lo: Math.max(0, p - z * se) * max, hi: Math.min(1, p + z * se) * max, mid: p * max, failAt: max * EXAM.failRatio };
  });
  const mid = subs.reduce((a, x) => a + x.mid, 0);
  const halfW = Math.sqrt(subs.reduce((a, x) => a + Math.pow((x.hi - x.lo) / 2, 2), 0));
  const lo = Math.max(0, Math.round(mid - halfW)), hi = Math.min(100, Math.round(mid + halfW));
  const risk = subs.filter((x) => x.n && x.lo < x.failAt);
  const status = lo >= EXAM.passTotal && !risk.length ? '여유' : hi < EXAM.passTotal ? '부족' : '아슬아슬';
  const weak = subs.filter((x) => x.n).sort((a, b) => (a.ok / a.n - b.ok / b.n) || (b.max - a.max))[0];
  return { subs, lo, hi, status, risk, weak, right: results.filter((x) => x.ok).length, total: results.length };
}
route(/^\/diagnose$/, (app) => {
  app.innerHTML = `<h1>10문제 실력 진단</h1>
    <div class="card"><p>실제 시험 비율대로 <b>1과목 2문제 · 2과목 2문제 · 3과목 6문제</b>를 풀어요. 끝나면 바로 예상 점수 범위와 약한 과목을 보여줘요.</p>
    <p class="small">10문제 기준이라 참고용이에요. 합격 확률이 아니라 점수 범위로만 보여줘요.</p></div>
    <button class="btn primary block" id="go">진단 시작</button>`;
  $('#go', app).addEventListener('click', () => {
    track('diagnose_start');
    quiz(app, examMix10(), { title: '10문제 실력 진단', mode: 'diag', onDone: (res) => diagResult(app, res) });
  });
});
function diagResult(app, res) {
  track('diagnose_complete'); window.scrollTo(0, 0);
  const D = diagEstimate(res);
  const cls = { 여유: 'ok', 아슬아슬: 'warn', 부족: 'bad' }[D.status];
  app.innerHTML = `<h1>진단 결과</h1>
    <div class="card"><div class="small">${ddayText()} · 10문제 중 ${D.right}문제 정답</div><div class="score">예상 ${D.lo}~${D.hi}점</div>
      <p>합격선 ${EXAM.passTotal}점 대비 <b class="${cls}">${D.status}</b>${D.weak ? ` · 약한 과목 <b>${D.weak.s.id}과목</b>` : ''}</p>
      <p class="small"><b>10문제 기준이라 참고용이에요.</b> 문제가 적어서 범위를 넓게 잡았어요. 더 풀수록 '합격 예측'이 정확해져요. 합격 확률은 표시하지 않아요.</p></div>
    <table class="plain"><tr><th>과목</th><th>맞힘</th><th>예상</th></tr>
      ${D.subs.map((x) => `<tr><td>${x.s.id}. ${esc(x.s.name)}</td><td>${x.ok} / ${x.n}</td><td>${Math.round(x.lo)}~${Math.round(x.hi)} / ${x.max}</td></tr>`).join('')}</table>
    <button class="btn primary block" id="share" style="margin-top:16px">인스타 스토리용 카드 저장</button>
    <div class="grid" style="margin-top:12px"><a class="btn" href="#/wrong">틀린 문제 다시 보기</a><a class="btn" href="#/mock">모의고사</a><a class="btn" href="#/predict">전체 기록으로 합격 예측</a></div>
    <p class="small"><a href="#/method">계산 방법 보기</a></p>`;
  $('#share', app).addEventListener('click', () => shareCard({
    label: 'ADsP 10문제 실력 진단', big: ddayText(), mid: `예상 ${D.lo}~${D.hi}점`,
    line: `${D.status}${D.weak ? ` · ${D.weak.s.id}과목 주의` : ''}`, note: '10문제 기준 참고용 · 자체 제작 예상문제',
  }));
}
route(/^\/wrong$/, (app) => {
  const list = Object.keys(DB.wrong).map((id) => QMAP[id]).filter(Boolean);
  if (!list.length) { app.innerHTML = `<h1>오답노트</h1><p class="muted">틀린 문제가 없어요. 문제를 풀면 틀린 문제가 여기에 자동으로 모여요.</p><a class="btn primary block" href="#/today">오늘의 10문제</a>`; return; }
  app.innerHTML = `<h1>오답노트</h1><p class="small">다시 풀어서 맞히면 목록에서 빠져요.</p>
    <a class="btn primary block" id="retry">틀린 ${list.length}문제 다시 풀기</a>
    ${list.map((q) => `<div class="card"><div class="tag">${q.subject}과목 · ${esc(itemName(q.item).split(' › ').pop())}</div><p>${esc(q.q)}</p></div>`).join('')}`;
  $('#retry', app).addEventListener('click', () => quiz(app, list, { title: '오답 다시 풀기', mode: 'wrong' }));
});

function shuffle(a) { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = (Math.random() * (i + 1)) | 0; [a[i], a[j]] = [a[j], a[i]]; } return a; }

function reportLink(q) {
  const title = `[오류 신고] ${q.id}`;
  const body = `문제 ID: ${q.id}\n출제 기준: ${itemName(q.item)}\n\n어떤 점이 잘못됐나요?\n\n근거(링크·교재 쪽수 등):\n\n베타 테스터 명단에 올릴 이름(원하지 않으면 비워 두세요):\n`;
  return `https://github.com/${CFG.repo}/issues/new?title=${encodeURIComponent(title)}&body=${encodeURIComponent(body)}`;
}
function qBody(q) {
  const code = q.code ? `<pre>${esc(q.code)}</pre>` : '';
  return `<div class="qtext">${esc(q.q)}</div>${code}`;
}
function explainBox(q, ok) {
  return `<div class="explain"><p class="res ${ok ? 'ok' : 'bad'}">${ok ? '정답' : '오답'} · 정답 ${NUM[q.answer]}</p>
    <p>${esc(q.explain)}</p>
    <p class="small">출제 기준: ${esc(itemName(q.item))}</p>
    ${(q.sources || []).length ? `<p class="small">근거: ${q.sources.map((x) => `<a href="${esc(x.u)}" target="_blank" rel="noopener">${esc(x.t)}</a>`).join(' · ')}</p>` : ''}
    ${q.verify ? `<p class="small">실행 검증: <a href="https://github.com/${CFG.repo}/blob/main/${esc(q.verify)}" target="_blank" rel="noopener">${esc(q.verify)}</a></p>` : ''}
    <a class="btn report-btn" href="${reportLink(q)}" target="_blank" rel="noopener" data-track="report_click">⚑ 이 문제 오류 신고</a></div>`;
}

function quiz(app, list, { title, mode, onDone }) {
  if (!list.length) { app.innerHTML = `<h1>${esc(title)}</h1><p class="muted">문제가 아직 없어요.</p>`; return; }
  let i = 0, right = 0; const results = [];
  const show = () => {
    const q = list[i];
    app.innerHTML = `<div class="qhead"><span>${esc(title)}</span><span>${i + 1} / ${list.length}</span></div>
      <div class="bar" style="margin:8px 0 4px"><i style="width:${(i / list.length) * 100}%"></i></div>
      <p class="tag">${q.subject}과목 · ${esc(itemName(q.item).split(' › ').pop())} · ${q.tags.map(esc).join(' · ')}</p>
      ${qBody(q)}
      <div class="choices">${q.choices.map((c, k) => `<button class="choice" data-k="${k}"><span class="n">${NUM[k]}</span><span>${esc(c)}</span></button>`).join('')}</div>
      <div id="after"></div>`;
    app.querySelectorAll('.choice').forEach((b) => b.addEventListener('click', () => {
      if (app.querySelector('.choice.right')) return;
      const k = +b.dataset.k; const ok = record(q, k, mode); if (ok) right++; results.push({ q, ok });
      app.querySelectorAll('.choice').forEach((c) => { const kk = +c.dataset.k; c.disabled = true; if (kk === q.answer) c.classList.add('right'); else if (kk === k) c.classList.add('wrong'); });
      $('#after', app).innerHTML = explainBox(q, ok) + `<button class="btn primary block" id="next" style="margin-top:14px">${i + 1 < list.length ? '다음 문제' : '결과 보기'}</button>`;
      $('#next', app).addEventListener('click', () => { i++; i < list.length ? show() : done(); });
      $('#after', app).scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }));
  };
  const done = () => {
    if (onDone) { onDone(results); return; }
    window.scrollTo(0, 0);
    app.innerHTML = `<h1>${esc(title)} 결과</h1><div class="card"><div class="score">${right} / ${list.length}</div><p class="muted">정답률 ${Math.round((right / list.length) * 100)}%</p></div>
      <div class="grid"><a class="btn primary" href="#/predict">합격 예측 보기</a><a class="btn" href="#/wrong">오답노트</a><a class="btn" href="#/">홈</a></div>`;
  };
  show();
}

// ---------- mock exam ----------
let TIMER = null;
const stopTimer = () => { if (TIMER) clearInterval(TIMER); TIMER = null; };
route(/^\/mock$/, async (app) => {
  let sets = [];
  try { sets = await getJSON('data/mock/index.json'); } catch { /* none yet */ }
  app.innerHTML = `<h1>모의고사</h1><p class="small">실제 시험과 같은 ${EXAM.totalQuestions}문항 · ${EXAM.durationMin}분. 끝나면 과목별 점수와 합격 여부를 보여줘요.</p>
    ${sets.length ? sets.map((m) => { const last = DB.mocks.filter((x) => x.id === m.id).pop();
      return `<div class="card"><b>${esc(m.title)}</b><p class="small">${last ? `최근 ${last.total}점 · ${last.pass ? '합격' : '불합격'}` : '아직 안 풀었어요'}</p><a class="btn primary block" href="#/mock/${m.id}">시작하기</a></div>`; }).join('')
      : '<p class="muted">모의고사 준비 중이에요.</p>'}`;
});
route(/^\/mock\/(\w+)$/, async (app, id) => {
  let set; try { set = (await getJSON('data/mock/index.json')).find((m) => m.id === id); } catch { }
  const list = set ? set.questions.map((qid) => QMAP[qid]).filter(Boolean) : [];
  if (!set || list.length !== set.questions.length) { app.innerHTML = `<h1>모의고사</h1><p class="muted">문제를 불러오지 못했어요.</p>`; return; }
  const ans = new Array(list.length).fill(null); let i = 0; const end = Date.now() + EXAM.durationMin * 60000;
  const tick = () => { const left = Math.max(0, end - Date.now()); const el = $('#timer', app);
    if (el) el.textContent = `${String(Math.floor(left / 60000)).padStart(2, '0')}:${String(Math.floor(left / 1000) % 60).padStart(2, '0')}`;
    if (!left) grade(); };
  const show = () => {
    const q = list[i];
    app.innerHTML = `<div class="qhead"><span>${esc(set.title)}</span><span class="timer" id="timer"></span></div>
      <div class="palette">${list.map((_, k) => `<button class="${ans[k] !== null ? 'done' : ''} ${k === i ? 'cur' : ''}" data-go="${k}">${k + 1}</button>`).join('')}</div>
      <p class="tag">${i + 1}번 · ${q.subject}과목</p>${qBody(q)}
      <div class="choices">${q.choices.map((c, k) => `<button class="choice ${ans[i] === k ? 'sel' : ''}" data-k="${k}"><span class="n">${NUM[k]}</span><span>${esc(c)}</span></button>`).join('')}</div>
      <div class="row" style="margin-top:16px"><button class="btn" id="prev" ${i ? '' : 'disabled'}>이전</button><button class="btn" id="nextQ" ${i + 1 < list.length ? '' : 'disabled'}>다음</button>
      <button class="btn primary" id="submit" style="margin-left:auto">제출</button></div>`;
    tick();
    app.querySelectorAll('.choice').forEach((b) => b.addEventListener('click', () => { ans[i] = +b.dataset.k; if (i + 1 < list.length) i++; show(); }));
    app.querySelectorAll('[data-go]').forEach((b) => b.addEventListener('click', () => { i = +b.dataset.go; show(); }));
    $('#prev', app).addEventListener('click', () => { i--; show(); });
    $('#nextQ', app).addEventListener('click', () => { i++; show(); });
    $('#submit', app).addEventListener('click', () => { const blank = ans.filter((a) => a === null).length;
      if (!blank || confirmInline(app, `안 푼 문제가 ${blank}개 있어요. 그래도 제출할까요?`)) grade(); });
  };
  let graded = false;
  const grade = () => {
    if (graded) return; graded = true; stopTimer(); track('mock_complete');
    const per = {}; EXAM.subjects.forEach((s) => (per[s.id] = { ok: 0, n: 0 }));
    list.forEach((q, k) => { per[q.subject].n++; const ok = ans[k] !== null && record(q, ans[k], 'mock'); if (ans[k] === null) { DB.attempts.push({ id: q.id, s: q.subject, ok: false, t: Date.now(), m: 'mock' }); DB.wrong[q.id] = Date.now(); } if (ok) per[q.subject].ok++; });
    const rows = EXAM.subjects.map((s) => { const p = per[s.id]; const pts = p.ok * EXAM.pointsEach; const max = p.n * EXAM.pointsEach; const fail = pts < max * EXAM.failRatio; return { s, pts, max, fail }; });
    const total = rows.reduce((a, r) => a + r.pts, 0); const pass = total >= EXAM.passTotal && !rows.some((r) => r.fail);
    DB.mocks.push({ id, t: Date.now(), total, pass, per: rows.map((r) => r.pts) }); save();
    app.innerHTML = `<h1>${esc(set.title)} 결과</h1><div class="card"><div class="score">${total}점</div><p class="${pass ? 'ok' : 'bad'}"><b>${pass ? '합격' : '불합격'}</b> 기준: 총점 ${EXAM.passTotal}점 이상, 과목별 ${EXAM.failRatio * 100}% 미만 과락</p></div>
      <table class="plain"><tr><th>과목</th><th>점수</th><th>과락</th></tr>${rows.map((r) => `<tr><td>${r.s.id}. ${esc(r.s.name)}</td><td>${r.pts} / ${r.max}</td><td>${r.fail ? '<span class="bad">과락</span>' : '-'}</td></tr>`).join('')}</table>
      <h2>문항별 해설</h2>${list.map((q, k) => `<details class="card"><summary>${k + 1}번 ${ans[k] === q.answer ? '<span class="ok">정답</span>' : '<span class="bad">오답</span>'} · ${esc(q.q.slice(0, 40))}…</summary>${qBody(q)}${explainBox(q, ans[k] === q.answer)}</details>`).join('')}
      <div class="grid"><a class="btn primary" href="#/predict">합격 예측 보기</a><a class="btn" href="#/wrong">오답노트</a></div>`;
  };
  track('mock_start'); show(); TIMER = setInterval(tick, 1000);
});
function confirmInline(_app, msg) { return window.confirm(msg); }

// ---------- prediction ----------
// Recency-weighted accuracy per subject; range widens when few problems are solved. No probabilities.
const HALF = 30; // weight halves every 30 attempts back (per subject)
function subjectStat(sid) {
  const at = DB.attempts.filter((a) => a.s === sid);
  let sw = 0, sw2 = 0, sok = 0;
  at.slice().reverse().forEach((a, k) => { const w = Math.pow(0.5, k / HALF); sw += w; sw2 += w * w; sok += w * (a.ok ? 1 : 0); });
  const nEff = sw ? (sw * sw) / sw2 : 0;
  const p = (sok + 1) / (sw + 2); // Laplace prior keeps tiny samples near 50%
  const se = Math.sqrt((p * (1 - p)) / (nEff + 2));
  const z = 1.28; // ~80% band
  return { n: at.length, nEff, p, lo: Math.max(0, p - z * se), hi: Math.min(1, p + z * se) };
}
function predict() {
  const subs = EXAM.subjects.map((s) => { const st = subjectStat(s.id); const max = s.questions * EXAM.pointsEach;
    return { s, ...st, max, lo: st.lo * max, hi: st.hi * max, mid: st.p * max, failAt: max * EXAM.failRatio }; });
  const mid = subs.reduce((a, x) => a + x.mid, 0);
  const halfW = Math.sqrt(subs.reduce((a, x) => a + Math.pow((x.hi - x.lo) / 2, 2), 0));
  const lo = Math.max(0, Math.round(mid - halfW)), hi = Math.min(100, Math.round(mid + halfW));
  const risk = subs.filter((x) => x.lo < x.failAt);
  const status = lo >= EXAM.passTotal && !risk.length ? '여유' : hi < EXAM.passTotal ? '부족' : '아슬아슬';
  // weakest tags, weighted by how many exam points the subject carries
  const tagStat = {};
  DB.attempts.forEach((a) => { const q = QMAP[a.id]; if (!q) return; q.tags.forEach((t) => { const k = `${q.subject}|${t}`; tagStat[k] = tagStat[k] || { s: q.subject, t, n: 0, ok: 0 }; tagStat[k].n++; tagStat[k].ok += a.ok ? 1 : 0; }); });
  const top = Object.values(tagStat).filter((x) => x.n >= 3).map((x) => ({ ...x, acc: x.ok / x.n, gain: (1 - x.ok / x.n) * subj(x.s).questions }))
    .sort((a, b) => b.gain - a.gain).slice(0, 3);
  return { subs, lo, hi, status, risk, top, total: DB.attempts.length };
}
route(/^\/predict$/, (app) => {
  const P = predict();
  if (P.total < 10) {
    app.innerHTML = `<h1>합격 예측</h1><p class="muted">문제를 10개 이상 풀면 예상 점수 범위를 보여줘요. 지금 ${P.total}개.</p><a class="btn primary block" href="#/today">오늘의 10문제</a><p class="small"><a href="#/method">예측 방법 보기</a></p>`;
    return;
  }
  const cls = { 여유: 'ok', 아슬아슬: 'warn', 부족: 'bad' }[P.status];
  app.innerHTML = `<h1>합격 예측</h1>
    <div class="card"><div class="small">${ddayText()} · 예상 점수 범위</div><div class="score">${P.lo}~${P.hi}점</div>
      <p>합격선 ${EXAM.passTotal}점 대비 <b class="${cls}">${P.status}</b></p>
      <p class="small">확률이 아니라 지금까지의 정답률로 계산한 범위예요. 푼 문제가 적을수록 범위가 넓어요.</p></div>
    <table class="plain"><tr><th>과목</th><th>예상</th><th>푼 문제</th><th>과락선</th></tr>
      ${P.subs.map((x) => `<tr><td>${x.s.id}. ${esc(x.s.name)}</td><td>${Math.round(x.lo)}~${Math.round(x.hi)} / ${x.max}</td><td>${x.n}</td><td>${x.lo < x.failAt ? `<span class="bad">위험 (${x.failAt}점 미만)</span>` : '안전'}</td></tr>`).join('')}</table>
    <h2>남은 기간에 올릴 유형 TOP 3</h2>
    ${P.top.length ? `<ol>${P.top.map((x) => `<li><a href="#/practice/${x.s}/${encodeURIComponent(x.t)}">${x.s}과목 · ${esc(x.t)}</a> <span class="small">정답률 ${Math.round(x.acc * 100)}% (${x.n}문제)</span></li>`).join('')}</ol>` : '<p class="muted">유형별로 3문제 이상 풀면 보여줘요.</p>'}
    <button class="btn primary block" id="share">인스타 스토리용 카드 저장</button>
    <p class="small"><a href="#/method">예측 방법 보기</a></p>`;
  $('#share', app).addEventListener('click', () => shareCard({
    label: 'ADsP 합격 예측', big: ddayText(), mid: `예상 ${P.lo}~${P.hi}점`,
    line: `${P.status} · ${P.risk.length ? `${P.risk.map((x) => x.s.id).join('·')}과목 주의` : '과락 위험 없음'}`,
    note: `자체 제작 예상문제 ${P.total}문제 풀이 기준`,
  }));
});
route(/^\/method$/, (app) => {
  app.innerHTML = `<h1>예측 방법</h1><div class="note">
  <p>합격 예측은 이 브라우저에 저장된 내 풀이 기록만으로 계산해요. 실제 합격자 데이터가 없어서 <b>합격 확률은 표시하지 않고</b>, 점수 범위와 상태만 보여줘요.</p>
  <h3>1. 과목별 정답률 (최근 풀이에 가중치)</h3>
  <p>과목마다 가장 최근 풀이의 가중치가 1이고, ${HALF}문제 전 풀이는 0.5, ${HALF * 2}문제 전은 0.25로 줄어요. 가중 정답률 p = (가중 정답 수 + 1) / (가중 풀이 수 + 2)로 계산해 풀이가 적을 때 50% 쪽으로 당겨요.</p>
  <h3>2. 범위</h3>
  <p>유효 풀이 수 n = (가중치 합)² / (가중치 제곱합)으로 표준오차 √(p(1−p)/(n+2))를 구하고, p ± 1.28×표준오차(약 80% 구간)를 과목 배점에 곱해요. 과목 범위를 합칠 때는 반폭을 제곱합의 제곱근으로 더해요. 그래서 푼 문제가 적으면 범위가 넓어져요.</p>
  <h3>3. 상태</h3>
  <table><tr><th>상태</th><th>조건</th></tr>
  <tr><td>여유</td><td>범위 하단 ≥ ${EXAM.passTotal}점, 과락 위험 과목 없음</td></tr>
  <tr><td>부족</td><td>범위 상단 &lt; ${EXAM.passTotal}점</td></tr>
  <tr><td>아슬아슬</td><td>그 밖의 경우</td></tr></table>
  <p>과락 위험: 과목 범위 하단이 과목 배점의 ${EXAM.failRatio * 100}% 미만. (합격 기준: 총점 ${EXAM.passTotal}점 이상, 과목별 ${EXAM.failRatio * 100}% 미만 과락 — 데이터자격시험 공식 안내)</p>
  <h3>10문제 실력 진단은?</h3>
  <p>진단은 그 10문제의 결과만 써요. 과목마다 p = (맞힌 수 + 1) / (푼 수 + 2), 범위는 p ± 1.64×표준오차(약 90% 구간)로 합격 예측보다 넓게 잡아요. 과목당 2~6문제라 참고용이에요.</p>
  <h3>4. 올릴 유형 TOP 3</h3>
  <p>3문제 이상 푼 유형 태그 중 (1 − 정답률) × 해당 과목 문항 수가 큰 순서예요. 문항이 많은 3과목의 약점이 먼저 올라와요.</p>
  <p class="small">문제는 자체 제작 예상문제라 실제 시험 난이도와 다를 수 있어요.</p></div>`;
});
route(/^\/about$/, (app) => {
  app.innerHTML = `<h1>사이트 소개</h1><div class="note">
  <p>ADsP(데이터분석 준전문가) 무료 문제풀이 사이트예요. 로그인·서버·광고 없이, 풀이 기록은 이 브라우저(localStorage)에만 저장돼요.</p>
  <h3>문제 출처</h3>
  <p>모든 문제는 한국데이터산업진흥원이 공개한 <b>출제 기준(과목·주요항목·세부항목)</b>을 바탕으로 직접 만든 <b>자체 제작 예상문제</b>예요. 진흥원은 기출문제의 복제·배포를 허가하지 않기 때문에 기출·복원 문제는 쓰지 않아요.</p>
  <h3>검증</h3>
  <p>계산·R 코드 문제는 실제로 코드를 실행해 정답을 확정하고, 실행 스크립트를 <a href="https://github.com/${CFG.repo}" target="_blank" rel="noopener">GitHub 저장소</a>에 공개해요. 개념 문제는 출제 기준 항목을 근거로 달고 한 번 더 교차 검토해요. 틀린 곳을 발견하면 각 문제의 '오류 신고'로 알려 주세요.</p>
  <h3>시험 정보</h3>
  <table><tr><th>항목</th><th>내용</th></tr>
  <tr><td>문항</td><td>${EXAM.totalQuestions}문항 객관식 (1과목 10 · 2과목 10 · 3과목 30), 각 ${EXAM.pointsEach}점</td></tr>
  <tr><td>시간</td><td>${EXAM.durationMin}분</td></tr><tr><td>합격</td><td>총점 ${EXAM.passTotal}점 이상, 과목별 ${EXAM.failRatio * 100}% 미만 과락</td></tr>
  <tr><td>${esc(EXAM.round)}</td><td>접수 ${esc(EXAM.schedule.apply)} · 시험 ${esc(EXAM.schedule.exam)} · 발표 ${esc(EXAM.schedule.result)}</td></tr></table>
  <p class="small">출처: ${esc(EXAM.source)}. 최신 정보는 <a href="https://www.dataq.or.kr" target="_blank" rel="noopener">dataq.or.kr</a>에서 확인하세요.</p>
  <p>made by <a href="${CFG.insta}" target="_blank" rel="noopener">@prie.note</a></p></div>`;
});

route(/^\/verify$/, (app) => {
  const n = QS.length, withSrc = QS.filter((q) => (q.sources || []).length).length, withRun = QS.filter((q) => q.verify).length;
  app.innerHTML = `<h1>문제 검증 방법</h1><div class="note">
  <p>이 사이트를 만든 사람도 ADsP를 아직 보지 않았어요. 그래서 한 사람의 판단에 기대지 않고 <b>여러 겹으로 검증</b>한 문제만 올려요. 확실하지 않은 문제는 뺐어요.</p>
  <table><tr><th>단계</th><th>하는 일</th><th>현재</th></tr>
  <tr><td>1. 출제 기준</td><td>모든 문제를 공식 출제 기준 세부항목에 연결</td><td>${n} / ${n}</td></tr>
  <tr><td>2. 공개 근거 링크</td><td>개념 문제마다 공개 문서(백과사전, 표준 용어사전, 정부 가이드라인 등) 링크를 달고, 링크를 실제로 열어 내용이 정답·해설과 일치하는지 확인. 근거를 못 찾은 문제는 제외</td><td>${withSrc} / ${n}</td></tr>
  <tr><td>3. 실행 검증</td><td>계산·R 코드 문제는 R 또는 Python으로 실제 실행해 정답 확정. 스크립트를 <a href="https://github.com/${CFG.repo}/tree/main/verify" target="_blank" rel="noopener">verify/ 폴더</a>에 공개</td><td>${withRun}문제</td></tr>
  <tr><td>4. 교차 검토</td><td>서로 다른 회사의 AI 모델 3개(Claude, ChatGPT, Gemini)에게 과목별 전체 문제를 보여 주고 틀리거나 애매하거나 복수정답인 문제를 찾게 함. 의견이 갈리고 확실하지 않으면 제외</td><td>전 과목 완료</td></tr>
  <tr><td>5. 베타 신고</td><td>풀이하는 분들의 오류 신고를 GitHub Issues로 받아 반영</td><td>상시</td></tr></table>
  <h3>과목별 교차 검토 현황</h3>
  <table><tr><th>과목</th><th>상태</th></tr>
  <tr><td>1과목 데이터 이해 (40)</td><td>공개 근거 확인 + Claude·ChatGPT·Gemini 교차 검토 완료</td></tr>
  <tr><td>2과목 데이터분석 기획 (40)</td><td>공개 근거 확인 + Claude·ChatGPT·Gemini 교차 검토 완료</td></tr>
  <tr><td>3과목 데이터분석 (90)</td><td>R·Python 실행 검증 + Claude·ChatGPT·Gemini 교차 검토 완료</td></tr></table>
  <p>기출·복원 문제는 쓰지 않아요. 한국데이터산업진흥원은 기출문제의 복제·배포를 허가하지 않아요(데이터자격시험 FAQ).</p>
  <p class="small">AI 교차 검토와 공개 근거도 틀릴 수 있어요. 이상한 점이 보이면 꼭 신고해 주세요.</p></div>`;
});
route(/^\/testers$/, async (app) => {
  let list = []; try { list = await getJSON('data/testers.json'); } catch { }
  app.innerHTML = `<h1>베타 테스터</h1><p class="muted">오류 신고가 반영된 분 중 이름 공개를 원한 분들이에요. 고맙습니다.</p>
    ${list.length ? `<ul>${list.map((t) => `<li>${esc(t.name)} <span class="small">${esc(t.note || '')}</span></li>`).join('')}</ul>` : '<p class="small">아직 없어요. 첫 번째 베타 테스터가 되어 주세요.</p>'}
    <a class="btn block" href="https://github.com/${CFG.repo}/issues/new" target="_blank" rel="noopener">⚑ 오류 신고하기</a>`;
});

// ---------- share card (1080x1920) ----------
async function shareCard({ label, big, mid, line, note }) {
  track('card_save');
  const c = document.createElement('canvas'); c.width = 1080; c.height = 1920; const g = c.getContext('2d');
  await document.fonts.ready;
  const F = '"Pretendard Variable", Pretendard, sans-serif';
  g.fillStyle = '#070708'; g.fillRect(0, 0, 1080, 1920);
  g.fillStyle = '#8E8E93'; g.font = `600 40px ${F}`; g.fillText(label, 96, 420);
  g.fillStyle = '#F5F5F2'; g.font = `800 150px ${F}`; g.fillText(big, 96, 610);
  g.font = `800 96px ${F}`; g.fillText(mid, 96, 790);
  g.font = `700 64px ${F}`; g.fillText(line, 96, 920);
  g.fillStyle = '#C8FF3D'; g.beginPath(); g.arc(112, 1010, 16, 0, Math.PI * 2); g.fill();
  g.fillStyle = '#8E8E93'; g.font = `500 38px ${F}`; g.fillText(note, 148, 1024);
  g.fillStyle = '#58585D'; g.font = `500 34px ${F}`; g.fillText(CFG.site, 96, 1440); g.fillText('@prie.note', 96, 1490);
  const url = c.toDataURL('image/png'); const a = document.createElement('a');
  a.href = url; a.download = `adsp_${big}.png`; document.body.appendChild(a); a.click(); a.remove();
}

// ---------- theme, PWA ----------
function applyTheme() { if (DB.theme) document.documentElement.dataset.theme = DB.theme; else delete document.documentElement.dataset.theme; }
$('#themeBtn').addEventListener('click', () => {
  const dark = DB.theme ? DB.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
  DB.theme = dark ? 'light' : 'dark'; save(); applyTheme();
});
let deferred = null;
window.addEventListener('beforeinstallprompt', (e) => { e.preventDefault(); deferred = e; if (!DB.banner) $('#installBanner').hidden = false; });
$('#installBtn').addEventListener('click', async () => { if (deferred) { deferred.prompt(); await deferred.userChoice; } DB.banner = true; save(); $('#installBanner').hidden = true; });
$('#installClose').addEventListener('click', () => { DB.banner = true; save(); $('#installBanner').hidden = true; });
if ('serviceWorker' in navigator && location.protocol !== 'file:') navigator.serviceWorker.register('sw.js').catch(() => {});

document.addEventListener('click', (e) => { const t = e.target.closest('[data-track]'); if (t) track(t.dataset.track); });

applyTheme();
loadData().then(() => { window.addEventListener('hashchange', render); render(); })
  .catch(() => { $('#app').innerHTML = '<p class="bad">데이터를 불러오지 못했어요. 새로고침해 주세요.</p>'; });
