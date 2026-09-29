"""Subject 3 expansion (s3-091~). Two kinds of question:
- E(): computational / R-output questions. `show` is what the student sees (R code; if `run=True` the real R console output
  is captured by running R here and appended). `rcode` (R) and `pycode` (Python, sets `result`) must both reproduce
  `value` (checked by verify/exec.py); the correct choice is the display string `right`.
- C(): concept questions with a public source and `evidence` phrases (checked by verify/sources.py).
The correct answer's position rotates with the id. Parts: scripts/s3_part1.py (3-1, 3-2-1), s3_part2.py (3-2-2~3-2-4), s3_part3.py (3-3).
Run: python scripts/new_s3.py -> bank/new_s3.json"""
import json, os, re, shutil, subprocess, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
W = 'https://en.wikipedia.org/wiki/'
RS = shutil.which('Rscript') or r'C:\Program Files\R\R-4.6.1\bin\Rscript.exe'
RDOC = 'https://stat.ethz.ch/R-manual/R-devel/library/'
qs, pending = [], []


def _place(i, right, wrong):
    pos = (i * 3 + 1) % 4
    ch = list(wrong); ch.insert(pos, right)
    return ch, pos


def src(pairs):
    return [{"t": t, "u": u if u.startswith('http') else W + u} for t, u in pairs]


def E(i, item, tags, level, q, show, rcode, pycode, value, right, wrong, ex, sources=(), run=False):
    ch, pos = _place(i, right, wrong)
    d = {"id": f"s3-{i:03d}", "subject": 3, "item": item, "tags": tags, "level": level, "q": q, "code": show, "choices": ch, "answer": pos,
         "explain": ex, "sources": src(sources), "rcode": rcode, "pycode": pycode, "verifyValue": value, "checked": "2026-09-30"}
    if not show: d.pop("code")
    if run: pending.append(d)
    qs.append(d)


def C(i, item, tags, level, q, right, wrong, ex, sources, ev):
    ch, pos = _place(i, right, wrong)
    qs.append({"id": f"s3-{i:03d}", "subject": 3, "item": item, "tags": tags, "level": level, "q": q, "choices": ch, "answer": pos,
               "explain": ex, "sources": src(sources), "evidence": ev, "checked": "2026-09-30"})


def capture():
    """run each pending `show` in R and append the console output (what a student would see)"""
    if not pending: return
    body = 'options(width = 70)\n' + ''.join(
        f'cat("@@BEGIN {d["id"]}\\n")\n{d["code"]}\ncat("@@END\\n")\n' for d in pending)
    tmp = 'C:/prie-lab/tmp/adsp_verify/show.R'; os.makedirs(os.path.dirname(tmp), exist_ok=True)
    body = re.sub(r'^(?!cat\(|options\()(.+)$', lambda m: f'print(withVisible({{{m.group(1)}}})$value)' if not re.match(r'\s*[\w.]+\s*<-', m.group(1)) else m.group(1), body, flags=re.M)
    open(tmp, 'w', encoding='utf-8').write(body)
    out = subprocess.run([RS, tmp], capture_output=True, text=True, encoding='utf-8')
    if out.returncode: sys.exit(out.stderr)
    blocks = dict(re.findall(r'@@BEGIN (\S+)\n(.*?)@@END', out.stdout, flags=re.S))
    for d in pending:
        o = blocks[d['id']].rstrip('\n')
        d['code'] = d['code'] + '\n' + '\n'.join(l for l in o.splitlines())


if __name__ == '__main__':
    import s3_part1, s3_part2, s3_part3
    for m in (s3_part1, s3_part2, s3_part3):
        m.add(E, C)
    capture()
    ids = [q['id'] for q in qs]
    assert len(ids) == len(set(ids)), 'duplicate ids'
    json.dump(qs, open(os.path.join(ROOT, 'bank', 'new_s3.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(len(qs), 'questions -> bank/new_s3.json')
