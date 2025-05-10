#!/bin/bash

# Criar diretório de logs se não existir
mkdir -p logs

# Ativar ambiente virtual (se estiver usando)
# source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Iniciar o Flask com Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app 