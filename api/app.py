from sqlalchemy.exc import SQLAlchemyError
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request
from urllib.parse import unquote
import joblib

from sqlalchemy.exc import IntegrityError

from model import Session, Vinho, Model
from logger import logger
from schemas import *
from flask_cors import CORS


# Instanciando o objeto OpenAPI
info = Info(title="Avaliação de Qualidade - Vinhos", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo tags para agrupamento das rotas
vinho_tag = Tag(
    name="Vinho",
    description="Adição, visualização, remoção e predição de avaliação de vinhos",
)


# Rota home
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect("/openapi/swagger")


# Recurso: Listagem de vinhos
@app.get(
    "/vinhos",
    tags=[vinho_tag],
    responses={"200": VinhoViewSchema, "404": ErrorSchema},
)
def get_vinhos():
    """Lista todos os vinhos cadastrados na base
    Retorna uma lista de vinhos cadastrados na base.
    """
    session = Session()

    # Buscando todos os vinhos
    vinhos = session.query(Vinho).all()

    if not vinhos:
        logger.warning("Não há vinhos cadastrados na base.")
        return {"message": "Não há vinhos cadastrados na base."}, 404
    else:
        logger.debug(f"%d vinhos econtrados" % len(vinhos))
        return apresenta_vinhos(vinhos), 200


# Recurso: Inclusão de vinho
@app.post(
    "/vinho",
    tags=[vinho_tag],
    responses={"201": VinhoViewSchema, "400": ErrorSchema, "409": ErrorSchema},
)
def predict(form: VinhoSchema):
    """Adiciona um novo vinho à base de dados
    Inclui um novo vinho e retorna uma representação dos vinhos avaliados e suas qualidades.

    Returns:
        Exibe o Schema da inclusão do vinho e todas as suas propriedades.
    """
    try:
        with Session() as session:

            print(f"Form: {form}")

            # Carregando modelo
            ml_path = "ml_model/vinho_qualidade_knn.pkl"
            scaler_path = joblib.load("ml_model/scaler.joblib")
            modelo = Model.carrega_modelo(ml_path, scaler_path)

            print(f"Modelo: {modelo}")

            # Verificar se o modelo foi carregado com sucesso
            if modelo is None:
                return {"message": "Erro ao carregar modelo"}, 500

            # Exibindo informações de depuração
            logger.debug(f"Modelo carregado: {modelo}")
            logger.debug(f"Caminho do modelo: {ml_path}")

            # Criando instância de Vinho
            vinho = Vinho(
                fixed_acidity=form.fixed_acidity,
                volatile_acidity=form.volatile_acidity,
                citric_acid=form.citric_acid,
                residual_sugar=form.residual_sugar,
                chlorides=form.chlorides,
                free_sulfur_dioxide=form.free_sulfur_dioxide,
                total_sulfur_dioxide=form.total_sulfur_dioxide,
                density=form.density,
                ph=form.ph,
                sulphates=form.sulphates,
                alcohol=form.alcohol,
                quality=Model.preditor(modelo, form)
            )

            logger.debug(f"Adicionando vinho: '{vinho.id}'")

            session = Session()
            session.add(vinho)
            session.commit()

            return apresenta_vinho(vinho), 200

    # Exceção específica para SQLAlchemyError
    except SQLAlchemyError as e:
        # Faz rollback se ocorrer uma exceção
        session.rollback()
        error_msg = f"Não foi possível salvar novo item. Detalhes: {str(e)}"
        logger.warning(f"Erro ao adicionar vinho '{vinho.id}', {error_msg}")
        return {"message": error_msg}, 400

    # Exceção genérica para qualquer outra exceção
    except Exception as e:
        error_msg = f"Erro inesperado. Detalhes: {str(e)}"
        logger.error(f"Erro ao adicionar vinho '{vinho.id}', {error_msg}")
        return {"message": error_msg}, 500


# Métodos baseados em ID
# Recurso: Busca de vinho por ID


@app.get(
    "/vinho",
    tags=[vinho_tag],
    responses={"200": VinhoViewSchema, "404": ErrorSchema},
)
def get_vinho(query: VinhoBuscaSchema):
    """Faz a busca por um vinho cadastrado na base a partir do ID

    Args:
        Id (int): Id do registro do vinho

    Returns:
        dict: representação do vinho
    """

    vinho_id = query.id
    logger.debug(f"Coletando dados sobre produto #{vinho_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    vinho = session.query(Vinho).filter(Vinho.id == vinho_id).first()

    if not vinho:
        # se o vinho não foi encontrado
        error_msg = f"Vinho com ID {vinho_id} não foi encontrado na base."
        logger.warning(f"Erro ao buscar produto '{vinho_id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Vinho econtrado: '{vinho.id}'")
        # retorna a representação do vinho
        return apresenta_vinho(vinho), 200


# Rota de remoção de vinho por id
@app.delete(
    "/vinho",
    tags=[vinho_tag],
    responses={"202": VinhoViewSchema, "404": ErrorSchema},
)
def delete_vinho(query: VinhoBuscaSchema):
    """Remove um vinho cadastrado a partir do id

    Args:
        nome (str): nome do paciente

    Returns:
        msg: Mensagem de sucesso ou erro
    """

    vinho_id = query.id
    logger.debug(f"Deletando dados sobre vinho #{vinho_id}")

    # Criando conexão com a base
    session = Session()

    # Buscando vinho
    vinho = session.query(Vinho).filter(Vinho.id == vinho_id).first()

    if not vinho:
        error_msg = "Vinho não encontrado na base."
        logger.warning(f"Erro ao deletar vinho '{vinho_id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        session.delete(vinho)
        session.commit()
        logger.debug(f"Vinho deletado #{vinho_id}")
        return {"message": f"Vinho {vinho_id} removido com sucesso!"}, 200
