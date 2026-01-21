import numpy as np
import statsmodels.api as sm
import pandas as pd

def bootstrap_regression(original_model, X, y, n_bootstrap=10000, random_state=42):
    np.random.seed(random_state)
    n, n_params = len(y), X.shape[1]
    boot_coefs = np.zeros((n_bootstrap, n_params))
    
    for i in range(n_bootstrap):
        indices = np.random.choice(n, size=n, replace=True)
        X_boot, y_boot = X.iloc[indices], y.values[indices]
        
        model_boot = sm.OLS(y_boot, X_boot, hasconst=True).fit()
        boot_coefs[i] = model_boot.params

    results = {}
    for i, name in enumerate(X.columns):
        original_coef = original_model.params[i]
        boot_mean = round(np.mean(boot_coefs[:, i]), 4)
        boot_se = round(np.std(boot_coefs[:, i], ddof=1), 4)
        ci_lower = round(np.percentile(boot_coefs[:, i], 100 * 0.05/2), 4)
        ci_upper = round(np.percentile(boot_coefs[:, i], 100 * (1 - 0.05/2)), 4)
        
        results[name] = {
            'original_coef': round(original_coef, 4),
            'boot_mean': boot_mean,
            'boot_se': boot_se,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
        }
    
    return pd.DataFrame(results).T
