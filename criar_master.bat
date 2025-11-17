@echo off
cd /d "C:\Users\josias.parisotto\Projeto_Integrador_SENAC"
call .env\Scripts\activate.bat
python criar_superuser.py
pause
