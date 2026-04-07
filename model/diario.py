from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base


class Diario(Base):
    __tablename__ = 'diario'

    id = Column("pk_diario", Integer, primary_key=True)
    descricao = Column(String(300))
    nota = Column(Integer)
    data_insercao = Column(DateTime, default=datetime.now)

    def __init__(self, descricao:str, nota:int, data_insercao:Union[DateTime, None] = None):
        """
        Cria um diario

        Arguments:
            descricao: texto do diario
            nota: avaliação do dia
            data_insercao: data de quando o diario foi inserido à base
        """
        self.descricao = descricao
        self.nota = nota

        # se não for informada, será a data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

