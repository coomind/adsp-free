"""s3-191~240: 3-3-1 데이터 마이닝 개요, 3-3-2 분류분석, 3-3-3 군집분석, 3-3-4 연관분석 (빈출: 혼동행렬 지표, 연관 규칙)"""
import itertools, math
import numpy as np
import statsmodels.api as sm

RD = 'https://stat.ethz.ch/R-manual/R-devel/library/'
f3 = lambda v: f"{v:.3f}"

# confusion matrix used by several questions (예측 × 실제)
TP, FN, FP, TN = 45, 15, 5, 35
CM = ("            실제 양성  실제 음성\n"
      f"예측 양성      {TP:>3}        {FP:>3}\n"
      f"예측 음성      {FN:>3}        {TN:>3}")

# logistic regression data
LX = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
LY = [0, 0, 0, 1, 0, 1, 0, 1, 1, 1]
RL = 'x <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10); y <- c(0, 0, 0, 1, 0, 1, 0, 1, 1, 1)'
lg = sm.Logit(LY, sm.add_constant(LX)).fit(disp=0)
OR = math.exp(lg.params[1])

# transactions for association rules
T = [{'우유', '빵', '달걀'}, {'빵', '기저귀', '맥주'}, {'우유', '빵', '기저귀', '맥주'}, {'우유', '빵'}, {'빵', '달걀'},
     {'우유', '기저귀', '맥주'}, {'우유', '빵', '달걀', '기저귀'}, {'빵', '맥주'}, {'우유', '달걀'}, {'우유', '빵', '맥주'}]
TX = '\n'.join(f"T{k + 1:<2} {', '.join(sorted(t))}" for k, t in enumerate(T))
ITEMS = ['기저귀', '달걀', '맥주', '빵', '우유']
sup = lambda *s: sum(set(s) <= t for t in T) / len(T)
conf = lambda a, b: sup(a, b) / sup(a)
lift = lambda a, b: conf(a, b) / sup(b)
# R: the same transactions as a 0/1 matrix (rows T1..T10, columns ITEMS)
RT = 'm <- matrix(c(' + ', '.join(str(int(i in t)) for t in T for i in ITEMS) + f'), nrow = 10, byrow = TRUE, dimnames = list(NULL, c({", ".join(chr(34) + i + chr(34) for i in ITEMS)})))'
PT = f"T = {[sorted(t) for t in T]!r}\nsup = lambda *s: sum(set(s) <= set(t) for t in T) / len(T)\n"


def add(E, C):
    # --- 3-3-1 데이터 마이닝 개요
    C(191, "3-3-1", ["지도학습"], "기본", "과거 고객 데이터에 '이탈함/유지함'이라는 정답이 붙어 있고, 이를 학습해 새 고객의 이탈을 예측하려 한다. 이 학습 방식은?",
      "지도학습", ["비지도학습", "강화학습", "연관 규칙 학습"],
      "정답(레이블)이 있는 데이터로 입력과 출력의 관계를 배우는 것이 지도학습이다.", [("Wikipedia: Supervised learning", 'Supervised_learning')], ["labeled"])
    C(192, "3-3-1", ["데이터 분할"], "실전", "모델의 하이퍼파라미터(예: 나무 깊이)를 고를 때 성능을 비교하는 데 쓰고, 최종 평가에는 쓰지 않는 데이터는?",
      "검증(validation) 데이터", ["훈련(training) 데이터", "시험(test) 데이터", "모집단 데이터"],
      "검증 데이터는 모델 선택·튜닝에, 시험 데이터는 마지막 한 번의 성능 평가에 쓴다.",
      [("Wikipedia: Training, validation, and test data sets", 'Training,_validation,_and_test_data_sets')], ["validation data set"])
    E(193, "3-3-1", ["붓스트랩"], "고난도", "n = 1000개 관측치에서 복원추출로 붓스트랩 표본(크기 1000)을 만들 때, 특정 관측치가 한 번도 뽑히지 않을 확률은? (소수 셋째 자리까지)", "",
      "r3((1 - 1/1000)^1000)", "result = round((1 - 1 / 1000) ** 1000, 3)", "0.368",
      "0.368", ["0.632", "0.500", "0.001"], "(1 − 1/n)ⁿ ≈ e⁻¹ ≈ 0.368. 그래서 붓스트랩 표본에는 원래 관측치의 약 63.2%만 들어가고, 뽑히지 않은 약 36.8%(OOB)로 평가할 수 있다.",
      [("Wikipedia: Bootstrapping (statistics)", 'Bootstrapping_(statistics)')])
    E(194, "3-3-1", ["교차검증"], "실전", "관측치 100개로 LOOCV(하나씩 빼고 교차검증)를 하면 모델을 몇 번 학습하는가?", "",
      "100", "result = 100", "100",
      "100번", ["10번", "1번", "99번"], "LOOCV는 관측치 하나를 검증용으로 빼고 나머지로 학습하는 것을 n번 반복한다.",
      [("Wikipedia: Cross-validation (statistics)", 'Cross-validation_(statistics)')])
    C(195, "3-3-1", ["과대적합"], "실전", "훈련 데이터 정확도는 99%인데 처음 보는 시험 데이터 정확도는 70%다. 가장 의심되는 문제와 대응은?",
      "과대적합이므로 모델을 단순화하거나 규제를 둔다", ["과소적합이므로 변수를 더 추가한다", "데이터가 너무 많으므로 줄인다", "정상이므로 그대로 쓴다"],
      "훈련 데이터에 지나치게 맞춰져 새 데이터에서 성능이 떨어지는 과대적합이다. 모델 단순화·규제·가지치기·교차검증으로 대응한다.",
      [("Wikipedia: Overfitting", 'Overfitting')], ["overfitting"])
    C(196, "3-3-1", ["분석 유형"], "기본", "메일을 '스팸/정상' 중 하나로 나누는 것처럼, 미리 정해진 범주 중 어디에 속하는지 예측하는 작업은?",
      "분류", ["군집", "연관 규칙", "차원 축소"],
      "분류는 새 관측치가 어느 범주(클래스)에 속하는지 예측하는 지도학습 작업이다.", [("Wikipedia: Statistical classification", 'Statistical_classification')], ["classification"])
    C(197, "3-3-1", ["분석 유형"], "기본", "정답 없이 비슷한 고객끼리 묶어 몇 개의 그룹을 찾는 작업은?",
      "군집 분석", ["분류", "회귀", "시계열 예측"],
      "군집 분석은 레이블 없이 서로 비슷한 객체끼리 묶는 비지도학습이다.", [("Wikipedia: Cluster analysis", 'Cluster_analysis')], ["cluster analysis"])

    # --- 3-3-2 분류분석: 혼동행렬 (최빈출)
    Q = f"다음 혼동행렬에서 {{}}는? (소수 셋째 자리까지)"
    E(198, "3-3-2", ["혼동행렬", "정확도"], "실전", Q.format("정확도(accuracy)"), CM, f"r3(({TP} + {TN}) / 100)", f"result = round(({TP} + {TN}) / 100, 3)", f3((TP + TN) / 100),
      f3((TP + TN) / 100), [f3(TP / (TP + FN)), "0.850", "0.700"], f"정확도 = (TP + TN) / 전체 = ({TP} + {TN}) / 100.")
    E(199, "3-3-2", ["혼동행렬", "재현율"], "실전", Q.format("재현율(민감도)"), CM, f"r3({TP} / ({TP} + {FN}))", f"result = round({TP} / ({TP} + {FN}), 3)", f3(TP / (TP + FN)),
      f3(TP / (TP + FN)), [f3(TP / (TP + FP)), f3(FN / (TP + FN)), "0.667"], f"재현율 = TP / (TP + FN) = {TP} / {TP + FN}. 실제 양성 중 맞게 찾은 비율이다.")
    E(200, "3-3-2", ["혼동행렬", "특이도"], "실전", Q.format("특이도(specificity)"), CM, f"r3({TN} / ({TN} + {FP}))", f"result = round({TN} / ({TN} + {FP}), 3)", f3(TN / (TN + FP)),
      f3(TN / (TN + FP)), [f3(FP / (FP + TN)), f3(TN / (TN + FN)), "0.750"], f"특이도 = TN / (TN + FP) = {TN} / {TN + FP}. 실제 음성 중 음성으로 맞힌 비율이다.")
    E(201, "3-3-2", ["혼동행렬", "정밀도"], "실전", Q.format("정밀도(precision)"), CM, f"r3({TP} / ({TP} + {FP}))", f"result = round({TP} / ({TP} + {FP}), 3)", f3(TP / (TP + FP)),
      f3(TP / (TP + FP)), [f3(TP / (TP + FN)), f3(FP / (TP + FP)), "0.818"], f"정밀도 = TP / (TP + FP) = {TP} / {TP + FP}. 양성이라고 예측한 것 중 실제 양성 비율이다.")
    F1 = 2 * (TP / (TP + FP)) * (TP / (TP + FN)) / ((TP / (TP + FP)) + (TP / (TP + FN)))
    E(202, "3-3-2", ["혼동행렬", "F1"], "고난도", Q.format("F1 점수"), CM, f"p <- {TP} / ({TP} + {FP}); r <- {TP} / ({TP} + {FN}); r3(2 * p * r / (p + r))",
      f"p = {TP} / ({TP} + {FP}); r = {TP} / ({TP} + {FN}); result = round(2 * p * r / (p + r), 3)", f3(F1),
      f3(F1), [f3(((TP / (TP + FP)) + (TP / (TP + FN))) / 2), "0.800", "0.765"], "F1 = 2 × 정밀도 × 재현율 / (정밀도 + 재현율). 단순 평균(산술평균)이 아니라 조화평균이다.")
    E(203, "3-3-2", ["혼동행렬", "ROC"], "고난도", Q.format("거짓 양성률(FPR)"), CM, f"r3({FP} / ({FP} + {TN}))", f"result = round({FP} / ({FP} + {TN}), 3)", f3(FP / (FP + TN)),
      f3(FP / (FP + TN)), [f3(FN / (FN + TP)), f3(FP / (FP + TP)), "0.875"], "FPR = FP / (FP + TN) = 1 − 특이도. ROC 곡선의 x축이다.")
    E(204, "3-3-2", ["혼동행렬", "오분류율"], "기본", Q.format("오분류율(error rate)"), CM, f"r3(({FP} + {FN}) / 100)", f"result = round(({FP} + {FN}) / 100, 3)", f3((FP + FN) / 100),
      f3((FP + FN) / 100), [f3(FP / 100), f3(FN / 100), "0.800"], "오분류율 = (FP + FN) / 전체 = 1 − 정확도.")
    C(205, "3-3-2", ["혼동행렬", "민감도"], "실전", "분류 지표 중 재현율(recall)과 같은 뜻의 지표는?",
      "민감도(참 양성률, TPR)", ["특이도", "정밀도", "거짓 양성률(FPR)"],
      "재현율 = 민감도 = 참 양성률(TPR) = TP / (TP + FN).", [("Wikipedia: Sensitivity and specificity", 'Sensitivity_and_specificity')], ["true positive rate"])
    C(206, "3-3-2", ["ROC"], "실전", "ROC 곡선의 x축과 y축으로 옳은 것은?",
      "x축 거짓 양성률(1 − 특이도), y축 참 양성률(민감도)", ["x축 정밀도, y축 재현율", "x축 민감도, y축 특이도", "x축 임계값, y축 정확도"],
      "ROC 곡선은 임계값을 바꾸며 FPR(x)에 대한 TPR(y)을 그린다. 정밀도-재현율 곡선과 헷갈리지 말자.",
      [("Wikipedia: Receiver operating characteristic", 'Receiver_operating_characteristic')], ["false positive rate", "true positive rate"])
    C(207, "3-3-2", ["임계값", "정밀도·재현율"], "고난도", "다른 조건이 같을 때, 분류 임계값(양성으로 판정하는 기준 확률)을 0.5에서 0.9로 올리면 일반적으로 나타나는 경향은?",
      "정밀도는 대체로 오르고 재현율은 떨어진다", ["정밀도와 재현율이 함께 오른다", "재현율은 오르고 정밀도는 떨어진다", "어떤 지표도 변하지 않는다"],
      "기준을 높이면 확실한 것만 양성으로 판정해 놓치는 양성이 늘어 재현율은 낮아지거나 같다. 거짓 양성이 줄어 정밀도는 대체로 높아지는 경향이 있지만, 데이터에 따라 항상 오르지는 않는다.",
      [("Wikipedia: Precision and recall", 'Precision_and_recall')], ["precision", "recall"])
    # 로지스틱 회귀
    E(208, "3-3-2", ["로지스틱 회귀", "R 출력 해석"], "고난도", "다음 로지스틱 회귀 결과에서 x가 1 증가할 때 오즈는 약 몇 배가 되는가? (소수 셋째 자리까지)",
      f"{RL}\nfit <- glm(y ~ x, family = binomial)\ncoef(summary(fit))", f"{RL}; r3(exp(coef(glm(y ~ x, family = binomial))[[2]]))",
      f"m = sm.Logit({LY}, sm.add_constant({LX})).fit(disp=0); result = round(math.exp(m.params[1]), 3)", f3(OR),
      f3(OR), [f3(lg.params[1]), f3(1 / OR), f3(math.exp(lg.params[0]))], "로지스틱 회귀 계수 β는 로그 오즈의 변화다. 오즈비 = e^β이므로 x의 Estimate에 exp를 취한다.",
      [("R 문서: glm", RD + 'stats/html/glm.html')], run=True)
    E(209, "3-3-2", ["로지스틱 회귀"], "실전", "로지스틱 회귀식 log(p / (1 − p)) = −2 + 0.5x에서 x = 6일 때 예측 확률 p는? (소수 셋째 자리까지)", "",
      "r3(plogis(-2 + 0.5 * 6))", "result = round(1 / (1 + math.exp(-(-2 + 0.5 * 6))), 3)", "0.731",
      "0.731", ["1.000", "0.500", "0.269"], "선형 예측값 −2 + 3 = 1, p = 1 / (1 + e⁻¹) ≈ 0.731.")
    C(210, "3-3-2", ["로지스틱 회귀"], "실전", "로지스틱 회귀에서 설명변수의 선형결합과 같다고 두는 것은?",
      "성공 확률의 로그 오즈(logit)", ["성공 확률 그 자체", "반응변수의 제곱", "잔차의 분산"],
      "로지스틱 회귀는 log(p / (1 − p)) = β₀ + β₁x로, 확률이 아니라 로그 오즈를 선형으로 모형화한다.",
      [("Wikipedia: Logistic regression", 'Logistic_regression')], ["log-odds"])
    # 의사결정나무
    ENT = lambda ps: -sum(p * math.log2(p) for p in ps if p > 0)
    IG = 1 - (0.4 * 0 + 0.6 * ENT([1 / 6, 5 / 6]))
    E(211, "3-3-2", ["의사결정나무", "정보이득"], "고난도", "양성 5 · 음성 5인 노드(엔트로피 1)를 나눠 왼쪽(양성 4 · 음성 0), 오른쪽(양성 1 · 음성 5)을 만들었다. 정보이득은? (엔트로피 밑 2, 소수 셋째 자리까지)", "",
      "H <- function(p) -sum(ifelse(p > 0, p * log2(p), 0)); r3(1 - (4/10 * H(c(1, 0)) + 6/10 * H(c(1/6, 5/6))))",
      "H = lambda ps: -sum(p * math.log2(p) for p in ps if p > 0); result = round(1 - (0.4 * H([1, 0]) + 0.6 * H([1/6, 5/6])), 3)", f3(IG),
      f3(IG), [f3(ENT([1 / 6, 5 / 6])), f3(1 - IG), "1.000"], f"정보이득 = 부모 엔트로피 − 자식 엔트로피의 가중평균 = 1 − (0.4 × 0 + 0.6 × {ENT([1/6, 5/6]):.3f}).",
      [("Wikipedia: Decision tree learning", 'Decision_tree_learning')])
    GW = 0.6 * (1 - (1 / 6) ** 2 - (5 / 6) ** 2)
    E(212, "3-3-2", ["의사결정나무", "지니"], "고난도", "s3-211과 같은 분할(왼쪽 4개 모두 양성, 오른쪽 양성 1 · 음성 5)의 자식 노드 지니 불순도 가중평균은? (소수 셋째 자리까지)".replace("s3-211과 같은 분할", "10개 관측치를 나눈 분할"), "",
      "g <- function(p) 1 - sum(p^2); r3(4/10 * g(c(1, 0)) + 6/10 * g(c(1/6, 5/6)))",
      "g = lambda ps: 1 - sum(p * p for p in ps); result = round(0.4 * g([1, 0]) + 0.6 * g([1/6, 5/6]), 3)", f3(GW),
      f3(GW), [f3(1 - (1 / 6) ** 2 - (5 / 6) ** 2), "0.500", f3(0.5 - GW)], "지니 = 1 − Σp². 왼쪽 0, 오른쪽 1 − (1/36 + 25/36) ≈ 0.278, 가중평균 = 0.6 × 0.278.",
      [("Wikipedia: Decision tree learning", 'Decision_tree_learning')])
    C(213, "3-3-2", ["의사결정나무", "가지치기"], "실전", "의사결정나무에서 가지치기(pruning)를 하는 주된 이유는?",
      "과대적합을 줄여 새 데이터에 대한 성능을 높이려고", ["분기를 더 늘려 훈련 데이터의 분류 규칙을 더 정교하게 만들려고", "과소적합을 해결하려고", "훈련 데이터를 모두 정확히 맞히는 나무를 만들려고"],
      "가지치기는 분류에 기여가 적은 가지를 잘라 나무를 단순하게 만들어 과대적합을 줄인다.",
      [("Wikipedia: Decision tree pruning", 'Decision_tree_pruning')], ["overfitting"])
    # 앙상블·신경망·기타 분류기 (빈출)
    C(214, "3-3-2", ["앙상블", "배깅"], "실전", "원자료에서 복원추출한 여러 붓스트랩 표본으로 모델을 각각 학습하고, 결과를 투표·평균으로 합치는 앙상블 기법은?",
      "배깅(Bagging)", ["부스팅(Boosting)", "스태킹(Stacking)", "가지치기(Pruning)"],
      "배깅(bootstrap aggregating)은 붓스트랩 표본마다 모델을 만들어 결과를 합친다. 부스팅은 앞 모델의 오류에 가중치를 두며 순차적으로 학습한다.",
      [("Wikipedia: Bootstrap aggregating", 'Bootstrap_aggregating')], ["bootstrap"])
    C(215, "3-3-2", ["앙상블", "부스팅"], "실전", "약한 학습기를 순차적으로 추가하며 앞 모델의 오류를 보완해 성능을 높이는 앙상블 기법은? (예: AdaBoost는 틀린 관측치에 더 큰 가중치를 준다)",
      "부스팅(Boosting)", ["배깅(Bagging)", "랜덤 포레스트", "k-최근접 이웃"],
      "부스팅은 이전 학습기의 오류를 보완하도록 약한 학습기를 순차적으로 결합한다. AdaBoost는 잘못 분류된 관측치의 가중치를 높이고, 그래디언트 부스팅은 이전 모델의 잔차를 학습한다. 배깅·랜덤 포레스트는 학습기를 독립적으로 만든다.",
      [("Wikipedia: Boosting (machine learning)", 'Boosting_(machine_learning)')], ["weak learner"])
    C(216, "3-3-2", ["앙상블", "랜덤 포레스트"], "고난도", "랜덤 포레스트에서 각 나무를 만들 때 붓스트랩 표본에 뽑히지 않은 관측치로 따로 검증 데이터 없이 오차를 추정하는 방법은?",
      "OOB(out-of-bag) 오차", ["훈련 오차", "잔차 제곱합", "AIC"],
      "각 나무의 붓스트랩 표본에서 빠진 관측치(OOB)로 예측 오차를 추정할 수 있다.",
      [("Wikipedia: Random forest", 'Random_forest')], ["out-of-bag"])
    E(217, "3-3-2", ["신경망", "시그모이드"], "기본", "시그모이드 함수 f(x) = 1 / (1 + e^(−x))에서 f(0)의 값은?", "",
      "1 / (1 + exp(0))", "result = 1 / (1 + math.exp(0))", "0.5",
      "0.5", ["0", "1", "−1"], "e⁰ = 1이므로 1 / 2 = 0.5. 시그모이드는 출력을 0과 1 사이로 바꿔 이진 분류의 확률처럼 쓴다.",
      [("Wikipedia: Sigmoid function", 'Sigmoid_function')])
    SM = np.exp([1, 2, 3]) / np.exp([1, 2, 3]).sum()
    E(218, "3-3-2", ["신경망", "소프트맥스"], "고난도", "출력층 값이 (1, 2, 3)일 때 소프트맥스 함수를 적용한 세 번째 클래스의 확률은? (소수 셋째 자리까지)", "",
      "z <- c(1, 2, 3); r3(exp(z[3]) / sum(exp(z)))", "z = np.array([1, 2, 3]); result = round(float(np.exp(z[2]) / np.exp(z).sum()), 3)", f3(SM[2]),
      f3(SM[2]), ["0.500", f3(1 / 3), f3(SM[1])], "소프트맥스는 e^zᵢ / Σe^z로 모든 클래스 확률의 합이 1이 되게 한다: e³ / (e + e² + e³) ≈ 0.665. 다중 클래스 분류의 출력층에 쓴다.",
      [("Wikipedia: Softmax function", 'Softmax_function')])
    C(219, "3-3-2", ["k-NN"], "고난도", "k-최근접 이웃(k-NN)에서 k를 1처럼 아주 작게 잡을 때의 특징으로 옳은 것은?",
      "잡음이 섞인 관측치 하나에도 결과가 흔들려 과대적합되기 쉽다", ["결정 경계가 매우 매끄러워진다", "학습 단계에서 모델 계수를 추정한다", "k와 무관하게 결과가 같다"],
      "k가 작으면 가장 가까운 한두 이웃에 좌우돼 잡음에 민감하다. k가 크면 경계가 매끄러워지지만 과소적합될 수 있다.",
      [("Wikipedia: k-nearest neighbors algorithm", 'K-nearest_neighbors_algorithm')], ["noise"])

    # --- 3-3-3 군집분석
    E(220, "3-3-3", ["계층적 군집", "평균 연결"], "실전", "수직선 위 군집 {0, 1}과 {4, 6} 사이의 평균 연결(average linkage) 거리는?", "",
      "mean(abs(outer(c(0, 1), c(4, 6), '-')))", "result = np.mean([abs(a - b) for a in (0, 1) for b in (4, 6)])", "4.5",
      "4.5", ["3", "6", "5"], "평균 연결은 두 군집의 모든 점 쌍 거리의 평균: (4 + 6 + 3 + 5) / 4 = 4.5. 단일 연결은 최소 3, 완전 연결은 최대 6이다.",
      [("Wikipedia: Hierarchical clustering", 'Hierarchical_clustering')])
    C(221, "3-3-3", ["계층적 군집", "와드"], "실전", "군집을 합칠 때 군집 내 오차제곱합(WSS)의 증가량이 가장 작은 쌍을 먼저 합치는 연결법은?",
      "와드(Ward) 연결법", ["단일 연결법", "완전 연결법", "중심 연결법"],
      "와드 방법은 병합으로 늘어나는 군집 내 오차제곱합이 가장 작은 두 군집을 합친다(최소 분산 기준).",
      [("Wikipedia: Ward's method", "Ward%27s_method")], ["minimum variance"])
    E(222, "3-3-3", ["계층적 군집", "R 코드"], "고난도", "다음 R 코드의 실행 결과는?", "cutree(hclust(dist(c(1, 2, 6, 7, 15))), k = 2)",
      "cutree(hclust(dist(c(1, 2, 6, 7, 15))), k = 2)",
      "from scipy.cluster.hierarchy import linkage, fcluster\nlab = fcluster(linkage([[1], [2], [6], [7], [15]], 'complete'), 2, 'maxclust')\nfirst = {}\nresult = [first.setdefault(v, len(first) + 1) for v in lab]",
      "1 1 1 1 2", "1 1 1 1 2", ["1 1 2 2 2", "1 1 2 2 3", "1 2 1 2 1"],
      "hclust 기본은 완전 연결. {1, 2}, {6, 7}이 먼저 묶이고 두 군집이 합쳐진 뒤 15가 마지막에 합쳐지므로, 2개로 자르면 {1, 2, 6, 7}과 {15}.",
      [("R 문서: cutree", RD + 'stats/html/cutree.html')])
    C(223, "3-3-3", ["k-means", "엘보"], "실전", "k-means에서 k를 늘려 가며 군집 내 제곱합을 그렸을 때 감소 폭이 급격히 줄어드는 지점을 k로 고르는 방법은?",
      "엘보(elbow) 방법", ["실루엣 폭 최대화", "덴드로그램 절단", "AIC 최소화"],
      "엘보 방법은 설명되는 변동의 증가가 꺾이는 팔꿈치 지점에서 k를 고른다.", [("Wikipedia: Elbow method (clustering)", 'Elbow_method_(clustering)')], ["elbow"])
    C(224, "3-3-3", ["실루엣"], "실전", "군집 결과를 평가하는 실루엣 계수에 대한 설명으로 옳은 것은?",
      "−1에서 1 사이 값이며 1에 가까울수록 자기 군집에 잘 속해 있다", ["0에서 100 사이 값이며 클수록 나쁘다", "항상 음수다", "군집 수와 같은 값을 가진다"],
      "실루엣 값은 −1 ~ +1이며, 클수록 자기 군집과 잘 맞고 이웃 군집과 멀다.", [("Wikipedia: Silhouette (clustering)", 'Silhouette_(clustering)')], ["silhouette value ranges from"])
    E(225, "3-3-3", ["실루엣"], "고난도", "어떤 점의 자기 군집 내 평균 거리 a = 2, 가장 가까운 다른 군집까지의 평균 거리 b = 5일 때 실루엣 값 s = (b − a) / max(a, b)는?", "",
      "(5 - 2) / max(2, 5)", "result = (5 - 2) / max(2, 5)", "0.6",
      "0.6", ["1.5", "0.4", "3"], "s = (5 − 2) / 5 = 0.6. 1에 가까울수록 군집이 잘 나뉜 것이다.", [("Wikipedia: Silhouette (clustering)", 'Silhouette_(clustering)')])
    C(226, "3-3-3", ["DBSCAN"], "실전", "군집 수를 미리 정하지 않고 밀도가 높은 영역을 군집으로 찾으며, 어느 군집에도 속하지 않는 점을 잡음으로 처리하는 방법은?",
      "DBSCAN", ["k-means", "와드 연결법", "주성분 분석"],
      "DBSCAN은 밀도 기반 군집으로 임의 모양의 군집을 찾고 저밀도 점을 잡음(noise)으로 둔다. k를 미리 정하지 않는다.",
      [("Wikipedia: DBSCAN", 'DBSCAN')], ["noise"])
    C(227, "3-3-3", ["SOM"], "실전", "고차원 데이터를 2차원 격자 지도로 표현하며, 경쟁 학습으로 입력과 가장 가까운 뉴런과 그 이웃을 갱신하는 신경망 기반 군집 방법은?",
      "자기조직화지도(SOM)", ["DBSCAN", "k-medoids", "계층적 군집"],
      "SOM은 경쟁 학습(competitive learning)으로 입력 공간의 구조를 저차원 격자에 보존한다.",
      [("Wikipedia: Self-organizing map", 'Self-organizing_map')], ["competitive learning"])
    C(228, "3-3-3", ["혼합분포 군집", "EM"], "고난도", "가우시안 혼합 모형 군집에서 모수를 추정할 때, 각 점이 어느 분포에 속할지의 기대값을 구하는 단계와 그 기대값으로 모수를 갱신하는 단계를 반복하는 알고리즘은?",
      "EM 알고리즘", ["경사 하강법만 사용", "아프리오리 알고리즘", "배깅"],
      "EM 알고리즘은 E 단계(기대값 계산)와 M 단계(최대화로 모수 갱신)를 수렴할 때까지 반복한다.",
      [("Wikipedia: Expectation–maximization algorithm", 'Expectation%E2%80%93maximization_algorithm')], ["expectation step", "maximization step"])
    C(229, "3-3-3", ["거리", "표준화"], "실전", "연봉(단위 만 원)과 나이(단위 세)로 k-means를 할 때 표준화를 먼저 하는 이유는?",
      "단위가 큰 변수가 거리 계산을 지배하는 것을 막으려고", ["군집 수를 자동으로 정하려고", "결측값을 없애려고", "변수 개수를 줄이려고"],
      "거리 기반 방법은 척도가 큰 변수에 좌우되므로 특성 척도를 맞춘다(feature scaling).",
      [("Wikipedia: Feature scaling", 'Feature_scaling')], ["distance"])
    C(230, "3-3-3", ["거리", "마할라노비스"], "고난도", "변수 사이의 상관(공분산)과 척도 차이를 반영해 거리를 재는 방법은?",
      "마할라노비스 거리", ["유클리드 거리", "맨해튼 거리", "자카드 거리"],
      "마할라노비스 거리는 공분산 행렬을 이용해 변수 간 상관과 척도를 반영한다.", [("Wikipedia: Mahalanobis distance", 'Mahalanobis_distance')], ["covariance"])
    C(231, "3-3-3", ["k-medoids"], "고난도", "k-means가 이상값에 민감한 단점을 줄이려고, 군집 중심으로 평균 대신 실제 관측치 하나(대표점)를 쓰는 방법은?",
      "k-medoids(PAM)", ["k-NN", "DBSCAN", "SOM"],
      "k-medoids는 중심을 실제 데이터 점(medoid)으로 잡아 잡음·이상값에 더 강하다.", [("Wikipedia: k-medoids", 'K-medoids')], ["outliers"])

    # --- 3-3-4 연관분석 (빈출: 지지도·신뢰도·향상도 계산)
    TQ = "거래 10건이 다음과 같다.\n" + TX
    E(232, "3-3-4", ["연관분석", "지지도"], "실전", "다음 거래에서 {빵, 우유}의 지지도는?", TQ,
      f'{RT}; mean(m[, "빵"] == 1 & m[, "우유"] == 1)', PT + "result = sup('빵', '우유')", str(sup('빵', '우유')),
      str(sup('빵', '우유')), [str(round(conf('빵', '우유'), 3)), str(sup('빵')), str(sup('우유'))], "지지도 = 두 품목을 함께 포함한 거래 수 / 전체 거래 수.",
      [("Wikipedia: Association rule learning", 'Association_rule_learning')])
    E(233, "3-3-4", ["연관분석", "신뢰도"], "실전", "다음 거래에서 규칙 {빵} → {우유}의 신뢰도는? (소수 셋째 자리까지)", TQ,
      f'{RT}; r3(sum(m[, "빵"] == 1 & m[, "우유"] == 1) / sum(m[, "빵"] == 1))', PT + "result = round(sup('빵', '우유') / sup('빵'), 3)", f3(conf('빵', '우유')),
      f3(conf('빵', '우유')), [f3(conf('우유', '빵')), f3(sup('빵', '우유')), f3(lift('빵', '우유'))], "신뢰도(A → B) = 지지도(A, B) / 지지도(A): 빵을 산 거래 중 우유도 산 비율.",
      [("Wikipedia: Association rule learning", 'Association_rule_learning')])
    E(234, "3-3-4", ["연관분석", "향상도"], "고난도", "다음 거래에서 규칙 {빵} → {우유}의 향상도는? (소수 셋째 자리까지)", TQ,
      f'{RT}; s <- function(...) mean(apply(m[, c(...), drop = FALSE] == 1, 1, all)); r3(s("빵", "우유") / (s("빵") * s("우유")))',
      PT + "result = round(sup('빵', '우유') / (sup('빵') * sup('우유')), 3)", f3(lift('빵', '우유')),
      f3(lift('빵', '우유')), [f3(conf('빵', '우유')), "1.000", f3(sup('빵', '우유'))],
      f"향상도 = 신뢰도 / 지지도(우유) = 지지도(빵, 우유) / (지지도(빵) × 지지도(우유)). {lift('빵', '우유'):.3f}로 1보다 {'작아 두 품목은 서로 음의 관계(함께 덜 산다)' if lift('빵', '우유') < 1 else '커서 양의 관계'}.",
      [("Wikipedia: Association rule learning", 'Association_rule_learning')])
    E(235, "3-3-4", ["연관분석", "향상도"], "고난도", "다음 거래에서 규칙 {기저귀} → {맥주}의 향상도와 그 해석으로 옳은 것은?", TQ,
      f'{RT}; s <- function(...) mean(apply(m[, c(...), drop = FALSE] == 1, 1, all)); r3(s("기저귀", "맥주") / (s("기저귀") * s("맥주")))',
      PT + "result = round(sup('기저귀', '맥주') / (sup('기저귀') * sup('맥주')), 3)", f3(lift('기저귀', '맥주')),
      f"{lift('기저귀', '맥주'):.3f}, 기저귀를 사면 맥주를 살 가능성이 평소보다 높다",
      [f"{lift('기저귀', '맥주'):.3f}, 두 품목은 서로 독립이다", f"{conf('기저귀', '맥주'):.3f}, 기저귀를 사면 맥주를 살 가능성이 평소보다 낮다", "1.000, 두 품목은 서로 독립이다"],
      "향상도 > 1이면 양의 관계(함께 잘 팔림), = 1이면 독립, < 1이면 음의 관계다.", [("Wikipedia: Association rule learning", 'Association_rule_learning')])
    C(236, "3-3-4", ["연관분석", "아프리오리"], "실전", "아프리오리 알고리즘이 계산량을 줄이는 원리로 옳은 것은?",
      "빈발하지 않은 항목집합의 상위(확대) 집합도 빈발하지 않으므로 탐색에서 뺀다", ["모든 항목 조합을 빠짐없이 계산한다", "신뢰도가 높은 규칙부터 무작위로 뽑는다", "거래 수를 절반으로 줄여 계산한다"],
      "어떤 항목집합이 최소 지지도를 넘지 못하면 그것을 포함하는 더 큰 집합도 넘지 못한다(하향 폐쇄성). 그래서 후보를 크게 줄인다.",
      [("Wikipedia: Apriori algorithm", 'Apriori_algorithm')], ["downward closure"])
    E(237, "3-3-4", ["연관분석", "신뢰도"], "실전", "다음 거래에서 {우유} → {빵}과 {빵} → {우유}의 신뢰도를 비교한 것으로 옳은 것은?", TQ,
      f'{RT}; ab <- sum(m[, "빵"] == 1 & m[, "우유"] == 1); c(r3(ab / sum(m[, "우유"] == 1)), r3(ab / sum(m[, "빵"] == 1)))',
      PT + "ab = sup('빵', '우유'); result = [f'{ab / sup(\"우유\"):.3f}', f'{ab / sup(\"빵\"):.3f}']",
      f"{conf('우유', '빵'):.3f} {conf('빵', '우유'):.3f}",
      f"우유 → 빵 {conf('우유', '빵'):.3f}, 빵 → 우유 {conf('빵', '우유'):.3f}로 방향에 따라 다르다",
      ["두 신뢰도는 항상 같다", f"둘 다 {sup('빵', '우유'):.3f}로 지지도와 같다", f"우유 → 빵 {conf('빵', '우유'):.3f}, 빵 → 우유 {conf('우유', '빵'):.3f}"],
      "지지도와 향상도는 방향이 없지만, 신뢰도는 조건부 확률이라 A → B와 B → A가 다를 수 있다(분모가 다름).",
      [("Wikipedia: Association rule learning", 'Association_rule_learning')])
    FREQ = [i for i in ITEMS if sup(i) >= 0.5]
    E(238, "3-3-4", ["연관분석", "최소 지지도"], "실전", "다음 거래에서 최소 지지도를 0.5로 정할 때 빈발한 단일 품목의 개수는?", TQ,
      f'{RT}; sum(colMeans(m) >= 0.5)', PT + "result = sum(sup(i) >= 0.5 for i in ['기저귀', '달걀', '맥주', '빵', '우유'])", str(len(FREQ)),
      f"{len(FREQ)}개", [f"{k}개" for k in (1, 2, 3, 4, 5) if k != len(FREQ)][:3], "품목별 지지도: " + ", ".join(f"{i} {sup(i):.1f}" for i in ITEMS) + f". 0.5 이상인 {', '.join(FREQ)}만 빈발 품목이다. 최소 지지도를 넘는 항목집합만 다음 단계 후보가 된다.")
    E(239, "3-3-4", ["연관분석", "향상도"], "실전", "지지도(A) = 0.4, 지지도(B) = 0.5, 지지도(A, B) = 0.3일 때 규칙 A → B의 향상도는?", "",
      "0.3 / (0.4 * 0.5)", "result = 0.3 / (0.4 * 0.5)", "1.5",
      "1.5", ["0.75", "0.6", "0.3"], "신뢰도 = 0.3 / 0.4 = 0.75, 향상도 = 0.75 / 0.5 = 1.5. 1보다 커서 양의 관계다.")
    C(240, "3-3-4", ["순차 패턴"], "실전", "'노트북 구매 → 한 달 뒤 마우스 구매'처럼 시간 순서를 고려해 자주 나타나는 구매 흐름을 찾는 방법은?",
      "순차 패턴 분석", ["단순 연관 규칙(장바구니) 분석", "주성분 분석", "k-means 군집"],
      "순차 패턴 마이닝은 순서가 있는 사건 열에서 빈발 패턴을 찾는다. 일반 연관 규칙은 한 거래 안의 동시 발생만 본다.",
      [("Wikipedia: Sequential pattern mining", 'Sequential_pattern_mining')], ["sequential pattern"])
