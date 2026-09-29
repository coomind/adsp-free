"""Execution gate. A computational question is published only if R and Python both reproduce its answer.
- legacy (verify: verify/s3.R): Rscript verify/s3.R must print verifyValue; verify/check.py re-computes them in Python.
- new (rcode + pycode): rcode is run in one R session (value printed with fmt below), pycode sets `result` in Python
  (numpy as np, scipy.stats as stats, statsmodels.api as sm, pandas as pd, math available). Both are compared with verifyValue.
Writes state[id]['exec'] = 'pass' | 'fail: …'."""
import json, math, os, re, shutil, subprocess, sys, tempfile
import numpy as np, pandas as pd, statsmodels.api as sm
from scipy import stats
from lib import ROOT, TMP, load_bank, load_state, save_state

RS = shutil.which('Rscript') or r'C:\Program Files\R\R-4.6.1\bin\Rscript.exe'
FMT = 'fmt <- function(x) paste(format(x, trim = TRUE), collapse = " ")\nr3 <- function(x) formatC(x, format = "f", digits = 3)\nr2 <- function(x) formatC(x, format = "f", digits = 2)\n'

def same(value, expect, tol=5e-4):
    """token-wise compare; numbers within tol (relative for big values)"""
    a, b = str(value).split(), str(expect).split()
    if len(a) != len(b): return False
    for x, y in zip(a, b):
        try:
            fx, fy = float(x), float(y)
            if not (abs(fx - fy) <= tol * max(1, abs(fy)) or (math.isnan(fx) and math.isnan(fy))): return False
        except ValueError:
            if x != y: return False
    return True

def pyfmt(v):
    if isinstance(v, (list, tuple, np.ndarray, pd.Series)): return ' '.join(pyfmt(x) for x in np.asarray(v).ravel())
    if isinstance(v, (bool, np.bool_)): return 'TRUE' if v else 'FALSE'
    if isinstance(v, (int, np.integer)): return str(int(v))
    if isinstance(v, (float, np.floating)): return repr(float(v))
    return str(v)

def run():
    qs = load_bank(); st = load_state(); res = {}
    # legacy: s3.R + check.py
    leg = [q for q in qs if q.get('verify') == 'verify/s3.R']
    if leg:
        out = subprocess.run([RS, os.path.join(ROOT, 'verify', 's3.R')], capture_output=True, text=True, check=True).stdout
        rout = dict(l.split('\t', 1) for l in out.strip().splitlines())
        py_ok = subprocess.run([sys.executable, os.path.join(ROOT, 'verify', 'check.py')], capture_output=True, text=True).returncode == 0
        for q in leg:
            ok = rout.get(q['id'], '').strip() == q['verifyValue']
            res[q['id']] = 'pass' if ok and py_ok else f"fail: R={rout.get(q['id'])!r} expected {q['verifyValue']!r}" + ('' if py_ok else ' / check.py failed')
    # new: rcode / pycode
    new = [q for q in qs if q.get('rcode')]
    if new:
        os.makedirs(TMP, exist_ok=True)
        body = FMT + ''.join(f'cat("@@{q["id"]}\t", tryCatch({{ .v <- local({{\n{q["rcode"]}\n}}); if (is.character(.v) && length(.v) == 1) .v else fmt(.v) }}, error = function(e) paste("ERROR", conditionMessage(e))), "\n", sep = "")\n' for q in new)
        rf = os.path.join(TMP, 'exec_new.R'); open(rf, 'w', encoding='utf-8').write(body)
        out = subprocess.run([RS, rf], capture_output=True, text=True, encoding='utf-8').stdout
        rout = dict(l[2:].split('\t', 1) for l in out.splitlines() if l.startswith('@@'))
        for q in new:
            rv = rout.get(q['id'], 'MISSING').strip()
            env = {'np': np, 'stats': stats, 'sm': sm, 'pd': pd, 'math': math}
            try:
                exec(q['pycode'], env); pv = pyfmt(env['result'])
            except Exception as e:
                pv = f'ERROR {e}'
            okr, okp = same(rv, q['verifyValue']), same(pv, q['verifyValue'])
            res[q['id']] = 'pass' if okr and okp else f"fail: R={rv!r} Py={pv!r} expected {q['verifyValue']!r}"
    for q in qs:
        if q['id'] in res: st.setdefault(q['id'], {})['exec'] = res[q['id']]
    save_state(st)
    bad = {k: v for k, v in res.items() if v != 'pass'}
    for k, v in bad.items(): print(k, v)
    print(f'exec: {len(res) - len(bad)} pass / {len(bad)} fail (of {len(res)} computational)')

if __name__ == '__main__':
    run()
