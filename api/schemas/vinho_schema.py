from pydantic import BaseModel
from typing import Optional, List
from model.vinho import Vinho
import json
import numpy as np


class VinhoSchema(BaseModel):
    """Define como um novo vinho a ser inserido deve ser representado"""

    fixed_acidity : float = 7.4
    volatile_acidity : float = 0.7
    citric_acid : float = 0
    residual_sugar : float = 1.9
    chlorides : float = 0.076
    free_sulfur_dioxide : float = 11
    total_sulfur_dioxide : float = 34
    density : float = 0.9978
    ph : float = 3.51
    sulphates : float = 0.56
    alcohol : float = 9.4


class VinhoViewSchema(BaseModel):
    """Define como um vinho será retornado"""

    id : int = 1
    fixed_acidity : float = 7.4
    volatile_acidity : float = 0.7
    citric_acid : float = 0
    residual_sugar : float = 1.9
    chlorides : float = 0.076
    free_sulfur_dioxide : float = 11
    total_sulfur_dioxide : float = 34
    density : float = 0.9978
    ph : float = 3.51
    sulphates : float = 0.56
    alcohol : float = 9.4
    quality : Optional[int] = None


class VinhoBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.
    Ela será feita com base no id do vinho.
    """

    id: int = 1


class ListaVinhoSchema(BaseModel):
    """Define como uma lista de vinhos será representada"""

    vinhos: List[VinhoSchema]


class VinhoDelSchema(BaseModel):
    """Define como um vinho para deleção será representado"""

    id: int = 1


# Apresenta apenas os dados de um vinho
def apresenta_vinho(vinho: Vinho):
    """Retorna uma representação do vinho seguindo o schema definido em
    VinhoViewSchema.
    """
    return {
        "id": vinho.id,
        "fixed_acidity" : vinho.fixed_acidity,
        "volatile_acidity" : vinho.volatile_acidity,
        "citric_acid" : vinho.citric_acid,
        "residual_sugar" : vinho.residual_sugar,
        "chlorides" : vinho.chlorides,
        "free_sulfur_dioxide" : vinho.free_sulfur_dioxide,
        "total_sulfur_dioxide" : vinho.total_sulfur_dioxide,
        "density" : vinho.density,
        "ph" : vinho.ph,
        "sulphates" : vinho.sulphates,
        "alcohol" : vinho.alcohol,
        "quality" : vinho.quality
    }


# Apresenta uma lista de vinhos
def apresenta_vinhos(vinhos: List[Vinho]):
    """Retorna uma representação do vinho seguindo o schema definido em
    VinhoViewSchema.
    """
    result = []
    for vinho in vinhos:
        result.append(
            {
            "id": vinho.id,
            "fixed_acidity" : vinho.fixed_acidity,
            "volatile_acidity" : vinho.volatile_acidity,
            "citric_acid" : vinho.citric_acid,
            "residual_sugar" : vinho.residual_sugar,
            "chlorides" : vinho.chlorides,
            "free_sulfur_dioxide" : vinho.free_sulfur_dioxide,
            "total_sulfur_dioxide" : vinho.total_sulfur_dioxide,
            "density" : vinho.density,
            "ph" : vinho.ph,
            "sulphates" : vinho.sulphates,
            "alcohol" : vinho.alcohol,
            "quality" : vinho.quality
            }
        )

    return {"vinhos": result}
