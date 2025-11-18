import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestor_linhas.settings')
django.setup()

from django.contrib.auth.models import User

# Verificar se o usuário já existe
if User.objects.filter(username='admin').exists():
    print('Superusuário "admin" já existe!')
    user = User.objects.get(username='admin')
    print(f'Username: {user.username}')
    print(f'Email: {user.email}')
else:
    # Criar superusuário
    user = User.objects.create_superuser(
        username='admin',
        email='admin@gestorlinhas.com',
        password='admin123'
    )
    print('Superusuário criado com sucesso!')
    print(f'Username: admin')
    print(f'Email: admin@gestorlinhas.com')
    print(f'Password: admin123')
    print('\n⚠️  IMPORTANTE: Altere a senha após o primeiro login!')
