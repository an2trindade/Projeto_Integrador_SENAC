#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestor_linhas.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Criar usuário
username = 'teste'
email = 'teste@example.com'
password = '123456'

if User.objects.filter(username=username).exists():
    print(f"Usuário '{username}' já existe!")
    user = User.objects.get(username=username)
    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print(f"Senha do usuário '{username}' atualizada para: {password}")
else:
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f"Superusuário criado com sucesso!")
    print(f"Username: {username}")
    print(f"Senha: {password}")
