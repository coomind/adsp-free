"""Checks the whole question bank. Exit code 1 on any failure.
1) structure: unique ids, 4 choices, valid answer, every question has a source link or an executed check
2) R: runs verify/s3.R and compares each printed value with the question's verifyValue
3) Python: recomputes the numeric answers independently (numpy/scipy/statsmodels) and the numbers quoted in explanations
Run: python verify/check.py   (needs R on PATH or at the default Windows install path)"""
import glob, json, os, shutil, subprocess, sys
import numpy as np
from scipy import stats
import statsmodels.api as sm

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
fail = []
def check(cond, msg):
    if not cond:
        fail.append(msg)

# 1) structure
qs = []
for f in sorted(glob.glob(os.path.join(ROOT, 'data', 'questions', 's*.json'))):
    qs += json.load(open(f, encoding='utf-8'))
ids = [q['id'] for q in qs]
check(len(ids) == len(set(ids)), 'duplicate ids')
for q in qs:
    check(len(q['choices']) == 4, f"{q['id']}: needs 4 choices")
    check(len(set(q['choices'])) == 4, f"{q['id']}: duplicate choices")
    check(0 <= q['answer'] < 4, f"{q['id']}: answer out of range")
    check(q.get('sources') or q.get('verify'), f"{q['id']}: no source and no executed check")
by = {q['id']: q for q in qs}

# 2) R
rs = shutil.which('Rscript') or r'C:\Program Files\R\R-4.6.1\bin\Rscript.exe'
res = subprocess.run([rs, os.path.join(ROOT, 'verify', 's3.R')], capture_output=True, text=True, check=True).stdout
rout = dict(line.split('\t', 1) for line in res.strip().splitlines())
for q in qs:
    if q.get('verify') == 'verify/s3.R':
        check(q['id'] in rout, f"{q['id']}: not computed by s3.R")
        check(rout.get(q['id'], '').strip() == q['verifyValue'], f"{q['id']}: R gives {rout.get(q['id'])!r}, bank says {q['verifyValue']!r}")
extra = set(rout) - {q['id'] for q in qs if q.get('verify')}
check(not extra, f"s3.R computes ids not marked verify: {extra}")

# 3) independent Python recomputation
def near(a, b, tol=5e-4):
    return abs(a - b) < tol
check(near(np.var([2, 4, 6, 8], ddof=1), 6.667), 's3-015 var')
check(near(np.std([2, 4, 4, 4, 5, 5, 7, 9], ddof=1), 2.138) and near(np.std([2, 4, 4, 4, 5, 5, 7, 9]), 2.0), 's3-017 sd')
check(near(stats.pearsonr([1, 2, 3, 4, 5], [2, 1, 4, 3, 5])[0], 0.8), 's3-018 cor')
check(near(100 * stats.norm.sf(90, 70, 10), 2.275, 1e-3) and near(stats.norm.cdf(2), 0.97725), 's3-023 normal tail')
m = sm.OLS([2, 3, 5, 6, 9], sm.add_constant([1, 2, 3, 4, 5])).fit()
check(near(m.params[0], -0.1) and near(m.params[1], 1.7), 's3-019 lm')
m2 = sm.OLS([2, 4, 5, 4, 5], sm.add_constant([1, 2, 3, 4, 5])).fit()
check(near(m2.params[0], 2.2) and near(m2.params[1], 0.6) and near(m2.ssr, 2.4) and near(m2.centered_tss, 6.0) and near(m2.rsquared, 0.6), 's3-020 r2 + explanation numbers')
v = np.array([2, 4, 4, 5, 6, 7, 8, 30])
q1, q3 = np.percentile(v, [25, 75])  # numpy 'linear' == R type 7
check(near(q1, 4) and near(q3, 7.25) and near(q3 + 1.5 * (q3 - q1), 12.125), 's3-013 quartiles in explanation')
check(list(v[(v < q1 - 1.5 * (q3 - q1)) | (v > q3 + 1.5 * (q3 - q1))]) == [30], 's3-013 outlier')
check(near(3 / (3 + 1), 0.75), 's3-026 pca')
check(near(40 / 60, 0.667) and near(40 / 50, 0.8), 's3-029 precision/recall')
tx = [{'A', 'B'}, {'A', 'B'}, {'A', 'B'}, {'A', 'C'}, {'A'}, {'B', 'C'}, {'C'}, {'C'}, {'D'}, {'B'}]
sup = lambda s: sum(s <= t for t in tx) / len(tx)
check(sup({'A'}) == 0.5 and sup({'B'}) == 0.5 and sup({'A', 'B'}) == 0.3, 's3-030 supports quoted in question')
check(near(sup({'A', 'B'}) / (sup({'A'}) * sup({'B'})), 1.2), 's3-030 lift')

# the marked choice must contain the verified value (formatting aside)
for q in qs:
    if q.get('verifyValue') and q['id'] not in ('s3-019',):
        ch = q['choices'][q['answer']].replace('"', '').replace('%', '')
        check(q['verifyValue'] in ch or ch in q['verifyValue'], f"{q['id']}: marked choice {ch!r} vs value {q['verifyValue']!r}")
check(by['s3-019']['choices'][by['s3-019']['answer']] == 'y = −0.1 + 1.7x', 's3-019 marked choice')

print(f"{len(qs)} questions, {sum(1 for q in qs if q.get('verify'))} executed in R + Python")
if fail:
    print('FAIL'); [print(' -', x) for x in fail]; sys.exit(1)
print('ALL OK')
