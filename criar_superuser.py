import os
import sys

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestor_linhas.settings')

import django
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = 'MASTER'
email = 'master@gestorlinhas.com'
password = '3210'

if User.objects.filter(username=username).exists():
    print(f'\n✓ Superusuário "{username}" já existe!')
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()
    print(f'✓ Senha atualizada!')
else:
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'\n✓ Superusuário criado com sucesso!')

print(f'\n📌 Credenciais:')
print(f'   Username: {username}')
print(f'   Password: {password}')
print(f'   Email: {email}')
print(f'\n🌐 Acesse: http://127.0.0.1:8000/linhas/login/')
print(f'\n⚠️  Altere a senha após o primeiro login!\n')
