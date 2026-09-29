"""Publish gate: data/questions/sN.json = only questions that pass every gate for their CURRENT content.
  lint == pass
  exec == pass                        (computational questions)
  source in (pass, legacy-manual)     (concept questions)
  last solve == ok on the current content hash   (independent solver agent, no answers shown)
  review ok on the current content hash          (Claude cross review agent)
  not excluded
Everything else is listed in verify/publish_report.json with the reason (copied into handoff/adsp_review.md)."""
import json, os
from collections import Counter
from lib import ROOT, load_bank, load_state, kind
from solve import chash

def reasons(q, s):
    r = []
    if s.get('excluded'): return ['excluded: ' + s['excluded']]
    if s.get('lint') != 'pass': r.append('lint ' + str(s.get('lint')))
    if kind(q) == 'exec' and s.get('exec') != 'pass': r.append('exec ' + str(s.get('exec')))
    if kind(q) == 'concept' and s.get('source') not in ('pass', 'legacy-manual'): r.append('source ' + str(s.get('source')))
    h = chash(q); sv = s.get('solve', [])
    if not sv or sv[-1]['h'] != h: r.append('not solved (current version)')
    elif sv[-1]['r'] != 'ok': r.append('solver ' + sv[-1]['r'])
    rv = s.get('review')
    if not rv or rv.get('h') != h: r.append('not reviewed (current version)')
    elif not rv['ok']: r.append('review: ' + rv.get('why', ''))
    return r

def run():
    qs = load_bank(); st = load_state(); pub = {1: [], 2: [], 3: []}; held = {}
    for q in qs:
        r = reasons(q, st.get(q['id'], {}))
        if r: held[q['id']] = r; continue
        pub[q['subject']].append({k: v for k, v in q.items() if not k.startswith('_') or k == '_file'})
    for s, lst in pub.items():
        lst.sort(key=lambda q: q['id'])
        json.dump([{k: v for k, v in q.items() if k != '_file'} for q in lst], open(os.path.join(ROOT, 'data', 'questions', f's{s}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    total = len(qs); n = sum(len(v) for v in pub.values())
    rep = {'bank': total, 'published': n, 'by_subject': {s: len(v) for s, v in pub.items()}, 'held': held,
           'excluded': {i: s['excluded'] for i, s in st.items() if s.get('excluded')}}
    json.dump(rep, open(os.path.join(ROOT, 'verify', 'publish_report.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    # public summary for the site's '검증 방법' page
    pubq = [q for v in pub.values() for q in v]
    firsts = [st[q['id']]['solve'][0]['r'] == 'ok' for q in qs if st.get(q['id'], {}).get('solve')]
    summ = {'bank': total, 'published': n, 'held': len(held), 'excluded': len(rep['excluded']),
            'exec': sum(1 for q in pubq if kind(q) == 'exec'), 'evidence': sum(1 for q in pubq if q.get('evidence')),
            'legacyManual': sum(1 for q in pubq if kind(q) == 'concept' and not q.get('evidence')),
            'solverFirstMatch': round(sum(firsts) / max(len(firsts), 1), 4), 'solverChecked': len(firsts),
            'reviewed': sum(1 for q in pubq if st[q['id']].get('review', {}).get('ok')),
            'externalReviewed': sum(1 for q in pubq if q['_file'].startswith('legacy')) if pubq and '_file' in pubq[0] else 170,
            'bySubject': rep['by_subject']}
    json.dump(summ, open(os.path.join(ROOT, 'data', 'verify_summary.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    exam = json.load(open(os.path.join(ROOT, 'data', 'exam.json'), encoding='utf-8'))
    items = [sb['id'] for S in exam['subjects'] for it in S['items'] for sb in it['subs']]
    cov = Counter(q['item'] for v in pub.values() for q in v)
    print(f"published {n} / bank {total} | by subject {rep['by_subject']} | held {len(held)} | excluded {len(rep['excluded'])} | coverage {sum(cov[i] > 0 for i in items)}/{len(items)}")
    for i, r in held.items(): print(' held', i, '; '.join(r))

if __name__ == '__main__':
    run()
