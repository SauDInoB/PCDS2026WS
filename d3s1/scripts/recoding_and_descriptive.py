import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import scipy
import statsmodels
import pyreadstat
import numpy as np
from scipy.stats import norm


#You can change the name of the database
filename="asthma_best_db.sav"

#The following block of code will allow for the creation of an dynamic path regardless of the computer the script is running on
current_dir=os.getcwd()
d2s1_folder=os.path.dirname(current_dir)
bd_path="data/raw"

#Now we create a personalized absolute path for the database
db_full_path=os.path.join(d2s1_folder, bd_path,filename)
print (db_full_path)

#We create a new object called my_df. Now we create a personalized absolute path for the database
df, meta = pyreadstat.read_sav(db_full_path)

#We will demonstrate the export to xslx and csv and reimport

df.to_excel(os.path.join(d2s1_folder,'outputs/db_in_excel.xlsx'))
df.to_csv(os.path.join(d2s1_folder,'outputs/db_in_csv.csv'))

df_new=pd.read_csv(os.path.join(d2s1_folder,'outputs/db_in_csv.csv'))

def get_labels():
    for var, label_set_name in meta.variable_to_label.items():
        if label_set_name in meta.value_labels:
            print(f"{var} → {meta.value_labels[label_set_name]}")

get_labels()

# Now we define most common metrics for decision for continuous variables

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

# Now we define most common metrics for frequencies

def get_abs_freq_per_category(column_name):
    result = df[f"{column_name}"].value_counts(dropna=False)
    return result

def get_relative_freq_per_category(column_name):
    result = df[column_name].value_counts(normalize=True, dropna=False)
    return result

#example for one variable 
print (get_mean_and_std("SEQN",1))
print (get_median_and_iqr("SEQN",1))
print (get_abs_freq_per_category("AGQ030"))
print (get_relative_freq_per_category("AGQ030"))
print ("......................................")

# we will copy the previosuly elaborated categorical list 

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

# and convert them to categorical
for i in categorical_list:
    df[f"{i}"]= pd.Categorical(df[f"{i}"])

# for each variable in the dataset, assess whether it is categorical or not and present the appropriate summary
for column in df.columns:
    is_cat = isinstance(df[f"{column}"].dtype, pd.CategoricalDtype)
    if is_cat:
        result1=get_abs_freq_per_category(f"{column}")
        result2=get_relative_freq_per_category(f"{column}")
        print(result1)
        print(result2)
    else:
        print ('Mean (SD): ', get_mean_and_std(f"{column}",1))
        print ('Mean (IQR): ',get_median_and_iqr(f"{column}",1))


# create a new categorical variable from cutpoints

df["Age_at_diagnosis_cat"] = pd.cut(df["MCQ025"], bins=[0, 18, 35, 65], labels=["Young", "Adult", "Senior"])
print(get_abs_freq_per_category("Age_at_diagnosis_cat"))

# apply some transformation to every row in a column
# FEV1 in mL to L (PS: not usually used)
df["FEV1_L"] = df["SPXNFEV1"].apply(lambda x: x / 1000)
print("FEV1_L")
print(get_mean_and_std("FEV1_L",2))

# create a new categorical variable from cutpoints with conditional
def anemia_status(row):
    if row["RIAGENDR"] == 1:
        cut = 13
    elif row["RIAGENDR"] == 2:
        cut = 12
    else:
        return np.nan  
    return "Yes" if row["LBXHGB"] < cut else "No"
 
df["Anemia_cat"] = df.apply(anemia_status, axis=1)

print(get_abs_freq_per_category("Anemia_cat"))

# Now we want to plot the different variables. Let's see some examples

# # Countplot com subdivisão por Sexo
# sns.countplot(data=df, x="Anemia_cat")
# plt.title("Contagem de Anemia por Sexo")
# plt.ylabel("Quantidade")
# plt.xlabel("Anemia")
# plt.show()


# Bar plot for asthma categorized
graph1=sns.catplot(
    data=df,
    x="MCQ010",
    kind="count", 
    color="skyblue" # ou "bar" para valores numéricos
).set(
    title="Diagnosed asthma",
    xlabel="Asthma diagnosis",
    ylabel="N of individuals"
)
graph1.tight_layout()
plt.show()

# create a function for new variables

def get_graph_bar(df,variable,x,y,title):
    graph=sns.catplot(
        data=df,
        x=variable,
        kind="count", 
        color="skyblue" # ou "bar" para valores numéricos
    ).set(
        title=title,
        xlabel=x,
        ylabel=y
    )
    graph.tight_layout()
    plt.savefig(f"{d2s1_folder}/outputs/figures/graph_bar_{variable}.png", dpi=300, bbox_inches='tight')
    plt.show()
    return None

get_graph_bar(df,"Anemia_cat","anemia","count","Anemia Count")

counts = df["Anemia_cat"].value_counts()

plt.figure(figsize=(6,6))
plt.pie(
    counts,
    labels=counts.index,
    autopct="%1.1f%%",
    startangle=90,
)
plt.title("Diagnosed Asthma")
plt.savefig(f"{d2s1_folder}/outputs/figures/pie_anemia_cat.png", dpi=300, bbox_inches='tight')
plt.show()


def get_hisplot(df,variable,x,title,bins, normality_curve):
    sns.histplot(
        data=df,
        x=variable,    # coluna numérica
        bins=bins,         # número de barras
        kde=False,       # True se quiser curva de densidade
        stat="density",
        color="skyblue"  # cor das barras
    ).set(
        title=title,
        xlabel=x,
    )
    if normality_curve:
        xmin, xmax = df[f"{variable}"].min(), df[f"{variable}"].max()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, df[f"{variable}"].mean(), df[f"{variable}"].std())
        plt.plot(x, p, 'r', lw=2)  #r for red
    plt.savefig(f"{d2s1_folder}/outputs/figures/hist_{variable}.png", dpi=300, bbox_inches='tight')
    plt.show()

get_hisplot(df,"SPXNFEV1","FEV1 in mL", "Histogram of FEV1", 20, True)

get_hisplot(df,"LBXHGB","Hb (g/dL)", "Hemoglobin", 20, False)

def get_box_plot():
    plt.figure(figsize=(12,5))
    sns.boxplot(data=my_df, orient="h")
    plt.title("Boxplot")
    plt.show()
