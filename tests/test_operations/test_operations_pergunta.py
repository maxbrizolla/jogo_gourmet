from database.DB import DB
from database.models import Pergunta
from database.operations import PerguntaOperations


def test_get_id():
    database = DB()
    op = PerguntaOperations(database=database)
    ret = op.get_id(1)
    assert ret is not None
    assert isinstance(ret, Pergunta)