# 001 Fintech - Service Catalog

Python 3.8

## Pré-requisitos Ambiente Docker:

Para trabalhar nesse projeto você ira precisar instalar:

*[ Docker ](https://www.docker.com/get-started)			
*[ Docker Compose ](https://docs.docker.com/compose/install/)


## Ambiente de desenvolvimento

Após isso rode o comando de build

    sudo docker-compose build


Para subir o projeto execute o comando de up

    sudo docker-compose up 001-service-catalog

    //Para rodar em background execute:
    sudo docker-compose up -d

Sempre que instalar uma nova dependência do python refaça o arquivo requirements.txt e execute o build novamente.

    //Entrar no container
    sudo docker exec -it 001-service-catalog bash

    //Rodar este comando dentro do container
    python3 -m pip freeze > requirements.txt

    //sair do container e rodar o build novamente
    exit

    sudo docker-compose build

## Pré-requisitos Linux:

Python 3.8 e venv

    #Instalando Python 3.8
    sudo apt install python3.8

    #Instalando Python virtualenv
    sudo apt install python3.8-venv

## Ambiente de desenvolvimento Linux

    #Criar ambiente virtual Python 3.8 a partir da raiz do projeto
    python3.8 -m venv venv 

    #Entrar no ambiente virtual:
    source venv/bin/activate

    #Instalando dependencias do projeto 
    pip install -r requirements.txt

    #Rodando aplicação
    python runserver.py

    #Saindo do ambiente virtualenv
    deactivate

## Dependências

Sempre que instalar uma nova depencência lembre de atualizar o  arquivo requirements.txt

    #A partir do ambiente virtual
    pip freeze > requirements.txt





