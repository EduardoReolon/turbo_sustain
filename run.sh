#!/bin/bash

# Nome do ambiente virtual
VENV_DIR="venv"

# Criar venv se não existir
if [ ! -d "$VENV_DIR" ]; then
    echo "🔹 Criando ambiente virtual..."
    python3 -m venv $VENV_DIR
    source $VENV_DIR/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "🔹 Ativando ambiente virtual..."
    source $VENV_DIR/bin/activate
fi

# Executar script
echo "🔹 Iniciando teste..."
python main.py
