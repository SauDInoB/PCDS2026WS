# %% [markdown]
# # Exercício prático — Aprendizagem não supervisionada
# ## K-means, PCA e interpretação de clusters em dados de saúde
#
# Neste exercício usa-se o Diabetes dataset incluído no scikit-learn.
#
# O objetivo é explorar perfis semelhantes com K-means, visualizar grupos com PCA
# e avaliar a separação dos clusters com o silhouette score.
#
# Como usar no Visual Studio Code:
# 1. Abrir este ficheiro no VS Code.
# 2. Garantir que as bibliotecas estão instaladas:
#        pip install pandas matplotlib scikit-learn
# 3. Executar célula a célula, usando as marcações # %%.
# 4. Completar todos os espaços assinalados com __________.

# %% [markdown]
# ## 0. Importar bibliotecas
#
# Complete os imports principais.
#
# Dicas:
# - load_diabetes: carregar o dataset
# - StandardScaler: normalizar dados
# - KMeans: criar clusters
# - PCA: reduzir dimensionalidade
# - silhouette_score: avaliar coesão/separação dos clusters

# %%
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import __________
from sklearn.preprocessing import __________
from sklearn.cluster import __________
from sklearn.decomposition import __________
from sklearn.metrics import __________


# %% [markdown]
# ## 1. Ler dados
#
# O target é carregado apenas para referência.
#
# Neste exercício o target não é usado para criar clusters.

# %%
data = __________(as_frame=True)

df = data.data
target = data.target

df.head()

df.shape


# %% [markdown]
# ## 2. Escolher variáveis
#
# Selecione quatro variáveis numéricas para a análise.
#
# Sugestão:
# - age : idade
# - bmi : índice de massa corporal
# - bp  : pressão arterial média
# - s5  : logaritmo dos triglicéridos séricos
#
# O objetivo não é prever uma resposta conhecida, mas procurar estrutura nos dados.

# %%
X = df[[
    __________,
    __________,
    __________,
    __________
]]

X.head()

# %% [markdown]
# ## 3. Normalizar dados
#
# A normalização é importante porque o K-means usa distâncias.
#
# Se uma variável tiver valores numa escala muito maior, pode dominar o cálculo da distância,
# mesmo que não seja clinicamente mais importante.

# %%
scaler = __________()

X_scaled = scaler.__________(X)


# %% [markdown]
# ### Verificação rápida
#
# Confirme se X e X_scaled têm o mesmo número de linhas e colunas.

# %%
X.shape, X_scaled.shape


# %% [markdown]
# ## 4. Aplicar K-means
#
# Começe com k = 3, ou seja, três clusters.
#
# Complete:
# - número de clusters;
# - random_state;
# - n_init (indica quantas vezes o algoritmo vai começar de novo com centróides iniciais diferentes);
# - método que treina o K-means e devolve o cluster de cada observação.

# %%
kmeans = __________(
    n_clusters=__________,
    random_state=__________,
    n_init=__________
)

clusters = kmeans.__________(X_scaled)


# %% [markdown]
# ### Tamanho dos clusters
#
# Quantas observações ficaram em cada cluster?

# %%
pd.Series(clusters).value_counts().sort_index()


# %% [markdown]
# ## 5. Visualizar com PCA
#
# A PCA reduz os dados para duas componentes principais, permitindo representar os clusters
# num gráfico 2D.
#
# Complete o número de componentes e o método que aplica PCA aos dados normalizados.

# %%
pca = __________(n_components=__________)

X_pca = pca.__________(X_scaled)


# %% [markdown]
# ### Variância explicada
#
# Esta informação indica quanta variabilidade dos dados é resumida por cada componente.

# %%
pca.explained_variance_ratio_


# %% [markdown]
# ## 6. Criar tabela de resultados
#
# Juntar:
# - variáveis originais escolhidas;
# - cluster atribuído a cada observação;
# - duas componentes principais.

# %%
df_resultados = X.copy()

df_resultados["cluster"] = __________
df_resultados["PC1"] = X_pca[:, __________]
df_resultados["PC2"] = X_pca[:, __________]

df_resultados.head()


# %% [markdown]
# ## 7. Resumir os clusters
#
# As médias por cluster ajudam a perceber em que variáveis os grupos diferem.

# %%
resumo_clusters = (
    df_resultados
    .groupby(__________)
    .mean()
)

resumo_clusters


# %% [markdown]
# ## 8. Calcular silhouette score
#
# O silhouette score ajuda a avaliar a coesão interna e a separação entre grupos.
#
# Interpretação geral:
# - próximo de 1: grupos mais separados;
# - próximo de 0: grupos sobrepostos;
# - negativo: atribuições problemáticas.

# %%
sil = __________(X_scaled, clusters)

sil


# %% [markdown]
# ## 9. Visualizar os clusters
#
# Complete os elementos necessários para criar o gráfico:
# - eixo X: PC1;
# - eixo Y: PC2;
# - cor: cluster.

# %%
plt.figure(figsize=(7, 5))

plt.scatter(
    df_resultados[__________],
    df_resultados[__________],
    c=df_resultados[__________],
    alpha=0.75
)

plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("Clusters obtidos com K-means")
plt.grid(True, alpha=0.3)
plt.show()


# %% [markdown]
# ## 10. Comparar diferentes valores de k
#
# Compare com k=2, k=3 e k=4.
#
# Complete o ciclo para:
# - treinar um K-means para cada valor de k;
# - obter os clusters;
# - calcular o silhouette score;
# - guardar os resultados numa tabela.

# %%
resultados_k = []

for k in [__________, __________, __________]:
    modelo = __________(
        n_clusters=__________,
        random_state=42,
        n_init=10
    )

    clusters_k = modelo.__________(X_scaled)
    sil_k = __________(X_scaled, clusters_k)

    resultados_k.append({
        "k": k,
        "silhouette_score": sil_k
    })

pd.DataFrame(resultados_k)


# %% [markdown]
# ## 11. Método do cotovelo
#
# O método do cotovelo compara a inércia para diferentes valores de k.
#
# A inércia tende a diminuir quando aumentamos o número de clusters.
# A ideia é procurar o ponto em que o ganho adicional começa a ser menor.
#
# Complete:
# - a lista de valores de k;
# - o modelo K-means;
# - o treino do modelo;
# - o valor de inércia.

# %%
valores_k = range(__________, __________)
inercias = []

for k in valores_k:
    modelo = __________(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    modelo.__________(X_scaled)
    inercias.append(modelo.__________)

plt.figure(figsize=(7, 5))
plt.plot(valores_k, inercias, marker="o")
plt.xlabel("Número de clusters (k)")
plt.ylabel("Inércia")
plt.title("Método do cotovelo")
plt.grid(True, alpha=0.3)
plt.show()


# %% [markdown]
# ## 12. Visualizar alternativas com k=2, k=3 e k=4
#
# Este bloco ajuda a perceber se diferentes valores de k originam grupos visualmente
# mais claros no espaço da PCA.

# %%
for k in [2, 3, 4]:
    modelo = KMeans(
        n_clusters=__________,
        random_state=42,
        n_init=10
    )

    clusters_k = modelo.__________(X_scaled)

    plt.figure(figsize=(6, 4))
    plt.scatter(
        X_pca[:, 0],
        X_pca[:, 1],
        c=__________,
        alpha=0.75
    )

    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title(f"Clusters com k={k}")
    plt.grid(True, alpha=0.3)
    plt.show()