"""Subject 3 question bank.
- Computational / R-code questions: the answer is whatever verify/s3.R prints (stored as verifyValue);
  verify/check.py re-runs R and a Python re-computation and fails on any mismatch.
- Concept questions cite a public source that was opened and checked (2026-09-29).
Run: python scripts/build_s3.py  (writes data/questions/s3.json)"""
import json, os

W = 'https://en.wikipedia.org/wiki/'
R = 'https://stat.ethz.ch/R-manual/R-devel/library/'
S = {
    'mean': ('R 문서: mean (na.rm)', R + 'base/html/mean.html'),
    'matrix': ('R 문서: matrix (byrow = FALSE → 열 우선)', R + 'base/html/matrix.html'),
    'apply': ('R 문서: apply (MARGIN 1 = 행)', R + 'base/html/apply.html'),
    'rep': ('R 문서: rep (times, each)', R + 'base/html/rep.html'),
    'quantile': ('R 문서: quantile (기본 type 7)', R + 'stats/html/quantile.html'),
    'var': ('R 문서: var·cor (분모 n−1)', R + 'stats/html/cor.html'),
    'type1': ('Wikipedia: Type I and type II errors', W + 'Type_I_and_type_II_errors'),
    'pval': ('Wikipedia: p-value', W + 'P-value'),
    'rule': ('Wikipedia: 68–95–99.7 rule', W + '68%E2%80%9395%E2%80%9399.7_rule'),
    'pnorm': ('R 문서: Normal (pnorm)', R + 'stats/html/Normal.html'),
    'ttest': ("Wikipedia: Student's t-test", W + "Student%27s_t-test"),
    'chisq': ('Wikipedia: Chi-squared test', W + 'Chi-squared_test'),
    'pca': ('Wikipedia: Principal component analysis', W + 'Principal_component_analysis'),
    'arima': ('Wikipedia: ARIMA', W + 'Autoregressive_integrated_moving_average'),
    'stat': ('Wikipedia: Stationary process', W + 'Stationary_process'),
    'kmeans': ('Wikipedia: k-means clustering', W + 'K-means_clustering'),
    'overfit': ('Wikipedia: Overfitting', W + 'Overfitting'),
    'pr': ('Wikipedia: Precision and recall', W + 'Precision_and_recall'),
    'arl': ('Wikipedia: Association rule learning (support, confidence, lift)', W + 'Association_rule_learning'),
}
V = 'verify/s3.R'


def Q(i, item, tags, q, ch, a, ex, src=(), code=None, value=None, fixed=False):
    d = {"id": f"s3-{i:03d}", "subject": 3, "item": item, "tags": tags, "q": q}
    if code:
        d["code"] = code
    d.update({"choices": ch, "answer": a, "explain": ex,
              "sources": [{"t": S[k][0], "u": S[k][1]} for k in src], "checked": "2026-09-29"})
    if value is not None:
        d["verify"] = V
        d["verifyValue"] = value
    if fixed:
        d["fixedOrder"] = True
    return d


qs = [
    Q(1, "3-1-1", ["R 코드", "결측값"], "다음 R 코드의 실행 결과는?", ["4", "NA", "8", "에러가 난다"], 1,
      "결측값(NA)이 있는 벡터의 평균은 na.rm = FALSE(기본값)일 때 NA다.", ["mean"], code="x <- c(3, NA, 5)\nmean(x)", value="NA"),
    Q(2, "3-1-1", ["R 코드", "결측값"], "다음 R 코드의 실행 결과는?", ["NA", "4", "2.67", "8"], 1,
      "na.rm = TRUE면 NA를 빼고 (3 + 5) / 2 = 4를 계산한다.", ["mean"], code="mean(c(3, NA, 5), na.rm = TRUE)", value="4"),
    Q(3, "3-1-1", ["R 코드", "인덱싱"], "다음 R 코드의 실행 결과는?", ["2", "1 3 4 5 6", "1 2 3 4 5", "3 4 5 6"], 1,
      "음수 인덱스는 해당 위치를 뺀다. x[-2]는 두 번째 원소(2)를 제외한 1 3 4 5 6이다.", code="x <- 1:6\nx[-2]", value="1 3 4 5 6"),
    Q(4, "3-1-1", ["R 코드", "벡터 생성"], "다음 R 코드의 실행 결과는?", ["2 5 8 11", "2 5 8", "2 3 4 5 6 7 8 9 10 11", "3 6 9"], 0,
      "seq(2, 11, by = 3)은 2부터 3씩 더해 11을 넘지 않을 때까지 만든다: 2 5 8 11.", code="seq(2, 11, by = 3)", value="2 5 8 11"),
    Q(5, "3-1-1", ["R 코드", "벡터 생성"], "다음 R 코드의 실행 결과는?", ["A A B B", "A B A B", "A B", "AB AB"], 1,
      "times = 2는 벡터 전체를 2번 반복한다(A B A B). 원소별로 반복하려면 each = 2(A A B B)를 쓴다.", ["rep"],
      code='rep(c("A", "B"), times = 2)', value="A B A B"),
    Q(6, "3-1-1", ["R 코드", "자료형"], "다음 R 코드의 실행 결과는?", ['"numeric"', '"logical"', '"character"', '"list"'], 2,
      "벡터는 한 가지 자료형만 가진다. 문자가 하나라도 섞이면 모든 원소가 문자형(character)으로 바뀐다.",
      code='class(c(1, "2", TRUE))', value="character"),
    Q(7, "3-1-1", ["R 코드", "행렬"], "다음 R 코드의 실행 결과는?", ["5", "6", "4", "3"], 1,
      "matrix는 기본값(byrow = FALSE)으로 열부터 채운다. 1열 = 1,2 / 2열 = 3,4 / 3열 = 5,6이므로 m[2, 3] = 6.", ["matrix"],
      code="m <- matrix(1:6, nrow = 2)\nm[2, 3]", value="6"),
    Q(8, "3-1-1", ["R 코드", "행렬"], "다음 R 코드의 실행 결과는?", ["3 7 11", "9 12", "6 15", "21"], 1,
      "MARGIN = 1은 행 단위다. 열부터 채운 행렬의 1행은 1,3,5(합 9), 2행은 2,4,6(합 12).", ["apply", "matrix"],
      code="apply(matrix(1:6, nrow = 2), 1, sum)", value="9 12"),
    Q(9, "3-1-3", ["R 코드", "결측값"], "다음 R 코드의 실행 결과는?", ["1", "2", "3", "4"], 1,
      "is.na()는 결측이면 TRUE를 돌려주고, sum()은 TRUE를 1로 센다. NA가 2개이므로 2.",
      code="sum(is.na(c(1, NA, 3, NA)))", value="2", fixed=True),
    Q(10, "3-1-1", ["R 코드", "벡터 생성"], "다음 R 코드의 실행 결과는?", ["3", "4", "NA", "에러가 난다"], 0,
      "NULL은 '값이 없음'이라 벡터에 들어가지 않는다. c(1, 2, NULL, 4)는 1 2 4이므로 길이는 3.",
      code="length(c(1, 2, NULL, 4))", value="3"),
    Q(11, "3-1-3", ["R 코드", "결측값"], "다음 R 코드의 실행 결과는?", ["0", "1", "2", "3"], 1,
      "complete.cases()는 모든 열에 결측이 없는 행만 TRUE다. 1행(b 결측)과 2행(a 결측)을 빼면 3행 하나만 남는다.",
      code="df <- data.frame(a = c(1, NA, 3), b = c(NA, 2, 3))\nsum(complete.cases(df))", value="1", fixed=True),
    Q(12, "3-1-3", ["R 코드", "결측값 대치"], "다음 R 코드를 실행한 뒤 a의 값은?", ["1 NA 3", "1 2 3", "1 0 3", "1 4 3"], 1,
      "결측값을 나머지 값의 평균((1 + 3) / 2 = 2)으로 채우는 평균 대치다.", ["mean"],
      code="a <- c(1, NA, 3)\na[is.na(a)] <- mean(a, na.rm = TRUE)\na", value="1 2 3"),
    Q(13, "3-1-3", ["R 코드", "이상값"], "다음 데이터에서 IQR 규칙(Q1 − 1.5×IQR 미만 또는 Q3 + 1.5×IQR 초과)으로 이상값이 되는 값은? (R quantile 기본값 사용)",
      ["2", "8", "30", "이상값 없음"], 2,
      "R 기본 quantile(type 7)로 Q1 = 4, Q3 = 7.25, IQR = 3.25다. 상한 7.25 + 4.875 = 12.125를 넘는 30만 이상값이다.", ["quantile"],
      code="v <- c(2, 4, 4, 5, 6, 7, 8, 30)", value="30"),
    Q(14, "3-3-3", ["군집분석"], "k-means 군집분석에 대한 설명으로 옳은 것은?",
      ["군집 수 k를 분석 전에 정해야 한다", "군집 수를 알고리즘이 자동으로 정한다", "범주형 목표변수가 반드시 필요하다", "덴드로그램으로 군집 수를 나중에 고른다"], 0,
      "k-means에서 군집 수 k는 입력값이라 미리 정해야 한다. k를 잘못 고르면 결과가 나빠질 수 있어 엘보 방법·실루엣 등으로 정한다.", ["kmeans"]),
    Q(15, "3-2-2", ["기술통계", "계산"], "R에서 var(c(2, 4, 6, 8))의 값은? (소수 셋째 자리까지)", ["5.000", "6.667", "20.000", "2.582"], 1,
      "평균 5, 편차 제곱합 = 9+1+1+9 = 20. R의 var는 분모 n−1 = 3을 쓰므로 20/3 ≈ 6.667.", ["var"], value="6.667"),
    Q(16, "3-3-1", ["데이터 마이닝 개요"], "과대적합(overfitting)에 대한 설명으로 옳은 것은?",
      ["학습 데이터에 지나치게 맞춰져 새 데이터에서 성능이 떨어지는 현상", "모형이 너무 단순해 학습 데이터도 설명하지 못하는 현상", "데이터가 많을수록 반드시 생기는 현상", "검증 데이터 성능이 학습 데이터보다 항상 높은 현상"], 0,
      "과대적합은 학습 데이터(잡음까지)에 너무 가깝게 맞춰져 새 데이터를 잘 예측하지 못하는 것이다. ②는 과소적합이다.", ["overfit"]),
    Q(17, "3-2-2", ["기술통계", "계산"], "R에서 sd(c(2, 4, 4, 4, 5, 5, 7, 9))의 값은? (소수 셋째 자리까지)", ["2.000", "2.138", "4.571", "5.000"], 1,
      "평균 5, 편차 제곱합 32. 분모 n−1 = 7로 나눈 분산 4.571의 제곱근 ≈ 2.138. (분모 n이면 2.000)", ["var"], value="2.138"),
    Q(18, "3-2-2", ["상관분석", "계산"], "x = 1, 2, 3, 4, 5와 y = 2, 1, 4, 3, 5의 피어슨 상관계수는?", ["0.5", "0.6", "0.8", "1"], 2,
      "x·y 평균은 모두 3. 편차곱의 합 8, x 편차제곱합 10, y 편차제곱합 10이므로 r = 8 / √(10×10) = 0.8.", value="0.8"),
    Q(19, "3-2-2", ["회귀분석", "계산"], "x = 1, 2, 3, 4, 5와 y = 2, 3, 5, 6, 9로 최소제곱 단순선형회귀를 적합했을 때의 회귀식은?",
      ["y = −0.1 + 1.7x", "y = 0.5 + 1.5x", "y = −1 + 2x", "y = 1 + 1.5x"], 0,
      "x 평균 3, y 평균 5. 기울기 = Σ(x−x̄)(y−ȳ) / Σ(x−x̄)² = 17 / 10 = 1.7, 절편 = 5 − 1.7×3 = −0.1.", value="-0.1 1.7"),
    Q(20, "3-2-2", ["회귀분석", "계산"], "x = 1, 2, 3, 4, 5와 y = 2, 4, 5, 4, 5로 단순선형회귀를 적합했을 때 결정계수 R²는? (소수 셋째 자리까지)",
      ["0.300", "0.600", "0.775", "0.900"], 1,
      "기울기 0.6, 절편 2.2. 잔차 제곱합 2.4, 총제곱합 6.0이므로 R² = 1 − 2.4/6.0 = 0.600.", value="0.600"),
    Q(21, "3-2-1", ["가설검정"], "유의수준 0.05에서 검정 결과 p-value가 0.03이었다. 올바른 판단은?",
      ["귀무가설을 기각한다", "귀무가설을 채택한다고 증명된다", "대립가설이 거짓이다", "유의수준을 0.01로 바꿔야 한다"], 0,
      "p-value가 유의수준보다 작으면 귀무가설을 기각한다.", ["pval"]),
    Q(22, "3-2-1", ["가설검정"], "제1종 오류에 대한 설명으로 옳은 것은?",
      ["귀무가설이 참인데 기각하는 오류", "귀무가설이 거짓인데 기각하지 않는 오류", "표본 크기가 작아 생기는 오류", "대립가설이 참인데 채택하는 경우"], 0,
      "제1종 오류는 참인 귀무가설을 잘못 기각하는 것(거짓 양성), 제2종 오류는 거짓인 귀무가설을 기각하지 못하는 것이다.", ["type1"]),
    Q(23, "3-2-1", ["확률분포", "계산"], "점수가 평균 70, 표준편차 10인 정규분포를 따를 때, 90점 이상일 확률은 약 얼마인가? (R의 1 - pnorm(90, 70, 10))",
      ["약 0.1%", "약 2.3%", "약 5.0%", "약 15.9%"], 1,
      "90점은 평균보다 2 표준편차 위(z = 2)다. P(Z ≥ 2) = 1 − 0.97725 ≈ 0.0228, 약 2.3%. (±2σ 안이 약 95%라 한쪽 꼬리는 약 2.5%에 가깝다)", ["rule", "pnorm"], value="2.3"),
    Q(24, "3-2-2", ["가설검정"], "서로 다른 두 집단(치료군 50명, 대조군 50명)의 평균을 비교할 때 가장 적합한 검정은?",
      ["독립표본 t-검정", "대응표본 t-검정", "카이제곱 독립성 검정", "상관분석"], 0,
      "겹치지 않는 두 독립 집단의 평균 비교에는 독립표본(two-sample) t-검정을 쓴다. 같은 사람을 두 번 재면 대응표본 t-검정이다.", ["ttest"]),
    Q(25, "3-2-2", ["가설검정"], "성별(남/여)과 선호 브랜드(A/B/C)가 서로 관련이 있는지 분할표로 검정하려면?",
      ["독립표본 t-검정", "카이제곱 독립성 검정", "단순선형회귀", "분산분석"], 1,
      "두 범주형 변수의 독립성은 분할표에 대한 카이제곱 검정으로 확인한다.", ["chisq"]),
    Q(26, "3-2-3", ["주성분분석", "계산"], "두 주성분의 고유값이 3과 1일 때, 첫 번째 주성분이 설명하는 분산의 비율은?", ["25%", "50%", "75%", "100%"], 2,
      "각 주성분의 설명 분산 비율 = 고유값 / 고유값 합 = 3 / 4 = 75%.", ["pca"], value="75", fixed=True),
    Q(27, "3-2-4", ["시계열"], "ARIMA(p, d, q) 모형에서 d가 뜻하는 것은?", ["자기회귀 차수", "차분 횟수", "이동평균 차수", "계절 주기"], 1,
      "p는 자기회귀(AR) 차수, d는 차분(differencing) 횟수, q는 이동평균(MA) 차수다.", ["arima"]),
    Q(28, "3-2-4", ["시계열"], "정상성(stationarity)을 가진 시계열에 대한 설명으로 옳은 것은?",
      ["평균과 분산 같은 통계적 성질이 시간에 따라 변하지 않는다", "시간이 지날수록 평균이 계속 증가한다", "분산이 시간에 비례해 커진다", "항상 계절성을 가진다"], 0,
      "정상 시계열은 평균·분산 등 통계적 성질이 시간이 지나도 일정하다.", ["stat"]),
    Q(29, "3-3-2", ["분류 평가", "계산"], "혼동행렬이 TP = 40, FN = 10, FP = 20, TN = 30일 때 정밀도(precision)는? (소수 셋째 자리까지)",
      ["0.667", "0.800", "0.700", "0.600"], 0,
      "정밀도 = TP / (TP + FP) = 40 / 60 ≈ 0.667. 재현율은 TP / (TP + FN) = 0.800.", ["pr"], value="0.667"),
    Q(30, "3-3-4", ["연관분석", "계산"],
      "거래 10건 중 A 포함 5건, B 포함 5건, A와 B를 함께 포함 3건이다. 규칙 A → B의 향상도(lift)는?",
      ["0.6", "1.2", "1.5", "0.3"], 1,
      "지지도(A,B) = 0.3, 지지도(A) = 0.5, 지지도(B) = 0.5. 향상도 = 0.3 / (0.5 × 0.5) = 1.2. 1보다 크면 A가 B 구매와 양의 관계다.", ["arl"], value="1.2"),
]

out = os.path.join(os.path.dirname(__file__), '..', 'data', 'questions', 's3.json')
json.dump(qs, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(qs), 'questions ->', os.path.normpath(out))
