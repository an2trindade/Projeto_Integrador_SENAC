#!/usr/bin/env python3
"""
Script para resolver merge e limpar estado do git
"""

import os
import subprocess
import sys

def run_command(command, description=""):
    """Executa um comando e retorna o resultado"""
    print(f"\n🔄 {description}")
    print(f"Executando: {command}")
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=r"C:\Users\ana.fausto\Projeto_Integrador_SENAC",
            capture_output=True, 
            text=True, 
            encoding='utf-8'
        )
        
        if result.stdout:
            print("📤 Output:", result.stdout.strip())
        if result.stderr:
            print("⚠️ Error:", result.stderr.strip())
        
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        print(f"❌ Erro ao executar comando: {e}")
        return False, "", str(e)

def main():
    print("🔧 Iniciando resolução de merge...")
    
    # 1. Limpar arquivos de merge
    print("\n1. Limpando arquivos de merge...")
    merge_files = [
        ".git/MERGE_HEAD",
        ".git/MERGE_MSG", 
        ".git/MERGE_MODE",
        ".git/.MERGE_MSG.swp"
    ]
    
    for file in merge_files:
        full_path = os.path.join(r"C:\Users\ana.fausto\Projeto_Integrador_SENAC", file)
        if os.path.exists(full_path):
            try:
                os.remove(full_path)
                print(f"✅ Removido: {file}")
            except Exception as e:
                print(f"⚠️ Erro ao remover {file}: {e}")
    
    # 2. Verificar status
    success, stdout, stderr = run_command("git status", "Verificando status do git")
    if not success:
        print("❌ Falha ao verificar status")
        return False
    
    print(f"\n📋 Status atual:\n{stdout}")
    
    # 3. Reset se necessário
    if "merge" in stdout.lower() or "merging" in stdout.lower():
        success, _, _ = run_command("git reset --hard HEAD", "Fazendo reset hard")
        if not success:
            print("❌ Falha no reset")
            return False
    
    # 4. Fazer pull
    success, stdout, stderr = run_command("git pull origin main", "Fazendo pull do repositório remoto")
    
    if "CONFLICT" in stdout or "CONFLICT" in stderr:
        print("\n⚠️ CONFLITOS DETECTADOS!")
        print("Conflitos encontrados nos seguintes arquivos:")
        
        # Listar arquivos com conflito
        success2, files, _ = run_command("git diff --name-only --diff-filter=U", "Listando arquivos com conflito")
        if success2 and files:
            for file in files.strip().split('\n'):
                if file.strip():
                    print(f"  📄 {file}")
        
        return False
    
    # 5. Verificar se merge foi bem sucedido
    success, stdout, stderr = run_command("git status", "Verificando status final")
    
    if "clean" in stdout.lower() or "nothing to commit" in stdout.lower():
        print("\n✅ MERGE RESOLVIDO COM SUCESSO!")
        print("Repository está limpo e sincronizado.")
        return True
    else:
        print(f"\n📋 Status final:\n{stdout}")
        return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎉 Processo concluído com sucesso!")
        else:
            print("\n⚠️ Processo concluído com avisos. Verifique os conflitos.")
    except KeyboardInterrupt:
        print("\n⏹️ Processo interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")