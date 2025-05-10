#!/bin/bash

# Criar diretório de logs se não existir
mkdir -p logs

# Ativar ambiente virtual (se estiver usando)
# source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Iniciar o Gunicorn
gunicorn -c gunicorn_config.py main:app 