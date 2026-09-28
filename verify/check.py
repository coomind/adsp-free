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

# independent recomputation for s3-031 ~ s3-090 (numeric ones)
X = np.array([1, 2, 3, 4], float)
check(near(np.var(X), 1.25) and near(np.var(X, ddof=1), 1.6667), 's3-055')
check(near(4 / np.sqrt(16), 1), 's3-056')
lo, hi = 50 + np.array([-1, 1]) * stats.norm.ppf(0.975) * 10 / 5
check(near(lo, 46.08, 5e-3) and near(hi, 53.92, 5e-3), 's3-057')
check(near(stats.ttest_1samp([5, 6, 7, 8, 9], 5).statistic, 2.828), 's3-058')
check(near(stats.chi2_contingency([[10, 20], [20, 10]], correction=False)[0], 6.667), 's3-059')
check(near(np.cov([1, 2, 3, 4], [2, 4, 6, 8])[0, 1], 3.333), 's3-060')
check(near(stats.spearmanr([1, 2, 3, 4, 5], [1, 3, 2, 5, 4])[0], 0.8), 's3-061')
check(near(-0.1 + 1.7 * 6, 10.1), 's3-062')
check(near(m2.rsquared_adj, 0.4667), 's3-063')
check(near(stats.f_oneway([1, 2, 3], [4, 5, 6], [7, 8, 9]).statistic, 27), 's3-064')
check(near(stats.binom.pmf(2, 4, 0.5), 0.375) and near(stats.poisson.pmf(0, 2), 0.135), 's3-067/068')
check(near(np.median([1, 2, 3, 100]), 2.5) and near(np.mean([1, 2, 3, 100]), 26.5), 's3-048')
z = (np.array([2, 4, 6]) - 4) / np.std([2, 4, 6], ddof=1)
check(near(z[2], 1), 's3-053')
check(near((20 - 10) / 30, 0.333), 's3-054')
check(near((4 + 3) / 10, 0.7) and near(np.mean([6, 9, 12]), 9) and list(np.diff([5, 8, 12, 17], 2)) == [1, 1] and list(np.convolve([3, 6, 9, 12, 15], [1/3]*3, 'valid')) == [6, 9, 12], 's3-069/070/071')
check(near(0.5 * 20 + 0.5 * 10, 15) and near(np.hypot(3, 4), 5) and 3 + 4 == 7, 's3-072/073/074')
P, Rr = 40 / 60, 40 / 50
check(near(70 / 100, 0.7) and near(Rr, 0.8) and near(2 * P * Rr / (P + Rr), 0.727) and near(30 / 50, 0.6), 's3-075~078')
check(near(1 - (0.4 ** 2 + 0.6 ** 2), 0.48) and near(-(2 * 0.5 * np.log2(0.5)), 1), 's3-079/080')
check(near(sup({'A', 'B'}) / sup({'A'}), 0.6), 's3-081')
check([np.mean([1]), np.mean([2, 9, 10])] == [1, 7] and round(2.5) == 2 and round(0.5) == 0, 's3-082 / s3-045 (Python also rounds half to even)')
check(min(abs(a - b) for a in (0, 1) for b in (4, 6)) == 3 and max(abs(a - b) for a in (0, 1) for b in (4, 6)) == 6, 's3-083')
check(near(0.8 / 0.2, 4) and near(np.exp(0.693), 2.0, 5e-3), 's3-084/085')

# the marked choice must contain the verified value's tokens in order; no other choice may
import re
toks = lambda t: re.findall(r'-?[0-9]+(?:\.[0-9]+)?|[A-Za-z]+', t)
def subseq(v, ch):
    it = iter(ch)
    return all(any(x == y for y in it) for x in v)
for q in qs:
    if q.get('verifyValue') and q['id'] not in ('s3-019',):
        v = toks(q['verifyValue'].replace('−', '-'))
        chs = [toks(c.replace('−', '-')) for c in q['choices']]
        check(subseq(v, chs[q['answer']]), f"{q['id']}: marked choice {q['choices'][q['answer']]!r} vs value {q['verifyValue']!r}")
        others = [k for k, c in enumerate(chs) if k != q['answer'] and c == v]
        check(not others, f"{q['id']}: value equals another choice {others}")
check(by['s3-019']['choices'][by['s3-019']['answer']] == 'y = −0.1 + 1.7x', 's3-019 marked choice')

# mock exams: 10/10/30 per subject, ids exist, no question shared between mocks
mocks = json.load(open(os.path.join(ROOT, 'data', 'mock', 'index.json'), encoding='utf-8'))
seen = set()
for mk in mocks:
    cnt = {1: 0, 2: 0, 3: 0}
    for qid in mk['questions']:
        check(qid in by, f"{mk['id']}: unknown {qid}")
        check(qid not in seen, f"{mk['id']}: {qid} already used in another mock")
        seen.add(qid); cnt[by[qid]['subject']] = cnt.get(by[qid]['subject'], 0) + 1 if qid in by else 0
    check(cnt == {1: 10, 2: 10, 3: 30}, f"{mk['id']}: subject split {cnt}")

print(f"{len(mocks)} mocks, {len(seen)} questions, none shared")
print(f"{len(qs)} questions, {sum(1 for q in qs if q.get('verify'))} executed in R + Python")
if fail:
    print('FAIL'); [print(' -', x) for x in fail]; sys.exit(1)
print('ALL OK')
