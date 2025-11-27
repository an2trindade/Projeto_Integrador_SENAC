import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestor_linhas.settings')
django.setup()

from django.contrib.auth.models import User

# Criar usuário de teste
username = 'USUARIO'
password = '0102'

# Verificar se já existe
if User.objects.filter(username=username).exists():
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()
    print(f'✓ Usuário "{username}" já existia - senha atualizada para "{password}"')
else:
    user = User.objects.create_user(username=username, password=password)
    print(f'✓ Usuário "{username}" criado com sucesso!')
    print(f'✓ Senha: "{password}"')

print(f'\nCredenciais de login:')
print(f'  Username: {username}')
print(f'  Password: {password}')
