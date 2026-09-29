"""Format gate: structure, duplicates, answer hints in the stem. Writes state[id]['lint'] = 'pass' | 'fail: …'.
Answer-position balance is a bank-level report (publish.py rebalances choice order where allowed)."""
import difflib, json, os, re, sys
from collections import Counter
from lib import ROOT, load_bank, load_state, save_state, norm_text

exam = json.load(open(os.path.join(ROOT, 'data', 'exam.json'), encoding='utf-8'))
ITEMS = {sb['id'] for S in exam['subjects'] for it in S['items'] for sb in it['subs']}
LEVELS = {'기본', '실전', '고난도'}
STOP = set('관리 분석 데이터 모델 방법 과정 단계 결과 기법 정보 영역 값은 값이 경우 것은 있는 없는 한다 된다 에서 으로 이다 는다 문제 다음 통계'.split())

def words(t):
    return {w for w in re.findall(r'[가-힣]{2,}|[A-Za-z]{3,}', t) if w not in STOP}

def run():
    qs = load_bank(); st = load_state(); errs = {}
    ids = Counter(q['id'] for q in qs)
    for q in qs:
        e = []
        if ids[q['id']] > 1: e.append('duplicate id')
        if len(q['choices']) != 4 or len(set(map(str.strip, q['choices']))) != 4: e.append('needs 4 distinct choices')
        if not (0 <= q['answer'] < 4): e.append('answer out of range')
        if q['item'] not in ITEMS: e.append(f"unknown item {q['item']}")
        if q.get('level') not in LEVELS: e.append('level missing')
        if not (q.get('sources') or q.get('rcode') or q.get('verify')): e.append('no source and no executed check')
        if not q.get('explain', '').strip(): e.append('no explanation')
        if q['_file'].startswith('new') and not q.get('fixedOrder') and re.search('[①-④]', q.get('explain', '')):
            e.append('explanation cites choice numbers but choice order rotates')
        # answer hint: a word of the correct choice appears in the stem but in none of the wrong choices
        if not (q.get('rcode') or q.get('verify')) and not q.get('hintOk'):
            right = words(q['choices'][q['answer']]); wrong = set().union(*(words(c) for k, c in enumerate(q['choices']) if k != q['answer']))
            leak = sorted(w for w in right - wrong if w in q['q'])
            if leak: e.append('hint in stem: ' + ','.join(leak))
        errs[q['id']] = e
    # near-duplicates within a subject (stem + code + choices)
    sig = {q['id']: norm_text(q['q'] + ' ' + q.get('code', '') + ' ' + ' '.join(sorted(q['choices']))) for q in qs}
    by = {}
    for q in qs: by.setdefault(q['subject'], []).append(q['id'])
    for s, lst in by.items():
        for i, a in enumerate(lst):
            for b in lst[i + 1:]:
                if difflib.SequenceMatcher(None, sig[a], sig[b]).ratio() > 0.9:
                    errs[b].append(f'near-duplicate of {a}')
    for q in qs:
        st.setdefault(q['id'], {})['lint'] = 'pass' if not errs[q['id']] else 'fail: ' + '; '.join(errs[q['id']])
    save_state(st)
    bad = {k: v for k, v in errs.items() if v}
    for k, v in bad.items(): print(k, v)
    for s in sorted(by):
        c = Counter(q['answer'] for q in qs if q['subject'] == s); n = sum(c.values())
        print(f'subject {s}: {n} questions, answer positions', [f'{c[i] / n:.0%}' for i in range(4)])
    print(f'lint: {len(qs) - len(bad)} pass / {len(bad)} fail')

if __name__ == '__main__':
    run()
