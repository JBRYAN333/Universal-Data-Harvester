@echo off
cd /d "%~dp0"
title DEUS CODE - DEBUG MODE
color 0c

echo =================================================
echo       MODO DE DIAGNOSTICO - NAO FECHE!
echo =================================================

:: 1. Verifica se o Python global existe
echo [1/4] Verificando Python no sistema...
python --version
if %errorlevel% neq 0 (
    echo [ERRO CRITICO] O comando 'python' nao foi encontrado no Windows.
    echo Voce precisa instalar o Python e marcar 'Add to PATH'.
    pause
    exit
)
echo [OK] Python encontrado.

:: 2. Cria ou Valida o Ambiente
echo.
echo [2/4] Verificando Matrix (nsa_env)...
if not exist "nsa_env" (
    echo [AVISO] Criando pasta nsa_env...
    python -m venv nsa_env
    if %errorlevel% neq 0 (
        echo [ERRO] Falha ao criar ambiente virtual.
        pause
        exit
    )
) else (
    echo [OK] Pasta nsa_env ja existe.
)

:: 3. Instala dependências (SEM MODO SILENCIOSO AGORA)
echo.
echo [3/4] Instalando bibliotecas (Isso pode demorar)...
echo -------------------------------------------------
.\nsa_env\Scripts\python.exe -m pip install -r requirements.txt
echo -------------------------------------------------

if %errorlevel% neq 0 (
    echo [ERRO] Falha na instalacao das bibliotecas.
    echo Tente apagar a pasta 'nsa_env' e rodar de novo.
    pause
    exit
)
echo [OK] Bibliotecas instaladas.

:: 4. Executa o App
echo.
echo [4/4] INICIANDO A INTERFACE GRAFICA...
echo Se der erro abaixo, copie e me mande.
echo =================================================
.\nsa_env\Scripts\python.exe app.py
echo =================================================

echo.
echo O programa fechou. Se foi um erro, leia acima.
pause