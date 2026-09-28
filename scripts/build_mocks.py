"""Build mock exams 2 and 3 with no question shared with mock 1 or each other.
Remaining questions are sorted by syllabus item and dealt alternately so each mock covers items evenly."""
import json, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
Q = {s: json.load(open(os.path.join(ROOT, 'data', 'questions', f's{s}.json'), encoding='utf-8')) for s in (1, 2, 3)}
idx_path = os.path.join(ROOT, 'data', 'mock', 'index.json')
idx = [m for m in json.load(open(idx_path, encoding='utf-8')) if m['id'] == 'm1']
used = set(idx[0]['questions'])
need = {1: 10, 2: 10, 3: 30}
sets = {'m2': [], 'm3': []}
for s in (1, 2, 3):
    rest = sorted([q for q in Q[s] if q['id'] not in used], key=lambda q: (q['item'], q['id']))
    a, b = rest[0::2][:need[s]], rest[1::2][:need[s]]
    assert len(a) == need[s] and len(b) == need[s], (s, len(a), len(b))
    sets['m2'] += [q['id'] for q in a]; sets['m3'] += [q['id'] for q in b]
for mid, title in (('m2', '모의고사 2회 (베타)'), ('m3', '모의고사 3회 (베타)')):
    idx.append({"id": mid, "title": title, "questions": sets[mid]})
all_ids = [i for m in idx for i in m['questions']]
assert len(all_ids) == len(set(all_ids)) == 150
json.dump(idx, open(idx_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for m in idx: print(m['id'], len(m['questions']))
