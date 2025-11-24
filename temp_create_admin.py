import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestor_linhas.settings')
django.setup()

from django.contrib.auth.models import User

if User.objects.filter(username='admin').exists():
    print('Superusuário já existe!')
else:
    User.objects.create_superuser('admin', 'admin@gestorlinhas.com', 'admin123')
    print('Superusuário criado com sucesso!')
    print('Usuário: admin')
    print('Senha: admin123')