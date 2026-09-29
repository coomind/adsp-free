"""Independent-solver gate (a separate agent answers without seeing answers or explanations).
  python verify/solve.py prep [batch_size]  -> C:/prie-lab/tmp/adsp_verify/solve/<round>_bNN.json for questions that need a (re)solve
  python verify/solve.py collect <round>    -> reads <round>_bNN_answers.json ({"id": choice_index 0-3}) and scores them
A question needs solving if it was never solved, or it missed and has been edited since (content hash changed).
Two consecutive misses (miss -> edit -> miss) => state[id]['excluded'] = 'solver missed twice'.
Also prepares review batches (with answers) for the Claude cross review: review_<round>_bNN.json -> ..._review.json
  ({"id": {"ok": true/false, "why": "..."}})."""
import glob, hashlib, json, os, sys, time
from lib import TMP, load_bank, load_state, save_state

D = os.path.join(TMP, 'solve'); os.makedirs(D, exist_ok=True)

def chash(q):
    return hashlib.sha1(json.dumps([q['q'], q.get('code', ''), q['choices'], q['answer'], q.get('explain', '')], ensure_ascii=False).encode()).hexdigest()[:12]

def prep(size=45):
    qs = load_bank(); st = load_state(); todo = []
    for q in qs:
        s = st.get(q['id'], {})
        if s.get('excluded'): continue
        hist = s.get('solve', [])
        if not hist or (hist[-1]['r'] != 'ok' and hist[-1]['h'] != chash(q)) or (s.get('review', {}).get('ok') is False and s['review'].get('h') != chash(q)):
            todo.append(q)
    rnd = time.strftime('r%m%d%H%M')
    for i in range(0, len(todo), size):
        part = todo[i:i + size]
        json.dump([{k: q[k] for k in ('id', 'q', 'code', 'choices') if k in q} for q in part],
                  open(os.path.join(D, f'{rnd}_b{i // size:02d}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        json.dump([{k: q[k] for k in ('id', 'item', 'q', 'code', 'choices', 'answer', 'explain', 'sources') if k in q} for q in part],
                  open(os.path.join(D, f'review_{rnd}_b{i // size:02d}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(rnd, len(todo), 'questions in', (len(todo) + size - 1) // size, 'batches ->', D)

def collect(rnd):
    qs = {q['id']: q for q in load_bank()}; st = load_state(); n = ok = 0
    # content hash of the version that was actually solved/reviewed (from the prep-time review file, which has every hashed field)
    ph = {}
    for f in glob.glob(os.path.join(D, f'review_{rnd}_b[0-9][0-9].json')):
        for e in json.load(open(f, encoding='utf-8')): ph[e['id']] = chash(e)
    for f in sorted(glob.glob(os.path.join(D, f'{rnd}_b*_answers.json'))):
        for i, a in json.load(open(f, encoding='utf-8')).items():
            if i not in qs: continue
            q = qs[i]; s = st.setdefault(i, {}); hist = s.setdefault('solve', [])
            if any(x.get('round') == rnd for x in hist): continue  # already collected
            a = int(a) if str(a).lstrip('-').isdigit() else -1
            r = 'ok' if a == q['answer'] else f'miss:{a}'  # q['answer'] may have moved only if content changed -> hash differs anyway
            hist.append({'r': r, 'h': ph.get(i, chash(q)), 'round': rnd}); n += 1; ok += r == 'ok'
            if r != 'ok' and len(hist) >= 2 and hist[-2]['r'] != 'ok' and hist[-2]['h'] != hist[-1]['h']:
                s['excluded'] = 'solver missed twice (after one fix)'
    for f in sorted(glob.glob(os.path.join(D, f'review_{rnd}_b*_review.json'))):
        for i, v in json.load(open(f, encoding='utf-8')).items():
            if i in qs: st.setdefault(i, {})['review'] = {'ok': bool(v.get('ok')), 'why': v.get('why', ''), 'h': ph.get(i, chash(qs[i])), 'round': rnd}
    save_state(st)
    miss = [i for i, s in st.items() if s.get('solve') and s['solve'][-1]['r'] != 'ok' and not s.get('excluded')]
    rev = [i for i, s in st.items() if s.get('review', {}).get('ok') is False and s['review'].get('round') == rnd]
    print(f'{rnd}: solved {n}, match {ok} ({ok / max(n, 1):.1%}); open misses {len(miss)}: {miss}; review problems {len(rev)}: {rev}')

if __name__ == '__main__':
    {'prep': lambda: prep(int(sys.argv[2]) if len(sys.argv) > 2 else 45), 'collect': lambda: collect(sys.argv[2])}[sys.argv[1]]()
