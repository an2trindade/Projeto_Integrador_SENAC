import os
import shutil
import subprocess

repo_path = r"C:\Users\josias.parisotto\Projeto_Integrador_SENAC"
os.chdir(repo_path)

print("=== Resolvendo conflitos do Git ===\n")

# Tentar continuar rebase com variável de ambiente
env = os.environ.copy()
env['GIT_EDITOR'] = 'true'

try:
    result = subprocess.run(['git', 'rebase', '--continue'], 
                          env=env, 
                          capture_output=True, 
                          text=True,
                          timeout=10)
    print("Rebase continue:", result.stdout, result.stderr)
except Exception as e:
    print(f"Erro no rebase: {e}")

# Se ainda houver problemas, remover manualmente o estado de rebase
rebase_dir = os.path.join(repo_path, '.git', 'rebase-merge')
if os.path.exists(rebase_dir):
    print("\nRemovendo estado de rebase manualmente...")
    try:
        shutil.rmtree(rebase_dir)
        print("✓ Estado de rebase removido")
    except Exception as e:
        print(f"Erro ao remover: {e}")

# Verificar status
print("\n=== Status do Git ===")
result = subprocess.run(['git', 'status'], capture_output=True, text=True)
print(result.stdout)

# Adicionar e commitar mudanças pendentes
print("\n=== Adicionando mudanças ===")
subprocess.run(['git', 'add', '.'])

print("\n=== Criando commit ===")
result = subprocess.run(['git', 'commit', '-m', 
                        'Update: database settings, login page design, and management commands'],
                       capture_output=True, text=True)
print(result.stdout)
print(result.stderr)

# Status final
print("\n=== Status Final ===")
result = subprocess.run(['git', 'status', '--short'], capture_output=True, text=True)
print(result.stdout)

print("\n✓ Conflitos resolvidos!")
print("\nPróximos passos:")
print("  - Execute: git push origin main")
print("  - Ou: git push -f origin main (se necessário)")

input("\nPressione ENTER para sair...")
