from typing import Union

from sqlalchemy import Column, Integer, String, Boolean

from database.models.base import Base


class Pergunta(Base):
    __tablename__ = "pergunta"
    id = Column(Integer, primary_key=True, autoincrement=True)
    pergunta = Column(String, nullable=False)
    proximo_sim = Column(Integer)
    proximo_nao = Column(Integer)
    fim = Column(Boolean)

    def __init__(self, pergunta, proximo_sim=None, proximo_nao=None, fim=False, id: Union[None, int] = None):
        self.id = id
        self.pergunta = pergunta
        self.proximo_sim = proximo_sim
        self.proximo_nao = proximo_nao
        self.fim = fim

    def info(self):
        return {"id": self.id, "pergunta": self.pergunta, "proximo_sim": self.proximo_sim, "proximo_nao": self.proximo_nao}
