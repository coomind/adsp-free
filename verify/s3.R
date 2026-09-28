# Executes every computational subject-3 question and prints "id<TAB>result".
# verify/check.py compares each result with the marked answer in data/questions/s3.json.
# Run: Rscript verify/s3.R   (R 4.6.1 was used on 2026-09-29)
out <- function(id, v) cat(id, "\t", v, "\n", sep = "")
fmt <- function(x) paste(format(x, trim = TRUE), collapse = " ")
r3 <- function(x) formatC(x, format = "f", digits = 3)

# --- R basics
x <- c(3, NA, 5)
out("s3-001", fmt(mean(x)))                          # NA
out("s3-002", fmt(mean(c(3, NA, 5), na.rm = TRUE)))  # 4
x <- 1:6
out("s3-003", fmt(x[-2]))
out("s3-004", fmt(seq(2, 11, by = 3)))
out("s3-005", fmt(rep(c("A", "B"), times = 2)))
out("s3-006", class(c(1, "2", TRUE)))
m <- matrix(1:6, nrow = 2)
out("s3-007", fmt(m[2, 3]))
out("s3-008", fmt(apply(matrix(1:6, nrow = 2), 1, sum)))
out("s3-009", fmt(sum(is.na(c(1, NA, 3, NA)))))
out("s3-010", fmt(length(c(1, 2, NULL, 4))))

# --- data mart, missing values, outliers
df <- data.frame(a = c(1, NA, 3), b = c(NA, 2, 3))
out("s3-011", fmt(sum(complete.cases(df))))
a <- c(1, NA, 3)
a[is.na(a)] <- mean(a, na.rm = TRUE)
out("s3-012", fmt(a))
v <- c(2, 4, 4, 5, 6, 7, 8, 30)
q <- quantile(v, c(0.25, 0.75))               # default type 7
iqr <- q[2] - q[1]
out("s3-013", fmt(v[v < q[1] - 1.5 * iqr | v > q[2] + 1.5 * iqr]))

# --- statistics
out("s3-015", r3(var(c(2, 4, 6, 8))))
out("s3-017", r3(sd(c(2, 4, 4, 4, 5, 5, 7, 9))))
out("s3-018", fmt(cor(1:5, c(2, 1, 4, 3, 5))))
fit <- lm(c(2, 3, 5, 6, 9) ~ I(1:5))
out("s3-019", fmt(round(unname(coef(fit)), 6)))       # intercept slope
out("s3-023", sprintf("%.1f", 100 * (1 - pnorm(90, 70, 10))))
fit2 <- lm(c(2, 4, 5, 4, 5) ~ I(1:5))
out("s3-020", r3(summary(fit2)$r.squared))
ev <- c(3, 1)
out("s3-026", fmt(100 * ev[1] / sum(ev)))

# --- data mining
TP <- 40; FN <- 10; FP <- 20; TN <- 30
out("s3-029", r3(TP / (TP + FP)))                      # precision
tx <- list(c("A","B"), c("A","B"), c("A","B"), c("A","C"), c("A"),
           c("B","C"), c("C"), c("C"), c("D"), c("B"))
n <- length(tx)
has <- function(items) sum(sapply(tx, function(t) all(items %in% t)))
sA <- has("A") / n; sB <- has("B") / n; sAB <- has(c("A", "B")) / n
out("s3-030", fmt(round(sAB / (sA * sB), 6)))           # lift A->B

# ===== added 2026-09-29: s3-031 ~ s3-090 =====
# R basics
out("s3-031", fmt(sort(c(5, 2, 9), decreasing = TRUE)))
out("s3-032", fmt(order(c(30, 10, 20))))
out("s3-033", fmt(which(c(3, 8, 1, 8) == 8)))
x <- c(a = 1, b = 2)
out("s3-034", fmt(names(x)))
out("s3-035", fmt(paste("A", 1:3, sep = "-")))
out("s3-036", fmt(length("ADsP")))
out("s3-037", substr("dataq", 2, 4))
out("s3-038", fmt(as.numeric("12") + 3))
x <- 1:10
out("s3-039", fmt(sum(x[x %% 2 == 0])))
l <- list(a = 1:3, b = "x")
out("s3-040", fmt(length(l)))
df <- data.frame(x = 1:4, y = c(2, 4, 6, 8))
out("s3-041", fmt(nrow(df[df$y > 3, ])))
out("s3-042", fmt(ifelse(c(1, 5, 10) > 4, "H", "L")))
m <- matrix(1:4, nrow = 2)
out("s3-043", fmt(t(m)[1, 2]))
out("s3-044", fmt(sort(c(3, NA, 1))))
out("s3-045", fmt(round(2.5)))
out("s3-046", fmt(unique(c(2, 2, 3, 1, 3))))
out("s3-047", fmt(levels(factor(c("b", "a", "b")))))
# data handling, missing values, outliers
out("s3-048", fmt(median(c(1, 2, 3, 100))))
out("s3-049", fmt(unname(colSums(is.na(data.frame(a = c(1, NA), b = c(NA, NA)))))))
x <- c(10, 20, NA, 40); x[is.na(x)] <- median(x, na.rm = TRUE)
out("s3-050", fmt(x))
ag <- aggregate(v ~ g, data = data.frame(g = c("a", "a", "b"), v = c(1, 3, 5)), FUN = mean)
out("s3-051", fmt(ag$v))
mg <- merge(data.frame(k = 1:3, a = c(10, 20, 30)), data.frame(k = c(2, 3, 4), b = c(1, 2, 3)))
out("s3-052", fmt(nrow(mg)))
out("s3-053", fmt(scale(c(2, 4, 6))[3]))
x <- c(10, 20, 40)
out("s3-054", r3(((x - min(x)) / (max(x) - min(x)))[2]))
# statistics
x <- c(1, 2, 3, 4)
out("s3-055", fmt(mean((x - mean(x))^2)))                  # population variance
out("s3-056", fmt(4 / sqrt(16)))                            # standard error
out("s3-057", paste(formatC(50 + c(-1, 1) * qnorm(0.975) * 10 / sqrt(25), format = "f", digits = 2), collapse = " "))
out("s3-058", r3(unname(t.test(c(5, 6, 7, 8, 9), mu = 5)$statistic)))
out("s3-059", r3(unname(chisq.test(matrix(c(10, 20, 20, 10), 2), correct = FALSE)$statistic)))
out("s3-060", r3(cov(1:4, c(2, 4, 6, 8))))
out("s3-061", fmt(cor(1:5, c(1, 3, 2, 5, 4), method = "spearman")))
fit <- lm(c(2, 3, 5, 6, 9) ~ I(1:5))
out("s3-062", fmt(round(unname(coef(fit)[1] + coef(fit)[2] * 6), 6)))
fit2 <- lm(c(2, 4, 5, 4, 5) ~ I(1:5))
out("s3-063", r3(summary(fit2)$adj.r.squared))
g <- factor(rep(c("a", "b", "c"), each = 3))
out("s3-064", fmt(round(summary(aov(c(1, 2, 3, 4, 5, 6, 7, 8, 9) ~ g))[[1]][["F value"]][1], 6)))
out("s3-067", fmt(dbinom(2, 4, 0.5)))
out("s3-068", r3(dpois(0, 2)))
# multivariate, time series
ev <- c(4, 3, 2, 1)
out("s3-069", fmt(100 * sum(ev[1:2]) / sum(ev)))
out("s3-070", fmt(as.numeric(stats::filter(c(3, 6, 9, 12, 15), rep(1/3, 3), sides = 1))))
out("s3-071", fmt(diff(c(5, 8, 12, 17), differences = 2)))
out("s3-072", fmt(0.5 * 20 + (1 - 0.5) * 10))
out("s3-073", fmt(sqrt(sum((c(1, 2) - c(4, 6))^2))))
out("s3-074", fmt(sum(abs(c(1, 2) - c(4, 6)))))
# data mining
TP <- 40; FN <- 10; FP <- 20; TN <- 30
P <- TP / (TP + FP); Rc <- TP / (TP + FN)
out("s3-075", r3((TP + TN) / (TP + FN + FP + TN)))
out("s3-076", r3(Rc))
out("s3-077", r3(2 * P * Rc / (P + Rc)))
out("s3-078", r3(TN / (TN + FP)))
p <- c(4, 6) / 10
out("s3-079", r3(1 - sum(p^2)))
p <- c(5, 5) / 10
out("s3-080", fmt(-sum(p * log2(p))))
out("s3-081", fmt(sAB / sA))                                  # confidence A->B (transactions above)
x <- c(1, 2, 9, 10); cl <- ifelse(abs(x - 1) <= abs(x - 2), 1, 2)
out("s3-082", fmt(unname(tapply(x, cl, mean))))
A <- c(0, 1); B <- c(4, 6)
d <- outer(A, B, function(a, b) abs(a - b))
out("s3-083", fmt(min(d)))
out("s3-084", fmt(0.8 / (1 - 0.8)))
out("s3-085", formatC(exp(0.693), format = "f", digits = 2))
lab <- c("A", "B", "B", "A", "A")
out("s3-086", paste(names(which.max(table(lab[1:3]))), names(which.max(table(lab[1:5])))))
