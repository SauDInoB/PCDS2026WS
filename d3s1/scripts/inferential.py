import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy import stats
from scipy.stats import shapiro,probplot,levene, mannwhitneyu, ttest_ind,chi2_contingency, fisher_exact, kruskal
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd

filename="asthma_best_db.sav"
current_dir=os.getcwd()
d2s2_folder=os.path.dirname(current_dir)
bd_path="data/raw"
db_full_path=os.path.join(d2s2_folder, bd_path,filename)

my_df =pd.read_spss(db_full_path)

categorical_list=[
    "RIAGENDR",
    "raca_etnia",
    "ENQ100",
    "MCQ010",
    "RDQ031",
    "RDQ050",
    "RDQ070", 
    "RDQ090",
    "RDQ100",
    "RDQ140", 
    "AGQ030", 
    "SMQ020",
    "SMQ040"
]

for i in categorical_list:
    my_df[f"{i}"]= pd.Categorical(my_df[f"{i}"])

my_df.rename(columns={'RIAGENDR': 'sex'}, inplace=True)
my_df.rename(columns={'RIDAGEEX': 'age'}, inplace=True)
my_df.rename(columns={'DMDHHSIZ': 'n_home'}, inplace=True)
my_df.rename(columns={'BMXBMI': 'BMI'}, inplace=True)
my_df.rename(columns={'LBXHGB': 'Hemoglobin'}, inplace=True)
my_df.rename(columns={'ENQ100': 'Cough_last_days'}, inplace=True)
my_df.rename(columns={'ENXMEAN': 'FeNO'}, inplace=True)
my_df.rename(columns={'MCQ010': 'Asthma_diagnosis'}, inplace=True)
my_df.rename(columns={'SPXNFEV1': 'FEV1_mL'}, inplace=True)

print(my_df.head())

x='sex'
y='Hemoglobin'
sns.boxplot(x=x, y=y, data=my_df, showmeans=True)

plt.title(f'Box plot of {y} by {x}')
plt.savefig(os.path.join(d2s2_folder,f'outputs/figures/box_plot_{y}_by_{x}.png'), dpi=300, bbox_inches='tight')
plt.show()

# normal (histogram, shapiro)
# homocedasticity (levene)
def t_test(df,testing_variable,group_variable):
    print("---------------------------------")
    groups = df[group_variable].dropna().unique()
    if len(groups) != 2:
        raise ValueError("Must have two groups.")
    g1, g2 = groups
    x = df[df[group_variable]==g1][testing_variable].dropna().values
    y = df[df[group_variable]==g2][testing_variable].dropna().values

    if len(x) < 2 or len(y) < 2:
        raise ValueError("Each group must have at least two valid observations.")

    print(f"Testing {testing_variable} by {group_variable}")
    stat,p=levene(x,y)
    print("Levene test for homocedasticity:", p)
    if p<0.05: 
        var_equal=False
        print("Variance not equal")
        result=ttest_ind(x, y, equal_var=False) # Welch
    if p>=0.05:
        result=ttest_ind(x, y, equal_var=True) # classic T test
        print("Variance equal")
    nx, ny = len(x), len(y)
    pooled_std = np.sqrt(((nx-1)*np.var(x, ddof=1) + (ny-1)*np.var(y, ddof=1)) / (nx + ny - 2))
    d = (np.mean(x) - np.mean(y)) / pooled_std
    print ("statistic", result.statistic)
    print ("p-value",result.pvalue)
    # print ("degrees of freedom", result.df)
    print ("Cohen d", d)

t_test(my_df,'Hemoglobin','sex')
t_test(my_df,'FEV1_mL','Asthma_diagnosis')
t_test(my_df,'FeNO','Asthma_diagnosis')

def test_normality(df,testing_variable, group_variable):
    print("---------")
    print("Testing normality for", testing_variable, "by", group_variable)
    groups = df[group_variable].dropna().unique()
    if len(groups) != 2:
        raise ValueError("Must have two groups.")
    g1, g2 = groups
    x = df[df[group_variable]==g1][testing_variable].dropna().values
    y = df[df[group_variable]==g2][testing_variable].dropna().values

    sns.histplot(x=x, bins=15)
    plt.title(f"Histogram of group1")
    plt.show()
    plt.figure(figsize=(6,6))
    probplot(x, dist="norm", plot=plt)
    plt.title(f"Q-Q Plot of group1")
    plt.show()

    sns.histplot(x=y, bins=15)
    plt.title(f"Histogram of group2")
    plt.show()
    plt.figure(figsize=(6,6))
    probplot(x, dist="norm", plot=plt)
    plt.title(f"Q-Q Plot of group2")
    plt.show()

    print("Normality test, shapiro:")
    stat_x, p_x = shapiro(x)
    stat_y, p_y = shapiro(y)
    if p_x > 0.05 and p_y > 0.05:
        print("Both groups approximately normal")
    else:
        print("At least one group is non-normal by Shapiro")

test_normality(my_df,'Hemoglobin','sex')
test_normality(my_df,'FEV1_mL','Asthma_diagnosis')
test_normality(my_df,'FeNO','Asthma_diagnosis')

def mann_whitney_u_test(df,testing_variable, group_variable):
    print("---------------------------------")
    print(f"Mann Whitney U for {testing_variable} with groups for {group_variable}")
    groups = df[group_variable].dropna().unique()
    if len(groups) != 2:
        raise ValueError("Must have two groups.")
    g1, g2 = groups
    x = df[df[group_variable]==g1][testing_variable].dropna().values
    y = df[df[group_variable]==g2][testing_variable].dropna().values
    stat, p = mannwhitneyu(x, y)
    n1, n2 = len(x), len(y)
    r = 1 - (2*stat)/(n1*n2)
    print("Mann-Whitney U statistic:", stat)
    print("p-value:", p)
    print("rank-biserial correlation", r)

mann_whitney_u_test(my_df,'FeNO','Asthma_diagnosis')

my_df["BMI_cat"] = pd.cut(my_df["BMI"], bins=[0,17.5, 25, 30,np.inf], labels=["Low weight", "Normal weight", "Excessive weight", "Obese"])
freq = my_df['BMI_cat'].value_counts(dropna=False)   # `dropna=False` also counts NaNs, if you have them
print(freq)

def anova_test(df,testing_variable, group_variable):
    # --- 1. Normality por grupo ---
    groups = df[group_variable].dropna().unique()
    if len(groups) < 2:
        raise ValueError("Must have at least 2 groups for ANOVA.")
    print ("---------------------------------------")
    print("Normality test (Shapiro-Wilk) por grupo:")
    normality_pass = True
    for g in groups:
        data = df[df[group_variable]==g][testing_variable].dropna()
        stat, p = shapiro(data)
        print(f"{g}: W={stat:.3f}, p={p:.3f}", end=' ')
        if p < 0.05:
            print("→ NOT normal")
            normality_pass = False
        else:
            print("→ approximately normal")

    print("Homocedasticity")
    data_lists = [df[df[group_variable]==g][testing_variable].dropna().values for g in groups]

    stat_levene, p_levene = levene(*data_lists)
    print(f"\nLevene test for equal variances: W={stat_levene:.3f}, p={p_levene:.3f}")
    if p_levene >= 0.05:
        var_equal = True
    else:
        var_equal = False
    
    if var_equal:
        print("\nPerforming classic one-way ANOVA:")
        f_stat, p_val = f_oneway(*data_lists)
        print(f"F = {f_stat:.3f}, p = {p_val:.4f}")
    else:
        print("\nWarning: variances not equal → Welch ANOVA recommended")
        # Welch ANOVA via statsmodels
        model = ols(f"{testing_variable} ~ C({group_variable})", data=df).fit()
        anova_table = sm.stats.anova_lm(model, typ=2, robust='hc3') # heteroskedasticity robust
        print(anova_table)
        f_stat=anova_table["F"].iloc[0]
        p_val=anova_table["PR(>F)"].iloc[0]

anova_test(my_df,"FEV1_mL","BMI_cat")

def tukey_test_pairwise(df, testing_variable, group_variable):
    # Seleciona apenas linhas sem NaN na variável dependente
    df_clean = df[[testing_variable, group_variable]].dropna(subset=[testing_variable, group_variable])
    
    # Converte todos os grupos para string
    df_clean[group_variable] = df_clean[group_variable].astype(str)
    
    from statsmodels.stats.multicomp import pairwise_tukeyhsd
    tukey = pairwise_tukeyhsd(endog=df_clean[testing_variable],
                              groups=df_clean[group_variable],
                              alpha=0.05)
    
    print(tukey.summary())

tukey_test_pairwise(my_df,"FEV1_mL","BMI_cat")


def test_two_categoric_variables(df,var1,var2):
    print ("-----------------------")
    contingency = pd.crosstab(my_df[f'{var1}'], df[f'{var2}'])
    chi2, p, dof, expected = chi2_contingency(contingency)
    print ("chi2",chi2)
    print ("chi2 p", p)
    print ("chi2 dof", dof)
    print("Expected counts:\n", expected)
    low_expected = (expected < 5).sum()
    total_cells = expected.size
    percent_low = low_expected / total_cells * 100
    print("expected percentage of low cells is", percent_low)
    oddsratio, p = fisher_exact(contingency)
    print("------------------------")
    print("Fisher's OR:", oddsratio)
    print("Fisher's p-value:", p)

test_two_categoric_variables(my_df,"sex","Asthma_diagnosis")