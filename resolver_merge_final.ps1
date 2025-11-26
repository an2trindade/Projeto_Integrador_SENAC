# Script para resolver merge
cd "C:\Users\ana.fausto\Projeto_Integrador_SENAC"

# Verificar se há processo vim rodando e matar
Get-Process | Where-Object {$_.Name -like "*vim*" -or $_.Name -like "*vi*"} | Stop-Process -Force

# Limpar qualquer estado de merge
git merge --abort 2>$null

# Verificar status
git status

# Fazer commit das mudanças locais se necessário
git add .
git commit -m "Resolver conflitos de merge - commit automático"

# Fazer pull
git pull origin main --no-edit

# Fazer push
git push origin main

Write-Host "Merge resolvido com sucesso!"