from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Cria o superusuário MASTER'

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'Teste'
        email = 'teste@gestorlinhas.com'
        password = '010203'

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user.set_password(password)
            user.is_superuser = True
            user.is_staff = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f'\n✓ Usuário "{username}" já existe - senha atualizada!'))
        else:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'\n✓ Superusuário "{username}" criado com sucesso!'))

        self.stdout.write(self.style.SUCCESS('\n📌 Credenciais:'))
        self.stdout.write(self.style.SUCCESS(f'   Username: {username}'))
        self.stdout.write(self.style.SUCCESS(f'   Password: {password}'))
        self.stdout.write(self.style.SUCCESS(f'\n🌐 Acesse: http://127.0.0.1:8000/linhas/login/\n'))
