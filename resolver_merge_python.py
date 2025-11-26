#!/usr/bin/env python3
import os
import subprocess
import sys

def run_command(cmd):
    """Executa comando e retorna resultado"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=r"C:\Users\ana.fausto\Projeto_Integrador_SENAC")
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)

def main():
    print("=== RESOLVENDO CONFLITOS DE MERGE ===")
    
    # Matar processos vim
    print("1. Matando processos vim...")
    run_command("taskkill /F /IM vim.exe 2>nul")
    run_command("taskkill /F /IM vi.exe 2>nul")
    
    # Abortar merge atual
    print("2. Abortando merge atual...")
    code, out, err = run_command("git merge --abort")
    
    # Verificar status
    print("3. Verificando status...")
    code, out, err = run_command("git status")
    print(out)
    
    # Add e commit mudanças locais
    print("4. Fazendo commit das mudanças locais...")
    run_command("git add .")
    code, out, err = run_command('git commit -m "Resolver conflitos de merge automaticamente"')
    
    # Pull com estratégia
    print("5. Fazendo pull com merge automático...")
    code, out, err = run_command("git pull origin main -X ours --no-edit")
    if code != 0:
        print(f"Erro no pull: {err}")
        # Tentar pull normal
        code, out, err = run_command("git pull origin main")
    
    print(out)
    
    # Push
    print("6. Fazendo push...")
    code, out, err = run_command("git push origin main")
    print(out)
    if err:
        print(f"Erro: {err}")
    
    print("=== MERGE RESOLVIDO ===")

if __name__ == "__main__":
    main()