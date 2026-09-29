"""Build 6 mock exams (10 + 10 + 30 questions each, no question shared) from the PUBLISHED bank (data/questions).
Per subject, questions are ordered by outline item — frequent items first (data/study.json freq weights) — and dealt
round-robin into the 6 mocks, so every mock covers the outline evenly and frequent topics appear in every mock.
Run after verify/publish.py: python scripts/build_mocks.py"""
import json, os
from collections import defaultdict

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
N, NEED = 6, {1: 10, 2: 10, 3: 30}
study = json.load(open(os.path.join(ROOT, 'data', 'study.json'), encoding='utf-8'))
weight = defaultdict(int)
for s, lst in study['freq'].items():
    for f in lst: weight[f['item']] = max(weight[f['item']], f['w'])

mocks = [[] for _ in range(N)]
for s in (1, 2, 3):
    qs = json.load(open(os.path.join(ROOT, 'data', 'questions', f's{s}.json'), encoding='utf-8'))
    by = defaultdict(list)
    for q in sorted(qs, key=lambda q: q['id']): by[q['item']].append(q['id'])
    order = sorted(by, key=lambda it: (-weight[it], it))  # frequent items first
    # interleave items: one question from each item in turn, so the deal spreads items across mocks
    stream, k = [], 0
    while any(by[it] for it in order):
        for it in order:
            if by[it]: stream.append(by[it].pop(k % len(by[it]) if False else 0))
    need = NEED[s] * N
    assert len(stream) >= need, (s, len(stream), need)
    for i, qid in enumerate(stream[:need]): mocks[i % N].append(qid)

idx = [{"id": f"m{i + 1}", "title": f"모의고사 {i + 1}회", "questions": m} for i, m in enumerate(mocks)]
ids = [q for m in idx for q in m['questions']]
assert len(ids) == len(set(ids)) == 50 * N
for m in idx:
    subj = [int(q[1]) for q in m['questions']]
    assert [subj.count(s) for s in (1, 2, 3)] == [10, 10, 30], m['id']
json.dump(idx, open(os.path.join(ROOT, 'data', 'mock', 'index.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(N, 'mocks x 50, none shared')
