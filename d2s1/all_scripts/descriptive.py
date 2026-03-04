import sys, subprocess

def pip_install(packages):
    """Install missing packages via pip."""
    for pkg in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

# Packages we use in the workshop
required = [
    "numpy", "pandas", "matplotlib", "seaborn", 
    "scipy", "statsmodels", "scikit-learn"
]
pip_install(required)


import pandas as pd
import matplotlib.pyplot as plt
import pyreadstat

# Caminho para o ficheiro .sav
file_path = "/Users/danielmdias/docs/docencia/escolaverao/bd_asthma.sav"

# Lê o ficheiro
df, meta = pyreadstat.read_sav(file_path)
# Mostra as primeiras linhas
print("Shape :", df.shape)                 
print("Number of dimensions  :", df.ndim)
print("\nColumns :", df.columns.tolist())
print("\nIndex   :", df.index)   
print(df.head())
print (df.tail())
print("\nData types:")
print(df.dtypes)
print("\nFull summary (incl. non‑numeric):")
print(df.describe(include='all').T)

def get_missings(column_name):
    num_missing = df[f"{column_name}"].isna().sum()
    result=f"Number of missings: {num_missing}"
    return result

def get_mean_and_std(column_name, number_of_decimals):
    result_mean=round(df[f"{column_name}"].mean(),number_of_decimals)
    result_sd=round(df[f"{column_name}"].std(),number_of_decimals)
    result=f"{result_mean} [{result_sd}]"
    return result

def get_median_and_iqr(column_name, number_of_decimals):
    result_median=round(df[f"{column_name}"].median(),number_of_decimals)
    result_q1=round(df[f"{column_name}"].quantile(0.25),number_of_decimals)
    result_q3=round(df[f"{column_name}"].quantile(0.75),number_of_decimals)
    result=f"{result_median} [{result_q1}-{result_q3}]"
    return result

def get_abs_freq_per_category(column_name):
    result = df[f"{column_name}"].value_counts(dropna=False)
    return result

def get_relative_freq_per_category(column_name):
    result = df[column_name].value_counts(normalize=True, dropna=False)
    return result

print (get_missings("SEQN"))
print (get_mean_and_std("SEQN",1))
print (get_median_and_iqr("SEQN",1))
print (get_abs_freq_per_category("AGQ030"))
print (get_relative_freq_per_category("AGQ030"))