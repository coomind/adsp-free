"""Subject 1 expansion (s1-050~089). Concept questions only: every one cites a public page and lists `evidence`
phrases that verify/sources.py must find in that page. Stems are written from the exam outline, never from past exams.
Priorities: empty outline items first (1-2-2, 1-2-5, 1-3-1, 1-3-3), then frequent topics (data/freq.json).
Run: python scripts/new_s1.py  -> bank/new_s1.json"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import positions

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
W = 'https://en.wikipedia.org/wiki/'
S = {
    'seci': ('Wikipedia: SECI model of knowledge dimensions', W + 'SECI_model_of_knowledge_dimensions'),
    'semi': ('Wikipedia: Semi-structured data', W + 'Semi-structured_data'),
    'unstr': ('Wikipedia: Unstructured data', W + 'Unstructured_data'),
    'oltp': ('Wikipedia: Online transaction processing', W + 'Online_transaction_processing'),
    'olap': ('Wikipedia: Online analytical processing', W + 'Online_analytical_processing'),
    'crm': ('Wikipedia: Customer relationship management', W + 'Customer_relationship_management'),
    'erp': ('Wikipedia: Enterprise resource planning', W + 'Enterprise_resource_planning'),
    'scm': ('Wikipedia: Supply chain management', W + 'Supply_chain_management'),
    'bi': ('Wikipedia: Business intelligence', W + 'Business_intelligence'),
    'bigdata': ('Wikipedia: Big data', W + 'Big_data'),
    'arl': ('Wikipedia: Association rule learning', W + 'Association_rule_learning'),
    'senti': ('Wikipedia: Sentiment analysis', W + 'Sentiment_analysis'),
    'sna': ('Wikipedia: Social network analysis', W + 'Social_network_analysis'),
    'ga': ('Wikipedia: Genetic algorithm', W + 'Genetic_algorithm'),
    'kanon': ('Wikipedia: k-anonymity', W + 'K-anonymity'),
    'ldiv': ('Wikipedia: l-diversity', W + 'L-diversity'),
    'tclose': ('Wikipedia: t-closeness', W + 'T-closeness'),
    'pseudo': ('Wikipedia: Pseudonymization', W + 'Pseudonymization'),
    'mask': ('Wikipedia: Data masking', W + 'Data_masking'),
    'dataf': ('Wikipedia: Datafication', W + 'Datafication'),
    'presc': ('Wikipedia: Prescriptive analytics', W + 'Prescriptive_analytics'),
    'gft': ('Wikipedia: Google Flu Trends', W + 'Google_Flu_Trends'),
    'ds': ('Wikipedia: Data science', W + 'Data_science'),
}
qs = []


def Q(i, item, tags, level, q, right, wrong, ex, src, ev):
    """right answer + 3 wrong choices; the right answer's position rotates with the id (balanced positions)"""
    pos = positions.pos(1, i)
    ch = list(wrong); ch.insert(pos, right)
    qs.append({"id": f"s1-{i:03d}", "subject": 1, "item": item, "tags": tags, "level": level, "q": q, "choices": ch, "answer": pos,
               "explain": ex, "sources": [{"t": S[k][0], "u": S[k][1]} for k in src], "evidence": ev, "checked": "2026-09-30"})


# --- 1-1-1 데이터와 정보: 지식 변환(SECI) — 빈출
Q(50, "1-1-1", ["지식 변환", "SECI"], "실전", "신입 직원이 선배 옆에서 함께 일하며 말로 설명하기 어려운 요령을 몸으로 익혔다. 이 지식 변환 과정은?",
  "공통화(Socialization)", ["표출화(Externalization)", "연결화(Combination)", "내면화(Internalization)"],
  "암묵지가 함께 일하는 경험을 통해 다른 사람의 암묵지로 옮겨 가는 것이 공통화(암묵지 → 암묵지)다.", ["seci"], ["from tacit knowledge to tacit knowledge ( socialization )"])
Q(51, "1-1-1", ["지식 변환", "SECI"], "실전", "숙련 기술자의 노하우를 인터뷰해 작업 매뉴얼 문서로 만들었다. 이 지식 변환 과정은?",
  "표출화(Externalization)", ["공통화(Socialization)", "연결화(Combination)", "내면화(Internalization)"],
  "머릿속 암묵지를 글·그림 같은 형식지로 옮기는 것이 표출화(암묵지 → 형식지)다.", ["seci"], ["externalization (tacit to explicit)"])
Q(52, "1-1-1", ["지식 변환", "SECI"], "실전", "부서마다 따로 있던 보고서들을 모아 하나의 통합 지침서로 재구성했다. 이 지식 변환 과정은?",
  "연결화(Combination)", ["공통화(Socialization)", "표출화(Externalization)", "내면화(Internalization)"],
  "이미 문서로 된 형식지들을 모아 새로운 형식지로 체계화하는 것이 연결화(형식지 → 형식지)다.", ["seci"], ["combination (explicit to explicit)"])
Q(53, "1-1-1", ["지식 변환", "SECI"], "실전", "직원이 업무 매뉴얼을 읽고 실제로 반복해 적용하면서 자기 몸에 밴 요령으로 만들었다. 이 지식 변환 과정은?",
  "내면화(Internalization)", ["공통화(Socialization)", "표출화(Externalization)", "연결화(Combination)"],
  "형식지를 읽고 실행하며 개인의 암묵지로 체화하는 것이 내면화(형식지 → 암묵지)다.", ["seci"], ["internalization (explicit to tacit)"])
Q(54, "1-1-1", ["데이터 유형"], "기본", "JSON이나 XML처럼 데이터 안에 태그·키로 구조 정보가 함께 들어 있는 데이터는?",
  "반정형 데이터", ["정형 데이터", "비정형 데이터", "메타데이터만 있는 데이터"],
  "반정형 데이터는 고정된 표 구조는 아니지만 태그·키 같은 표시로 스스로 구조를 설명한다(self-describing). JSON·XML이 대표 예다.", ["semi"], ["self-describing", "json", "xml"])
Q(55, "1-1-1", ["데이터 유형"], "기본", "미리 정해진 데이터 모델이 없고 주로 글·이미지 형태인 고객 리뷰, 상담 녹취 같은 데이터는?",
  "비정형 데이터", ["정형 데이터", "반정형 데이터", "트랜잭션 데이터"],
  "비정형 데이터는 미리 정의된 데이터 모델이 없거나 정해진 방식으로 정리되지 않은 데이터로, 텍스트가 많은 경우가 흔하다.", ["unstr"], ["pre-defined data model", "text-heavy"])

# --- 1-1-3 데이터베이스 활용: OLTP·OLAP(빈출), 기업 내부 시스템
Q(56, "1-1-3", ["OLTP", "OLAP"], "실전", "은행 창구에서 입출금 거래를 실시간으로 처리하고 기록하는 시스템에 가장 가까운 것은?",
  "OLTP", ["OLAP", "데이터 마이닝", "ETL"],
  "OLTP는 거래(트랜잭션) 중심 업무를 실시간으로 처리하는 운영계 시스템이다. OLAP은 쌓인 데이터를 다차원으로 분석하는 쪽이다.", ["oltp"], ["transaction-oriented applications"])
Q(57, "1-1-3", ["OLTP", "OLAP"], "실전", "지역·기간·상품별 매출을 여러 관점으로 빠르게 집계하고 비교하는 데 가장 적합한 방식은?",
  "OLAP", ["OLTP", "트랜잭션 로그 복구", "정규화"],
  "OLAP은 다차원 분석 질의(multi-dimensional analytical queries)에 빠르게 답하기 위한 방식이다.", ["olap"], ["multi-dimensional analytical (mda) queries"])
Q(58, "1-1-3", ["OLAP"], "고난도", "OLAP 연산 중 '월별 매출'을 '분기별 매출'로 묶어 더 높은 수준으로 요약하는 것은?",
  "롤업(Roll-up)", ["드릴다운(Drill-down)", "슬라이싱(Slicing)", "피벗(Pivot)"],
  "롤업(통합)은 데이터를 한 차원 이상에서 더 높은 수준으로 집계하는 연산이다. 드릴다운은 반대로 세부로 내려간다.", ["olap"], ["consolidation (roll-up)", "drill-down"])
Q(59, "1-1-3", ["기업 내부 시스템"], "기본", "고객과의 모든 접점(상담·구매·문의) 이력을 관리해 관계를 강화하려는 시스템은?",
  "CRM", ["ERP", "SCM", "OLTP"],
  "CRM(고객관계관리)은 고객과의 상호작용을 관리하는 과정·시스템이다.", ["crm"], ["interactions with customers"])
Q(60, "1-1-3", ["OLAP"], "실전", "OLAP 큐브에서 '2025년' 데이터만 잘라 낸 뒤, 그 조각을 지역·상품 등 다른 관점으로 돌려 보는 기능은?",
  "슬라이싱과 다이싱", ["롤업", "드릴다운", "정규화"],
  "슬라이싱은 큐브에서 특정 데이터 조각을 잘라 내는 것, 다이싱은 그 조각을 여러 관점으로 보는 것이다. 롤업은 요약 수준을 높이고, 드릴다운은 세부로 내려간다.", ["olap"], ["take out (slicing) a specific set of data of the olap cube"])
Q(61, "1-1-3", ["기업 내부 시스템"], "기본", "원자재 조달부터 생산·유통·판매까지 물자와 서비스의 흐름을 관리하는 시스템은?",
  "SCM", ["CRM", "ERP", "OLAP"],
  "SCM(공급망관리)은 재화와 서비스의 흐름을 관리한다.", ["scm"], ["flow of goods and services"])

# --- 1-2-1 빅데이터의 이해
Q(62, "1-2-1", ["빅데이터 특징"], "실전", "센서가 초마다 쏟아내는 데이터를 실시간으로 받아 바로 처리해야 하는 상황과 가장 관련 깊은 빅데이터 특징은?",
  "Velocity", ["Volume", "Variety", "Veracity"],
  "생성·처리 속도가 빠른 것이 Velocity다. 양은 Volume, 다양성은 Variety, 신뢰성은 Veracity.", ["bigdata"], ["volume , variety , and velocity"])
Q(63, "1-2-1", ["빅데이터 정의"], "기본", "빅데이터를 설명한 것으로 가장 적절한 것은?",
  "기존 데이터 처리 소프트웨어로 다루기 어려울 만큼 크거나 복잡한 데이터",
  ["항상 정형 데이터만으로 이루어진 데이터", "용량이 1TB를 넘는 모든 데이터", "관계형 데이터베이스에 저장된 데이터 전체"],
  "빅데이터는 전통적인 처리 소프트웨어로 다루기에 너무 크거나 복잡한 데이터를 가리킨다. 정해진 용량 기준은 없다.", ["bigdata"], ["too large or complex to be dealt with by traditional data-processing software"])

# --- 1-2-2 빅데이터의 가치와 영향 (문제 0개였던 항목)
Q(64, "1-2-2", ["빅데이터 가치"], "실전", "빅데이터 분석이 주는 가치로 볼 수 있는 것은?",
  "대량의 데이터에서 새로운 상관관계를 찾아 경향을 파악하고 질병 예방 등에 활용한다",
  ["데이터가 많을수록 인과관계가 자동으로 증명된다", "분석하지 않아도 저장만 하면 가치가 생긴다", "데이터 품질과 무관하게 결론이 항상 옳다"],
  "대량 데이터 분석으로 새로운 상관관계를 찾아 비즈니스 경향 파악·질병 예방 등에 쓸 수 있다. 상관관계가 곧 인과관계는 아니다.", ["bigdata"], ["find new correlations"])
Q(65, "1-2-2", ["빅데이터 영향"], "기본", "빅데이터가 활용되는 분야로 가장 거리가 먼 것은?",
  "데이터 없이 경험만으로 결정하는 전통 방식 유지", ["정부 정책", "의료(헬스케어)", "마케팅"],
  "빅데이터는 정부·국제개발·금융·의료·교육·미디어·보험·사물인터넷·마케팅 등 폭넓게 활용된다.", ["bigdata"], ["government", "healthcare", "marketing"])
Q(66, "1-2-2", ["빅데이터 가치", "위험"], "고난도", "빅데이터의 '가치(Value)'를 정확히 산정하기 어려운 이유와 가장 거리가 먼 것은?",
  "데이터가 한 번 분석되면 다른 목적으로는 재사용할 수 없기 때문에",
  ["같은 데이터도 어떤 목적으로 재사용하느냐에 따라 가치가 달라지기 때문에", "지금은 없는 분석 기법이 나중에 새로운 가치를 만들 수 있기 때문에", "데이터를 조합하면서 처음 수집 목적과 다른 가치가 생기기 때문에"],
  "데이터는 재사용·재조합·새 기법으로 가치가 계속 바뀌어 한 번에 값을 매기기 어렵다. '한 번 쓰면 재사용 불가'는 오히려 반대다. 빅데이터 문헌도 가치를 조직이 '만들고 잡아내는(create and capture value)' 역량의 문제로 본다.", ["bigdata"], ["create and capture value from big data"])
Q(67, "1-2-2", ["빅데이터 영향"], "실전", "빅데이터 기술 발달이 사회에 준 영향으로 가장 적절한 것은?",
  "건강·고용·범죄·재난 등 개발 분야의 의사결정 개선에 활용될 수 있다",
  ["데이터 분석 인력의 필요가 사라졌다", "개인정보 문제는 더 이상 생기지 않는다", "표본을 뽑는 조사는 모두 금지되었다"],
  "빅데이터는 의료·고용·경제·범죄·안전·재난 같은 분야의 의사결정 개선에 쓰일 수 있다. 동시에 개인정보(privacy) 문제는 여전히 핵심 과제다.", ["bigdata"], ["improve decision-making in critical development areas", "privacy"])

# --- 1-2-3 비즈니스 모델: 분석 기법 활용 사례(빈출)
Q(68, "1-2-3", ["분석 기법 활용"], "실전", "마트가 '기저귀를 사는 고객은 맥주도 함께 산다' 같은 구매 패턴을 찾으려 할 때 알맞은 분석 기법은?",
  "연관 규칙 학습(장바구니 분석)", ["감성 분석", "유전 알고리즘", "회귀 분석"],
  "함께 구매되는 품목의 규칙을 찾는 것이 연관 규칙 학습(장바구니 분석)이다.", ["arl"], ["market basket analysis"])
Q(69, "1-2-3", ["분석 기법 활용"], "실전", "신제품 출시 뒤 SNS 게시글에 나타난 고객의 긍정·부정 반응을 파악하려 할 때 알맞은 분석 기법은?",
  "감성 분석(오피니언 마이닝)", ["연관 규칙 학습", "유전 알고리즘", "군집 분석"],
  "텍스트에서 주관적 정보와 감정 상태를 추출하는 것이 감성 분석(opinion mining)이다.", ["senti"], ["opinion mining", "subjective information"])
Q(70, "1-2-3", ["분석 기법 활용"], "실전", "사용자 간 친구 관계에서 영향력이 큰 '인플루언서'를 찾으려 할 때 알맞은 분석 기법은?",
  "소셜 네트워크 분석", ["감성 분석", "연관 규칙 학습", "유전 알고리즘"],
  "소셜 네트워크 분석은 노드(사람)와 관계(연결)로 구조를 보고, 중심성 같은 지표로 영향력 있는 노드를 찾는다.", ["sna"], ["nodes", "centrality"])
Q(71, "1-2-3", ["분석 기법 활용"], "고난도", "택배 차량 수십 대의 배송 경로 조합 중 좋은 해를, 해 후보를 교배·변이시키며 세대를 거듭해 찾으려 한다. 알맞은 기법은?",
  "유전 알고리즘", ["감성 분석", "연관 규칙 학습", "소셜 네트워크 분석"],
  "유전 알고리즘은 자연선택에서 착안해 선택·교차·변이를 반복하며 최적해에 가까운 해를 찾는다.", ["ga"], ["natural selection", "mutation, crossover"])
Q(72, "1-2-3", ["기업 내부 시스템"], "기본", "기업 데이터를 분석해 경영 전략과 운영 의사결정에 쓰이는 정보를 제공하는 기술·전략을 통틀어 부르는 말은?",
  "BI(비즈니스 인텔리전스)", ["OLTP", "SCM", "ETL"],
  "BI는 비즈니스 정보를 분석·관리해 전략과 운영을 뒷받침하는 기술과 전략이다.", ["bi"], ["business information to inform business strategies"])

# --- 1-2-4 위기 요인과 통제 방안: 비식별화 기법(빈출)
Q(73, "1-2-4", ["비식별화", "가명처리"], "실전", "이름·주민번호 같은 식별 항목을 임의의 코드(가명)로 바꾸되, 추가 정보가 있으면 다시 식별될 수 있는 처리는?",
  "가명처리", ["익명화", "총계처리", "데이터 삭제"],
  "가명처리는 식별 항목을 인위적 식별자(가명)로 바꾸는 것으로, 추가 정보와 결합하면 재식별될 수 있다. 익명화는 재식별 자체를 막는 것이 목적이다.", ["pseudo"], ["artificial identifiers", "re-identified"])
Q(74, "1-2-4", ["비식별화", "마스킹"], "기본", "민감한 값을 알아볼 수 없게 바꾸되 형식은 유지해, 권한 없는 사람에게는 쓸모없게 만드는 처리는?",
  "데이터 마스킹", ["데이터 정규화", "데이터 백업", "데이터 암호 해독"],
  "데이터 마스킹(난독화)은 민감한 데이터를 권한 없는 사람에게 가치가 없도록 바꾸는 과정이다.", ["mask"], ["modifying sensitive data"])
Q(75, "1-2-4", ["비식별화", "k-익명성"], "고난도", "k-익명성에 대한 설명으로 옳은 것은?",
  "준식별자 조합이 같은 레코드가 적어도 k개 이상이 되도록 만들어 특정인을 구분하기 어렵게 한다",
  ["민감한 속성 값이 그룹 안에서 적어도 k가지 이상 나오도록 한다", "민감한 속성의 분포가 전체 분포와 k 이하로 차이 나도록 한다", "모든 레코드를 k번 복제해 저장한다"],
  "k-익명성은 서로 다른 준식별자 조합마다 적어도 k개 레코드가 있도록 한다. '민감한 값이 k가지 이상'은 l-다양성, '분포 차이가 일정 이하'는 t-근접성 설명이다.", ["kanon"], ["quasi-identifiers", "at least k records"])
Q(76, "1-2-4", ["비식별화", "l-다양성"], "고난도", "k-익명성을 만족해도 한 그룹의 민감한 값이 모두 같으면 그 값이 드러나는 동질성 공격을 막기 위해 나온 모델은?",
  "l-다양성", ["k-익명성", "t-근접성", "가명처리"],
  "l-다양성은 그룹 안의 민감한 값이 다양하도록 요구해 동질성(homogeneity) 문제를 보완한다.", ["ldiv", "kanon"], ["homogeneity", "l -diversity"])
Q(77, "1-2-4", ["비식별화", "t-근접성"], "고난도", "그룹 안의 민감한 속성 분포가 전체 데이터의 분포와 일정 수준 이하로만 차이 나도록 하는 모델은?",
  "t-근접성", ["k-익명성", "l-다양성", "데이터 마스킹"],
  "t-근접성은 그룹 내 민감 속성 분포와 전체 분포 사이의 거리가 t 이하가 되도록 한다.", ["tclose"], ["distribution of a sensitive attribute"])
Q(78, "1-2-4", ["비식별화", "k-익명성"], "실전", "나이 '34'를 '30대'로, 주소 '서울시 마포구 ○○동'을 '서울시'로 바꾸는 비식별 방법은?",
  "일반화(범주화)", ["삭제(억제)", "가명처리", "암호화"],
  "개별 값을 더 넓은 범주로 바꾸는 것이 일반화(generalization)다. 값을 '*'로 지우는 것은 억제(suppression)다.", ["kanon"], ["generalization", "suppression"])

# --- 1-2-5 미래의 빅데이터 (문제 0개였던 항목)
Q(79, "1-2-5", ["데이터화"], "기본", "SNS 활동, 걸음 수, 위치 이동처럼 생활의 여러 측면이 데이터로 바뀌어 가는 흐름을 가리키는 말은?",
  "데이터화(Datafication)", ["정규화(Normalization)", "비식별화(De-identification)", "시각화(Visualization)"],
  "데이터화는 생활의 많은 측면을 데이터로 바꾸고, 이를 정보·가치로 전환하는 기술 흐름이다.", ["dataf"], ["turning many aspects of our life into data"])
Q(80, "1-2-5", ["데이터화"], "실전", "웨어러블 기기와 건강 앱이 늘면서 생긴 변화로 '데이터화'의 예에 가장 가까운 것은?",
  "운동량·수면 같은 개인 건강 활동이 자동으로 기록되어 분석 대상이 된다",
  ["건강 기록을 모두 종이로만 보관한다", "개인 데이터 수집이 전면 금지된다", "병원 방문 기록이 더 이상 남지 않는다"],
  "웨어러블 기기·건강 앱은 생활을 데이터로 바꾸는 데이터화의 대표 예다.", ["dataf"], ["wearable fitness and health devices"])
Q(81, "1-2-5", ["사물인터넷"], "기본", "앞으로 빅데이터의 양을 크게 늘릴 요인으로, 기기·센서가 네트워크에 연결되어 데이터를 주고받는 환경은?",
  "사물인터넷(IoT)", ["OLTP", "정규화", "메인프레임"],
  "사물인터넷(IoT)은 빅데이터의 주요 원천이자 활용 분야다.", ["bigdata"], ["internet of things (iot)"])

# --- 1-3-1 빅데이터분석과 전략 인사이트 (문제 0개였던 항목)
Q(82, "1-3-1", ["분석 단계"], "실전", "'무슨 일이 일어났는가'를 요약하는 분석에서 나아가, 앞으로 일어날 일뿐 아니라 '어떻게 대응해야 하는가'까지 제안하는 분석은?",
  "처방적 분석(Prescriptive analytics)", ["기술적 분석(Descriptive analytics)", "예측적 분석(Predictive analytics)", "탐색적 자료 분석(EDA)"],
  "비즈니스 분석은 기술적 → 예측적 → 처방적 순으로 나아간다. 처방적 분석은 무엇이 언제·왜 일어날지 예상하고 대응 방안(의사결정 선택지)까지 제시한다.", ["presc"], ["descriptive analytics", "predictive analytics", "suggests decision options"])
Q(83, "1-3-1", ["분석 단계"], "기본", "현재 기업 분석의 대부분을 차지하며, 과거 데이터를 요약해 무슨 일이 있었는지 보여 주는 첫 단계 분석은?",
  "기술적 분석(Descriptive analytics)", ["처방적 분석(Prescriptive analytics)", "예측적 분석(Predictive analytics)", "인과 추론(Causal inference)"],
  "기술적 분석이 비즈니스 분석의 첫 단계이며 지금도 대부분을 차지한다.", ["presc"], ["the first stage of business analytics is descriptive analytics"])
Q(84, "1-3-1", ["전략 인사이트"], "고난도", "빅데이터 분석에서 전략적 인사이트를 얻는 데 가장 중요한 태도는?",
  "상관관계를 발견하면 인과관계인지 따로 검토하고 비즈니스 맥락과 연결해 해석한다",
  ["데이터가 많으면 상관관계를 곧 인과관계로 받아들인다", "분석 결과는 맥락 없이 수치만 보고한다", "기존 업무에 맞는 결과만 골라 쓴다"],
  "빅데이터는 새로운 상관관계를 찾게 해 주지만, 인과 효과를 추론하려면 따로 검토가 필요하다. 인사이트는 결과를 맥락과 연결할 때 나온다.", ["bigdata"], ["find new correlations", "causal effects"])

# --- 1-3-2 필요 역량(빈출: 데이터 사이언티스트 역량)
Q(85, "1-3-2", ["데이터 사이언티스트"], "실전", "데이터 사이언스를 설명한 것으로 가장 적절한 것은?",
  "통계·컴퓨팅·도메인 지식을 결합해 데이터에서 지식과 인사이트를 얻는 학제 간 분야",
  ["통계학 이론만 다루는 순수 학문", "데이터베이스 관리자의 백업 업무", "프로그래밍 언어 문법을 연구하는 분야"],
  "데이터 사이언스는 통계·과학적 컴퓨팅 등을 쓰는 학제 간(interdisciplinary) 분야로, 응용 분야의 도메인 지식을 통합한다.", ["ds"], ["interdisciplinary academic field", "domain knowledge"])
Q(86, "1-3-2", ["데이터 사이언티스트"], "실전", "데이터 사이언스에 필요한 역량으로 거론되는 것 중, 분석 결과를 다른 사람에게 전달하는 소프트 스킬에 해당하는 것은?",
  "커뮤니케이션(소통)", ["통계학", "컴퓨터 과학", "수학"],
  "데이터 사이언스는 컴퓨터 과학·수학·시각화·그래픽 디자인·커뮤니케이션·비즈니스 등을 아우른다. 이 중 결과 전달은 커뮤니케이션 역량이다.", ["ds"], ["communication"])

# --- 1-3-3 빅데이터 그리고 데이터 사이언스의 미래 (문제 0개였던 항목): 한계와 신뢰
Q(87, "1-3-3", ["빅데이터 한계"], "고난도", "검색어 데이터로 독감 유행을 예측한 구글 독감 트렌드가 여러 해 동안 실제보다 크게 예측한 사례가 주는 교훈은?",
  "데이터가 많아도 모형과 데이터의 한계를 검증하지 않으면 예측이 틀릴 수 있다",
  ["검색어 데이터는 어떤 예측에도 쓸 수 없다", "데이터가 많으면 검증 없이도 정확하다", "독감 통계는 공개되지 않아 비교할 수 없다"],
  "구글 독감 트렌드는 검색어를 모아 독감 활동을 예측했지만 2011~2013년 계속 과대 예측했다. 빅데이터도 검증과 한계 인식이 필요하다.", ["gft"], ["google search queries", "overestimated"])
Q(88, "1-3-3", ["빅데이터 한계"], "실전", "빅데이터 연구에서 데이터가 많아도 여전히 주의해야 할 점으로 가장 적절한 것은?",
  "표본(샘플링) 방식과 데이터의 신뢰성(Veracity)",
  ["저장 장치의 색상", "데이터 파일 이름의 길이", "분석 도구의 로고"],
  "빅데이터에도 표본 추출 문제가 남고, 데이터 신뢰성(Veracity)이 부족하면 분석 결과를 믿기 어렵다.", ["bigdata"], ["sampling big data", "veracity"])
Q(89, "1-3-3", ["데이터 사이언스의 미래"], "기본", "앞으로 빅데이터 활용에서 계속 중요해질 과제로 빅데이터 문헌이 드는 것은?",
  "정보 프라이버시(개인정보 보호)",
  ["데이터 저장 금지", "모든 분석의 수작업 전환", "데이터 공유의 전면 중단"],
  "빅데이터의 과제에는 저장·공유·전송·시각화·질의·갱신과 함께 정보 프라이버시가 포함된다.", ["bigdata"], ["information privacy"])

os.makedirs(os.path.join(ROOT, 'bank'), exist_ok=True)
json.dump(qs, open(os.path.join(ROOT, 'bank', 'new_s1.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(qs), 'questions -> bank/new_s1.json')
