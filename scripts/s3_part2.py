"""s3-137~190: 3-2-2 기초 통계분석(회귀·검정 출력 해석), 3-2-3 다변량 분석, 3-2-4 시계열.
Numbers in the choices are computed here with numpy/statsmodels; verify/exec.py re-checks them against R."""
import numpy as np
import statsmodels.api as sm
from scipy import stats

RD = 'https://stat.ethz.ch/R-manual/R-devel/library/'
f3 = lambda v: f"{v:.3f}"

# data used in several questions (written out so R and Python see the same numbers)
X1 = [1, 2, 3, 4, 5, 6, 7, 8]
Y1 = [3.1, 4.9, 7.2, 8.8, 11.1, 13.0, 14.8, 17.2]
RX1, RY1 = 'x <- c(1, 2, 3, 4, 5, 6, 7, 8)', 'y <- c(3.1, 4.9, 7.2, 8.8, 11.1, 13.0, 14.8, 17.2)'
m1 = sm.OLS(Y1, sm.add_constant(X1)).fit()
B0, B1, R2 = m1.params[0], m1.params[1], m1.rsquared

A = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
B = [5, 3, 6, 2, 7, 4, 8, 3, 6, 5]
Y2 = [5.3, 6.8, 9.1, 10.6, 13.2, 15.0, 16.9, 19.3, 20.7, 23.1]
RD2 = 'd <- data.frame(a = c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10), b = c(5, 3, 6, 2, 7, 4, 8, 3, 6, 5), y = c(5.3, 6.8, 9.1, 10.6, 13.2, 15.0, 16.9, 19.3, 20.7, 23.1))'
m2 = sm.OLS(Y2, sm.add_constant(np.column_stack([A, B]))).fit()
assert m2.pvalues[1] < 0.05 and m2.pvalues[2] > 0.05, 'b must be the non-significant variable'

PRE = [72, 75, 68, 80, 77, 71, 74, 79]
POST = [75, 79, 70, 84, 80, 72, 78, 83]
RPP = 'pre <- c(72, 75, 68, 80, 77, 71, 74, 79); post <- c(75, 79, 70, 84, 80, 72, 78, 83)'
tp = stats.ttest_rel(POST, PRE)

G1 = [12, 15, 14, 13, 16]; G2 = [18, 17, 20, 19, 16]; G3 = [22, 21, 24, 23, 20]
RAOV = 'g <- data.frame(v = c(12, 15, 14, 13, 16, 18, 17, 20, 19, 16, 22, 21, 24, 23, 20), grp = factor(rep(c("A", "B", "C"), each = 5)))'

PX = np.array([[2.5, 1.2, 3.0, 4.1], [0.5, 2.8, 1.9, 2.2], [2.2, 0.9, 3.6, 1.5], [1.9, 2.1, 1.2, 3.8], [3.1, 1.4, 2.2, 2.9],
               [2.3, 3.0, 3.1, 1.1], [2.0, 1.7, 0.8, 2.5], [1.0, 2.6, 2.7, 3.3], [1.5, 0.6, 1.5, 1.9], [1.1, 2.2, 2.4, 4.0]])
RPX = 'X <- data.frame(' + ', '.join(f"v{j + 1} = c(" + ', '.join(str(v) for v in PX[:, j]) + ")" for j in range(4)) + ')'
ev = np.sort(np.linalg.eigvalsh(np.corrcoef(PX, rowvar=False)))[::-1]
PROP = ev / ev.sum()
NPC80 = int(np.argmax(np.cumsum(PROP) >= 0.8) + 1)
LOW = ['v1', 'v2', 'v3', 'v4'][int(np.argmin(abs(np.linalg.eigh(np.corrcoef(PX, rowvar=False))[1][:, -1])))]
PYPX = 'X = np.array(' + repr(PX.tolist()) + ')\nev = np.sort(np.linalg.eigvalsh(np.corrcoef(X, rowvar=False)))[::-1]\n'


def add(E, C):
    # --- 3-2-2 회귀분석: summary(lm) 출력 해석 (빈출)
    E(137, "3-2-2", ["회귀분석", "R 출력 해석"], "실전", "다음은 R의 단순선형회귀 결과다. x의 회귀계수(기울기) 추정값은?",
      f"{RX1}\n{RY1}\nsummary(lm(y ~ x))", f"{RX1}; {RY1}; r3(coef(lm(y ~ x))[[2]])",
      f"m = sm.OLS({Y1}, sm.add_constant({X1})).fit(); result = round(m.params[1], 3)", f3(B1),
      f3(B1), [f3(B0), f3(R2), f3(m1.bse[1])], "Coefficients 표의 x 행 Estimate가 기울기다. (Intercept) 행은 절편, Multiple R-squared는 결정계수다.",
      [("R 문서: summary.lm", RD + 'stats/html/summary.lm.html')], run=True)
    E(138, "3-2-2", ["회귀분석", "예측"], "실전", "다음 회귀 결과로 x = 10일 때 y의 예측값을 구하면? (소수 셋째 자리까지)",
      f"{RX1}\n{RY1}\ncoef(lm(y ~ x))", f"{RX1}; {RY1}; r3(predict(lm(y ~ x), data.frame(x = 10))[[1]])",
      f"m = sm.OLS({Y1}, sm.add_constant({X1})).fit(); result = round(m.params[0] + 10 * m.params[1], 3)", f3(B0 + 10 * B1),
      f3(B0 + 10 * B1), [f3(10 * B1), f3(B0 + 9 * B1), f3(B1 + 10 * B0)], f"예측값 = 절편 + 기울기 × 10 = {B0:.6f} + {B1:.6f} × 10 ≈ {f3(B0 + 10 * B1)}. 출력의 (Intercept)가 절편, x가 기울기다. 계수를 미리 반올림하면 끝자리가 달라진다.",
      [("R 문서: lm", RD + 'stats/html/lm.html')], run=True)
    E(139, "3-2-2", ["회귀분석", "결정계수"], "실전", "회귀분석에서 총제곱합(SST)이 200, 잔차제곱합(SSE)이 50이다. 결정계수 R²는?", "",
      "1 - 50 / 200", "result = 1 - 50 / 200", "0.75",
      "0.75", ["0.25", "4", "0.5"], "R² = 1 − SSE / SST = 1 − 50 / 200 = 0.75. 모형이 y 변동의 75%를 설명한다.")
    E(140, "3-2-2", ["회귀분석", "자유도"], "기본", "관측치 8개로 단순선형회귀(설명변수 1개)를 적합했다. 잔차의 자유도는?", "",
      f"{RX1}; {RY1}; df.residual(lm(y ~ x))", "result = 8 - 2", "6",
      "6", ["7", "8", "1"], "잔차 자유도 = n − (추정한 계수 개수) = 8 − 2(절편, 기울기) = 6. R 출력의 'Residual standard error: … on 6 degrees of freedom'에 나온다.")
    E(141, "3-2-2", ["다중회귀", "R 출력 해석"], "고난도", "다음 다중회귀 결과에서 유의수준 0.05로 볼 때 y에 유의한 영향을 준다고 할 수 없는 변수는?",
      f"{RD2}\nsummary(lm(y ~ a + b, data = d))", f"{RD2}; p <- summary(lm(y ~ a + b, data = d))$coefficients[-1, 4]; names(p)[p > 0.05]",
      f"m = sm.OLS({Y2}, sm.add_constant(np.column_stack([{A}, {B}]))).fit(); result = ['a', 'b'][int(np.argmax(m.pvalues[1:] > 0.05))]", "b",
      "b", ["a", "a와 b 모두", "둘 다 유의하다"], "Coefficients 표의 Pr(>|t|)가 0.05보다 큰 변수는 계수가 0이라는 귀무가설을 기각할 수 없다. b의 p값이 0.05보다 크다.",
      [("R 문서: summary.lm", RD + 'stats/html/summary.lm.html')], run=True)
    E(142, "3-2-2", ["다중회귀", "F검정"], "실전", "관측치 10개, 설명변수 2개로 다중회귀를 적합했다. 모형 전체 F검정의 자유도는?", "",
      f"{RD2}; unname(summary(lm(y ~ a + b, data = d))$fstatistic[2:3])", "result = [2, 10 - 2 - 1]", "2 7",
      "(2, 7)", ["(3, 7)", "(2, 8)", "(1, 9)"], "F 자유도는 (설명변수 개수 p, n − p − 1) = (2, 10 − 2 − 1 = 7).")
    C(143, "3-2-2", ["회귀분석", "결정계수"], "실전", "추가한 설명변수가 실제로 종속변수 설명에 기여하는지와 관계없이, 설명변수를 추가하기만 하면 항상 커지거나 같아지는 지표는?",
      "결정계수(R²)", ["수정 결정계수(adjusted R²)", "AIC", "잔차 표준오차"],
      "R²는 변수를 넣기만 해도 줄지 않는다. 그래서 변수 수를 고려해 벌점을 주는 수정 결정계수로 비교한다.",
      [("Wikipedia: Coefficient of determination", 'Coefficient_of_determination')], ["adjusted r"])
    E(144, "3-2-2", ["다중공선성", "VIF"], "실전", "어떤 설명변수를 나머지 설명변수들로 회귀했을 때 결정계수가 0.9였다. 이 변수의 VIF는?", "",
      "1 / (1 - 0.9)", "result = 1 / (1 - 0.9)", "10",
      "10", ["0.1", "9", "1.9"], "VIF = 1 / (1 − R²ⱼ) = 1 / 0.1 = 10. 보통 10 이상이면 다중공선성이 심하다고 본다.",
      [("Wikipedia: Variance inflation factor", 'Variance_inflation_factor')])
    C(145, "3-2-2", ["다중공선성"], "고난도", "다중공선성이 심할 때 회귀분석에서 나타나는 현상으로 옳은 것은?",
      "계수 추정값의 표준오차가 커져 계수가 불안정해진다", ["결정계수가 반드시 0이 된다", "잔차가 모두 0이 된다", "예측값을 전혀 계산할 수 없다"],
      "설명변수끼리 강하게 얽히면 개별 계수의 표준오차가 커지고 부호·크기가 불안정해진다. VIF로 진단하고 변수 제거·주성분 회귀 등으로 대응한다.",
      [("Wikipedia: Multicollinearity", 'Multicollinearity')], ["standard errors"])
    C(146, "3-2-2", ["변수 선택"], "실전", "모든 설명변수를 넣은 모형에서 시작해 가장 덜 유의한 변수를 하나씩 빼 나가는 변수 선택법은?",
      "후진 제거법", ["전진 선택법", "단계적 선택법", "능형 회귀"],
      "후진 제거(backward elimination)는 전체 모형에서 변수를 하나씩 제거한다. 전진 선택은 빈 모형에서 하나씩 추가한다.",
      [("Wikipedia: Stepwise regression", 'Stepwise_regression')], ["backward elimination"])
    C(147, "3-2-2", ["변수 선택"], "실전", "변수가 없는 모형에서 시작해 설명력을 가장 크게 높이는 변수를 하나씩 추가하는 방법은?",
      "전진 선택법", ["후진 제거법", "라쏘 회귀", "교차 검증"],
      "전진 선택(forward selection)은 빈 모형에서 변수를 하나씩 추가한다. 추가·제거를 번갈아 하면 단계적 선택이다.",
      [("Wikipedia: Stepwise regression", 'Stepwise_regression')], ["forward selection"])
    C(148, "3-2-2", ["변수 선택", "AIC"], "실전", "여러 후보 회귀모형의 AIC가 모형1 120.5, 모형2 98.2, 모형3 101.7이다. AIC 기준으로 가장 좋은 모형은?",
      "모형2", ["모형1", "모형3", "AIC로는 비교할 수 없다"],
      "AIC는 작을수록 좋은 모형이다(적합도와 복잡도의 균형). 최솟값 98.2인 모형2.",
      [("Wikipedia: Akaike information criterion", 'Akaike_information_criterion')], ["minimum aic value"])
    C(149, "3-2-2", ["회귀 가정", "잔차"], "고난도", "잔차도에서 x가 커질수록 잔차가 부채꼴로 점점 크게 퍼진다. 위반된 회귀 가정은?",
      "등분산성", ["독립성", "선형성", "정규성"],
      "잔차의 분산이 일정해야 한다는 등분산성(homoscedasticity)이 깨진 이분산성이다.",
      [("Wikipedia: Homoscedasticity and heteroscedasticity", 'Homoscedasticity_and_heteroscedasticity')], ["heteroscedasticity"])
    C(150, "3-2-2", ["회귀 가정", "잔차"], "고난도", "시간 순서로 모은 데이터의 회귀 잔차에 자기상관이 있는지 확인하는 통계량은?",
      "더빈-왓슨 통계량", ["VIF", "샤피로-윌크 통계량", "카이제곱 통계량"],
      "더빈-왓슨 통계량은 잔차의 자기상관을 검정한다(2에 가까우면 자기상관이 거의 없음).",
      [("Wikipedia: Durbin–Watson statistic", 'Durbin%E2%80%93Watson_statistic')], ["autocorrelation"])
    C(151, "3-2-2", ["회귀분석", "더미 변수"], "실전", "범주가 4개(봄·여름·가을·겨울)인 변수를 회귀모형에 넣을 때 절편이 있는 모형에서 필요한 더미 변수 개수는?",
      "3개", ["4개", "1개", "2개"],
      "범주 수보다 하나 적은 k − 1개의 더미를 쓴다. 4개를 모두 넣으면 절편과 완전한 공선성이 생긴다(더미 변수 함정).",
      [("Wikipedia: Dummy variable (statistics)", 'Dummy_variable_(statistics)')], ["dummy variable trap"])
    # 가설검정 출력 해석
    E(152, "3-2-2", ["t검정", "R 출력 해석"], "실전", "같은 학생 8명의 교육 전(pre)·후(post) 점수를 비교했다. 다음 결과의 t 통계량은? (소수 셋째 자리까지)",
      f"{RPP}\nt.test(post, pre, paired = TRUE)", f"{RPP}; r3(t.test(post, pre, paired = TRUE)$statistic[[1]])",
      f"result = round(stats.ttest_rel({POST}, {PRE}).statistic, 3)", f3(tp.statistic),
      f3(tp.statistic), [f3(tp.statistic / 2), f3(np.mean(np.array(POST) - np.array(PRE))), "7.000"],
      "같은 대상의 전후 비교는 대응표본 t검정이다. 출력의 t 값을 읽는다. df = 8 − 1 = 7.", [("R 문서: t.test", RD + 'stats/html/t.test.html')], run=True)
    E(153, "3-2-2", ["t검정", "p-value"], "실전", "두 매장(A, B)의 하루 매출을 비교한 다음 결과에서 유의수준 0.05의 결론으로 옳은 것은?",
      "A <- c(20, 22, 19, 24, 21); B <- c(25, 27, 24, 28, 26)\nt.test(A, B, var.equal = TRUE)",
      "A <- c(20, 22, 19, 24, 21); B <- c(25, 27, 24, 28, 26); t.test(A, B, var.equal = TRUE)$p.value < 0.05",
      "result = bool(stats.ttest_ind([20, 22, 19, 24, 21], [25, 27, 24, 28, 26]).pvalue < 0.05)", "TRUE",
      "p-value가 0.05보다 작아 두 매장의 평균 매출이 같다는 귀무가설을 기각한다",
      ["p-value가 0.05보다 커 귀무가설을 기각할 수 없다", "t 통계량이 음수라 B의 평균이 더 작다", "표본이 5개씩이라 검정할 수 없다"],
      "출력의 p-value가 0.05보다 작으면 평균이 같다는 귀무가설을 기각한다. t가 음수인 것은 A − B가 음수(B가 더 큼)라는 뜻이다.",
      [("R 문서: t.test", RD + 'stats/html/t.test.html')], run=True)
    E(154, "3-2-2", ["t검정"], "실전", "두 독립 집단(각 10명)의 평균을 등분산을 가정한 t검정(var.equal = TRUE)으로 비교할 때 자유도는?", "",
      "t.test(1:10, 2:11, var.equal = TRUE)$parameter[[1]]", "result = 10 + 10 - 2", "18",
      "18", ["20", "19", "9"], "등분산 독립표본 t검정의 자유도는 n₁ + n₂ − 2 = 18.")
    E(155, "3-2-2", ["t검정"], "고난도", "R에서 t.test(x, y)를 옵션 없이 실행하면 어떤 검정이 수행되는가?", "",
      "t.test(c(1, 2, 3, 4), c(2, 4, 6, 9))$method", "result = 'Welch Two Sample t-test'", "Welch Two Sample t-test",
      "등분산을 가정하지 않는 웰치(Welch) t검정", ["등분산을 가정한 합동분산 t검정", "대응표본 t검정", "윌콕슨 순위합 검정"],
      "R의 t.test 기본값은 var.equal = FALSE라 웰치 t검정이 수행된다. 대응표본은 paired = TRUE를 줘야 한다.", [("R 문서: t.test", RD + 'stats/html/t.test.html')])
    C(156, "3-2-2", ["정규성 검정"], "기본", "데이터가 정규분포를 따르는지 검정하는 데 쓰는 것은?",
      "샤피로-윌크 검정", ["카이제곱 독립성 검정", "더빈-왓슨 검정", "F 검정"],
      "샤피로-윌크 검정은 표본이 정규분포 모집단에서 왔는지 검정한다(R: shapiro.test).",
      [("Wikipedia: Shapiro–Wilk test", 'Shapiro%E2%80%93Wilk_test')], ["normally distributed"])
    C(157, "3-2-2", ["p-value"], "고난도", "p-value에 대한 설명으로 옳은 것은?",
      "귀무가설이 참이라고 가정할 때, 관측한 결과만큼 또는 그보다 극단적인 결과가 나올 확률",
      ["귀무가설이 참일 확률", "대립가설이 참일 확률", "표본이 잘못 뽑혔을 확률"],
      "p-value는 귀무가설 아래에서 관측값 이상으로 극단적인 결과가 나올 확률이다. 가설이 참일 확률이 아니다.",
      [("Wikipedia: p-value", 'P-value')], ["at least as extreme"])
    E(158, "3-2-2", ["p-value", "양측검정"], "고난도", "양측검정에서 검정통계량 z = 1.8일 때 p-value는? (소수 셋째 자리까지)", "",
      "r3(2 * pnorm(-1.8))", "result = round(2 * stats.norm.cdf(-1.8), 3)", "0.072",
      "0.072", ["0.036", "0.964", "0.180"], "양측 p = 2 × P(Z ≥ 1.8) ≈ 2 × 0.036 = 0.072. 유의수준 0.05에서는 기각하지 못한다(단측이면 0.036).")
    E(159, "3-2-2", ["상관분석", "R 출력 해석"], "실전", "다음 cor.test 결과에서 표본 상관계수는? (소수 셋째 자리까지)",
      f"{RX1}\n{RY1}\ncor.test(x, y)", f"{RX1}; {RY1}; r3(cor(x, y))",
      f"result = round(stats.pearsonr({X1}, {Y1})[0], 3)", f3(stats.pearsonr(X1, Y1)[0]),
      f3(stats.pearsonr(X1, Y1)[0]), [f3(-stats.pearsonr(X1, Y1)[0]), f3(B1), "0.050"], "출력 마지막 sample estimates의 cor 값이 표본 상관계수다. 결정계수(R²)는 이 값의 제곱이다.",
      [("R 문서: cor.test", RD + 'stats/html/cor.test.html')], run=True)
    C(160, "3-2-2", ["상관분석"], "실전", "만족도 순위처럼 서열척도이거나 정규성을 가정하기 어려운 두 변수의 관계를 볼 때 알맞은 상관계수는?",
      "스피어만 순위상관계수", ["피어슨 상관계수", "결정계수", "공분산"],
      "스피어만 상관은 값 대신 순위(rank)로 계산해 서열 자료나 단조 관계에 쓴다.",
      [("Wikipedia: Spearman's rank correlation coefficient", "Spearman%27s_rank_correlation_coefficient")], ["rank"])
    E(161, "3-2-2", ["카이제곱 검정"], "실전", "3개 지역 × 4개 선호 브랜드 분할표로 카이제곱 독립성 검정을 할 때 자유도는?", "",
      "(3 - 1) * (4 - 1)", "result = (3 - 1) * (4 - 1)", "6",
      "6", ["12", "7", "11"], "독립성 검정 자유도 = (행 수 − 1)(열 수 − 1) = 2 × 3 = 6.")
    E(162, "3-2-2", ["카이제곱 검정"], "실전", "전체 100명 중 남성 40명, 브랜드 A 선호 30명일 때, 독립이라면 '남성이면서 A 선호'의 기대도수는?", "",
      "40 * 30 / 100", "result = 40 * 30 / 100", "12",
      "12", ["30", "40", "70"], "기대도수 = 행 합계 × 열 합계 / 전체 = 40 × 30 / 100 = 12.")
    E(163, "3-2-2", ["분산분석", "R 출력 해석"], "실전", "다음 일원분산분석 결과에서 잔차(Residuals)의 자유도는?",
      f"{RAOV}\nsummary(aov(v ~ grp, data = g))", f"{RAOV}; df.residual(aov(v ~ grp, data = g))",
      "result = 15 - 3", "12",
      "12", ["2", "14", "3"], "잔차 자유도 = 전체 관측치 − 집단 수 = 15 − 3 = 12. 집단(grp) 자유도는 3 − 1 = 2.", [("R 문서: aov", RD + 'stats/html/aov.html')], run=True)
    E(164, "3-2-2", ["분산분석"], "고난도", "일원분산분석에서 집단 간 제곱합 54(자유도 2), 집단 내 제곱합 36(자유도 12)일 때 F 통계량은?", "",
      "(54 / 2) / (36 / 12)", "result = (54 / 2) / (36 / 12)", "9",
      "9", ["1.5", "18", "27"], "F = (집단 간 제곱합 / 자유도) / (집단 내 제곱합 / 자유도) = 27 / 3 = 9.")
    C(165, "3-2-2", ["분산분석", "사후검정"], "고난도", "분산분석에서 세 집단 평균이 모두 같다는 귀무가설을 기각한 뒤, 어느 집단끼리 다른지 알아보는 방법은?",
      "투키(Tukey) HSD 같은 사후 다중비교", ["한 번 더 같은 F검정", "상관분석", "주성분 분석"],
      "F검정은 '적어도 한 집단이 다르다'까지만 알려 준다. 어느 쌍이 다른지는 투키 HSD 같은 다중비교로 본다.",
      [("Wikipedia: Tukey's range test", "Tukey%27s_range_test")], ["multiple comparison"])
    E(166, "3-2-2", ["구간추정"], "고난도", "모집단 표준편차를 알고(z 구간) 신뢰수준이 같을 때, 표본 크기를 4배로 늘리면 평균의 신뢰구간 폭은 몇 배가 되는가?", "",
      "sqrt(1 / 4)", "result = (1 / 4) ** 0.5", "0.5",
      "0.5배", ["0.25배", "4배", "2배"], "신뢰구간 폭은 σ / √n에 비례하므로 n이 4배면 폭은 1/√4 = 0.5배.")

    # --- 3-2-3 다변량 분석: 주성분 분석 출력 해석
    E(167, "3-2-3", ["주성분분석", "R 출력 해석"], "실전", "다음 주성분 분석 결과에서 첫 번째 주성분(PC1)이 설명하는 분산 비율은? (소수 셋째 자리까지)",
      f"{RPX}\nsummary(prcomp(X, scale. = TRUE))", f"{RPX}; r3(summary(prcomp(X, scale. = TRUE))$importance[2, 1])",
      PYPX + "result = round(ev[0] / ev.sum(), 3)", f3(PROP[0]),
      f3(PROP[0]), [f3(PROP[1]), f3(ev[0] / 10), f3(np.sqrt(ev[0]))], "summary 출력의 Proportion of Variance 행 PC1 값이다. Standard deviation은 고유값의 제곱근이다.",
      [("R 문서: prcomp", RD + 'stats/html/prcomp.html')], run=True)
    E(168, "3-2-3", ["주성분분석"], "실전", f"주성분 분석의 누적 설명 비율이 PC1 {np.cumsum(PROP)[0]:.3f}, PC2 {np.cumsum(PROP)[1]:.3f}, PC3 {np.cumsum(PROP)[2]:.3f}, PC4 1.000이다. 누적 80% 이상을 설명하려면 주성분이 최소 몇 개 필요한가?", "",
      f"{RPX}; which(summary(prcomp(X, scale. = TRUE))$importance[3, ] >= 0.8)[[1]]", PYPX + "result = int(np.argmax(np.cumsum(ev / ev.sum()) >= 0.8) + 1)", str(NPC80),
      f"{NPC80}개", [f"{k}개" for k in (1, 2, 3, 4) if k != NPC80][:3], "누적 비율이 0.8 이상이 처음 나오는 주성분까지 센다.")
    E(169, "3-2-3", ["주성분분석", "고유값"], "고난도", "변수 4개를 표준화해 주성분 분석을 했을 때 모든 주성분의 분산(고유값) 합은?", "",
      f"{RPX}; round(sum(prcomp(X, scale. = TRUE)$sdev^2), 6)", PYPX + "result = round(ev.sum(), 6)", "4",
      "4", ["1", "2", "변수마다 달라 알 수 없다"], "표준화하면 각 변수의 분산이 1이라 총분산 = 변수 개수 = 4. 주성분은 이 총분산을 나눠 가진다.")
    C(170, "3-2-3", ["주성분분석"], "실전", "주성분들 사이의 관계로 옳은 것은?",
      "서로 직교하며 상관관계가 없다", ["서로 강한 양의 상관이 있다", "항상 원래 변수와 같은 수의 1/2개만 만든다", "첫 주성분의 분산이 가장 작다"],
      "주성분은 서로 직교(orthogonal)하는 방향이라 상관이 없고, 첫 주성분이 분산을 가장 많이 설명한다.",
      [("Wikipedia: Principal component analysis", 'Principal_component_analysis')], ["orthogonal"])
    C(171, "3-2-3", ["주성분분석"], "실전", "키(cm)와 몸무게(kg)처럼 단위가 다른 변수로 주성분 분석을 할 때, 단위(척도) 차이가 결과를 좌우하지 않게 하려면 어떻게 하는가?",
      "변수를 표준화(상관행렬 사용)한다", ["단위가 큰 변수만 남긴다", "변수를 모두 제곱한다", "주성분 수를 변수 수보다 늘린다"],
      "주성분 분석은 변수의 척도에 민감하다. 단위가 다르면 일반적으로 표준화해(상관행렬 기반) 분석한다(R: prcomp(scale. = TRUE)).",
      [("Wikipedia: Principal component analysis", 'Principal_component_analysis')], ["scaling"])
    C(172, "3-2-3", ["주성분분석", "스크리 도표"], "기본", "주성분 개수를 정할 때, 고유값을 순서대로 그린 그래프에서 기울기가 급격히 완만해지는 '팔꿈치' 지점을 보는 방법은?",
      "스크리 도표(scree plot)", ["산점도 행렬", "덴드로그램", "잔차도"],
      "스크리 도표에서 고유값 감소가 급격하다가 완만해지는 팔꿈치(elbow) 지점을 기준으로 적절한 주성분 수를 판단한다.",
      [("Wikipedia: Scree plot", 'Scree_plot')], ["elbow"])
    E(173, "3-2-3", ["주성분분석"], "고난도", "두 표준화 변수의 상관계수가 0.6일 때 첫 번째 주성분의 설명 비율은?", "",
      "e <- eigen(matrix(c(1, 0.6, 0.6, 1), 2))$values; 100 * e[1] / sum(e)", "e = np.linalg.eigvalsh([[1, 0.6], [0.6, 1]]); result = 100 * max(e) / e.sum()", "80",
      "80%", ["60%", "40%", "100%"], "상관행렬 [[1, 0.6], [0.6, 1]]의 고유값은 1.6과 0.4. 첫 주성분 비율 = 1.6 / 2 = 80%.")
    C(174, "3-2-3", ["다차원 척도법"], "실전", "개체 간 거리(비유사성)를 보존하며 2차원 지도처럼 배치해 관계를 시각화하는 방법은?",
      "다차원 척도법(MDS)", ["주성분 분석", "연관 분석", "로지스틱 회귀"],
      "다차원 척도법은 개체 사이 거리 정보를 저차원 공간에 최대한 보존해 배치한다.",
      [("Wikipedia: Multidimensional scaling", 'Multidimensional_scaling')], ["distances"])
    C(175, "3-2-3", ["다차원 척도법"], "고난도", "다차원 척도법의 적합도를 나타내는 스트레스(stress) 값에 대한 설명으로 옳은 것은?",
      "작을수록 원래 거리를 잘 보존한 좋은 배치다", ["클수록 좋은 배치다", "항상 1이다", "변수 개수와 같다"],
      "스트레스는 원래 거리와 배치된 거리의 불일치 정도라 작을수록 좋다.",
      [("Wikipedia: Multidimensional scaling", 'Multidimensional_scaling')], ["stress"])
    C(176, "3-2-3", ["요인분석"], "실전", "여러 관측 변수 뒤에 있는 관측되지 않는 공통 잠재 요인을 찾으려는 다변량 기법은?",
      "요인분석", ["주성분 분석", "군집 분석", "판별 분석"],
      "요인분석은 관측 변수들의 변동을 적은 수의 잠재 요인으로 설명한다.",
      [("Wikipedia: Factor analysis", 'Factor_analysis')], ["latent"])
    E(177, "3-2-3", ["주성분분석", "고유값"], "실전", "고유값이 2.3, 1.1, 0.4, 0.2일 때 '고유값 1 이상'(카이저 기준)으로 선택하는 주성분 개수는?", "",
      "sum(c(2.3, 1.1, 0.4, 0.2) >= 1)", "result = sum(v >= 1 for v in [2.3, 1.1, 0.4, 0.2])", "2",
      "2개", ["1개", "3개", "4개"], "카이저 기준은 고유값 1 이상(표준화 변수 하나보다 많은 분산을 설명)인 성분만 남긴다: 2.3, 1.1.",
      [("Wikipedia: Factor analysis", 'Factor_analysis')])
    E(178, "3-2-3", ["주성분분석"], "고난도", "다음 주성분 적재값(rotation)에서 PC1에 대한 기여(적재값의 절댓값)가 가장 작은 변수는?",
      f"{RPX}\nround(prcomp(X, scale. = TRUE)$rotation[, 1:2], 3)",
      f"{RPX}; names(which.min(abs(prcomp(X, scale. = TRUE)$rotation[, 1])))",
      PYPX + "w, V = np.linalg.eigh(np.corrcoef(X, rowvar=False)); result = ['v1', 'v2', 'v3', 'v4'][int(np.argmin(abs(V[:, np.argmax(w)])))]",
      LOW, LOW, [v for v in ['v1', 'v2', 'v3', 'v4'] if v != LOW],
      "PC1 열에서 절댓값이 작을수록 그 변수가 PC1에 덜 기여한다. 부호는 방향일 뿐이라 크기는 절댓값으로 비교한다.",
      [("R 문서: prcomp", RD + 'stats/html/prcomp.html')], run=True)
    # --- 3-2-4 시계열 예측
    C(179, "3-2-4", ["시계열", "ACF·PACF"], "고난도", "ACF가 시차 q 이후 급격히 0으로 끊기고 PACF는 서서히 줄어드는 시계열에 알맞은 모형은?",
      "MA(q)", ["AR(p)", "백색잡음", "랜덤워크"],
      "MA(q)는 ACF가 q 이후 절단되고 PACF가 점차 감소한다. AR(p)는 반대로 PACF가 p 이후 절단된다.",
      [("Wikipedia: Box–Jenkins method", 'Box%E2%80%93Jenkins_method')], ["moving average", "partial autocorrelation"])
    C(180, "3-2-4", ["시계열", "ACF·PACF"], "고난도", "PACF가 시차 2 이후 0으로 끊기고 ACF는 서서히 줄어드는 시계열에 알맞은 모형은?",
      "AR(2)", ["MA(2)", "ARMA(0, 0)", "MA(1)"],
      "PACF가 p 이후 절단되고 ACF가 점차 감소하면 AR(p)다. 여기서는 p = 2.",
      [("Wikipedia: Box–Jenkins method", 'Box%E2%80%93Jenkins_method')], ["autoregressive", "partial autocorrelation"])
    C(181, "3-2-4", ["시계열", "ARIMA"], "실전", "ARIMA(0, 1, 1) 모형에 대한 설명으로 옳은 것은?",
      "1번 차분해 정상화한 뒤 MA(1)을 적용한다", ["AR(1)을 적용한 뒤 차분하지 않는다", "2번 차분한 뒤 AR(1)을 적용한다", "계절 주기가 1인 모형이다"],
      "ARIMA(p, d, q)에서 p = 0(AR 없음), d = 1(1차 차분), q = 1(MA(1)).",
      [("Wikipedia: ARIMA", 'Autoregressive_integrated_moving_average')], ["differenc"])
    C(182, "3-2-4", ["시계열", "분해"], "기본", "아이스크림 판매량이 매년 여름마다 늘고 겨울마다 주는 것처럼, 일정한 주기로 반복되는 변동 요인은?",
      "계절 요인", ["추세 요인", "순환 요인", "불규칙 요인"],
      "고정된 주기(연·월·요일)로 반복되는 변동은 계절 요인이다.",
      [("Wikipedia: Decomposition of time series", 'Decomposition_of_time_series')], ["seasonal"])
    C(183, "3-2-4", ["시계열", "분해"], "실전", "경기 변동처럼 반복은 되지만 주기가 일정하지 않고 보통 1년보다 긴 변동 요인은?",
      "순환 요인", ["계절 요인", "추세 요인", "불규칙 요인"],
      "순환 요인은 고정되지 않은 주기의 상승·하락이다. 주기가 고정되면 계절 요인이다.",
      [("Wikipedia: Decomposition of time series", 'Decomposition_of_time_series')], ["cyclical"])
    C(184, "3-2-4", ["시계열", "백색잡음"], "실전", "평균이 0이고 분산이 일정하며 서로 자기상관이 없는 시계열은?",
      "백색잡음", ["랜덤워크", "추세 시계열", "계절 시계열"],
      "백색잡음은 서로 상관없는(uncorrelated) 확률변수열로, 평균 0·일정 분산이다.",
      [("Wikipedia: White noise", 'White_noise')], ["uncorrelated"])
    E(185, "3-2-4", ["시계열", "이동평균"], "기본", "4, 6, 8, 10의 2기간 이동평균(연속한 두 값의 평균)은?", "",
      "as.numeric(na.omit(stats::filter(c(4, 6, 8, 10), rep(1/2, 2), sides = 1)))", "x = [4, 6, 8, 10]; result = [(a + b) / 2 for a, b in zip(x, x[1:])]", "5 7 9",
      "5 7 9", ["4 6 8", "6 8 10", "5 6 7"], "(4 + 6) / 2, (6 + 8) / 2, (8 + 10) / 2 = 5, 7, 9.")
    E(186, "3-2-4", ["시계열", "지수평활"], "실전", "단순 지수평활에서 α = 0.2, 이전 평활값 50, 이번 관측값 60일 때 새 평활값은?", "",
      "0.2 * 60 + 0.8 * 50", "result = 0.2 * 60 + 0.8 * 50", "52",
      "52", ["58", "55", "60"], "s = α·x + (1 − α)·s_prev = 0.2 × 60 + 0.8 × 50 = 52. α가 작을수록 과거 평활값에 더 무게를 둔다.")
    E(187, "3-2-4", ["시계열", "자기상관"], "고난도", "다음 R 코드의 결과(시차 1 자기상관)는?", "acf(c(1, 2, 3, 4, 5), plot = FALSE)$acf[2]",
      "acf(c(1, 2, 3, 4, 5), plot = FALSE)$acf[2]",
      "x = np.array([1, 2, 3, 4, 5.]); d = x - x.mean(); result = float((d[:-1] * d[1:]).sum() / (d ** 2).sum())", "0.4",
      "0.4", ["1", "0.8", "0.5"], "R의 acf는 Σ(xₜ − x̄)(xₜ₊₁ − x̄) / Σ(xₜ − x̄)² = 4 / 10 = 0.4로 계산한다.", [("R 문서: acf", RD + 'stats/html/acf.html')])
    C(188, "3-2-4", ["시계열", "정상성 검정"], "고난도", "시계열에 단위근(unit root)이 있어 비정상인지 검정하는 방법은?",
      "ADF(확장 디키-풀러) 검정", ["샤피로-윌크 검정", "카이제곱 검정", "투키 HSD"],
      "ADF 검정의 귀무가설은 '단위근이 있다(비정상)'이다.",
      [("Wikipedia: Augmented Dickey–Fuller test", 'Augmented_Dickey%E2%80%93Fuller_test')], ["unit root"])
    C(189, "3-2-4", ["시계열", "정상성"], "실전", "시간이 갈수록 변동 폭이 커지는 시계열의 분산을 안정시키기 위해 흔히 적용하는 방법은?",
      "로그를 취한다", ["원자료를 그대로 쓴다", "관측 순서를 뒤집는다", "누적합으로 바꾼다"],
      "로그 같은 분산 안정화 변환으로 변동 폭을 일정하게 만든 뒤, 추세는 차분으로 제거한다.",
      [("Wikipedia: Variance-stabilizing transformation", 'Variance-stabilizing_transformation')], ["logarithm"])
    E(190, "3-2-4", ["시계열", "차분"], "기본", "다음 R 코드의 실행 결과는?", "diff(c(100, 103, 101, 106))",
      "diff(c(100, 103, 101, 106))", "result = list(np.diff([100, 103, 101, 106]))", "3 -2 5",
      "3 -2 5", ["103 101 106", "3 2 5", "-3 2 -5"], "diff는 이웃한 값의 차이(뒤 − 앞)를 구한다: 3, −2, 5. 차분은 추세를 없애 정상성을 만드는 데 쓴다.")
