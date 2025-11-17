# Script para resolver merge do Git
$ErrorActionPreference = "Continue"

Write-Host "`n=== Resolvendo Merge do Git ===" -ForegroundColor Cyan

# Navegar para o diretório
Set-Location "C:\Users\josias.parisotto\Projeto_Integrador_SENAC"

# Tentar abortar rebase se estiver em andamento
Write-Host "`n1. Abortando rebase em andamento..." -ForegroundColor Yellow
git rebase --abort 2>&1 | Out-Null

# Aguardar um momento
Start-Sleep -Seconds 2

# Verificar status
Write-Host "`n2. Verificando status..." -ForegroundColor Yellow
git status --short

# Adicionar todas as alterações
Write-Host "`n3. Adicionando alterações..." -ForegroundColor Yellow
git add .

# Fazer commit
Write-Host "`n4. Criando commit..." -ForegroundColor Yellow
git commit -m "Update: database settings (SQLite default), login page design (dark theme), and management commands"

# Status final
Write-Host "`n5. Status final:" -ForegroundColor Yellow
git status

Write-Host "`n=== Merge resolvido com sucesso! ===" -ForegroundColor Green
Write-Host "`nPróximos passos:" -ForegroundColor Cyan
Write-Host "  - Execute: git push origin main" -ForegroundColor White
Write-Host "  - Ou execute: git push -f origin main (se necessário)" -ForegroundColor White

Read-Host "`nPressione ENTER para sair"
