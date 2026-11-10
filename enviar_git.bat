@echo off
chcp 65001 >nul
cd /d "%~dp0"

set "REMOTO=https://github.com/seculus-2023/kb_site.git"
set "BRANCH=main"

rem Garante que o remoto "kbsite" existe
git remote get-url kbsite >nul 2>&1 || git remote add kbsite %REMOTO%

rem Seguranca: nunca enviar o .env
git rm --cached --quiet .env >nul 2>&1

echo.
echo === Arquivos alterados ===
git status --short
echo.

set "MSG="
set /p "MSG=Mensagem do commit (Enter = data/hora): "
if "%MSG%"=="" set "MSG=Atualizacao %date% %time:~0,5%"

git add -A
git commit -m "%MSG%"
if errorlevel 1 echo Nada novo para salvar. Enviando mesmo assim...

git push -u kbsite %BRANCH%
if errorlevel 1 (
    echo.
    echo *** Erro ao enviar. Verifique login do GitHub e a internet. ***
) else (
    echo.
    echo === Enviado para %REMOTO% ===
)
echo.
pause
