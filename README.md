# BarberEase


# Guia de Configuração do Ambiente de Desenvolvimento

Este guia fornecerá instruções passo a passo para configurar um ambiente de desenvolvimento para o projeto Django. Certifique-se de seguir essas etapas para começar a trabalhar no projeto.

## Pré-Requisitos

Certifique-se de ter as seguintes ferramentas instaladas em seu sistema:

- Python 3.6 ou superior
- Ambiente virtual (recomendado)
- Postgres e PgAdmin
- Outras dependências listadas em `requirements.txt`

## Configuração do Repositório na sua Máquina Local

1. Abra o terminal na pasta onde você deseja clonar o projeto.

2. Clone o repositório:

    ```bash
    git clone git@github.com:ana-flav/projeto_barberease.git
3. Inicie o git flow:

    ```bash
    git flow init
## Configuração do Ambiente Virtual

Recomendamos criar um ambiente virtual para isolar as dependências do projeto. Siga os passos abaixo para configurar o ambiente:

1. Abra um terminal na raiz do seu projeto.
2. Crie um ambiente virtual:

   ```bash
   python -m venv venv
   
3. Ative o ambiente virtual (dependendo do seu sistema operacional):
   no windowns:
   ```bash
   venv\Scripts\activate
   
  No macOS e Linux:
   ```bash
    source venv/bin/activate
```

4. Instale as depedências do projeto
   ```bash
    pip install -r requirements.txt
