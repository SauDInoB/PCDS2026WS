import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import seaborn as sns
import os
from scipy import stats
from scipy.stats import shapiro,probplot,levene, mannwhitneyu, ttest_ind,chi2_contingency, fisher_exact, kruskal
import recoding_and_descriptive

# st.header("Dashboard for Winter School 26")

st.markdown("""
<style>
/* Selectbox container */
div.stSelectbox > div[data-baseweb="select"] {
    background-color: #e0e0e0 !important;  /* fundo cinzento */
    color: black !important;                /* texto preto */
    border-radius: 5px;
}

/* Texto da opção selecionada */
div.stSelectbox span {
    color: black !important;
}

/* Dropdown menu aberto */
div.stSelectbox div[class*="menu"] {
    background-color: #e0e0e0 !important;  /* fundo da lista cinzento */
    color: black !important;               /* texto preto */
}

/* Item selecionado na lista */
div.stSelectbox div[class*="option"][aria-selected="true"] {
    background-color: #c0c0c0 !important;  /* fundo cinza mais escuro */
    color: black !important;               /* texto preto */
}

/* Hover do item */
div.stSelectbox div[class*="option"]:hover {
    background-color: #d0d0d0 !important;
    color: black !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>Dashboard for Winter School 26</h1>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Drag your database in .csv", 
                                 type=["csv"])
if uploaded_file is not None:

    df=pd.read_csv(uploaded_file, index_col=0)
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
            df[f"{i}"]= pd.Categorical(df[f"{i}"])

    with st.expander("General information"):
        st.write("Rows:", df.shape[0])
        st.write("Columns:", df.shape[1])
        df_columns=df.columns.tolist()
        df_columns_text=", ".join(df_columns)
        st.write("Column names:", df_columns_text)

    with st.expander("Variable Descriptive Analysis"):
        choice=st.selectbox("Select your variable of interest:",
        ["SEQN - Número de Identificação", "RIAGENDR - Sexo",
        "RIDAGEEX - Idade (Meses)", "raca_etnia - Raça / Etnia",
        "DMDHHSIZ - Número membros do Agregado familiar","BMXWT - Peso (kg)",
        "BMXHT - Altura (cm)", "BMXBMI - Índice Massa Corporal (kg/m**2)",
        "LBXHGB - Hemoglobina (g/dL)", "LBXHCT - Hematócrito (%)", "ENQ100 - Tosse, constipação ou infec. resp. nos últimos 7 dias?;",
        "ENXMEAN - FeNO (ppb)", "MCQ010 - Diagnóstico de asma", "MCQ025 - Idade qd diagnóstico de asma", "RDQ031 - Tosse na maioria dos dias - últimos 3 meses",
        "RDQ050 - Expectoração frequente - últimos 3 meses", "RDQ070 - Pieira - último ano", "RDQ090 - Acordar por causa da pieira - último ano", "RDQ100 - Pieira durante o exercício",
        "RDQ134 - Médico perscreveu medicação para pieira;", "RDQ140 - Tosse seca à noite no último ano;", "AGQ030 - Episódio de Rinite Alérgica no último ano",
        "SMQ020 - Fumou pelo menos 100 cigarros na vida?", "SMD030 - Idade em que começou a fumar regularmente", "SMQ040 - Actualmente, fuma?", "SPXNFVC - FVC (mL)",
        "SPXNFEV1 - FEV 1 (mL)", "SPXNPEF - PEF (mL/s)", "SPXBFVC - FVC Pós-Broncodilatador (mL)", "SPXBFEV1 - FEV 1 Pós-Broncodilatador (mL)", "SPXBPEF - PEF Pós-Broncodilatador (mL/s)"])

        if choice is "Select your variable of interest:":
            None
        elif choice is not "Select your variable of interest:":
            tab1, tab2= st.tabs(["Summary measures", "Graphs"])
            choice=choice.split()[0]
            with tab1:
                if df[choice].dtype == "category":
                    df_a = recoding_and_descriptive.get_abs_freq_per_category(choice)
                    df_b=recoding_and_descriptive.get_relative_freq_per_category(choice)
                    df_merged = pd.merge(df_a, df_b, on=choice, how="inner")
                    st.dataframe(df_merged)
                elif df[choice].dtype=='float64':
                    st.write("Mean [SD]", recoding_and_descriptive.get_mean_and_std(choice,2))
                    st.write("Median [IQR]", recoding_and_descriptive.get_median_and_iqr(choice,2))
            with tab2:

                if df[choice].dtype == "float64":
                    fig, ax = plt.subplots()
                    sns.histplot(df[f"{choice}"].dropna())
                    st.pyplot(fig)
                elif df[choice].dtype=='category':
                    counts = df[choice].value_counts(dropna=False).sort_values(ascending=True)
                    fig, ax = plt.subplots(figsize=(8,5))
                    sns.barplot(
                        x=counts.index,      # categorias no eixo x
                        y=counts.values,     # frequências no eixo y
                        color="skyblue",
                        ci=None,             # sem barras de erro
                        ax=ax
                    )
                    st.pyplot(fig)

    with st.expander("Useful links"):
        st.write("https://github.com/")
        st.write("https://positron.posit.co/")
        st.write("https://seaborn.pydata.org/")
        st.write("https://www.utc.fr/~jlaforet/Suppl/python-cheatsheets.pdf")
        st.write("https://streamlit.io/")
        st.write("https://www.docker.com/")
col1, col2=st.columns(2)
with col1:
    st.image("page_support/logo-medicds.png",width=300)
with col2: 
    st.image("page_support/winterschool.png",width=150)


# def data_prep(df):
#     categorical_list=[
#         "RIAGENDR",
#         "raca_etnia",
#         "ENQ100",
#         "MCQ010",
#         "RDQ031",
#         "RDQ050",
#         "RDQ070", 
#         "RDQ090",
#         "RDQ100",
#         "RDQ140", 
#         "AGQ030", 
#         "SMQ020",
#         "SMQ040"
#     ]

#     for i in categorical_list:
#         my_df[f"{i}"]= pd.Categorical(my_df[f"{i}"])

#     my_df.rename(columns={'RIAGENDR': 'sex'}, inplace=True)
#     my_df.rename(columns={'RIDAGEEX': 'age'}, inplace=True)
#     my_df.rename(columns={'DMDHHSIZ': 'n_home'}, inplace=True)
#     my_df.rename(columns={'BMXBMI': 'BMI'}, inplace=True)
#     my_df.rename(columns={'LBXHGB': 'Hemoglobin'}, inplace=True)
#     my_df.rename(columns={'ENQ100': 'Cough_last_days'}, inplace=True)
#     my_df.rename(columns={'ENXMEAN': 'FeNO'}, inplace=True)
#     my_df.rename(columns={'MCQ010': 'Asthma_diagnosis'}, inplace=True)
#     my_df.rename(columns={'SPXNFEV1': 'FEV1_mL'}, inplace=True)
#     return my_df

# my_df=data_prep(uploaded_file)

# st.write(my_df.columns)
