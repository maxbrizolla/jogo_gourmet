# Jogo Gourmet

O jogo foi criado para demostrar os conhecimentos em python.

O mesmo tem por finalidade de, através das respostas fornecidas adivinhar qual prato o usuário está pensando.

Caso a resposta não esteja na lista é possível cadastrar novas opções.

## Requisitos

Python 3.9

## Instalação


```bash
git clone https://github.com/maxbrizolla/jogo_gourmet.git

cd jogo_gourmet

pip install -r requirements.txt

python app.py
```

## Configuração

Foi adicionado uma requisição lambda AWS para testar a funcionalidade. Em virtude de que esse EndPoint esteja desabilitado em um futuro próximo, segue como desabilitar o uso da função.

```bash

export USE_AWS=0

python app.py

```

Bom jogo....