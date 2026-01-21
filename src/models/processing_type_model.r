library(lme4)
library(lmerTest)
library(performance)
library(sjPlot)
library(MuMIn)
library(see)
library(emmeans)

# Load data
dataset <- read.csv("data/processed/02_long_df_unstandardized_one_primary.csv")

dataset$process_code <- factor(dataset$process_code)

# 1) FIT MODELS
# Full model
model_full <- lmer(wrongness ~ value_relevance * process_code + 
                     (1 | Participant_ID) + 
                     (1 | Vignette_ID), 
                   data = dataset,
                   REML = FALSE)

# Null model (random effects only)
model_null <- lmer(wrongness ~ 1 + 
                     (1 | Participant_ID) + 
                     (1 | Vignette_ID), 
                   data = dataset,
                   REML = FALSE)


# 2) MODEL COMPARISON
# Likelihood ratio test
comparison <- anova(model_null, model_full)
print(comparison)


model_full <- lmer(wrongness ~ value_relevance * process_code + 
                     (1 | Participant_ID) + 
                     (1 | Vignette_ID), 
                   data = dataset,
                   REML = TRUE)


# 3) Coefficients
# Fixed effects with p-values
print(summary(model_full))

# Confidence intervals
print(confint(model_full, method = "Wald"))

# Variance explained (R²)
r2 <- r.squaredGLMM(model_full)
print(r2)
cat("\nMarginal R² (fixed effects):", r2[1], "\n")
cat("Conditional R² (fixed + random):", r2[2], "\n")

# Random effects variance
print(VarCorr(model_full))

# ICC (intraclass correlation)
icc_result <- performance::icc(model_full)
print(icc_result)

# 4) ASSUMPTION CHECKS
# Check all assumptions at once
check_model(model_full)

# Normality of residuals
cat("\n=== NORMALITY OF RESIDUALS ===\n")
plot(check_normality(model_full))
ks_test <- ks.test(residuals(model_full), "pnorm", 
                           mean = mean(residuals(model_full)), 
                           sd = sd(residuals(model_full)))
print(ks_test)

# Histogram of residuals
hist(residuals(model_full), breaks = 30, 
     main = "Histogram of Residuals", xlab = "Residuals")
par(mfrow = c(1, 1))

# Check for outliers
cat("\n=== OUTLIERS ===\n")
outliers <- check_outliers(model_full)
print(outliers)

# Summary of assumption checks
cat("\n=== OVERALL MODEL DIAGNOSTICS ===\n")
model_performance <- model_performance(model_full)
print(model_performance)

# Pairwise comparisons
emm_process <- emmeans(model_full, ~ process_code)
print(emm_process)

# Pairwise comparisons with Tukey adjustment
pairwise_process <- pairs(emm_process, adjust = "tukey", reverse =TRUE)
print(pairwise_process)
confint(pairwise_process)


# Get marginal means for value relevance (averaged over process_code)
emm_value <- emmeans(model_full, ~ value_relevance)
print(emm_value)

# Get Main Effects
pairs(emm_value, reverse = TRUE)
confint(pairs(emm_value, reverse = TRUE))

joint_tests(model_full, by = NULL)


# Get simple effects of binary at each level of nominal
emm <- emmeans(model_full, ~ value_relevance | process_code)
print(emm)
pairs(emm, reverse = TRUE)
confint(pairs(emm, reverse = TRUE))