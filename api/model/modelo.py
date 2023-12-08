import numpy as np
import pickle
import joblib


class Model:
    @staticmethod
    def carrega_modelo(path, scaler_path=None):
        """Dependendo se o final for .pkl ou .joblib, carregamos de uma forma ou de outra"""

        if path.endswith(".pkl"):
            model = pickle.load(open(path, "rb"))
        elif path.endswith(".joblib"):
            model = joblib.load(path)
        else:
            raise Exception("Formato de arquivo não suportado")

        if scaler_path is not None:
            model.scaler = scaler_path

        return model

    @staticmethod
    def preditor(model, form):
        """Realiza a predição de um vinho com base no modelo treinado"""
        X_input = np.array([
            form.fixed_acidity,
            form.volatile_acidity,
            form.citric_acid,
            form.residual_sugar,
            form.chlorides,
            form.free_sulfur_dioxide,
            form.total_sulfur_dioxide,
            form.density,
            form.ph,
            form.sulphates,
            form.alcohol,
        ])

        # Faremos o reshape para que o modelo entenda que estamos passando
        X_input = X_input.reshape(1, -1)

        # Padronização nos dados de entrada usando o scaler utilizado em X_train
        X_input_scaled = model.scaler.transform(X_input)

        # Adicionando uma dimensão extra para corresponder ao formato esperado pelo modelo
        avaliacao = model.predict(X_input_scaled.reshape(1, -1))

        return int(avaliacao[0])
