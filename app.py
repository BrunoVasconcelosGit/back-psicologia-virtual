from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc

from model import Session, Diario
from schemas import *
from flask_cors import CORS

info = Info(title="api-psicologia-virtual", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
diario_tag = Tag(name="Diario", description="Adição, visualização e remoção de registros à base")


@app.get('/', tags=[diario_tag])
def home():
    """Redireciona para /openapi/swagger, tela do Swagger.
    """
    return redirect('/openapi/swagger')


@app.post('/diario', tags=[diario_tag],
          responses={"200": DiarioViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_diario(form: DiarioSchema):
    """Adiciona um novo registro à base de dados

    Retorna uma representação dos diários.
    """
    diario = Diario(
        descricao=form.descricao,
        nota=form.nota)
    try:
        # criando conexão com a base
        session = Session()
        # adicionando diário
        session.add(diario)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        
        return apresenta_diario(diario), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Houve algum erro."
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível processar a informação."
        
        return {"mesage": error_msg}, 400


@app.put('/diario', tags=[diario_tag],
          responses={"200": DiarioViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def edit_diario(form: DiarioEditaSchema):
    """Edita um registro da base de dados

    Retorna uma representação do diário editado.
    """

    try:
        # criando conexão com a base
        session = Session()

        # busca diário
        diario = session.query(Diario).filter(Diario.id == form.id).first()

        # retorna not found em caso de não exisitr o id procurado na tabela
        if not diario:
            return {"message": "Registro não encontrado"}, 404

        # Atualiza os campos
        diario.descricao = form.descricao
        diario.nota = form.nota
        
        # efetivando o camando de edição de item na tabela
        session.commit()
        
        return apresenta_diario(diario), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Houve algum erro."
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível processar a informação."
        
        return {"mesage": error_msg}, 400


@app.get('/diarios', tags=[diario_tag],
         responses={"200": ListagemDiariosSchema, "404": ErrorSchema})
def get_diarios():
    """Faz a busca por todos os registros cadastrados

    Retorna uma representação da listagem de diários.
    """
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    diarios = session.query(Diario).order_by(desc(Diario.data_insercao)).all()

    if not diarios:
        # se não há registros cadastrados
        return {"diarios": []}, 200
    else:
        # retorna a representação de registro
        print(diarios)
        return apresenta_diarios(diarios), 200


@app.get('/diario', tags=[diario_tag],
         responses={"200": DiarioViewSchema, "404": ErrorSchema})
def get_diario(query: DiarioBuscaSchema):
    """Faz a busca por um registro a partir do id do dia

    Retorna uma representação dos diários
    """
    diario_id = query.id
    
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    diario = session.query(Diario).filter(Diario.id == diario_id).first()

    if not diario:
        # se o registro não foi encontrado
        error_msg = "Registro não encontrado na base"
        
        return {"mesage": error_msg}, 404
    else:
        
        # retorna a representação de registro
        return apresenta_diario(diario), 200


@app.delete('/diario', tags=[diario_tag],
            responses={"200": DiarioDelSchema, "404": ErrorSchema})
def del_diario(query: DiarioBuscaSchema):
    """Deleta um registro a partir da sua descrição

    Retorna uma mensagem de confirmação da remoção.
    """
    diario_id = query.id
    print(diario_id)
    
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Diario).filter(Diario.id == diario_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        return {"mesage": "Registro removido", "id": diario_id}
    else:
        # se o registro não foi encontrado
        error_msg = "Registro não encontrado na base"
        
        return {"mesage": error_msg}, 404
