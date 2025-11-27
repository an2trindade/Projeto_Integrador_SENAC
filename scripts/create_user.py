from django.contrib.auth.models import User
user, created = User.objects.get_or_create(username='USUARIO')
user.set_password('0102')
user.save()
msg = 'Usuario USUARIO criado!' if created else 'Usuario USUARIO ja existia - senha atualizada!'
print(msg)
print('Credenciais: USUARIO / 0102')
