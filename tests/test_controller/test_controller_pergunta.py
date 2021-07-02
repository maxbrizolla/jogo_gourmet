from controller import valida_resposta, valida_reposta_str


def test_valida_resposta():
    verifica = valida_resposta(3)
    assert isinstance(verifica, bool)
    assert verifica


def test_valida_resposta_str():
    verifica = valida_reposta_str('')
    assert isinstance(verifica, bool)
    assert verifica
