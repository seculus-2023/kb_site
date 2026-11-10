@echo off
REM Inicia o servidor Django com Waitress e o Nginx
REM Ajuste os caminhos conforme necessário

REM Inicia o Django/Waitress
start "Django" cmd /c "python server.py"

REM Aguarda 3 segundos para garantir que o Django subiu
ping 127.0.0.1 -n 3 > nul

REM Inicia o Nginx
set NGINX_PATH=C:\nginx-1.28.0\nginx.exe
start "Nginx" "%NGINX_PATH%"

echo Servidores Django (Waitress) e Nginx iniciados!
pause
