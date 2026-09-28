# ADsP 무료 문제풀이 (베타)

데이터분석 준전문가(ADsP) 대비 무료 문제풀이 사이트예요. 로그인·서버·광고 없이, 풀이 기록은 브라우저(localStorage)에만 저장돼요.

**사이트:** https://coomind.github.io/adsp-free/

## 무엇이 있나
- 과목별 요약 노트 (공식 출제 기준 항목 순서)
- 유형별 예제, 오늘의 10문제, 오답노트
- 모의고사 (50문항·90분, 과목별 점수와 과락·합격 판정)
- 합격 예측 (확률이 아니라 점수 범위와 상태만, 계산 방법 공개)
- 홈 화면 추가(PWA), 오프라인 열람

## 문제는 어떻게 만들고 검증했나
- 모든 문제는 한국데이터산업진흥원이 공개한 **출제 기준**을 바탕으로 만든 **자체 제작 예상문제**예요. 진흥원이 기출문제의 복제·배포를 허가하지 않기 때문에 기출·복원 문제는 쓰지 않아요.
- 개념 문제: 문제마다 공개 근거 링크(백과사전, TTA 정보통신용어사전, 정부 가이드라인, R 공식 문서)를 달고, 링크를 열어 내용이 일치하는지 확인했어요. 근거를 못 찾은 문제는 뺐어요.
- 계산·R 코드 문제: `verify/s3.R`로 R에서 실제 실행하고, `verify/check.py`가 Python으로 다시 계산해 정답과 비교해요.
  ```
  python verify/check.py
  ```
- 교차 검토: 과목마다 Claude·ChatGPT·Gemini에게 전체 문제를 보여 주고 틀리거나 애매한 문제를 찾게 했어요. 검토 요청문은 `review/`에 있어요.

## 오류 신고
틀린 문제를 찾으면 사이트의 **⚑ 이 문제 오류 신고** 버튼(또는 [Issues](https://github.com/coomind/adsp-free/issues))으로 알려 주세요. 반영되면 원하는 분은 베타 테스터 명단에 이름을 올려 드려요.

## 구조
```
index.html, css/, js/app.js     정적 사이트 (빌드 없음)
data/exam.json                  시험 정보·출제 기준
data/questions/s1~s3.json       문제 (근거 링크, 실행 검증 값 포함)
data/notes/s1~s3.html           요약 노트
data/mock/index.json            모의고사 구성
scripts/                        문제 생성·정답 위치 균형·검토 요청문 생성
verify/                         R 실행 검증 + 전체 점검
```

## 라이선스
- 코드: MIT
- 문제·노트·해설: CC BY-NC 4.0 (출처 표시, 비영리)

made by [@prie.note](https://www.instagram.com/prie.note/)
