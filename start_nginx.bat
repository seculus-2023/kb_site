@echo off
REM Inicia o serviço Nginx no Windows
REM Altere o caminho abaixo para o diretório onde o nginx.exe está instalado
set NGINX_PATH=C:\nginx-1.28.0\nginx.exe

REM Inicia o Nginx
start "Nginx" "%NGINX_PATH%"

echo Nginx iniciado!
pause
