@echo off
title Iniciar tudo - Caddy + BolsaTrader + Site
REM Liga o Caddy (HTTPS), o Django do BolsaTrader e o Django do Site,
REM cada um em sua janela. O que ja estiver rodando nao e aberto de novo.
REM
REM Copie este arquivo para C:\webapps\iniciar_tudo.bat no servidor.
REM
REM   Caddy        -> portas 80, 443 e 8002 (publicas, HTTPS)
REM   BolsaTrader  -> 127.0.0.1:8005  (https://bolsatrader.duckdns.org)
REM   Site         -> 127.0.0.1:18002 (https://www.arpjr.com.br e https://24.152.36.103:8002)

set "CADDY_DIR=C:\webapps\caddy"
set "BOLSA_DIR=C:\webapps\bolsatrader"
set "SITE_DIR=C:\webapps\site"

echo ========================================
echo   INICIANDO CADDY + BOLSATRADER + SITE
echo ========================================
echo.

REM ---------- BolsaTrader (127.0.0.1:8005) ----------
netstat -ano | findstr /R /C:"127.0.0.1:8005 .*LISTENING" >nul
if not errorlevel 1 (
    echo [ok] BolsaTrader ja esta rodando na porta 8005.
) else if not exist "%BOLSA_DIR%\.venv\Scripts\python.exe" (
    echo [ERRO] BolsaTrader: .venv nao encontrado em %BOLSA_DIR%
) else (
    echo [..] Iniciando BolsaTrader...
    start "BolsaTrader - Django" /d "%BOLSA_DIR%" cmd /k ".venv\Scripts\python.exe manage.py migrate && .venv\Scripts\python.exe manage.py runserver 127.0.0.1:8005"
)

REM ---------- Site (127.0.0.1:18002) ----------
netstat -ano | findstr /R /C:"127.0.0.1:18002 .*LISTENING" >nul
if not errorlevel 1 (
    echo [ok] Site ja esta rodando na porta 18002.
) else if not exist "%SITE_DIR%\venv\Scripts\python.exe" (
    echo [ERRO] Site: venv nao encontrado em %SITE_DIR%
) else (
    echo [..] Iniciando Site...
    start "Site - Django" /d "%SITE_DIR%" cmd /k "venv\Scripts\python.exe manage.py runserver 127.0.0.1:18002"
)

REM ---------- Caddy (HTTPS) ----------
tasklist /FI "IMAGENAME eq caddy.exe" | find /I "caddy.exe" >nul
if not errorlevel 1 (
    echo [ok] Caddy ja esta rodando. Recarregando a configuracao...
    "%CADDY_DIR%\caddy.exe" reload --config "%CADDY_DIR%\Caddyfile"
) else if not exist "%CADDY_DIR%\caddy.exe" (
    echo [ERRO] Caddy nao encontrado em %CADDY_DIR%
) else (
    echo [..] Iniciando Caddy...
    start "Caddy - HTTPS" /d "%CADDY_DIR%" caddy.exe run --config Caddyfile
)

echo.
echo Pronto. Enderecos:
echo   https://bolsatrader.duckdns.org
echo   https://www.arpjr.com.br
echo   https://24.152.36.103:8002
echo.
echo Para desligar, feche as janelas "BolsaTrader - Django", "Site - Django" e "Caddy - HTTPS".
pause
