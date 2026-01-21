library(lme4)
library(lmerTest)
library(performance)
library(sjPlot)
library(MuMIn)
library(see)
library(emmeans)
library(parameters)

emm_options(lmerTest.limit = 10000)

# -------- DATASET -------- # 
dataset <- read.csv("data/processed/02_long_df_standardized_one_primary.csv")
dataset$value_relevance <- factor(dataset$value_relevance)

# -------- MODELS -------- # 
model_full <- lmer(wrongness ~ (AOT + CM + PIT + PE + CRT_Correct + CRT_Heuristic) * value_relevance + 
                     (1 | Participant_ID) + 
                     (1 | Vignette_ID), 
                   data = dataset,
                   REML = FALSE)

model_null <- lmer(wrongness ~ 1 + 
                     (1 | Participant_ID) + 
                     (1 | Vignette_ID), 
                   data = dataset,
                   REML = FALSE)

comparison <- anova(model_null, model_full, refit = FALSE)
print(comparison)

model_full <- lmer(wrongness ~ (AOT + CM + PIT + PE + CRT_Correct + CRT_Heuristic) * value_relevance + 
                     (1 | Participant_ID) + 
                     (1 | Vignette_ID), 
                   data = dataset,
                   REML = TRUE)

# -------- COEFFICIENTS -------- # 
print(summary(model_full))


print(anova(model_full))
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

# -------- ASSUMPTIONS -------- # 
check_model(model_full)

# Normality of residuals
plot(check_normality(model_full))
ks_test <- ks.test(residuals(model_full), "pnorm", 
                   mean = mean(residuals(model_full)), 
                   sd = sd(residuals(model_full)))
print(ks_test)

# Histogram of residuals
hist(residuals(model_full), breaks = 30, 
     main = "Histogram of Residuals", xlab = "Residuals")


hetero_check <- check_heteroscedasticity(model_full)
print(hetero_check)

# -------- OUTLIERS -------- # 
outliers <- check_outliers(model_full)
print(outliers)

# Summary of assumption checks
model_performance <- model_performance(model_full)
print(model_performance)

# -------- MARGINAL EFFECTS -------- # 
emm_value <- emmeans(model_full, ~ value_relevance)
print(emm_value)
pairs(emm_value, reverse = TRUE)
confint(pairs(emm_value, reverse = TRUE))

overall_slopes <- data.frame()
slopes_by_level <- data.frame()
# Loop through all continuous predictors
for(var in c("AOT", "CM", "PIT", "PE", "CRT_Correct", "CRT_Heuristic")) {
  
  overall <- emtrends(model_full, ~ 1, var = var)
  overall_summary <- summary(overall)
  overall_test <- test(overall)
  
  overall_row <- data.frame(
    Variable = var,
    Overall_Slope = overall_summary[[2]],
    SE = overall_summary$SE,
    CI_lower = overall_summary$lower.CL,
    CI_upper = overall_summary$upper.CL,
    df = overall_test$df,
    t_value = overall_test$t.ratio,
    p_value = overall_test$p.value
  )
  overall_slopes <- rbind(overall_slopes, overall_row)

  by_level <- emtrends(model_full, ~ value_relevance, var = var)
  by_level_summary <- summary(by_level)
  by_level_test <- test(by_level)
  
  for(i in 1:nrow(by_level_summary)) {
    level_row <- data.frame(
      Variable = var,
      value_relevance = by_level_summary$value_relevance[i],
      Slope = by_level_summary[[2]][i],
      SE = by_level_summary$SE[i],
      CI_lower = by_level_summary$lower.CL[i],
      CI_upper = by_level_summary$upper.CL[i],
      df = by_level_test$df[i],
      t_value = by_level_test$t.ratio[i],
      p_value = by_level_test$p.value[i]
    )
    slopes_by_level <- rbind(slopes_by_level, level_row)
  }
}


write.csv(overall_slopes, "results/coefficients/04_wrongness_overall_slopes.csv", row.names = FALSE)
write.csv(slopes_by_level, "results/coefficients/04_wrongness_slopes_by_value_relevance.csv", row.names = FALSE)

model_summary <- summary(model_full)
fixed_effects <- as.data.frame(model_summary$coefficients)
fixed_effects$Variable <- rownames(fixed_effects)
fixed_effects <- fixed_effects[, c("Variable", "Estimate", "Std. Error", "df", "t value", "Pr(>|t|)")]
colnames(fixed_effects) <- c("Variable", "Estimate", "SE", "df", "t_value", "p_value")
write.csv(fixed_effects, "results/coefficients/04_wrongness_fixed_effects.csv", row.names = FALSE)



write.csv(as.data.frame(
  joint_tests(model_full, by = NULL)),
  "results/coefficients/04_wrongness_joint_tests.csv",
  row.names = FALSE
)
