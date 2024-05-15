# Projeto 1 - Sistemas Distribuídos: Jogo quatro em linha

## Índice

* [Instruções de uso](#instruções-de-uso)
* [Contribuições](#contribuições)
* [Licença](#licença)
* [Autores](#autores)

## Instruções de uso

Para usar o repositório, basta cloná-lo para o seu computador. Você pode usar o seguinte comando para clonar o repositório:

```bash
git clone https://github.com/matheusssilva991/compiladores.git
```

Em seguida, você deve criar um ambiente virtual ou ambiente Anaconda para instalar as bibliotecas necessárias para executar as atividades.

### Criar um ambiente virtual com Python

Para criar um ambiente virtual com Python, você pode usar o seguinte comando:

```bash
python -m venv [nome-do-ambiente] # Windows
python3 -m venv [nome-do-ambiente] # Linux
```

Para ativar o ambiente virtual, você pode usar o seguinte comando:

* Windows

```bash
.\[nome-do-ambiente]\Script\activate
```

* Linux

```bash
source [nome-do-ambiente]/bin/activate
```

Para instalar as bibliotecas usando os arquivos de requisitos, você pode usar o seguinte comando:

```bash
pip install -r requirements.txt
```

* Windows e Linux

Para desativar o ambiente, você pode usar o seguinte comando

```bash
deactivate
```

### Rodar o jogo

Para rodar o servidor

```bash
python3 src/server/server.py # Linux
python src/server/server.py # Windows
```

Para rodar o cliente

```bash
python3 src/client/client.py # Linux
python src/client/client.py # Windows
```

### Rodar os testes

```bash
python3 -m unittest src/tests/tests.py -v # Linux
python -m unittest src/tests/tests.py -v # Windows
```

## Contribuições

Se você tiver alguma contribuição para o repositório, fique à vontade para enviar um pull request.

## Licença

Este repositório está licenciado sob a licença MIT.

## Autores

* [Matheus Santos Silva](https://github.com/matheusssilva991)
