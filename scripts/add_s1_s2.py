"""Append 10 sourced questions each to subject 1 (s1-040~049) and subject 2 (s2-031~040). Idempotent.
Every question's source was opened and checked on 2026-09-29."""
import json, os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
W = 'https://en.wikipedia.org/wiki/'
TTA_DS = 'https://terms.tta.or.kr/dictionary/dictionaryView.do?subject=%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EA%B3%BC%ED%95%99%EC%9E%90'
S = {
    'bigdata': ('Wikipedia: Big data (Characteristics)', W + 'Big_data'),
    'dikw': ('Wikipedia: DIKW pyramid', W + 'DIKW_pyramid'),
    'tacit': ('Wikipedia: Tacit knowledge', W + 'Tacit_knowledge'),
    'meta': ('Wikipedia: Metadata', W + 'Metadata'),
    'dw': ('Wikipedia: Data warehouse (Inmon의 특징)', W + 'Data_warehouse'),
    'olap': ('Wikipedia: Online analytical processing (operations)', W + 'Online_analytical_processing'),
    'ttads': ('TTA 정보통신용어사전: 데이터 과학자', TTA_DS),
    'sna': ('Wikipedia: Social network analysis (Centrality)', W + 'Social_network_analysis'),
    'kdd': ('Wikipedia: Data mining (KDD process, Pre-processing)', W + 'Data_mining'),
    'crisp': ('Wikipedia: CRISP-DM', W + 'Cross-industry_standard_process_for_data_mining'),
    'semma': ('Wikipedia: SEMMA', W + 'SEMMA'),
    'pmbok': ('Wikipedia: Project Management Body of Knowledge', W + 'Project_Management_Body_of_Knowledge'),
    'spiral': ('Wikipedia: Spiral model', W + 'Spiral_model'),
}


def Q(sub, i, item, tags, q, ch, a, ex, src, fixed=False):
    d = {"id": f"s{sub}-{i:03d}", "subject": sub, "item": item, "tags": tags, "q": q, "choices": ch, "answer": a,
         "explain": ex, "sources": [{"t": S[k][0], "u": S[k][1]} for k in src], "checked": "2026-09-29"}
    if fixed:
        d["fixedOrder"] = True
    return d


V4 = ["Volume", "Variety", "Velocity", "Veracity"]
S1 = [
    Q(1, 40, "1-2-1", ["빅데이터 특징"], "빅데이터 특징 중 '데이터의 종류와 성격이 정형·반정형·비정형 등으로 다양함'을 뜻하는 것은?", V4, 1,
      "Variety는 데이터의 유형과 성격(다양성)이다. Volume 규모, Velocity 속도, Veracity 신뢰성.", ['bigdata'], True),
    Q(1, 41, "1-2-1", ["빅데이터 특징"], "빅데이터 특징 중 '데이터의 진실성·신뢰성(품질)'을 뜻하는 것은?", V4, 3,
      "Veracity는 데이터의 진실성 또는 신뢰성이다.", ['bigdata'], True),
    Q(1, 42, "1-2-1", ["빅데이터 특징"], "빅데이터 특징 중 '생성·저장되는 데이터의 양'을 뜻하는 것은?", V4, 0,
      "Volume은 생성·저장되는 데이터의 양(규모)이다.", ['bigdata'], True),
    Q(1, 43, "1-1-1", ["DIKW"], "DIKW 피라미드의 가장 위(꼭대기)에 있는 단계는?", ["데이터", "정보", "지식", "지혜"], 3,
      "DIKW는 데이터가 바닥, 지혜가 꼭대기인 위계다.", ['dikw'], True),
    Q(1, 44, "1-1-1", ["암묵지·형식지"], "다음 중 형식지에 해당하는 것은?", ["자전거를 타는 요령", "반죽을 치대는 손 감각", "악기 연주 감각", "회사 업무 매뉴얼"], 3,
      "글·그림으로 옮겨 쉽게 전달되는 지식이 형식지다. 자전거 타기·반죽·악기 연주는 대표적인 암묵지 예다.", ['tacit']),
    Q(1, 45, "1-1-2", ["DB 용어"], "책의 제목·저자·출판일은 그 책에 대한 무엇에 해당하는가?", ["메타데이터", "원시 데이터", "인덱스", "트랜잭션"], 0,
      "다른 데이터의 특징을 정의·설명하는 데이터가 메타데이터다. 책의 제목·저자·출판일이 대표 예다.", ['meta']),
    Q(1, 46, "1-1-3", ["DW"], "여러 운영 시스템에서 온 데이터의 불일치를 없애 일관된 형식으로 모으는 데이터 웨어하우스의 특징은?",
      ["주제지향적", "통합적", "시계열적", "비휘발적"], 1,
      "여러 원천 시스템의 불일치를 제거해 하나로 맞추는 것이 통합적(integrated) 특징이다.", ['dw'], True),
    Q(1, 47, "1-1-3", ["OLAP"], "OLAP에서 요약된 데이터에서 더 세부적인 데이터로 내려가며 살펴보는 연산은?", ["드릴다운", "롤업", "슬라이싱", "ETL"], 0,
      "드릴다운은 세부 내용으로 내려가 탐색하는 연산이다. 롤업(통합)은 반대로 한 차원 이상에서 데이터를 집계한다.", ['olap']),
    Q(1, 48, "1-3-2", ["데이터 사이언티스트"], "분석 결과를 기획자·경영진 등 이해관계자에게 시각 자료와 비기술적 언어로 전달해 의사결정으로 연결하는 역량은?",
      ["도메인 지식과 의사소통 능력", "데이터 수집 및 처리 역량", "통계적 모델링 역량", "알고리즘 구현 속도"], 0,
      "TTA 용어사전은 데이터 과학자의 주요 역량으로 데이터 수집·처리, 통계적 모델링·알고리즘 활용, 도메인 지식과 의사소통 능력을 들고, 결과를 이해관계자에게 전달하는 것을 의사소통 능력으로 설명한다.", ['ttads']),
    Q(1, 49, "1-2-3", ["활용 테크닉"], "소셜 네트워크 분석에서 노드의 '중요도·영향력'을 수치로 나타내는 지표는?", ["중심성", "지지도", "신뢰도", "엔트로피"], 0,
      "중심성(centrality)은 네트워크에서 노드의 중요도나 영향력을 수치화하는 지표다. 지지도·신뢰도는 연관분석, 엔트로피는 불순도 지표다.", ['sna']),
]
S2 = [
    Q(2, 31, "2-1-2", ["KDD"], "KDD 절차에서 '데이터 마이닝' 바로 다음 단계는?", ["데이터셋 선택", "전처리", "변환", "결과 해석·평가"], 3,
      "KDD는 선택 → 전처리 → 변환 → 데이터 마이닝 → 결과 해석·평가다.", ['kdd'], True),
    Q(2, 32, "2-1-2", ["KDD"], "KDD 절차에서 '전처리' 바로 다음 단계는?", ["데이터셋 선택", "전처리", "변환", "데이터 마이닝"], 2,
      "전처리 다음은 변환(Transformation), 그다음이 데이터 마이닝이다.", ['kdd'], True),
    Q(2, 33, "2-1-2", ["CRISP-DM"], "CRISP-DM에서 '데이터 준비' 바로 다음 단계는?", ["데이터 이해", "모델링", "평가", "전개"], 1,
      "데이터 준비 다음은 모델링(Modeling)이다.", ['crisp']),
    Q(2, 34, "2-1-2", ["SEMMA"], "SEMMA에서 'Explore' 바로 다음 단계는?", ["Sample", "Modify", "Model", "Assess"], 1,
      "SEMMA는 Sample → Explore → Modify → Model → Assess다.", ['semma'], True),
    Q(2, 35, "2-1-4", ["프로젝트 관리"], "프로젝트의 비용을 계획·추정하고 예산을 세워 통제하는 영역은 PMBOK의 10개 지식 영역 중 무엇인가?",
      ["원가 관리", "조달 관리", "범위 관리", "자원 관리"], 0,
      "원가 관리(Cost Management)는 비용 계획·추정·예산 수립·통제를 다룬다.", ['pmbok']),
    Q(2, 36, "2-1-4", ["프로젝트 관리"], "품질 정책·목표·책임을 정하는 영역은 PMBOK의 10개 지식 영역 중 무엇인가?",
      ["품질 관리", "리스크 관리", "통합 관리", "일정 관리"], 0,
      "품질 관리(Quality Management)는 품질 정책·목표·책임을 정한다.", ['pmbok']),
    Q(2, 37, "2-1-4", ["프로젝트 관리"], "프로젝트 정보를 제때 적절하게 계획·수집·생성·배포하는 영역은 PMBOK의 10개 지식 영역 중 무엇인가?",
      ["의사소통 관리", "이해관계자 관리", "자원 관리", "조달 관리"], 0,
      "의사소통 관리(Communications Management)는 프로젝트 정보의 적시·적절한 계획·수집·생성·배포를 다룬다.", ['pmbok']),
    Q(2, 38, "2-1-4", ["프로젝트 관리"], "여러 프로젝트 관리 활동을 식별·정의·결합·조정해 하나로 묶는 영역은 PMBOK의 10개 지식 영역 중 무엇인가?",
      ["통합 관리", "범위 관리", "품질 관리", "의사소통 관리"], 0,
      "통합 관리(Integration Management)는 여러 프로세스와 활동을 식별·정의·결합·통일·조정한다.", ['pmbok']),
    Q(2, 39, "2-1-4", ["프로젝트 관리"], "프로젝트 팀을 조직·관리·이끄는 영역은 PMBOK의 10개 지식 영역 중 무엇인가?",
      ["자원 관리", "조달 관리", "원가 관리", "리스크 관리"], 0,
      "자원 관리(Resource Management, 이전 명칭 인적자원 관리)는 프로젝트 팀을 조직·관리·이끈다.", ['pmbok']),
    Q(2, 40, "2-1-2", ["분석 방법론 모델"], "나선형 모델이 폭포수·점진적·진화적 프로토타이핑 가운데 어떤 방식의 요소를 쓸지 정하는 기준은?",
      ["프로젝트의 위험 패턴", "코드 줄 수", "개발자 선호", "최소 비용만"], 0,
      "나선형 모델은 위험 중심(risk-driven)으로, 프로젝트 고유의 위험 패턴에 따라 다른 모델의 요소를 채택한다.", ['spiral']),
]

for sub, new in ((1, S1), (2, S2)):
    p = os.path.join(ROOT, 'data', 'questions', f's{sub}.json')
    qs = json.load(open(p, encoding='utf-8'))
    have = {q['id'] for q in qs}
    qs += [q for q in new if q['id'] not in have]
    json.dump(qs, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(p, len(qs))
