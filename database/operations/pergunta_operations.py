from typing import Optional

from sqlalchemy import Integer

from database.DB import DB
from database.models import Pergunta
from database.operations.operation import Operation


class PerguntaOperations(Operation):

    def __init__(self, database: DB):
        super().__init__(database=database, table=Pergunta)

    def add_perguntas_iniciais(self):
        self.delete_all()

        self.add(obj=Pergunta(
            id=1,
            pergunta='Pense em um prato que você gosta [1, 2, 3]?',
            proximo_sim=2
        ))
        self.add(obj=Pergunta(
            id=2,
            pergunta='Massa',
            proximo_sim=3,
            proximo_nao=4
        ))
        self.add(obj=Pergunta(
            id=3,
            pergunta='Lasanha',
            proximo_sim=5,

        ))
        self.add(obj=Pergunta(
            id=4,
            pergunta='Bolo de chocolate',
            proximo_sim=5,
        ))
        self.add(obj=Pergunta(
            id=5,
            pergunta='Acertei de novo!',
            fim=True
        ))

    def get_id(self, id: int) -> Optional[Pergunta]:
        result = self.get(id)
        return result
