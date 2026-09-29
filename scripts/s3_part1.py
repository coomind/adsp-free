"""s3-091~136: 3-1-1 R기초, 3-1-2 데이터 마트, 3-1-3 결측값·이상값, 3-2-1 통계학 개론"""
RD = 'https://stat.ethz.ch/R-manual/R-devel/library/'


def add(E, C):
    # --- 3-1-1 R 기초 (코드를 읽고 결과 예측)
    E(91, "3-1-1", ["R 코드", "apply 계열"], "실전", "다음 R 코드의 실행 결과는?", "sapply(1:3, function(i) i^2)",
      "sapply(1:3, function(i) i^2)", "result = [i**2 for i in range(1, 4)]", "1 4 9",
      "1 4 9", ["1 2 3", "2 4 6", "1 8 27"], "sapply는 각 원소에 함수를 적용해 벡터로 돌려준다. 1², 2², 3² = 1 4 9.", [("R 문서: lapply/sapply", RD + 'base/html/lapply.html')])
    E(92, "3-1-1", ["R 코드", "인덱싱"], "기본", "다음 R 코드의 실행 결과는?", "x <- c(5, 3, 8)\nwhich.max(x)",
      "x <- c(5, 3, 8); which.max(x)", "result = [5, 3, 8].index(8) + 1", "3",
      "3", ["8", "1", "2"], "which.max는 최댓값의 '위치'를 돌려준다. 8은 세 번째에 있다.")
    E(93, "3-1-1", ["R 코드", "빈도표"], "실전", "다음 R 코드의 실행 결과는?", 'as.vector(table(c("a", "b", "a", "c", "a")))',
      'as.vector(table(c("a", "b", "a", "c", "a")))', "from collections import Counter\nc = Counter('abaca'); result = [c[k] for k in sorted(c)]", "3 1 1",
      "3 1 1", ["1 1 3", "3 2 1", "1 3 1"], "table은 값을 정렬된 순서(a, b, c)로 세어 준다. a 3번, b 1번, c 1번.")
    E(94, "3-1-1", ["R 코드", "누적합"], "기본", "다음 R 코드의 실행 결과는?", "cumsum(1:4)",
      "cumsum(1:4)", "result = list(np.cumsum([1, 2, 3, 4]))", "1 3 6 10",
      "1 3 6 10", ["1 2 3 4", "10", "4 3 2 1"], "cumsum은 누적 합: 1, 1+2, 1+2+3, 1+2+3+4.")
    E(95, "3-1-1", ["R 코드", "데이터 프레임"], "실전", "다음 R 코드의 실행 결과는?", 'df <- data.frame(a = 1:3, b = c(2, 4, 6))\ndf[df$a >= 2, "b"]',
      'df <- data.frame(a = 1:3, b = c(2, 4, 6)); df[df$a >= 2, "b"]', "result = [b for a, b in zip([1, 2, 3], [2, 4, 6]) if a >= 2]", "4 6",
      "4 6", ["2 4", "6", "2 4 6"], "a가 2 이상인 행(2·3행)의 b 열 값: 4, 6.")
    E(96, "3-1-1", ["R 코드", "자료 구조"], "실전", "다음 R 코드의 실행 결과는?", "class(lapply(1:2, sqrt))",
      "class(lapply(1:2, sqrt))", "result = 'list'", "list",
      '"list"', ['"numeric"', '"matrix"', '"character"'], "lapply는 항상 리스트를 돌려준다. 벡터로 받고 싶으면 sapply를 쓴다.", [("R 문서: lapply/sapply", RD + 'base/html/lapply.html')])
    E(97, "3-1-1", ["R 코드", "재사용 규칙"], "고난도", "다음 R 코드의 실행 결과는?", "c(1, 2, 3, 4) + c(10, 20)",
      "c(1, 2, 3, 4) + c(10, 20)", "result = [a + b for a, b in zip([1, 2, 3, 4], [10, 20] * 2)]", "11 22 13 24",
      "11 22 13 24", ["11 22 33 44", "11 22", "에러가 난다"], "길이가 짧은 벡터는 반복(재사용)된다: 10, 20, 10, 20을 더해 11 22 13 24.")
    E(98, "3-1-1", ["R 코드", "문자열"], "기본", "다음 R 코드의 실행 결과는?", 'nchar(c("R", "ADsP"))',
      'nchar(c("R", "ADsP"))', "result = [len('R'), len('ADsP')]", "1 4",
      "1 4", ["2", "5", "1 1"], "nchar는 원소마다 글자 수를 센다: 'R'은 1, 'ADsP'는 4.")
    E(99, "3-1-1", ["R 코드", "행렬"], "실전", "다음 R 코드의 실행 결과는?", "m <- matrix(1:6, nrow = 2, byrow = TRUE)\nm[2, 1]",
      "m <- matrix(1:6, nrow = 2, byrow = TRUE); m[2, 1]", "result = np.arange(1, 7).reshape(2, 3)[1, 0]", "4",
      "4", ["2", "3", "5"], "byrow = TRUE면 행부터 채운다: 1행 1 2 3, 2행 4 5 6. m[2, 1] = 4.", [("R 문서: matrix", RD + 'base/html/matrix.html')])
    E(100, "3-1-1", ["R 코드", "결측값"], "기본", "다음 R 코드의 실행 결과는?", "is.na(NA + 1)",
      "is.na(NA + 1)", "result = True", "TRUE",
      "TRUE", ["FALSE", "NA", "에러가 난다"], "NA가 들어간 계산 결과는 NA이므로 is.na는 TRUE다.")

    # --- 3-1-2 데이터 마트 (요약·결합·변환)
    E(101, "3-1-2", ["R 코드", "그룹 요약"], "실전", "다음 R 코드를 실행했을 때 a와 b 그룹의 값은 각각 얼마인가?", 'tapply(c(10, 20, 30, 40), c("a", "b", "a", "b"), mean)',
      'unname(tapply(c(10, 20, 30, 40), c("a", "b", "a", "b"), mean))', "result = [np.mean([10, 30]), np.mean([20, 40])]", "20 30",
      "a = 20, b = 30", ["a = 25, b = 25", "a = 10, b = 40", "a = 30, b = 20"], "tapply는 그룹별로 함수를 적용한다. a = (10 + 30) / 2 = 20, b = (20 + 40) / 2 = 30.")
    E(102, "3-1-2", ["R 코드", "데이터 결합"], "실전", "다음 R 코드의 실행 결과는?", "x <- data.frame(k = 1:3, a = 1:3)\ny <- data.frame(k = 2:4, b = 1:3)\nnrow(merge(x, y, all.x = TRUE))",
      "x <- data.frame(k = 1:3, a = 1:3); y <- data.frame(k = 2:4, b = 1:3); nrow(merge(x, y, all.x = TRUE))",
      "result = len(pd.merge(pd.DataFrame({'k': [1, 2, 3]}), pd.DataFrame({'k': [2, 3, 4]}), how='left'))", "3",
      "3", ["2", "4", "1"], "all.x = TRUE는 왼쪽(x) 기준 조인이라 x의 행 3개가 모두 남는다(k = 1은 b가 NA).", [("R 문서: merge", RD + 'base/html/merge.html')])
    E(103, "3-1-2", ["R 코드", "데이터 결합"], "고난도", "고객 표(id 1~4)와 주문 표(id 3~6)를 합쳐 어느 한쪽에라도 있는 id를 모두 남기려 한다. 다음 코드의 결과 행 수는?", "cust <- data.frame(id = 1:4, name = letters[1:4])\nord  <- data.frame(id = 3:6, amt = c(10, 20, 30, 40))\nnrow(merge(cust, ord, all = TRUE))",
      "cust <- data.frame(id = 1:4, name = letters[1:4]); ord <- data.frame(id = 3:6, amt = c(10, 20, 30, 40)); nrow(merge(cust, ord, all = TRUE))",
      "result = len(pd.merge(pd.DataFrame({'id': [1, 2, 3, 4]}), pd.DataFrame({'id': [3, 4, 5, 6]}), how='outer'))", "6",
      "6", ["2", "4", "8"], "all = TRUE는 완전 외부 조인이다. 양쪽 id의 합집합 1~6이 남아 6행(공통 id 3, 4는 한 행씩). 내부 조인(기본값)이면 2행이다.", [("R 문서: merge", RD + 'base/html/merge.html')])
    E(104, "3-1-2", ["R 코드", "범주화"], "실전", "다음 R 코드의 실행 결과는?", 'as.character(cut(c(1, 5, 9), breaks = c(0, 3, 6, 10), labels = c("L", "M", "H")))',
      'as.character(cut(c(1, 5, 9), breaks = c(0, 3, 6, 10), labels = c("L", "M", "H")))',
      "result = list(pd.cut([1, 5, 9], [0, 3, 6, 10], labels=['L', 'M', 'H']).astype(str))", "L M H",
      "L M H", ["L L H", "M M H", "H M L"], "cut은 구간 (0,3], (3,6], (6,10]에 따라 1 → L, 5 → M, 9 → H로 나눈다.", [("R 문서: cut", RD + 'base/html/cut.html')])
    E(105, "3-1-2", ["R 코드", "apply 계열"], "실전", "다음 R 코드의 실행 결과는?", "apply(matrix(1:4, nrow = 2), 2, max)",
      "apply(matrix(1:4, nrow = 2), 2, max)", "result = list(np.array([[1, 3], [2, 4]]).max(axis=0))", "2 4",
      "2 4", ["3 4", "2 3", "4"], "matrix(1:4, nrow = 2)는 [1 3; 2 4]. MARGIN = 2는 열 단위라 열별 최댓값 2, 4.", [("R 문서: apply", RD + 'base/html/apply.html')])
    E(106, "3-1-2", ["R 코드", "정렬"], "기본", "다음 R 코드의 실행 결과는?", 'df <- data.frame(n = c("a", "b", "c"), s = c(70, 90, 80))\ndf$n[order(-df$s)]',
      'df <- data.frame(n = c("a", "b", "c"), s = c(70, 90, 80)); df$n[order(-df$s)]',
      "result = [n for n, s in sorted(zip('abc', [70, 90, 80]), key=lambda t: -t[1])]", "b c a",
      "b c a", ["a c b", "a b c", "c b a"], "order(-s)는 점수 내림차순 위치를 돌려준다: 90(b), 80(c), 70(a).")
    C(107, "3-1-2", ["데이터 변환", "reshape"], "실전", "R에서 학생별로 '국어, 영어, 수학' 점수가 한 행에 옆으로 있는 표를, (학생, 과목, 점수) 한 줄씩 쌓인 형태로 바꾸려 한다. reshape의 direction 값은?",
      '"long"', ['"wide"', '"merge"', '"split"'],
      "여러 열에 흩어진 값을 행으로 쌓는 것이 long 형식 변환이다. 반대로 행을 열로 펼치면 wide.", [("R 문서: reshape", RD + 'stats/html/reshape.html')], ['reshape to long format'])
    E(108, "3-1-2", ["R 코드", "그룹 요약"], "실전", "다음 R 코드의 v 값은?", 'aggregate(v ~ g, data = data.frame(g = c("x", "y", "x", "y"), v = c(1, 2, 3, 4)), FUN = sum)$v',
      'aggregate(v ~ g, data = data.frame(g = c("x", "y", "x", "y"), v = c(1, 2, 3, 4)), FUN = sum)$v',
      "result = [1 + 3, 2 + 4]", "4 6",
      "4 6", ["3 7", "10", "1 2"], "g별 합계: x = 1 + 3 = 4, y = 2 + 4 = 6.", [("R 문서: aggregate", RD + 'stats/html/aggregate.html')])

    # --- 3-1-3 결측값 처리와 이상값 검색
    E(109, "3-1-3", ["이상값", "boxplot"], "고난도", "다음 R 코드의 실행 결과는?", "boxplot.stats(c(1, 2, 3, 4, 5, 100))$out",
      "boxplot.stats(c(1, 2, 3, 4, 5, 100))$out",
      "x = sorted([1, 2, 3, 4, 5, 100]); n = len(x)\nlo = np.median(x[:(n + 1) // 2]); hi = np.median(x[n // 2:]); c = 1.5 * (hi - lo)\nresult = [v for v in x if v < lo - c or v > hi + c]", "100",
      "100", ["1 100", "없음(numeric(0))", "5 100"],
      "boxplot.stats는 힌지(fivenum)로 상자를 만든다: 하위 힌지 2, 상위 힌지 5, 폭 3. 5 + 1.5 × 3 = 9.5를 넘는 100만 이상값이다.", [("R 문서: boxplot.stats", RD + 'grDevices/html/boxplot.stats.html')])
    E(110, "3-1-3", ["결측값"], "기본", "다음 R 코드의 실행 결과는?", "length(na.omit(c(1, NA, 3, NA, 5)))",
      "length(na.omit(c(1, NA, 3, NA, 5)))", "result = len([v for v in [1, None, 3, None, 5] if v is not None])", "3",
      "3", ["5", "2", "NA"], "na.omit은 NA를 뺀 값(1, 3, 5)만 남긴다.")
    E(111, "3-1-3", ["결측값", "대치"], "실전", "x <- c(2, NA, 4, NA, 6)의 결측값을 관측값의 평균으로 대치했다. 대치 후 x의 평균은?", "",
      "x <- c(2, NA, 4, NA, 6); x[is.na(x)] <- mean(x, na.rm = TRUE); mean(x)", "result = np.mean([2, 4, 4, 4, 6])", "4",
      "4", ["2.4", "3", "6"], "관측값 평균 4로 채우면 2, 4, 4, 4, 6이 되어 평균은 그대로 4다. 평균 대치는 평균은 지키지만 흩어짐(분산)은 줄인다.")
    C(112, "3-1-3", ["결측값", "대치"], "고난도", "결측값을 그 변수의 평균으로 채우는 평균 대치법의 문제점으로 옳은 것은?",
      "다른 변수와의 상관관계를 약하게 만들 수 있고, 분포의 흩어짐(분산)을 줄인다",
      ["분포의 흩어짐(분산)을 키운다", "다른 변수와의 상관관계를 실제보다 강하게 만든다", "항상 편향 없는 추정을 보장한다"],
      "평균 대치는 관측값 평균은 유지하지만, 같은 값이 여러 개 들어가 분산이 줄고 변수 간 상관이 약해지는 등 추정을 왜곡할 수 있다.", [("Wikipedia: Imputation (statistics)", 'Imputation_(statistics)')], ["mean imputation", "attenuates any correlations"])
    C(113, "3-1-3", ["결측값", "결측 유형"], "실전", "결측 여부가 관측된 변수든 결측된 값이든 어떤 변수와도 관계없이, 순전히 우연으로 생긴 경우는?",
      "MCAR(완전 무작위 결측)", ["MAR(무작위 결측)", "MNAR(비무작위 결측)", "이상값"],
      "결측 여부가 어떤 변수와도 무관하면 MCAR, 관측된 다른 변수와만 관련 있으면 MAR, 결측된 값 자체와 관련 있으면 MNAR이다.", [("Wikipedia: Missing data", 'Missing_data')], ["missing completely at random"])
    C(114, "3-1-3", ["결측값", "결측 유형"], "고난도", "소득이 높은 사람일수록 소득 문항에 응답하지 않아 결측이 생겼다. 이 결측 유형은?",
      "MNAR(비무작위 결측)", ["MCAR(완전 무작위 결측)", "MAR(무작위 결측)", "구조적 0"],
      "결측 여부가 결측된 값(소득) 자체와 관련 있으면 MNAR이다.", [("Wikipedia: Missing data", 'Missing_data')], ["missing not at random"])
    C(115, "3-1-3", ["결측값", "결측 유형"], "고난도", "설문에서 나이가 어린 응답자일수록 체중 문항을 비워 두는 경향이 있고, 나이는 모두 관측되었다. 체중 결측의 유형은?",
      "MAR(무작위 결측)", ["MCAR(완전 무작위 결측)", "MNAR(비무작위 결측)", "측정 오차"],
      "결측 여부가 관측된 다른 변수(나이)로 설명되면 MAR이다.", [("Wikipedia: Missing data", 'Missing_data')], ["missing at random"])
    E(116, "3-1-3", ["이상값", "표준화"], "실전", "다음 R 코드의 실행 결과는? (소수 셋째 자리까지)", "round(scale(c(2, 4, 6, 8, 10))[5], 3)",
      "round(scale(c(2, 4, 6, 8, 10))[5], 3)", "x = np.array([2, 4, 6, 8, 10]); result = round((10 - x.mean()) / x.std(ddof=1), 3)", "1.265",
      "1.265", ["1.414", "2.000", "1.000"], "평균 6, 표본표준편차 √10 ≈ 3.162. (10 − 6) / 3.162 ≈ 1.265. 표준화한 값의 절댓값이 매우 크면 이상값인지 추가로 살펴본다.", [("R 문서: scale", RD + 'base/html/scale.html')])
    E(117, "3-1-3", ["이상값", "IQR"], "실전", "다음 R 코드의 실행 결과는?", "IQR(c(1, 3, 5, 7, 9, 11))",
      "IQR(c(1, 3, 5, 7, 9, 11))", "q1, q3 = np.percentile([1, 3, 5, 7, 9, 11], [25, 75]); result = q3 - q1", "5",
      "5", ["6", "4", "8"], "R 기본(type 7) 사분위수: Q1 = 3.5, Q3 = 8.5, IQR = 5.", [("R 문서: quantile", RD + 'stats/html/quantile.html')])
    E(118, "3-1-3", ["결측값"], "실전", "다음 R 코드는 열별로 무엇을, 얼마로 계산하는가?", "df <- data.frame(a = c(1, NA, 3, 4), b = c(NA, NA, 3, 4))\ncolMeans(is.na(df))",
      "df <- data.frame(a = c(1, NA, 3, 4), b = c(NA, NA, 3, 4)); unname(colMeans(is.na(df)))",
      "result = list(pd.DataFrame({'a': [1, None, 3, 4], 'b': [None, None, 3, 4]}).isna().mean())", "0.25 0.5",
      "결측 비율, a 0.25 · b 0.5", ["결측 개수, a 1 · b 2", "평균, a 2.67 · b 3.5", "결측 비율, a 0.5 · b 0.25"],
      "is.na로 결측을 TRUE(1)로 바꾼 뒤 colMeans로 평균을 내면 열별 결측 비율이 된다: a 1/4 = 0.25, b 2/4 = 0.5.")

    # --- 3-2-1 통계학 개론: 척도·표본추출·오차·분포·확률
    C(119, "3-2-1", ["척도"], "기본", "섭씨 온도처럼 값 사이 간격은 의미가 있지만 0이 '없음'을 뜻하지 않아 비율 비교(2배 덥다)가 의미 없는 척도는?",
      "등간척도(구간척도)", ["명목척도", "서열척도", "비율척도"],
      "등간척도는 간격이 같지만 절대 영점이 없다. 절대 영점이 있으면 비율척도다.", [("Wikipedia: Level of measurement", 'Level_of_measurement')], ["interval", "celsius"])
    C(120, "3-2-1", ["척도"], "기본", "몸무게처럼 절대 영점이 있어 '두 배 무겁다'는 비교가 의미 있는 척도는?",
      "비율척도", ["명목척도", "서열척도", "등간척도"],
      "비율척도는 의미 있는 0(절대 영점)이 있어 비율 비교가 가능하다.", [("Wikipedia: Level of measurement", 'Level_of_measurement')], ["ratio", "true zero"])
    C(121, "3-2-1", ["척도"], "기본", "만족도를 '매우 불만~매우 만족' 5단계로 물었다. 순서는 있지만 단계 사이 간격이 같다고 보장할 수 없는 척도는?",
      "서열척도", ["명목척도", "등간척도", "비율척도"],
      "서열척도는 순서만 의미 있고 간격은 같다고 볼 수 없다.", [("Wikipedia: Level of measurement", 'Level_of_measurement')], ["ordinal"])
    C(122, "3-2-1", ["척도"], "기본", "혈액형(A, B, O, AB)처럼 순서 없이 구분만 하는 척도는?",
      "명목척도", ["서열척도", "등간척도", "비율척도"],
      "명목척도는 범주를 구분하는 이름표 역할만 한다.", [("Wikipedia: Level of measurement", 'Level_of_measurement')], ["nominal"])
    C(123, "3-2-1", ["표본추출"], "실전", "모집단을 성별·연령대 같은 서로 겹치지 않는 집단으로 나눈 뒤, 각 집단에서 따로 무작위로 뽑는 방법은?",
      "층화추출", ["군집추출", "계통추출", "단순 무작위 추출"],
      "층화추출은 모집단을 동질적인 층으로 나누고 층마다 독립적으로 표본을 뽑는다.", [("Wikipedia: Stratified sampling", 'Stratified_sampling')], ["stratified sampling"])
    C(124, "3-2-1", ["표본추출"], "실전", "전국 학교 중 몇 개 학교를 무작위로 고른 뒤, 뽑힌 학교의 학생을 모두 조사하는 방법은?",
      "군집추출", ["층화추출", "계통추출", "할당추출"],
      "군집추출은 모집단을 군집(학교)으로 나눠 군집 단위로 뽑는다.", [("Wikipedia: Cluster sampling", 'Cluster_sampling')], ["cluster sampling"])
    C(125, "3-2-1", ["표본추출"], "실전", "명단에서 무작위 출발점을 정한 뒤 10번째마다 한 명씩 뽑는 방법은?",
      "계통추출", ["층화추출", "군집추출", "편의추출"],
      "계통추출은 일정 간격(k번째)마다 뽑는 방법이다.", [("Wikipedia: Systematic sampling", 'Systematic_sampling')], ["systematic sampling"])
    C(126, "3-2-1", ["표본오차"], "고난도", "표본을 아무리 크게 늘려도 줄어들지 않는 오차로, 응답자의 거짓 응답이나 조사원의 기록 실수에서 생기는 것은?",
      "비표본오차", ["표본오차", "표준오차", "제1종 오류"],
      "비표본오차는 표본추출이 아닌 과정(측정·응답·처리)에서 생기며 표본 크기를 늘려도 줄지 않는다.", [("Wikipedia: Non-sampling error", 'Non-sampling_error')], ["non-sampling error"])
    C(127, "3-2-1", ["분포", "왜도"], "실전", "소득처럼 오른쪽으로 꼬리가 긴(양의 왜도) 전형적인 분포에서 일반적으로 나타나는 관계는?",
      "평균 > 중앙값", ["평균 < 중앙값", "평균 = 중앙값 = 최빈값", "중앙값 > 최빈값 > 평균"],
      "오른쪽 꼬리가 길면 큰 값들이 평균을 끌어올려 보통 평균이 중앙값보다 크다.", [("Wikipedia: Skewness", 'Skewness')], ["positive skew", "right"])
    E(128, "3-2-1", ["대푯값"], "기본", "데이터 1, 2, 2, 3, 10의 평균과 중앙값은?", "",
      "x <- c(1, 2, 2, 3, 10); c(mean(x), median(x))", "x = [1, 2, 2, 3, 10]; result = [np.mean(x), np.median(x)]", "3.6 2",
      "평균 3.6, 중앙값 2", ["평균 2, 중앙값 3.6", "평균 3.6, 중앙값 3", "평균 2, 중앙값 2"], "평균 = 18 / 5 = 3.6, 정렬했을 때 가운데 값 = 2. 이상값 10이 평균만 끌어올린다.")
    E(129, "3-2-1", ["확률분포", "기댓값"], "기본", "공정한 주사위를 한 번 던질 때 나오는 눈의 기댓값은?", "",
      "mean(1:6)", "result = np.mean(range(1, 7))", "3.5",
      "3.5", ["3", "4", "6"], "E(X) = (1 + 2 + … + 6) / 6 = 21 / 6 = 3.5.")
    E(130, "3-2-1", ["확률분포", "분산"], "실전", "공정한 주사위 눈 X의 분산 Var(X)는? (소수 셋째 자리까지)", "",
      "x <- 1:6; r3(mean(x^2) - mean(x)^2)", "x = np.arange(1, 7); result = round(np.var(x), 3)", "2.917",
      "2.917", ["3.500", "1.708", "3.500²"], "Var(X) = E(X²) − E(X)² = 91/6 − 3.5² = 35/12 ≈ 2.917.")
    E(131, "3-2-1", ["확률분포", "이항분포"], "실전", "앞면 확률 0.5인 동전을 3번 던질 때 앞면이 적어도 한 번 나올 확률은?", "",
      "1 - dbinom(0, 3, 0.5)", "result = 1 - stats.binom.pmf(0, 3, 0.5)", "0.875",
      "0.875", ["0.5", "0.125", "0.75"], "P(X ≥ 1) = 1 − P(X = 0) = 1 − 0.5³ = 0.875.", [("R 문서: Binomial", RD + 'stats/html/Binomial.html')])
    E(132, "3-2-1", ["확률분포", "정규분포"], "실전", "표준정규분포에서 P(−1.96 < Z < 1.96)은? (소수 셋째 자리까지)", "",
      "r3(pnorm(1.96) - pnorm(-1.96))", "result = round(stats.norm.cdf(1.96) - stats.norm.cdf(-1.96), 3)", "0.950",
      "0.950", ["0.975", "0.900", "0.680"], "양쪽 꼬리 2.5%씩을 빼면 가운데 95%. 95% 신뢰구간의 1.96이 여기서 나온다.", [("R 문서: Normal", RD + 'stats/html/Normal.html')])
    E(133, "3-2-1", ["확률분포", "포아송분포"], "실전", "한 시간에 평균 3건 오는 문의가 포아송분포를 따를 때, 한 시간에 정확히 2건 올 확률은? (소수 셋째 자리까지)", "",
      "r3(dpois(2, 3))", "result = round(stats.poisson.pmf(2, 3), 3)", "0.224",
      "0.224", ["0.149", "0.050", "0.423"], "P(X = 2) = e^(−3) × 3² / 2! ≈ 0.224.", [("R 문서: Poisson", RD + 'stats/html/Poisson.html')])
    E(134, "3-2-1", ["기댓값", "분산"], "고난도", "E(X) = 5, Var(X) = 4일 때 Y = 3X + 2의 기댓값과 분산은?", "",
      "c(3 * 5 + 2, 3^2 * 4)", "result = [3 * 5 + 2, 9 * 4]", "17 36",
      "E(Y) = 17, Var(Y) = 36", ["E(Y) = 17, Var(Y) = 14", "E(Y) = 15, Var(Y) = 12", "E(Y) = 17, Var(Y) = 12"],
      "E(aX + b) = aE(X) + b = 17, Var(aX + b) = a²Var(X) = 9 × 4 = 36. 더하는 상수는 분산에 영향이 없다.")
    C(135, "3-2-1", ["상관계수"], "실전", "키와 몸무게의 관계를 볼 때, 키의 단위를 cm에서 m로 바꿔 다시 계산해도 값이 변하지 않는 것은?",
      "키와 몸무게의 피어슨 상관계수", ["키와 몸무게의 공분산", "키의 분산", "키의 표준편차"],
      "상관계수는 공분산을 두 표준편차로 나눠 정규화한 값이라 단위(척도)를 바꿔도 변하지 않는다. 공분산·분산·표준편차는 단위에 따라 달라진다.", [("Wikipedia: Pearson correlation coefficient", 'Pearson_correlation_coefficient')], ["covariance", "product of their standard deviations"])
    E(136, "3-2-1", ["조건부 확률"], "실전", "P(A ∩ B) = 0.12, P(B) = 0.4일 때 P(A | B)는?", "",
      "0.12 / 0.4", "result = 0.12 / 0.4", "0.3",
      "0.3", ["0.048", "0.52", "0.12"], "P(A | B) = P(A ∩ B) / P(B) = 0.12 / 0.4 = 0.3.")
