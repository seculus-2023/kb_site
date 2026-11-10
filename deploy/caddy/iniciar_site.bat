@echo off
title Site - Django (atras do Caddy/HTTPS)

cd /d C:\webapps\site

if not exist "venv\Scripts\python.exe" (
    echo ERRO: Ambiente virtual nao encontrado!
    pause
    exit /b 1
)

echo Iniciando Site...
echo O acesso publico e pelo Caddy: https://24.152.36.103:8002/
echo.

REM Porta interna: so o Caddy (mesma maquina) acessa. A porta 8002 publica e do Caddy.
"venv\Scripts\python.exe" manage.py runserver 127.0.0.1:18002

pause
