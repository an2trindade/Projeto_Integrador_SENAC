import os
import shutil

# Caminho para o diretório .git
git_dir = r'C:\Users\ana.fausto\Projeto_Integrador_SENAC\.git'

# Arquivos de merge para remover
merge_files = [
    'MERGE_HEAD',
    'MERGE_MODE', 
    'MERGE_MSG',
    'AUTO_MERGE',
    '.MERGE_MSG.swp'
]

print("Removendo arquivos de merge...")
for file in merge_files:
    file_path = os.path.join(git_dir, file)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"Removido: {file}")
        except Exception as e:
            print(f"Erro ao remover {file}: {e}")
    else:
        print(f"Arquivo não encontrado: {file}")

print("\nArquivos de merge removidos. Merge cancelado.")