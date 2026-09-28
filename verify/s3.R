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
