"""Build the cross-review prompt for one subject (pasted once into each external model).
Usage: python scripts/review_prompt.py 2   -> review/s2_review_prompt.txt"""
import json, os, sys

s = sys.argv[1]
root = os.path.join(os.path.dirname(__file__), '..')
exam = json.load(open(os.path.join(root, 'data', 'exam.json'), encoding='utf-8'))
name = next(x['name'] for x in exam['subjects'] if str(x['id']) == s)
qs = json.load(open(os.path.join(root, 'data', 'questions', f's{s}.json'), encoding='utf-8'))
N = '①②③④'
out = [f"다음은 ADsP(데이터분석 준전문가) {s}과목 '{name}' 대비로 직접 만든 4지선다 예상문제 {len(qs)}개입니다. 각 문제에 우리가 정한 정답과 해설을 붙였습니다.",
       "",
       "요청: 틀리거나, 애매하거나, 복수정답인 문제를 찾아 주세요. 문제가 없다고 판단하더라도 가장 약한 3문제를 골라 이유와 함께 알려 주세요.",
       "답변 형식: [문제 ID] 판정(정답오류/복수정답/애매/해설오류/약함) - 이유 - 수정 제안",
       ""]
for q in qs:
    out.append(f"[{q['id']}] {q['q']}")
    if q.get('code'):
        out.append(q['code'])
    out += [f"  {N[i]} {c}" for i, c in enumerate(q['choices'])]
    out.append(f"  정답: {N[q['answer']]} / 해설: {q['explain']}")
    out.append("")
os.makedirs(os.path.join(root, 'review'), exist_ok=True)
path = os.path.join(root, 'review', f's{s}_review_prompt.txt')
open(path, 'w', encoding='utf-8').write('\n'.join(out))
print(path, len('\n'.join(out)))
