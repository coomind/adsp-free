"""Spread correct-answer positions evenly within a question file.

Moves each question's correct choice to a target slot (round-robin 0..3) by swapping it with the
choice currently in that slot. Questions whose explanation refers to choice numbers (①②③④) are
left alone. Usage: python scripts/balance_answers.py data/questions/s1.json
"""
import json, sys

path = sys.argv[1]
qs = json.load(open(path, encoding='utf-8'))
slot = 0
for q in qs:
    if any(c in q['explain'] for c in '①②③④') or q.get('fixedOrder'):
        continue
    a = q['answer']
    q['choices'][a], q['choices'][slot] = q['choices'][slot], q['choices'][a]
    q['answer'] = slot
    slot = (slot + 1) % 4
json.dump(qs, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
from collections import Counter
print(path, Counter(q['answer'] for q in qs))
