import pandas as pd
import statsmodels.api as sm
import os
import matplotlib.pyplot as plt
import scipy.stats as stats
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.formula.api as smf
import numpy as np
from sklearn.metrics import roc_curve, roc_auc_score
from scipy.stats import chi2


filename="study_samp.xlsx"
current_dir=os.getcwd()
d3s1_folder=os.path.dirname(current_dir)
bd_path="data/raw"
db_full_path=os.path.join(d3s1_folder, bd_path,filename)

my_df = pd.read_excel(os.path.join(db_full_path))

print (my_df.columns)

categorical_variables=[
    "gender",
    "smoker",
    "race",
    "income"
]

for categorical in categorical_variables:
    my_df[categorical] = pd.Categorical(my_df[categorical])

current_df=my_df[['fglu', 'waistc', 'age',"gender","smoker","race","income"]]
current_df.dropna()

X = current_df[['waistc', 'age']]
X = sm.add_constant(X)
y = current_df['fglu']

model = sm.OLS(y, X).fit()
print(model.summary())

residuals = model.resid
# # Valores ajustados
fitted = model.fittedvalues

plt.scatter(fitted, residuals)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Valores Ajustados')
plt.ylabel('Resíduos')
plt.title('Resíduos vs. Valores Ajustados')
plt.show()

# Histograma
plt.hist(residuals, bins=5, edgecolor='k')
plt.title('Histograma dos Resíduos')
plt.show()

# Q-Q plot
standardized_residuals = model.get_influence().resid_studentized_internal
sm.qqplot(standardized_residuals, line='45')
plt.title('Q-Q Plot dos Resíduos')
plt.show()

# Teste formal (Shapiro-Wilk)
shapiro_test = stats.shapiro(residuals)
print("Shapiro-Wilk:", shapiro_test)

# # Calcular VIF
vif_data = pd.DataFrame()
vif_data["feature"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
print(vif_data)

### including categorical

current_df=my_df[['fglu', 'waistc', 'age',"gender","smoker","race","income"]]
current_df.dropna()

model = smf.ols("fglu ~ waistc + age + C(gender)+C(smoker)+C(race)+C(income)", data=current_df).fit()
print(model.summary())

current_df["gender"] = current_df["gender"].cat.reorder_categories(
    ["Male","Female"],
    ordered=False
)
model = smf.ols("fglu ~ waistc + age + C(gender)+C(smoker)+C(race)+C(income)", data=current_df).fit()
print(model.summary())
# print(current_df)

new_df = pd.DataFrame({
    "waistc": [80],
    "age": [60],
    "gender": ["Female"],
    "smoker": ["Never"],
    "race": ["Non-Hispanic Black"],
    "income": ["above $55,000"]
})

for col in ["gender", "smoker", "race", "income"]:
    new_df[col] = new_df[col].astype("category")

predictions = model.predict(new_df)
print (predictions)

#### CHALLENGE
# Create a new script that users to predict new patients based on the previous model, using streamlit as the interface. 

## LOGISTIC REGRESSION 

current_df = my_df[['fglu', 'waistc', 'age',"gender","smoker","race","income"]].copy()

current_df['fglu_cat'] = np.where(current_df['fglu'] >= 126, 1, 0)

current_df.dropna()

logit_model = smf.logit(
    "fglu_cat ~ waistc + age + C(gender) + C(smoker) + C(race) + C(income)",
    data=current_df
).fit()
print(logit_model.summary())

coef = logit_model.params
conf = logit_model.conf_int()

OR = np.exp(coef)

OR_lower = np.exp(conf[0])
OR_upper = np.exp(conf[1])

OR_summary = pd.DataFrame({
    'OR': OR,
    '2.5% CI': OR_lower,
    '97.5% CI': OR_upper
})

print(OR_summary)


# Valores ajustados
fitted_probs = logit_model.fittedvalues
y_obs = current_df['fglu_cat']

# Criar grupos (deciles)
current_df['decile'] = pd.qcut(fitted_probs, 10, labels=False)

hl_table = current_df.groupby('decile').agg(
    obs_high=('fglu_cat','sum'),
    obs_total=('fglu_cat','count'),
    pred_prob=('fglu_cat', lambda x: fitted_probs[x.index].mean())
)

hl_table['expected_high'] = hl_table['pred_prob'] * hl_table['obs_total']
hl_table['expected_low'] = (1 - hl_table['pred_prob']) * hl_table['obs_total']

hl_stat = (((hl_table['obs_high'] - hl_table['expected_high'])**2 / hl_table['expected_high']) +
           ((hl_table['obs_total'] - hl_table['obs_high'] - hl_table['expected_low'])**2 / hl_table['expected_low'])).sum()

p_value = 1 - chi2.cdf(hl_stat, df=8)  # df = number of groups - 2
print("Hosmer-Lemeshow statistic:", hl_stat)
print("p-value:", p_value)


fpr, tpr, thresholds = roc_curve(y_obs, fitted_probs)
auc = roc_auc_score(y_obs, fitted_probs)
print ("auc",auc)

plt.plot(fpr, tpr, label=f'AUC = {auc:.3f}')
plt.plot([0,1],[0,1],'--', color='gray')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()
plt.show()

influence = logit_model.get_influence()

# DFFITS, Cook's distance, leverage
print(cooks)
print(leverage)

plt.scatter(leverage, cooks)
plt.xlabel('Leverage')
plt.ylabel("Cook's distance")
plt.title("Influence Plot")
plt.show()