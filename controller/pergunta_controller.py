import json
import sys
from time import sleep

import pylab as p
import requests

from config.config import USE_AWS
from database.models import Pergunta
from database.operations import PerguntaOperations


def valida_resposta(resposta: str) -> bool:
    if USE_AWS == 1:
        try:
            payload = {'resposta': resposta}
            headers = {'content-type': 'application/json'}
            r = requests.post("https://n5439v6q40.execute-api.us-east-1.amazonaws.com/test",
                              data=json.dumps(payload), headers=headers)
            j = json.loads(r.text)
            return j['statusCode'] == 200
        except Exception as ex:
            return False
    else:
        try:
            ret = int(resposta)
            if ret not in [1, 2, 3]:
                return False
            else:
                return True
        except ValueError:
            return False


def valida_reposta_str(resposta: str) -> bool:
    return (resposta.strip(' ') != '')


class PerguntasController:
    PERGUNTA_BASE = '\nO prato que você pensou é {} [1, 2, 3]?'
    PERGUNTA_QUAL_PRATO = '\nQual prato você pensou [texto]?'
    PERGUNTA_E_MAS_NAO = '\n{} é _____ mas,  {} não. [texto]'
    PERGUNTA_FINAL = 5
    PERGUNTA_INICIAL = 1

    def __init__(self, po: PerguntaOperations, pergunta_id: int = 1):
        self.po = po
        self.pergunta_id = pergunta_id

    def faz_pergunta(self):
        pergunta = self.po.get_id(self.pergunta_id)
        resposta = input(self.PERGUNTA_BASE.format(pergunta.pergunta) if self.pergunta_id > self.PERGUNTA_INICIAL else pergunta.pergunta)

        verifica = valida_resposta(resposta=resposta)
        if verifica:
            self.determina_fluxo(resposta, pergunta)
        else:
            print('\nOpção inválida, tente de novo.')
            self.faz_pergunta()

    def determina_fluxo(self, resposta: str, pergunta: Pergunta):
        res = int(resposta)

        if res == 3:
            sys.exit(9)
        if res == 1:
            self.fluxo_sim(pergunta=pergunta)

        if res == 2:
            self.fluxo_nao(pergunta=pergunta)

    def fluxo_nao(self, pergunta: Pergunta):
        if self.pergunta_id == 1:
            sys.exit(9)

        if pergunta.proximo_nao is None:
            self.faz_pergunta_qual_prato(pergunta_original=pergunta)
        else:
            self.pergunta_id = pergunta.proximo_nao
            self.faz_pergunta()

    def faz_pergunta_qual_prato(self, pergunta_original: Pergunta):
        resposta = input(self.PERGUNTA_QUAL_PRATO)

        verifica = valida_reposta_str(resposta=resposta)

        if not verifica:
            print('\nOps... Não entendi, você não penso em nenhum prato? Tente de novo')
            self.faz_pergunta_qual_prato(pergunta_original=pergunta_original)

        pergunta = self.po.add(
            Pergunta(pergunta=resposta, proximo_sim=self.PERGUNTA_FINAL)
        )
        self.faz_pergunta_e_mas_nao(pergunta_nova=pergunta, pergunta_original=pergunta_original)

    def faz_pergunta_e_mas_nao(self, pergunta_nova: Pergunta, pergunta_original: Pergunta):
        resposta = input(self.PERGUNTA_E_MAS_NAO.format(pergunta_nova.pergunta, pergunta_original.pergunta))

        verifica = valida_reposta_str(resposta=resposta)

        if not verifica:
            print('\nOps... Fiquei confuso, poderia repetir por favor. Não sei trabalhar com respostas em branco.')
            self.faz_pergunta_e_mas_nao(pergunta_nova=pergunta_nova, pergunta_original=pergunta_original)

        pergunta = self.po.add(
            Pergunta(pergunta=resposta, proximo_sim=pergunta_nova.id, proximo_nao=pergunta_original.id)
        )

        self.ajusta_fluxo(pergunta_nova=pergunta, pergunta_original=pergunta_original)

        self.pergunta_id = self.PERGUNTA_INICIAL
        self.faz_pergunta()

    def ajusta_fluxo(self, pergunta_nova: Pergunta, pergunta_original: Pergunta):
        pergunta_anterior = self.po.find_where(Pergunta.proximo_sim == pergunta_original.id)

        if len(pergunta_anterior) == 0:
            pergunta_anterior = self.po.find_where(Pergunta.proximo_nao == pergunta_original.id)
            pergunta_anterior = pergunta_anterior[0]
            pergunta_anterior.proximo_nao = pergunta_nova.id
        else:
            pergunta_anterior = pergunta_anterior[0]
            pergunta_anterior.proximo_sim = pergunta_nova.id

        self.po.add(
            pergunta_anterior
        )

    def fluxo_sim(self, pergunta: Pergunta):
        proxima_pergunta = self.po.get_id(pergunta.proximo_sim)

        if proxima_pergunta.fim:
            print('')
            print(proxima_pergunta.pergunta)
            sleep(2)
            self.pergunta_id = self.PERGUNTA_INICIAL
            self.faz_pergunta()
        else:
            self.pergunta_id = pergunta.proximo_sim
            self.faz_pergunta()
