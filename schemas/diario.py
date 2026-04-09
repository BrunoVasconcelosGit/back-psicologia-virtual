from pydantic import BaseModel
from typing import Optional, List
from model.diario import Diario


class DiarioSchema(BaseModel):
    """ Define como um novo registro deve inserido deve ser representado
    """
    descricao: str = "Me sinto normal porque o dia transcorreu sem grandes alegrias, ou infelicidades."
    nota: Optional[int] = 5


class DiarioBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base na descrição do dia.
    """
    id: int = 1

class DiarioEditaSchema(BaseModel):
    """ 
        Define o que deve ser passado para edição de um registro
    """
    id: int = 1
    descricao: str = "Me sinto normal porque o dia transcorreu sem grandes alegrias, ou infelicidades."
    nota: Optional[int] = 5


class ListagemDiariosSchema(BaseModel):
    """ Define como uma listagem de diarios será retornada.
    """
    diarios:List[DiarioSchema]


def apresenta_diarios(diarios: List[Diario]):
    """ Retorna uma representação do diario seguindo o schema definido em
        DiarioViewSchema.
    """
    result = []
    for diario in diarios:
        result.append({
            "id": diario.id,
            "descricao": diario.descricao,
            "nota": diario.nota,
            "data_insercao": diario.data_insercao.strftime("%d/%m/%Y %H:%M")
        })

    return {"diarios": result}


class DiarioViewSchema(BaseModel):
    """ Define como um diário será retornado.
    """
    id: int = 1
    descricao: str = "Me sinto normal porque o dia transcorreu sem grandes alegrias, ou infelicidades."
    nota: Optional[int] = 5


class DiarioDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    descricao: str

def apresenta_diario(diario: Diario):
    """ Retorna uma representação do diario seguindo o schema definido em
        DiarioViewSchema.
    """
    return {
        "id": diario.id,
        "descricao": diario.descricao,
        "nota": diario.nota,
        "data_insercao": diario.data_insercao.strftime("%d/%m/%Y %H:%M")
    }
