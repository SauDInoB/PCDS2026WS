# %% [markdown]
# Exercício prático — Aprendizagem supervisionada
# Classificação com o Heart Disease Dataset — Cleveland
#
# Objetivo:
# Treinar e avaliar um modelo supervisionado para prever a presença/ausência
# de doença cardíaca a partir de variáveis clínicas.
#
# Como usar no Visual Studio Code:
# 1. Abrir este ficheiro no VS Code.
# 2. Garantir que as bibliotecas estão instaladas:
#       pip install pandas scikit-learn
# 3. Executar célula a célula, usando as marcações "# %%".
# 4. Completar todos os espaços assinalados com __________.
#
# Nota:
# Este dataset é pequeno e serve apenas para aprendizagem.
# Não deve ser usado para desenvolver uma ferramenta clínica real.


# %% [markdown]
# 0. Importar bibliotecas
#
# Completar os imports principais.
# Dica:
# - train_test_split: divisão treino/teste
# - StandardScaler: normalização
# - DecisionTreeClassifier: modelo supervisionado
# - accuracy_score, confusion_matrix, classification_report: avaliação

# %%
import pandas as pd

from sklearn.model_selection import __________
from sklearn.preprocessing import __________
from sklearn.tree import __________
from sklearn.metrics import __________, __________, __________


# %% [markdown]
# 1. Ler dados
#
# Este bloco já está completo.
#
# O dataset original usa valores 0, 1, 2, 3 e 4 no diagnóstico.
# Aqui vamos transformar o problema numa classificação binária:
# - 0 = sem doença cardíaca
# - 1 = com doença cardíaca

# %%
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"

colunas = [
    "age",       # idade
    "sex",       # sexo: 1 = masculino; 0 = feminino
    "cp",        # tipo de dor no peito
    "trestbps",  # pressão arterial em repouso
    "chol",      # colesterol sérico
    "fbs",       # glicemia em jejum > 120 mg/dl
    "restecg",   # resultado do ECG em repouso
    "thalach",   # frequência cardíaca máxima atingida
    "exang",     # angina induzida por exercício
    "oldpeak",   # depressão ST induzida por exercício
    "slope",     # inclinação do segmento ST
    "ca",        # número de vasos principais observados por fluoroscopia
    "thal",      # resultado do teste de thalassemia
    "target"     # diagnóstico: 0 = ausência; 1-4 = presença de doença cardíaca
]

df = pd.read_csv(url, header=None, names=colunas, na_values="?")

# Remover observações com valores em falta.
df = df.dropna().reset_index(drop=True)

# Transformar o alvo original em classificação binária.
df["doenca_cardiaca"] = (df["target"] > 0).astype(int)

target_names = ["sem doença cardíaca", "com doença cardíaca"]

df.head()

# Dimensão do dataset
df.shape


# %% [markdown]
# 2. Definir X e y
#
# Completar:
# - X deve conter as variáveis preditoras.
# - y deve conter a variável-alvo.
#
# Atenção:
# A coluna "target" é o alvo original.
# A coluna "doenca_cardiaca" é o alvo binário que vamos prever.
# Nenhuma das duas deve ficar dentro de X.

# %%
X = df.drop(columns=[__________, __________])
y = df[__________]

print("Dimensão de X:", X.shape)
print("Dimensão de y:", y.shape)


# %% [markdown]
# Distribuição das classes
#
# Este bloco já está completo.
# Observe se as classes estão equilibradas ou desequilibradas.

# %%
y.value_counts().sort_index().rename(index={
    0: target_names[0],
    1: target_names[1]
})


# %% [markdown]
# 3. Dividir treino/teste
#
# Completar a divisão dos dados.
#
# Dicas:
# - test_size define a percentagem reservada para teste.
# - random_state torna a divisão reproduzível.
# - stratify mantém a proporção das classes em treino e teste.
#
# Mensagem-chave:
# O conjunto de teste deve ficar "intocado" até ao fim.

# %%
X_train, X_test, y_train, y_test = train_test_split(
    __________,
    __________,
    test_size=__________,
    random_state=__________,
    stratify=__________
)

print("Treino:", X_train.shape)
print("Teste:", X_test.shape)


# %% [markdown]
# 4. Normalizar dados
#
# Completar a normalização.
#
# Dica:
# - No treino é usado fit_transform, onde o scaler aprende média/desvio-padrão
#   do conjunto de treino e transforma o treino.
# - No teste é usado o transform, porque o teste não pode ensinar nada ao modelo.

# %%
scaler = StandardScaler()

X_train_scaled = scaler.__________(__________)
X_test_scaled = scaler.__________(__________)


# %% [markdown]
# 5. Criar e treinar o modelo
#
# Começar com uma árvore de decisão.
#
# Completar:
# - o random_state
# - o método que faz o modelo aprender
# - os dados usados no treino

# %%
modelo = DecisionTreeClassifier(
    random_state=__________
)

modelo.__________(__________, __________)


# %% [markdown]
# 6. Fazer previsões
#
# Completar:
# - aplicar o modelo ao conjunto de teste normalizado.

# %%
y_pred = modelo.__________(__________)


# %% [markdown]
# 7. Avaliar o modelo
#
# Completar as métricas.
#
# Dicas:
# - Accuracy: proporção de casos corretamente classificados.
# - Matriz de confusão: permite ver falsos positivos e falsos negativos.
# - Relatório de classificação: inclui precision, recall, f1-score e support.

# %%
acc = accuracy_score(__________, __________)

cm = confusion_matrix(__________, __________)

report = classification_report(__________, __________, target_names=target_names)

print("Accuracy:")
print(acc)

print("\nMatriz de confusão:")
print(cm)

print("\nRelatório de classificação:")
print(report)


# %% [markdown]
# 8. Ver a matriz de confusão com nomes das classes
#
# Completar:
# - usar a matriz de confusão criada anteriormente.
# - usar os nomes das classes para facilitar a leitura.

# %%
cm_df = pd.DataFrame(
    __________,
    index=[f"Real: {classe}" for classe in __________],
    columns=[f"Previsto: {classe}" for classe in __________]
)

cm_df


# %% [markdown]
# 9. Comparar com outros modelos
#
# Completar:
# - os imports dos modelos em falta.
# - o dicionário de modelos.
# - o treino, previsão e cálculo da accuracy.
#
# Pergunta:
# Se dois modelos tiverem desempenhos semelhantes, qual escolheriam em contexto de saúde?
# Porquê?

# %%
from sklearn.linear_model import __________
from sklearn.ensemble import __________

modelos = {
    "Árvore de decisão": DecisionTreeClassifier(random_state=42),
    "Regressão logística": __________(max_iter=1000),
    "Random forest": __________(random_state=42)
}

resultados = []

for nome, modelo in modelos.items():
    modelo.__________(__________, __________)
    y_pred_modelo = modelo.__________(__________)

    acc_modelo = accuracy_score(__________, __________)

    resultados.append({
        "modelo": nome,
        "accuracy": acc_modelo
    })

pd.DataFrame(resultados)


# %% [markdown]
# 10. Relatório para o modelo escolhido
#
# Escolha um modelo como modelo final.
#
# Completar:
# - criação do modelo final.
# - treino.
# - previsão.
# - relatório final.

# %%
modelo_final = __________(max_iter=1000)

modelo_final.__________(__________, __________)
y_pred_final = modelo_final.__________(__________)

print(classification_report(
    __________,
    __________,
    target_names=__________
))