from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base

class Vinho(Base):
    __tablename__ = "vinhos"

    # entrada
    id = Column(Integer, primary_key=True)
    fixed_acidity = Column("fixed_acidity", Integer)
    volatile_acidity = Column("volatile_acidity", Float)
    citric_acid = Column("citric_acid", Float)
    residual_sugar = Column("residual_sugar", Float)
    chlorides = Column("chlorides", Float)
    free_sulfur_dioxide = Column("free_sulfur_dioxide", Float)
    total_sulfur_dioxide = Column("total_sulfur_dioxide", Float)
    density = Column("density", Float)
    ph = Column("ph", Float)
    sulphates = Column("sulphates", Float)
    alcohol = Column("alcohol", Float)
    # Saída
    quality = Column("quality", Integer, nullable=True)
    insert_date = Column(DateTime, default=datetime.now())

    def __init__(
        self,
        fixed_acidity: float,
        volatile_acidity: float,
        citric_acid: float,
        residual_sugar: float,
        chlorides: float,
        free_sulfur_dioxide: float,
        total_sulfur_dioxide: float,
        density: float,
        ph: float,
        sulphates: float,
        alcohol: float,
        quality:int,
        insert_date: Union[DateTime, None] = None,
    ):
        """
        Registra uma análise de Vinho

        Arguments:

            fixed_acidity (float): Acidez fixa
            volatile_acidity (float): Acidez volátil
            citric_acid (float): Ácido cítrico
            residual_sugar (float): Açúcar residual
            chlorides (float): Cloretos
            free_sulfur_dioxide (float): Dióxido de enxofre livre
            total_sulfur_dioxide (float): Dióxido de enxofre total
            density (float): Densidade
            ph (float): pH
            sulphates (float): Sulfatos
            alcohol (float): Teor alcoólico
            quality (int): Avaliação de qualidade
            insert_data: Data de inserção dos dados do vinho
        """

        self.fixed_acidity = fixed_acidity
        self.volatile_acidity = volatile_acidity
        self.citric_acid = citric_acid
        self.residual_sugar = residual_sugar
        self.chlorides = chlorides
        self.free_sulfur_dioxide = free_sulfur_dioxide
        self.total_sulfur_dioxide = total_sulfur_dioxide
        self.density = density
        self.ph = ph
        self.sulphates = sulphates
        self.alcohol = alcohol
        self.quality = quality

        # Se não for informada, será o data exata da inserção no banco
        if insert_date:
            self.insert_date = insert_date
