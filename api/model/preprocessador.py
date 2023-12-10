from sklearn.model_selection import train_test_split


class PreProcessador:
    def pre_processar(self, dataset, percentual_teste, seed=7):
        """Cuida de todo o pré-processamento."""
        # limpeza dos dados e eliminação de outliers

        def normalize(value):
            if value >= 6:
                return 1
            else:
                return 0

        # Aplicar a função à coluna 12 do dataset
        dataset.iloc[:, 11] = dataset.iloc[:, 11].apply(normalize)

        # Remover as linhas com valores NaN
        dataset = dataset.dropna()

        # feature selection

        # divisão em treino e teste
        X_train, X_test, Y_train, Y_test = self.__preparar_holdout(
            dataset, percentual_teste, seed
        )
        # normalização/padronização

        print(f"Dataset: {dataset}")

        return (X_train, X_test, Y_train, Y_test)

    def __preparar_holdout(self, dataset, percentual_teste, seed):
        """Divide os dados em treino e teste usando o método holdout.
        Assume que a variável target está na última coluna.
        O parâmetro test_size é o percentual de dados de teste.
        """
        dados = dataset.values
        print(f"Dados holdout: {dados}")
        X = dados[:, 0:-1]
        Y = dados[:, 11]
        return train_test_split(X, Y, test_size=percentual_teste, random_state=seed)
