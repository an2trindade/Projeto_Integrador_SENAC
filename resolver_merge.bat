@echo off
cd /d C:\Users\ana.fausto\Projeto_Integrador_SENAC
echo Matando processos vim...
taskkill /F /IM vim.exe >nul 2>&1
taskkill /F /IM vi.exe >nul 2>&1
taskkill /F /IM git.exe >nul 2>&1

echo Abortando merge...
git merge --abort >nul 2>&1

echo Status atual:
git status

echo Fazendo commit...
git add .
git commit -m "Resolver merge automaticamente"

echo Pull das mudancas remotas...
git pull origin main --no-edit

echo Push das mudancas...
git push origin main

echo Merge resolvido!
pause