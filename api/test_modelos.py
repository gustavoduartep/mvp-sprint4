from model.avaliador import Avaliador
from model.carregador import Carregador
from model.modelo import Model

# Instanciação das Classes
carregador = Carregador()
modelo = Model()
avaliador = Avaliador()

# Parâmetros
url_dados = "db/dataset-qualidade-vinho-tinto.csv"
colunas = [
    "fixed_acidity",
    "volatile_acidity",
    "citric_acid",
    "residual_sugar",
    "chlorides",
    "free_sulfur_dioxide",
    "total_sulfur_dioxide",
    "density",
    "ph",
    "sulphates",
    "alcohol",
    "quality"
]

# Carga dos dados
dataset = carregador.carregar_dados(url_dados, colunas)

# Construindo o dado de avaliação binária - Se maior ou igual a 6 retorna 1, se não, retorna 0


def normalize(value):
    if value >= 6:
        return 1
    else:
        return 0


# Aplicar a função à coluna de número 12 do dataset
dataset.iloc[:, 11] = dataset.iloc[:, 11].apply(normalize)

# Remove as linhas com valores NaN
dataset = dataset.dropna()

"""
# Separando em dados de entrada e saída
X = dataset.iloc[:, 0:-1]
Y = dataset.iloc[:, -1]
"""
# Separando os dados
# Entrada
# seleciona as colunas 1, 3, 4, 5, 6, 7, 8, 9 e 10
X = dataset.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
# Saida
Y = dataset.iloc[:, 11]  # seleciona a coluna 11

Y = Y.astype(int)

print("Valores de entrada X:")
print(X)

print("\nValores de saída Y:")
print(Y)


# Método para testar o modelo de Regressão Logística a partir do arquivo correspondente
def test_modelo_lr():
    # Importando o modelo de regressão logística
    lr_path = "ml_model/vinho_qualidade_lr.pkl"
    modelo_lr = modelo.carrega_modelo(lr_path)

    # Obtendo as métricas da Regressão Logística
    acuracia_lr, recall_lr, precisao_lr, f1_lr = avaliador.avaliar(
        modelo_lr, X, Y)

    # Testando as métricas da Regressão Logística
    # Modifique as métricas de acordo com seus requisitos
    assert acuracia_lr >= 0.6, f"Acurácia esperada >= 0.6, obtido {acuracia_lr}"
    assert recall_lr >= 0.5, f"Recall esperado >= 0.5, obtido {recall_lr}"
    assert precisao_lr >= 0.5, f"Precisão esperada >= 0.5, obtido {precisao_lr}"
    assert f1_lr >= 0.5, f"F1 Score esperado >= 0.5, obtido {f1_lr}"


# Método para testar modelo KNN a partir do arquivo correspondente
def test_modelo_knn():
    # Importando modelo de KNN
    knn_path = "ml_model/vinho_qualidade_knn.pkl"
    modelo_knn = modelo.carrega_modelo(knn_path)

    # Obtendo as métricas do KNN
    acuracia_knn, recall_knn, precisao_knn, f1_knn = avaliador.avaliar(
        modelo_knn, X, Y)

    # Testando as métricas do KNN
    # Modifique as métricas de acordo com seus requisitos
    assert acuracia_knn >= 0.6, f"Acurácia esperada >= 0.6, obtido {acuracia_knn}"
    assert recall_knn >= 0.5, f"Recall esperado >= 0.5, obtido {recall_knn}"
    assert precisao_knn >= 0.5, f"Precisão esperada >= 0.5, obtido {precisao_knn}"
    assert f1_knn >= 0.5, f"F1 Score esperado >= 0.5, obtido {f1_knn}"
