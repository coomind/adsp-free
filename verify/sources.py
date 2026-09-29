"""Source gate for concept questions. Each question lists "evidence": phrases that must all appear (case/space-insensitive)
in the text of its source pages, which are downloaded fresh (cache: C:/prie-lab/tmp/adsp_verify/src).
Legacy questions without evidence were opened and checked by hand on 2026-09-29 (handoff/adsp_review.md) -> 'legacy-manual'.
Writes state[id]['source'] = 'pass' | 'legacy-manual' | 'fail: …'."""
import hashlib, html, io, json, os, re, sys, urllib.request
from lib import TMP, load_bank, load_state, save_state, norm_text, kind

CACHE = os.path.join(TMP, 'src'); os.makedirs(CACHE, exist_ok=True)
UA = {'User-Agent': 'Mozilla/5.0 (adsp-free source check; +https://coomind.github.io/adsp-free/)'}

def page(url, refresh=False):
    f = os.path.join(CACHE, hashlib.sha1(url.encode()).hexdigest() + '.txt')
    if os.path.exists(f) and not refresh: return open(f, encoding='utf-8').read()
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=40) as r:
        data = r.read(); ctype = r.headers.get('Content-Type', '')
    if 'pdf' in ctype or url.lower().endswith('.pdf'):
        from pypdf import PdfReader
        text = '\n'.join((p.extract_text() or '') for p in PdfReader(io.BytesIO(data)).pages)
    else:
        t = data.decode('utf-8', 'replace')
        t = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', t)
        text = html.unescape(re.sub(r'<[^>]+>', ' ', t))
    open(f, 'w', encoding='utf-8').write(text)
    return text

def run(refresh=False):
    qs = load_bank(); st = load_state(); res = {}; errors = {}
    for q in qs:
        if kind(q) != 'concept': continue
        ev = q.get('evidence')
        if not ev:
            res[q['id']] = 'legacy-manual' if q['_file'].startswith('legacy') else 'fail: no evidence phrases'
            continue
        texts = []
        for s in q['sources']:
            try: texts.append(norm_text(page(s['u'], refresh)))
            except Exception as e: errors[s['u']] = str(e)
        blob = ' '.join(texts)
        miss = [p for p in ev if norm_text(p) not in blob]
        res[q['id']] = 'pass' if texts and not miss else 'fail: ' + ('source unreachable' if not texts else 'not found: ' + ' | '.join(miss))
    for k, v in res.items(): st.setdefault(k, {})['source'] = v
    save_state(st)
    for u, e in errors.items(): print('UNREACHABLE', u, e)
    bad = {k: v for k, v in res.items() if v.startswith('fail')}
    for k, v in bad.items(): print(k, v)
    print(f"sources: {sum(v == 'pass' for v in res.values())} pass / {sum(v == 'legacy-manual' for v in res.values())} legacy-manual / {len(bad)} fail")

if __name__ == '__main__':
    run('--refresh' in sys.argv)
