from django.contrib.auth.models import User
if User.objects.filter(username='admin').exists():
    print('Superusuário já existe!')
else:
    User.objects.create_superuser('admin', 'admin@gestorlinhas.com', 'admin123')
    print('Superusuário criado: admin / admin123')
