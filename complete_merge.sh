#!/bin/bash
cd "C:\Users\ana.fausto\Projeto_Integrador_SENAC"

# Remove arquivos conflitantes do ambiente virtual do staging
git reset HEAD .env/

# Adiciona apenas arquivos do projeto principal
git add db.sqlite3
git add docs/
git add linhas/
git add gestor_linhas/
git add manage.py
git add requirements.txt
git add README.md
git add scripts/
git add static/

# Faz o commit do merge
git commit -m "Merge branch main: resolve conflitos mantendo apenas arquivos do projeto"

echo "Merge finalizado com sucesso!"
git status