"""Subject 2 expansion (s2-041~080). Concept questions with public sources + evidence phrases (checked by verify/sources.py).
Textbook-only frameworks (analysis topic 4 types, maturity 4 levels, readiness, org structure types, priority quadrant) have no
public source, so they are not asked here; they stay in the notes as '교재 정리'.
Run: python scripts/new_s2.py -> bank/new_s2.json"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import positions

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
W = 'https://en.wikipedia.org/wiki/'
S = {
    'semi': ('Wikipedia: Semi-structured data', W + 'Semi-structured_data'),
    'unstr': ('Wikipedia: Unstructured data', W + 'Unstructured_data'),
    'prob': ('Wikipedia: Problem statement', W + 'Problem_statement'),
    'poc': ('Wikipedia: Proof of concept', W + 'Proof_of_concept'),
    'crisp': ('Wikipedia: CRISP-DM', W + 'Cross-industry_standard_process_for_data_mining'),
    'kdd': ('Wikipedia: Data mining (KDD process)', W + 'Data_mining'),
    'water': ('Wikipedia: Waterfall model', W + 'Waterfall_model'),
    'spiral': ('Wikipedia: Spiral model', W + 'Spiral_model'),
    'proto': ('Wikipedia: Software prototyping', W + 'Software_prototyping'),
    'agile': ('Wikipedia: Agile software development', W + 'Agile_software_development'),
    'scrum': ('Wikipedia: Scrum (software development)', W + 'Scrum_(software_development)'),
    'tdbu': ('Wikipedia: Top-down and bottom-up design', W + 'Top-down_and_bottom-up_design'),
    'dt': ('Wikipedia: Design thinking', W + 'Design_thinking'),
    'unsup': ('Wikipedia: Unsupervised learning', W + 'Unsupervised_learning'),
    'pmbok': ('Wikipedia: Project Management Body of Knowledge', W + 'Project_Management_Body_of_Knowledge'),
    'roi': ('Wikipedia: Return on investment', W + 'Return_on_investment'),
    'road': ('Wikipedia: Technology roadmap', W + 'Technology_roadmap'),
    'gov': ('Wikipedia: Data governance', W + 'Data_governance'),
    'stew': ('Wikipedia: Data steward', W + 'Data_steward'),
    'mdm': ('Wikipedia: Master data management', W + 'Master_data_management'),
    'dq': ('Wikipedia: Data quality', W + 'Data_quality'),
    'meta': ('Wikipedia: Metadata', W + 'Metadata'),
    'lake': ('Wikipedia: Data lake', W + 'Data_lake'),
}
qs = []


def Q(i, item, tags, level, q, right, wrong, ex, src, ev):
    pos = positions.pos(2, i)
    ch = list(wrong); ch.insert(pos, right)
    qs.append({"id": f"s2-{i:03d}", "subject": 2, "item": item, "tags": tags, "level": level, "q": q, "choices": ch, "answer": pos,
               "explain": ex, "sources": [{"t": S[k][0], "u": S[k][1]} for k in src], "evidence": ev, "checked": "2026-09-30"})


# --- 2-1-1 분석 기획 방향성 도출 (문제 0개였던 항목): 문제 정의, 가용 데이터 유형, 파일럿
Q(41, "2-1-1", ["문제 정의"], "기본", "분석 기획의 출발점으로, 해결해야 할 이슈나 개선할 상황을 명확히 적은 것은?",
  "문제 기술서(Problem statement)", ["데이터 사전", "분석 결과 보고서", "마스터 데이터"],
  "문제 기술서는 다룰 이슈나 개선할 상황을 설명한 것이다. 분석은 무엇을 풀지부터 명확히 해야 방향이 선다.", ["prob"], ["description of an issue to be addressed"])
Q(42, "2-1-1", ["가용 데이터"], "실전", "분석 기획 때 가용 데이터를 검토하다 보니 콜센터 상담 녹취와 고객 후기 텍스트가 대부분이었다. 이 데이터의 유형은?",
  "비정형 데이터", ["정형 데이터", "반정형 데이터", "마스터 데이터"],
  "정해진 데이터 모델이 없고 텍스트가 많은 데이터는 비정형 데이터다. 분석 기획에서는 데이터 유형에 따라 필요한 기술과 비용이 달라진다.", ["unstr"], ["pre-defined data model", "text-heavy"])
Q(43, "2-1-1", ["가용 데이터"], "실전", "웹 서버가 남기는 JSON 형식 로그처럼, 표는 아니지만 키로 구조를 스스로 설명하는 데이터의 유형은?",
  "반정형 데이터", ["정형 데이터", "비정형 데이터", "메타데이터"],
  "반정형 데이터는 고정된 표 구조는 없지만 태그·키로 스스로 구조를 설명(self-describing)한다. JSON·XML이 대표 예이고, JSON처럼 구조를 갖춘 로그 형식도 여기에 속한다.", ["semi"], ["self-describing", "log file formats"])
Q(44, "2-1-1", ["파일럿", "PoC"], "실전", "분석 아이디어나 방법이 실제로 구현 가능한지(실현 가능성) 보여 주려고 핵심 부분을 직접 구현해 보는 것은?",
  "개념 증명(PoC)", ["분석 마스터 플랜 수립", "폭포수 모형", "데이터 거버넌스 체계 수립"],
  "개념 증명(PoC)은 방법이나 아이디어를 구현해 실현 가능성(feasibility)을 보여 주는 것이다.", ["poc"], ["demonstrate its feasibility"])
Q(45, "2-1-1", ["문제 정의"], "고난도", "분석 기획 방향을 잡을 때 가장 먼저 해야 할 일로 적절한 것은?",
  "해결할 이슈와 개선할 상황을 명확히 정의한다", ["가장 최신 알고리즘부터 고른다", "데이터를 모두 모은 뒤 나중에 목적을 정한다", "시각화 도구의 디자인부터 정한다"],
  "분석은 해결할 문제를 명확히 정의하는 데서 시작한다(문제 기술서). 도구·알고리즘 선택은 그다음이다.", ["prob"], ["a condition to be improved upon"])

# --- 2-1-2 분석 방법론: CRISP-DM·KDD·개발 모형
Q(46, "2-1-2", ["분석 방법론", "스크럼"], "실전", "스크럼 팀에서 해야 할 일의 우선순위 목록(백로그)을 관리하고, 팀이 만드는 결과물의 가치를 최대화할 책임을 지는 역할은?",
  "제품 책임자(Product Owner)", ["스크럼 마스터", "개발자", "외부 감사인"],
  "제품 책임자는 제품 백로그를 관리하며 팀이 전달하는 가치를 최대화할 책임이 있다.", ["scrum"], ["product owners manage the product backlog"])
Q(47, "2-1-2", ["분석 방법론", "프로토타이핑"], "고난도", "요구사항을 확인하려고 빠르게 만든 뒤, 최종 결과물에 포함하지 않고 버리는 프로토타입은?",
  "폐기형(Throwaway) 프로토타입", ["진화형(Evolutionary) 프로토타입", "증분형 모듈", "운영 배포판"],
  "폐기형(빠른) 프로토타이핑은 결국 버려질 모델을 만드는 것이다. 진화형은 견고한 프로토타입을 계속 다듬어 최종 결과물로 발전시킨다.", ["proto"], ["eventually be discarded", "evolutionary prototyping"])
Q(48, "2-1-2", ["KDD"], "실전", "KDD 절차에서 '데이터 마이닝'은 어떤 위치에 있는가?",
  "변환 다음, 해석·평가 전 단계", ["선택 바로 다음 단계", "전처리 이전 단계", "절차의 마지막 단계"],
  "KDD는 선택 → 전처리 → 변환 → 데이터 마이닝 → 해석·평가다. 데이터 마이닝은 KDD 과정의 분석 단계다.", ["kdd"], ["selection pre-processing transformation data mining interpretation/evaluation"])
Q(49, "2-1-2", ["분석 방법론", "개발 모형"], "기본", "요구사항 분석부터 설계·구현·테스트까지 앞 단계가 끝나야 다음 단계로 넘어가는 선형 순차 모형은?",
  "폭포수 모형", ["나선형 모형", "프로토타입 모형", "애자일(스크럼)"],
  "폭포수 모형은 순차적 단계로 개발을 진행하는 선형 모형이다.", ["water"], ["linear sequence of steps"])
Q(50, "2-1-2", ["분석 방법론", "개발 모형"], "실전", "요구가 불명확해 사용자가 먼저 만져 볼 수 있는 미완성 버전을 빠르게 만들어 피드백을 받는 접근은?",
  "프로토타이핑", ["폭포수 모형", "데이터 거버넌스", "마스터 플랜"],
  "프로토타이핑은 개발 중인 소프트웨어의 미완성 버전(프로토타입)을 만들어 보는 활동이다.", ["proto"], ["incomplete versions of the software program"])
Q(51, "2-1-2", ["분석 방법론", "개발 모형"], "실전", "고객과의 협업과 변화 대응을 중시하고, 동작하는 결과물을 짧은 주기로 반복해 내놓는 방법론은?",
  "애자일", ["폭포수 모형", "나선형 모형", "V 모형"],
  "애자일 선언은 계약 협상보다 고객 협업, 계획 준수보다 변화 대응, 포괄적 문서보다 동작하는 소프트웨어를 중시한다.", ["agile"], ["customer collaboration over contract negotiation", "responding to change over following a plan"])
Q(52, "2-1-2", ["분석 방법론", "개발 모형"], "기본", "스크럼(Scrum)에서 정해진 짧은 기간 동안 목표한 작업을 끝내는 반복 단위를 부르는 말은?",
  "스프린트", ["마일스톤", "게이트", "베이스라인"],
  "스크럼은 스프린트라는 짧은 반복 단위로 일하며 데일리 스크럼으로 매일 진행 상황을 맞춘다.", ["scrum"], ["sprint", "daily scrum"])

# --- 2-1-3 분석 과제 발굴: 하향식·상향식(빈출), 디자인 싱킹
Q(53, "2-1-3", ["하향식 접근"], "실전", "'매출 감소'라는 큰 문제를 채널별·지역별·상품별 원인으로 잘게 나눠 분석 과제를 도출하는 방식은?",
  "하향식(Top-down) 접근", ["상향식(Bottom-up) 접근", "프로토타이핑", "애자일"],
  "하향식은 큰 문제(시스템)를 작은 부분으로 분해해 나간다. 상향식은 작은 요소를 조합해 더 큰 것을 만든다.", ["tdbu"], ["decomposition"])
Q(54, "2-1-3", ["상향식 접근"], "실전", "정해진 문제 없이, 가진 데이터를 먼저 살펴 조합하면서 새로운 분석 과제를 찾아가는 방식은?",
  "상향식(Bottom-up) 접근", ["하향식(Top-down) 접근", "폭포수 모형", "마스터 플랜"],
  "상향식은 작은 요소(데이터)를 조합해 더 큰 의미를 만들어 가는 방식이다.", ["tdbu"], ["piecing together of systems"])
Q(55, "2-1-3", ["상향식 접근", "비지도학습"], "고난도", "정답(레이블)이 없는 고객 데이터에서 비슷한 고객 묶음을 찾아 새로운 과제를 발굴하려 한다. 이때 주로 쓰는 학습 방식은?",
  "비지도 학습", ["지도 학습", "강화 학습", "전이 학습"],
  "비지도 학습은 레이블 없는 데이터에서 패턴을 찾는다. 상향식 과제 발굴에서 데이터 자체의 구조를 볼 때 쓰인다.", ["unsup"], ["unlabeled data"])
Q(56, "2-1-3", ["디자인 싱킹"], "실전", "디자인 싱킹에서 아이디어를 최대한 넓게 펼친 뒤 가장 나은 것으로 좁혀 가는 두 가지 사고의 조합은?",
  "발산적 사고와 수렴적 사고", ["연역적 사고와 귀납적 사고", "순차적 사고와 병렬적 사고", "정량적 사고와 정성적 사고"],
  "디자인 싱킹의 아이디어 단계는 발산(divergent)과 수렴(convergent) 사고를 번갈아 쓴다.", ["dt"], ["divergent and convergent thinking"])
Q(57, "2-1-3", ["디자인 싱킹"], "기본", "디자인 싱킹에서 사용자 입장을 깊이 이해하는 단계를 부르는 말은?",
  "공감(Empathy)", ["아이디어 도출(Ideation)", "프로토타입(Prototype)", "테스트(Test)"],
  "디자인 싱킹에서 공감(Empathy)은 관찰·인터뷰 등으로 사용자의 경험과 요구를 깊이 이해하는 단계다. 아이디어 도출은 해결책을 넓게 떠올리는 단계, 프로토타입·테스트는 해결책을 만들어 확인하는 단계다.", ["dt"], ["empathy", "ideation"])
Q(58, "2-1-3", ["하향식 접근"], "고난도", "하향식 접근의 설명으로 옳은 것은?",
  "전체 문제를 먼저 정의하고 작은 하위 문제로 나누어 과제를 도출한다",
  ["데이터를 먼저 모은 뒤 의미 있는 패턴에서 문제를 찾는다", "정답이 없는 데이터에서 군집을 먼저 찾는다", "과제 없이 시각화부터 만든다"],
  "하향식은 문제를 분해(decomposition)해 내려가는 방식이다. '데이터에서 패턴을 먼저 찾는다', '정답 없는 데이터에서 군집을 찾는다'는 상향식 접근의 특징이다.", ["tdbu"], ["decomposition"])
Q(59, "2-1-3", ["상향식 접근"], "실전", "상향식 접근이 특히 유용한 상황은?",
  "문제가 명확하지 않아 데이터에서 먼저 단서를 찾아야 할 때", ["해결할 문제가 이미 명확히 정의되어 있을 때", "분석할 데이터가 전혀 없을 때", "결과물을 한 번에 순차 개발해야 할 때"],
  "상향식은 요소(데이터)를 조합해 의미를 만드는 방식이라, 문제가 불명확해 데이터에서 출발해야 할 때 유용하다.", ["tdbu"], ["bottom-up approach is the piecing together"])

# --- 2-1-4 분석 프로젝트 관리: PMBOK 지식 영역·프로세스 그룹
Q(60, "2-1-4", ["PMBOK"], "기본", "분석 프로젝트 중 요청하지 않은 기능이 계속 추가되어 일정이 밀리는 것을 막으려고, 필요한 작업만 빠짐없이 포함되도록 관리하는 PMBOK 지식 영역은?",
  "범위 관리", ["일정 관리", "조달 관리", "원가 관리"],
  "범위 관리는 프로젝트가 필요한 모든 작업, 그리고 필요한 작업만 포함하도록 하는 프로세스다.", ["pmbok"], ["scope management", "all the work required"])
Q(61, "2-1-4", ["PMBOK"], "기본", "외부 업체에서 장비·서비스를 구매·계약하는 활동을 다루는 PMBOK 지식 영역은?",
  "조달 관리", ["범위 관리", "품질 관리", "자원 관리"],
  "조달 관리는 제품·서비스·결과물을 구매하거나 획득하는 프로세스다.", ["pmbok"], ["procurement management", "purchase or acquire products"])
Q(62, "2-1-4", ["PMBOK"], "실전", "프로젝트가 기한 안에 끝나도록 활동 순서와 기간을 관리하는 PMBOK 지식 영역은?",
  "일정 관리", ["범위 관리", "조달 관리", "통합 관리"],
  "일정 관리는 프로젝트를 제때 완료하도록 관리하는 프로세스다.", ["pmbok"], ["schedule management", "timely completion"])
Q(63, "2-1-4", ["PMBOK"], "실전", "프로젝트 영향을 받는 사람·조직을 식별하고 참여를 이끄는 PMBOK 지식 영역은?",
  "이해관계자 관리", ["의사소통 관리", "자원 관리", "조달 관리"],
  "이해관계자 관리(참여)는 프로젝트에 영향을 받는 사람·조직을 식별하고 참여를 관리한다.", ["pmbok"], ["stakeholder engagement", "impacted by"])
Q(64, "2-1-4", ["PMBOK", "프로세스 그룹"], "실전", "PMBOK에서 전통적으로 쓰는 5개 프로세스 그룹의 순서로 옳은 것은?",
  "착수 → 계획 → 실행 → 감시·통제 → 종료", ["계획 → 착수 → 실행 → 종료 → 감시·통제", "착수 → 실행 → 계획 → 감시·통제 → 종료", "계획 → 실행 → 착수 → 종료 → 감시·통제"],
  "PMBOK 프로세스 그룹은 착수(Initiating), 계획(Planning), 실행(Executing), 감시·통제(Monitoring and Controlling), 종료(Closing)다.", ["pmbok"], ["five process groups", "monitoring and controlling", "closing"])
Q(65, "2-1-4", ["PMBOK", "리스크"], "고난도", "분석 과제에서 '원천 데이터 제공이 늦어질 가능성'을 미리 식별하고 대응 계획을 세우는 PMBOK 지식 영역은?",
  "리스크 관리", ["범위 관리", "조달 관리", "의사소통 관리"],
  "리스크 관리는 리스크 관리 계획·식별·분석·대응 계획·통제를 수행한다.", ["pmbok"], ["risk management planning, identification, analysis"])

# --- 2-2-1 마스터 플랜 수립 (문제 0개였던 항목): ROI, 로드맵
Q(66, "2-2-1", ["ROI", "우선순위"], "기본", "여러 분석 과제의 우선순위를 정할 때 '투입 비용 대비 얻는 이익'을 비교하는 지표는?",
  "ROI(투자수익률)", ["KPI 달성률", "데이터 품질 지수", "스프린트 속도"],
  "ROI는 순이익과 투자의 비율로, 투자 대비 효과를 비교할 때 쓴다.", ["roi"], ["ratio between net income and investment"])
Q(67, "2-2-1", ["ROI"], "실전", "분석 과제 A에 1,000만 원을 투자해 투자금을 포함한 총 1,300만 원을 회수했다. ROI는?",
  "30%", ["130%", "23%", "3%"],
  "순이익 = 1,300 - 1,000 = 300만 원, ROI = 순이익 / 투자 = 300 / 1,000 = 30%. 회수액 전체를 투자로 나누면 130%, 순이익을 회수액으로 나누면 약 23%라 틀린다.", ["roi"], ["ratio between net income and investment"])
Q(68, "2-2-1", ["로드맵"], "실전", "마스터 플랜에서 단기·장기 목표를 구체적인 기술·과제와 연결해 단계별 추진 일정을 세운 것은?",
  "로드맵", ["데이터 사전", "혼동행렬", "스프린트 백로그"],
  "로드맵은 단기·장기 목표를 구체적 기술 해결책과 맞춰 전략적·장기 계획을 돕는 유연한 계획이다.", ["road"], ["matching short-term and long-term goals"])
Q(69, "2-2-1", ["로드맵"], "고난도", "분석 로드맵에 대한 설명으로 가장 적절한 것은?",
  "단기 목표와 장기 목표를 연결해 단계적으로 추진할 과제를 배치한 유연한 계획이다",
  ["한 번 정하면 절대 바꿀 수 없는 고정 일정이다", "개별 분석 모델의 하이퍼파라미터 목록이다", "데이터베이스 테이블 정의서다"],
  "로드맵은 전략적·장기 계획을 위한 유연한(flexible) 계획으로, 단기·장기 목표를 맞춘다.", ["road"], ["flexible planning schedule"])
Q(70, "2-2-1", ["ROI"], "고난도", "두 과제의 투자액과 순이익이 A(투자 500, 순이익 100), B(투자 2,000, 순이익 300)일 때 ROI 기준으로 옳은 것은?",
  "A의 ROI(20%)가 B(15%)보다 높다", ["B의 ROI가 더 높다", "두 과제의 ROI가 같다", "순이익이 큰 B가 항상 우선이다"],
  "ROI = 순이익 / 투자: A = 100 / 500 = 20%, B = 300 / 2,000 = 15%. 순이익 규모와 ROI는 다를 수 있다.", ["roi"], ["ratio between net income and investment"])

# --- 2-2-2 분석 거버넌스 체계 수립: 데이터 거버넌스·품질·메타데이터
Q(71, "2-2-2", ["데이터 거버넌스"], "기본", "조직 안에서 데이터를 효과적이고 책임 있게 쓰도록 이끄는 원칙·정책·프로세스의 집합은?",
  "데이터 거버넌스", ["데이터 마이닝", "데이터 레이크", "데이터 마스킹"],
  "데이터 거버넌스는 데이터의 효과적이고 책임 있는 사용을 이끄는 원칙·정책·프로세스다.", ["gov"], ["set of principles, policies, and processes"])
Q(72, "2-2-2", ["데이터 스튜어드"], "실전", "데이터 거버넌스에서 조직 데이터 자산의 품질과 목적 적합성(메타데이터 포함)을 책임지는 역할은?",
  "데이터 스튜어드", ["데이터 엔지니어", "프로젝트 스폰서", "외부 감사인"],
  "데이터 스튜어드는 데이터 자산(메타데이터 포함)의 품질과 목적 적합성을 책임지는 거버넌스 역할이다.", ["stew"], ["fitness for purpose"])
Q(73, "2-2-2", ["마스터 데이터"], "실전", "고객·제품처럼 여러 시스템이 함께 쓰는 핵심 기준 데이터를 일관되고 정확하게 관리하는 활동은?",
  "마스터 데이터 관리(MDM)", ["데이터 마스킹", "데이터 레이크 구축", "OLAP 롤업"],
  "MDM은 기업이 공유하는 공식 마스터 데이터의 균일성·정확성·의미적 일관성을 보장한다.", ["mdm"], ["semantic consistency"])
Q(74, "2-2-2", ["데이터 품질"], "실전", "'고객 테이블의 전화번호 칸이 30% 비어 있다'는 문제는 데이터 품질의 어떤 차원과 가장 관련 깊은가?",
  "완전성(Completeness)", ["적시성(Timeliness)", "유일성(Uniqueness)", "정확성(Accuracy)"],
  "필요한 값이 빠짐없이 채워져 있는지는 완전성이다. 데이터 품질은 정확성·완전성·일관성·신뢰성·목적 적합성 등으로 본다.", ["dq"], ["accuracy, completeness, consistency"])
Q(75, "2-2-2", ["데이터 품질"], "실전", "같은 고객이 두 번 등록되어 중복 레코드가 생긴 문제와 가장 관련 깊은 데이터 품질 차원은?",
  "유일성(Uniqueness)", ["완전성(Completeness)", "적시성(Timeliness)", "유효성(Validity)"],
  "같은 대상이 한 번만 기록되어야 한다는 것이 유일성이다.", ["dq"], ["uniqueness"])
Q(76, "2-2-2", ["데이터 품질"], "고난도", "어제 바뀐 재고 수량이 일주일 뒤에야 분석 시스템에 반영된다. 가장 관련 깊은 데이터 품질 차원은?",
  "적시성(Timeliness)", ["유일성(Uniqueness)", "완전성(Completeness)", "유효성(Validity)"],
  "필요한 시점에 최신 데이터가 제공되는지는 적시성(지연, latency)이다.", ["dq"], ["timeliness or latency"])
Q(77, "2-2-2", ["메타데이터"], "기본", "문서의 작성자·작성일·파일 크기·키워드처럼 데이터를 설명하는 데이터는?",
  "메타데이터", ["마스터 데이터", "트랜잭션 데이터", "원시 데이터"],
  "메타데이터는 데이터를 설명하는 데이터다. 문서의 작성자·작성일·파일 크기·키워드는 설명용(descriptive) 메타데이터의 예다.", ["meta"], ["descriptive metadata for a document might include the author"])
Q(78, "2-2-2", ["데이터 레이크"], "실전", "정형·비정형 데이터를 가공하지 않은 원래 형태 그대로 모아 두는 저장소는?",
  "데이터 레이크", ["데이터 마트", "OLTP 데이터베이스", "데이터 사전"],
  "데이터 레이크는 데이터를 원래(raw) 형식 그대로 저장하는 저장소다.", ["lake"], ["data stored in a raw format"])
Q(79, "2-2-2", ["데이터 거버넌스"], "고난도", "데이터 거버넌스 팀 구성에 대한 설명으로 가장 적절한 것은?",
  "경영진·프로젝트 관리·업무 부서 관리자·데이터 스튜어드가 함께 참여한다",
  ["IT 부서만으로 구성하고 업무 부서는 참여하지 않는다", "데이터 스튜어드 없이 외부 감사인이 데이터 품질을 전담한다", "경영진은 빠지고 데이터 입력 실무자만 참여한다"],
  "데이터 거버넌스 팀은 경영진·프로젝트 관리·업무 부서 관리자·데이터 스튜어드 등으로 구성된다.", ["gov"], ["line-of-business managers , and data stewards"])
Q(80, "2-2-2", ["데이터 품질"], "기본", "데이터 품질의 의미로 가장 적절한 것은?",
  "정확성·완전성·일관성·신뢰성 등을 바탕으로 데이터가 의도한 목적에 맞는 정도",
  ["데이터 용량이 큰 정도", "데이터 파일의 암호화 여부", "데이터베이스 제품의 가격"],
  "데이터 품질은 정확성·완전성·일관성·신뢰성과 목적 적합성으로 본다.", ["dq"], ["fit for its intended purpose"])

json.dump(qs, open(os.path.join(ROOT, 'bank', 'new_s2.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(qs), 'questions -> bank/new_s2.json')
