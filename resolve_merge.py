import os
import subprocess

# Mudar para o diretório do projeto
os.chdir(r'C:\Users\ana.fausto\Projeto_Integrador_SENAC')

print("Diretório atual:", os.getcwd())

try:
    # Verificar status
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    print("Status git:", result.stdout)
    
    # Adicionar todos os arquivos do projeto (ignorando .env)
    subprocess.run(['git', 'add', 'db.sqlite3'], check=True)
    subprocess.run(['git', 'add', 'docs/'], check=True)
    subprocess.run(['git', 'add', 'linhas/'], check=True)
    subprocess.run(['git', 'add', 'gestor_linhas/'], check=True)
    subprocess.run(['git', 'add', 'manage.py'], check=True)
    subprocess.run(['git', 'add', 'requirements.txt'], check=True)
    subprocess.run(['git', 'add', 'scripts/'], check=True)
    subprocess.run(['git', 'add', 'static/'], check=True)
    subprocess.run(['git', 'add', '*.sh'], check=True)
    subprocess.run(['git', 'add', '*.bat'], check=True)
    
    print("Arquivos adicionados com sucesso")
    
    # Fazer commit do merge
    result = subprocess.run(['git', 'commit', '-m', 'Merge: resolve conflitos e sincroniza arquivos do projeto'], 
                          capture_output=True, text=True)
    print("Commit result:", result.stdout)
    print("Commit errors:", result.stderr)
    
    # Verificar status final
    result = subprocess.run(['git', 'status'], capture_output=True, text=True)
    print("Status final:", result.stdout)
    
except subprocess.CalledProcessError as e:
    print(f"Erro: {e}")
except Exception as e:
    print(f"Erro geral: {e}")