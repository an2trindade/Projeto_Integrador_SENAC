@echo off
cd /d "C:\Users\josias.parisotto\Projeto_Integrador_SENAC"

echo Resolvendo conflitos do Git...
echo.

REM Definir editor vazio para aceitar mensagem padrão
set GIT_EDITOR=true

REM Continuar o rebase
git rebase --continue

REM Se falhar, tentar abortar e fazer commit normal
if errorlevel 1 (
    echo.
    echo Rebase falhou, abortando e fazendo commit normal...
    git rebase --abort
    git add .
    git commit -m "Update: database settings, login page design, and management commands"
)

echo.
echo Status final:
git status

echo.
echo Pronto! Conflitos resolvidos.
pause
