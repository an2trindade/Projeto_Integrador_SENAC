import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestor_linhas.settings')
django.setup()

from django.contrib.auth.models import User

try:
    # Verificar se o superusuário já existe
    if User.objects.filter(username='admin').exists():
        print('✅ Superusuário já existe!')
        user = User.objects.get(username='admin')
        print(f'Usuário: {user.username}')
        print(f'Email: {user.email}')
    else:
        # Criar o superusuário
        user = User.objects.create_superuser(
            username='admin',
            email='admin@gestorlinhas.com',
            password='admin123'
        )
        print('✅ Superusuário criado com sucesso!')
        print('Credenciais de acesso:')
        print('Usuário: admin')
        print('Senha: admin123')
        print('Email: admin@gestorlinhas.com')
        
except Exception as e:
    print(f'❌ Erro ao criar superusuário: {e}')
    sys.exit(1)