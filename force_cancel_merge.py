import os
import stat

def force_remove_file(file_path):
    """Remove arquivo forçadamente, mesmo se for read-only"""
    try:
        if os.path.exists(file_path):
            # Remover atributo read-only se existir
            os.chmod(file_path, stat.S_IWRITE)
            os.remove(file_path)
            print(f"✅ Removido: {os.path.basename(file_path)}")
            return True
        else:
            print(f"❌ Arquivo não encontrado: {os.path.basename(file_path)}")
            return False
    except Exception as e:
        print(f"❌ Erro ao remover {os.path.basename(file_path)}: {e}")
        return False

# Diretório .git
git_dir = r'C:\Users\ana.fausto\Projeto_Integrador_SENAC\.git'

# Arquivos de merge para remover
merge_files = [
    'MERGE_HEAD',
    'MERGE_MODE', 
    'MERGE_MSG',
    'AUTO_MERGE',
    '.MERGE_MSG.swp'
]

print("🔧 Removendo arquivos de merge forçadamente...")
print("=" * 50)

success_count = 0
for file in merge_files:
    file_path = os.path.join(git_dir, file)
    if force_remove_file(file_path):
        success_count += 1

print("=" * 50)
print(f"✅ {success_count}/{len(merge_files)} arquivos removidos com sucesso")

if success_count == len(merge_files):
    print("🎉 Merge cancelado com sucesso!")
else:
    print("⚠️  Alguns arquivos não puderam ser removidos")