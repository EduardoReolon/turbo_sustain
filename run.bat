@echo off
set VENV_DIR=venv

REM Criar venv se não existir
if not exist %VENV_DIR% (
    echo 🔹 Criando ambiente virtual...
    python -m venv %VENV_DIR%
    call %VENV_DIR%\Scripts\activate
    pip install --upgrade pip
    pip install -r requirements.txt
) else (
    echo 🔹 Ativando ambiente virtual...
    call %VENV_DIR%\Scripts\activate
)

REM Executar script
echo 🔹 Iniciando teste...
python main.py
