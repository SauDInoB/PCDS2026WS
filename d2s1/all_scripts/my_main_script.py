https://pmc.ncbi.nlm.nih.gov/articles/PMC4134966/


import sys, subprocess

def pip_install(packages):
    """Install missing packages via pip (works inside Jupyter)."""
    for pkg in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

# Packages we use in the workshop
required = [
    "numpy", "pandas", "matplotlib", "seaborn", 
    "scipy", "statsmodels", "scikit-learn"
]
pip_install(required)

# ----------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.utils import resample   # for bootstrapping

# ----------------------------------------------------------------------
# 1️⃣  Summary statistics
# ----------------------------------------------------------------------


plt.figure(figsize=(12,5))
sns.boxplot(data=df, orient="h")
plt.title("Boxplots – Quick look for outliers")
plt.show()

# Hexbin – better for dense clouds
plt.figure(figsize=(8,6))
plt.hexbin(df["sleep_hours"], df["productivity_score"], gridsize=30, cmap="Blues", mincnt=1)
plt.xlabel("Sleep Hours")
plt.ylabel("Productivity")
plt.title("Hexbin Density Plot")
cb = plt.colorbar()
cb.set_label("count")
plt.show()

# simulate a population 

def sample_means(sample_size=30, reps=5000):
    """Return an array of sample means drawn from df."""
    means = []
    for _ in range(reps):
        samp = df["productivity_score"].sample(sample_size, replace=True)
        means.append(samp.mean())
    return np.array(means)

sample_means_arr = sample_means()
sample_means_arr.mean(), sample_means_arr.std()

### Plot sampling distribution & compare to Normal

plt.figure(figsize=(8,5))
sns.histplot(sample_means_arr, kde=True, stat="density", bins=30, color="teal")
x = np.linspace(sample_means_arr.min(), sample_means_arr.max(), 200)
plt.plot(x, stats.norm.pdf(x, loc=pop_mean, scale=pop_std/np.sqrt(30)),
         color="red", lw=2, label="Theoretical Normal")
plt.title("Sampling Distribution of the Mean (n=30)")
plt.legend()
plt.show()


se = pop_std / np.sqrt(30)
ci_low = pop_mean - 1.96*se
ci_high = pop_mean + 1.96*se
print(f"95 % CI (Normal approx.): [{ci_low:.2f}, {ci_high:.2f}]")

# bootstrap confidence interval
# Bootstrap replicate function
def bootstrap_ci(series, n_boot=2000, ci=95):
    boot_means = []
    for _ in range(n_boot):
        boot = resample(series)          # sample with replacement
        boot_means.append(boot.mean())
    lower = np.percentile(boot_means, (100-ci)/2)
    upper = np.percentile(boot_means, 100-(100-ci)/2)
    return lower, upper

boot_low, boot_high = bootstrap_ci(df["productivity_score"])
print(f"Bootstrap {95}% CI: [{boot_low:.2f}, {boot_high:.2f}]")

# Normality tests 

4️⃣ 1️⃣ Two‑sample t‑test (low vs high stress)

# Separate groups
low_stress  = df[df["stress_level"] <= 2]["productivity_score"]
high_stress = df[df["stress_level"] >= 4]["productivity_score"]

# Test for equal variances first (Levene)
levene_p = stats.levene(low_stress, high_stress).pvalue
equal_var = levene_p > .05

tstat, pval = stats.ttest_ind(low_stress, high_stress, equal_var=equal_var)
print(f"Levene p = {levene_p:.3f} → equal var? {equal_var}")
print(f"t = {tstat:.3f},  p = {pval:.4f}")
4️⃣ 2️⃣ One‑way ANOVA (all stress levels)

# Prepare data in long format for statsmodels
model = smf.ols('productivity_score ~ C(stress_level)', data=df).fit()
anova_tbl = sm.stats.anova_lm(model, typ=2)
anova_tbl
4️⃣ 3️⃣ Non‑parametric test (Mann‑Whitney) for skewed variable

Suppose coffee_cups is highly skewed (many zeros).

# Split into "no coffee" vs "coffee"
no_coffee = df[df["coffee_cups"] == 0]["productivity_score"]
coffee    = df[df["coffee_cups"] > 0]["productivity_score"]

u_stat, u_p = stats.mannwhitneyu(no_coffee, coffee, alternative='two-sided')
print(f"Mann‑Whitney U = {u_stat}, p = {u_p:.4f}")
4️⃣ 4️⃣ Checking normality (Shapiro‑Wilk) and QQ plot

# Shapiro on the residuals of the ANOVA model
resid = model.resid
shapiro_p = stats.shapiro(resid)[1]
print(f"Shapiro‑Wilk p‑value for residuals = {shapiro_p:.4f}")

# QQ plot
sm.qqplot(resid, line='s')
plt.title("QQ Plot of ANOVA Residuals")
plt.show()

# calculo d - cohen 
# ---- Solution ---------------------------------------------------------
df["sleep_hours_after"] = df["sleep_hours"] + np.random.normal(0.5, 0.7, N)

# Paired t-test
t, p = stats.ttest_rel(df["sleep_hours"], df["sleep_hours_after"])
print(f"Paired t = {t:.3f}, p = {p:.4f}")

# Cohen's d for paired samples
diff = df["sleep_hours_after"] - df["sleep_hours"]
cohen_d = diff.mean() / diff.std(ddof=1)
print(f"Cohen's d = {cohen_d:.2f}")

# Simple multiple regression (all predictors)
formula = ("productivity_score ~ study_hours + coffee_cups + sleep_hours + "
           "exercise_min + stress_level")
model_full = smf.ols(formula, data=df).fit()
print(model_full.summary())

# VIF requires numeric matrix (no intercept column)
X = model_full.model.exog
vif = pd.DataFrame({
    "variable": model_full.model.exog_names,
    "VIF": [sm.stats.outliers_influence.variance_inflation_factor(X, i) 
            for i in range(X.shape[1])]
})
vif


# Residuals vs. Fitted
plt.figure(figsize=(7,5))
sns.residplot(x=model_full.fittedvalues, y=model_full.resid, lowess=True,
              scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
plt.axhline(0, color='grey', linestyle='--')
plt.xlabel("Fitted values")
plt.ylabel("Residuals")
plt.title("Residuals vs. Fitted")
plt.show()

# QQ plot (normality)
sm.qqplot(model_full.resid, line='s')
plt.title("QQ Plot of Residuals")
plt.show()

# Breusch‑Pagan test (heteroskedasticity)
bp_test = sm.stats.diagnostic.het_breuschpagan(model_full.resid, model_full.model.exog)
bp_labels = ['LM Statistic', 'LM-Test p‑value', 'F‑Statistic', 'F‑Test p‑value']
print(dict(zip(bp_labels, bp_test)))

5️⃣ 4️⃣ Plot actual vs. predicted


plt.figure(figsize=(7,5))
plt.scatter(model_full.fittedvalues, df["productivity_score"], alpha=0.6)
plt.plot([df["productivity_score"].min(), df["productivity_score"].max()],
         [df["productivity_score"].min(), df["productivity_score"].max()],
         color='red', lw=2, linestyle='--')
plt.xlabel("Predicted productivity")
plt.ylabel("Observed productivity")
plt.title("Observed vs. Predicted")
plt.show()

#predições 
pred = model_full.predict(new_person)
pred

6️⃣ 1️⃣ Create a categorical version of study_hours

# Bin study_hours into three groups: low, medium, high
df["study_group"] = pd.cut(df["study_hours"], bins=[-0.1, 3, 6, 12],
                           labels=["Low","Medium","High"])
df["study_group"].value_counts()
6️⃣ 2️⃣ Two‑way ANOVA (study_group × stress_level)

formula2 = "productivity_score ~ C(study_group) * C(stress_level)"
model_anova2 = smf.ols(formula2, data=df).fit()
anova2_tbl = sm.stats.anova_lm(model_anova2, typ=2)
anova2_tbl
6️⃣ 3️⃣ Regression with interaction (study_hours × stress_level)

formula_int = ("productivity_score ~ study_hours * stress_level + "
                "coffee_cups + sleep_hours + exercise_min")
model_int = smf.ols(formula_int, data=df).fit()
print(model_int.summary())
6️⃣ 4️⃣ Bootstrap CI for regression coefficients

def bootstrap_regression(df, formula, n_boot=2000, ci=95):
    """Return percentile CI for each coefficient."""
    coefs = []
    for _ in range(n_boot):
        boot = resample(df)                    # sample rows with replacement
        fit = smf.ols(formula, data=boot).fit()
        coefs.append(fit.params)
    coefs = pd.DataFrame(coefs)
    lower = coefs.quantile((100-ci)/2/100)
    upper = coefs.quantile(1 - (100-ci)/2/100)
    return pd.concat([lower, upper], axis=1, keys=["lower","upper"])

boot_ci = bootstrap_regression(df, formula_int, n_boot=3000)
boot_ci
6️⃣ 5️⃣ Model comparison (AIC / BIC)

print(f"Model (no interaction) AIC = {model_full.aic:.1f}, BIC = {model_full.bic:.1f}")
print(f"Model (with interaction) AIC = {model_int.aic:.1f}, BIC = {model_int.bic:.1f}")


## from sklearn.model_selection import KFold, cross_val_score
from sklearn.linear_model import LinearRegression

X = df[["study_hours","coffee_cups","sleep_hours","exercise_min","stress_level"]]
y = df["productivity_score"]

kf = KFold(n_splits=5, shuffle=True, random_state=42)
linreg = LinearRegression()
scores = cross_val_score(linreg, X, y, cv=kf, scoring="r2")
print(f"5‑fold CV R² scores: {scores}")
print(f"Mean CV R² = {scores.mean():.3f}  (± {scores.std():.3f})")



# ---- Solution ---------------------------------------------------------
from sklearn.linear_model import Ridge, Lasso
from sklearn.metrics import mean_squared_error

ridge = Ridge(alpha=1.0)
lasso = Lasso(alpha=0.5)

# simple train‑test split for illustration
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

ridge.fit(X_train, y_train)
lasso.fit(X_train, y_train)

ridge_rmse = mean_squared_error(y_test, ridge.predict(X_test), squared=False)
lasso_rmse = mean_squared_error(y_test, lasso.predict(X_test), squared=False)
ols_rmse   = mean_squared_error(y_test, model_full.predict(X_test), squared=False)

print(f"OLS RMSE   = {ols_rmse:.2f}")
print(f"Ridge RMSE = {ridge_rmse:.2f}")
print(f"Lasso RMSE = {lasso_rmse:.2f}")

#export to jupyter notebook
pip install jupytext
jupytext --to notebook workshop_statistics.py