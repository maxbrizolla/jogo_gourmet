from controller.pergunta_controller import PerguntasController
from database.DB import DB
from database.operations import PerguntaOperations

if __name__ == '__main__':
    print('Instruções de Uso:')
    print(
        'Use os números 1 para Sim/Continuar, '
        '2 para Não ou 3 para encerrar o programa e tecle Enter para confirmar a escolha.')
    print(
        'Haverá perguntas que a resposta precisará ser preenchida com um texto, após tecle Enter para confirmar. ')

    database = DB()
    database.create_database()

    po = PerguntaOperations(database=database)

    po.add_perguntas_iniciais()

    pc = PerguntasController(po, 1)

    pc.faz_pergunta()



